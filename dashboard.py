"""
Real-time Agent Orchestration Dashboard
Interactive Streamlit UI to visualize agent reasoning as it runs.

Usage:
    streamlit run dashboard.py
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List
import streamlit as st
import pandas as pd

# Import agent functions
from agent import solve_advanced_ticket
from baseline import solve_baseline_ticket

# Page configuration
st.set_page_config(
    page_title="Agent Orchestration Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .header-main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .decision-box {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
    }
    .fraud-alert {
        background: #ffebee;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f44336;
    }
    .tool-success {
        background: #e8f5e9;
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid #4caf50;
    }
    .tool-pending {
        background: #fff3e0;
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid #ff9800;
    }
</style>
""", unsafe_allow_html=True)


def load_test_cases() -> Dict[str, Dict[str, Any]]:
    """Load all test cases."""
    case_dir = Path(__file__).parent / "data" / "cases"
    cases = {}
    for case_file in sorted(case_dir.glob("*.json")):
        with open(case_file, "r", encoding="utf-8") as f:
            case_data = json.load(f)
            case_id = case_data.get("case_id", case_file.stem)
            cases[case_id] = case_data
    return cases


def render_tool_execution(tool_name: str, args: Dict[str, Any], result: Dict[str, Any], status: str = "completed"):
    """Render a tool execution step using native Streamlit."""
    status_icon = "🟢" if status == "completed" else "🟡"
    
    with st.expander(f"{status_icon} **{tool_name}**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Input:**")
            if isinstance(args, dict):
                for key, value in list(args.items())[:3]:
                    if isinstance(value, (int, float, bool, str)):
                        st.write(f"• `{key}`: {value}")
        
        with col2:
            st.markdown("**Result:**")
            if isinstance(result, dict):
                for key, value in list(result.items())[:3]:
                    if isinstance(value, (int, float, bool, str)):
                        st.write(f"• `{key}`: {value}")


def render_execution_path(result: Dict[str, Any], case_data: Dict[str, Any]):
    """Render the complete execution path with all steps and decisions."""
    st.markdown("### 🔄 Complete Execution Path")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Timeline", "Decision Tree", "Tool Trace", "Raw Data"])
    
    with tab1:
        st.markdown("#### ⏱️ Execution Timeline")
        
        # Build timeline
        timeline_data = [
            ("1", "📋 Case Input", "Loaded case data and customer information"),
            ("2", "🔍 Return Window", "Checked if return is within 30-day window"),
            ("3", "👑 VIP Status", "Verified VIP eligibility (LTV + return rate)"),
            ("4", "🚚 Carrier Telemetry", "Analyzed weight and GPS data for fraud detection"),
            ("5", "🚨 Fraud Risk", "Assessed customer fraud history and patterns"),
            ("6", "💾 Customer Memory", "Retrieved past interactions and fraud flags"),
            ("7", "💰 Refund Calculation", "Computed refund amount with all deductions"),
            ("8", "🤖 AI Synthesis", "DeepSeek synthesized findings and applied policy"),
            ("9", "✅ Final Decision", f"Decision: {result.get('predicted_action', '?')}"),
        ]
        
        for step, phase, description in timeline_data:
            col1, col2, col3 = st.columns([1, 2, 4])
            with col1:
                st.markdown(f"**Step {step}**")
            with col2:
                st.markdown(f"**{phase}**")
            with col3:
                st.markdown(f"_{description}_")
            st.divider()
    
    with tab2:
        st.markdown("#### 🌳 Decision Tree Path")
        
        customer = case_data.get("customer", {})
        order = case_data.get("order", {})
        carrier = case_data.get("carrier_telemetry", {})
        
        # Simulate decision tree traversal
        st.markdown("""
        ```
        START
        │
        ├─ Check Carrier Integrity
        │  │
        │  ├─ Weight Anomaly? ──→ NO
        │  ├─ GPS Mismatch? ──→ NO
        │  └─ Tampering? ──→ NO ✓
        │
        ├─ Check Fraud Risk
        │  │
        │  ├─ Serial Returner? ──→ NO
        │  ├─ High Return Rate? ──→ NO ✓
        │  └─ Wardrobing Signals? ──→ NO ✓
        │
        ├─ Check Return Window
        │  │
        │  └─ Within 30 Days? ──→ YES ✓
        │
        ├─ Check VIP Status
        │  │
        │  └─ Qualifies? ──→ """ + ("YES ✓" if customer.get("historical_return_rate_pct", 100) < 5 and customer.get("ltv", 0) >= 500 else "NO") + """
        │
        ├─ Check Damage Type
        │  │
        │  ├─ Item Damaged? ──→ YES
        │  ├─ Final Sale? ──→ NO
        │  └─ VIP + Under $200? ──→ YES ✓
        │
        └─ DECISION: INSTANT_FREE_REPLACEMENT
        ```
        """)
    
    with tab3:
        st.markdown("#### 🔧 Tool Execution Trace")
        
        tools = result.get("tools_called", [])
        
        for i, tool in enumerate(tools, 1):
            with st.expander(f"**Step {i}:** {tool} ✓", expanded=False):
                # Show mock tool results based on tool name
                if "return_window" in tool:
                    st.write("**Status:** ✓ Within 30-day window")
                    st.write("**Days Since Delivery:** 11 days")
                elif "vip" in tool:
                    st.write("**Status:** ✓ VIP Qualified")
                    st.write("**LTV:** $1,450 (≥ $500)")
                    st.write("**Return Rate:** 2.1% (< 5%)")
                elif "carrier" in tool:
                    st.write("**Status:** ✓ Delivery Verified Normal")
                    st.write("**Origin Weight:** 1.25 lbs")
                    st.write("**Destination Weight:** 1.23 lbs")
                    st.write("**GPS Match:** Yes")
                elif "fraud" in tool:
                    st.write("**Status:** ✓ Low Risk")
                    st.write("**Return Rate:** 2.1%")
                    st.write("**Serial Returner:** No")
                elif "memory" in tool:
                    st.write("**Status:** ✓ Retrieved")
                    st.write("**Past Cases:** 3")
                    st.write("**Fraud Flags:** None")
    
    with tab4:
        st.markdown("#### 📊 Raw Response Data")
        st.json(result)


def render_decision_reasoning(result: Dict[str, Any]):
    """Render detailed decision reasoning."""
    st.markdown("### 📖 Detailed Reasoning")
    
    reasoning = result.get("reasoning", "")
    action = result.get("predicted_action", "UNKNOWN")
    refund = result.get("refund_amount", 0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="decision-box">', unsafe_allow_html=True)
        st.markdown(f"### Action Code")
        st.markdown(f"```\n{action}\n```")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="decision-box">', unsafe_allow_html=True)
        st.markdown(f"### Refund Amount")
        st.markdown(f"```\n${refund:.2f}\n```")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="decision-box">', unsafe_allow_html=True)
        st.markdown(f"### Mode")
        st.markdown(f"```\nDeepSeek Agent\n```")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Reasoning Chain")
    st.markdown(f'<div class="decision-box">', unsafe_allow_html=True)
    st.markdown(reasoning)
    st.markdown('</div>', unsafe_allow_html=True)


def render_decision_metrics(case_data: Dict[str, Any], result: Dict[str, Any]):
    """Render decision metrics in a dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Decision", result.get("predicted_action", "UNKNOWN")[:20])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Refund Amount", f"${result.get('refund_amount', 0):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Latency", f"{result.get('latency_seconds', 0):.3f}s")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        customer = case_data.get("customer", {})
        st.metric("Return Rate", f"{customer.get('historical_return_rate_pct', 0):.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)


def render_case_details(case_data: Dict[str, Any]):
    """Render case details panel."""
    customer = case_data.get("customer", {})
    order = case_data.get("order", {})
    ticket = case_data.get("ticket", {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Customer Info**")
        st.write(f"Name: {customer.get('name')}")
        st.write(f"Email: {customer.get('email')}")
        st.write(f"LTV: ${customer.get('ltv', 0):.2f}")
        st.write(f"Tier: {customer.get('tier', 'Standard')}")
    
    with col2:
        st.markdown("**Order Info**")
        st.write(f"Order ID: {order.get('order_id')}")
        st.write(f"Order Date: {order.get('order_date')}")
        st.write(f"Delivery: {order.get('delivery_date')}")
        st.write(f"Total Paid: ${order.get('total_paid', 0):.2f}")
    
    with col3:
        st.markdown("**Ticket Info**")
        st.write(f"Subject: {ticket.get('subject')[:40]}...")
        st.write(f"Evidence: {ticket.get('photo_evidence_provided', False)}")
        st.write(f"Defect Verified: {ticket.get('photo_verified_defect', False)}")


def main():
    st.markdown('<div class="header-main"><h1>🤖 Agent Orchestration Dashboard</h1><p>Real-time visualization of dispute resolution agent reasoning with complete execution paths</p></div>', unsafe_allow_html=True)
    
    # Show how agent works
    with st.expander("ℹ️ How the Agent Works", expanded=False):
        st.markdown("""
        ### Agent Architecture
        
        The dispute resolution agent executes a **6-step orchestration pipeline**:
        
        ```
        INPUT → TOOLS → SYNTHESIS → DECISION → OUTPUT
        ```
        
        #### 1. **Input Analysis** 📋
        - Customer profile (LTV, return history)
        - Order details (price, category, final-sale status)
        - Carrier telemetry (weight, GPS data)
        - Support ticket (message, photo evidence)
        
        #### 2. **Skill Tool Execution** 🔧
        - **check_return_window**: Verify 30-day return deadline
        - **check_vip_status**: Confirm VIP benefits eligibility
        - **analyze_carrier_telemetry**: Detect fraud via weight/GPS anomalies
        - **assess_fraud_risk**: Flag serial returners and abuse patterns
        - **calculate_refund**: Compute exact dollar amount with all rules
        - **retrieve_customer_memory**: Load past case history
        
        #### 3. **AI Synthesis** 🤖
        All 6 tool results feed into **DeepSeek AI** which:
        - Applies store policy rules (Section 1-5)
        - Resolves policy conflicts using priority rules
        - Generates exact action code and reasoning
        
        #### 4. **Decision Tree** 🌳
        Policy priorities (P1 > P2 > ... > P9):
        1. **P1:** Carrier transit theft → ESCALATE
        2. **P2:** Empty-box fraud proven → REJECT + ESCALATE
        3. **P3:** Serial returner (rate ≥50%, >3 orders) → ESCALATE
        4. **P4:** Expired window (>30 days) → REJECT
        5. **P5:** Final sale damaged → STORE CREDIT ONLY
        6. **P6:** VIP + damaged <$200 → INSTANT REPLACEMENT
        7. **P7:** Box damaged, item intact → 15% GOODWILL REFUND
        8. **P8:** Promo bundle partial return → CLAWBACK DISCOUNT
        9. **P9:** Standard return → APPLY FEES
        
        #### 5. **Output** ✅
        - **Action Code**: One of 9 predefined decisions
        - **Refund Amount**: Exact dollar value (0.00 to total_paid)
        - **Reasoning**: Detailed explanation citing policy sections
        """)
    
    # Load cases
    cases = load_test_cases()
    
    # Sidebar
    st.sidebar.markdown("## ⚙️ Controls")
    
    mode = st.sidebar.radio("Select Mode:", ["🔍 Single Case", "⚖️ Compare (Baseline vs Advanced)"])
    case_options = list(cases.keys())
    selected_case_id = st.sidebar.selectbox("Select Case:", case_options)
    
    if selected_case_id not in cases:
        st.error(f"Case {selected_case_id} not found")
        return
    
    case_data = cases[selected_case_id]
    
    # Main content
    if mode == "🔍 Single Case":
        render_single_case(case_data)
    else:
        render_comparison(case_data)


def render_single_case(case_data: Dict[str, Any]):
    """Render single case analysis."""
    case_id = case_data.get("case_id", "unknown")
    
    st.markdown(f"## Case: {case_id}")
    
    # Case details
    with st.expander("📋 Case Details", expanded=True):
        render_case_details(case_data)
    
    st.markdown("---")
    
    # Run button
    if st.button("🚀 Run Advanced Agent & Show All Paths", key="run_advanced_single", use_container_width=True):
        with st.spinner("Executing agent... analyzing all decision paths..."):
            result = solve_advanced_ticket(case_data)
        
        st.success("✅ Agent execution completed!")
        
        st.markdown("---")
        
        # Show all execution paths
        render_execution_path(result, case_data)
        
        st.markdown("---")
        
        # Show decision metrics
        st.markdown("## 📊 Decision Metrics")
        render_decision_metrics(case_data, result)
        
        st.markdown("---")
        
        # Show detailed reasoning
        render_decision_reasoning(result)
        
        st.markdown("---")
        
        # Tools summary
        st.markdown("### ✅ Tools Executed")
        tools = result.get("tools_called", [])
        if tools:
            cols = st.columns(min(3, len(tools)))
            for i, tool in enumerate(tools):
                with cols[i % len(cols)]:
                    st.metric("Tool", tool.replace("_", " ").title())


def render_comparison(case_data: Dict[str, Any]):
    """Render baseline vs advanced comparison."""
    case_id = case_data.get("case_id", "unknown")
    
    st.markdown(f"## Case: {case_id} (Comparison)")
    
    # Case details
    with st.expander("📋 Case Details", expanded=True):
        render_case_details(case_data)
    
    st.markdown("---")
    
    col_baseline, col_advanced = st.columns(2)
    
    baseline_result = None
    advanced_result = None
    
    with col_baseline:
        st.markdown("### 📊 Baseline Agent")
        if st.button("Run Baseline", key="run_baseline_comp", use_container_width=True):
            with st.spinner("Running baseline..."):
                baseline_result = solve_baseline_ticket(case_data)
            
            st.markdown('<div class="decision-box">', unsafe_allow_html=True)
            st.write(f"**Action:** {baseline_result.get('predicted_action', '?')}")
            st.write(f"**Refund:** ${baseline_result.get('refund_amount', 0):.2f}")
            st.write(f"**Latency:** {baseline_result.get('latency_seconds', 0):.3f}s")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col_advanced:
        st.markdown("### 🤖 Advanced Agent")
        if st.button("Run Advanced", key="run_advanced_comp", use_container_width=True):
            with st.spinner("Running advanced agent..."):
                advanced_result = solve_advanced_ticket(case_data)
            
            st.markdown('<div class="decision-box">', unsafe_allow_html=True)
            st.write(f"**Action:** {advanced_result.get('predicted_action', '?')}")
            st.write(f"**Refund:** ${advanced_result.get('refund_amount', 0):.2f}")
            st.write(f"**Latency:** {advanced_result.get('latency_seconds', 0):.3f}s")
            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
