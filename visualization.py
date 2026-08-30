"""
Agent execution-path tracer.

Used by the orchestrator to record tool calls, results, and the final
verdict. Renders live in Streamlit when a script run context exists;
otherwise stays silent so CLI evaluation is unaffected.
"""

from __future__ import annotations

import json
from typing import Any


def _in_streamlit() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


def _preview(value: Any, limit: int = 400) -> str:
    try:
        text = json.dumps(value, default=str, ensure_ascii=False)
    except Exception:
        text = str(value)
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


class AgentPathVisualizer:
    """Records and optionally displays the agent's tool-call trajectory."""

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.steps: list[dict[str, Any]] = []
        self.decision: dict[str, Any] | None = None
        self._live = _in_streamlit()
        self._st = None
        if self._live:
            import streamlit as st

            self._st = st
            st.caption(f"Tracing agent path · `{case_id}`")

    def log_tool_call(self, name: str, args: dict[str, Any] | None = None) -> None:
        self.steps.append({"event": "call", "tool": name, "args": args or {}})
        if self._st is not None:
            self._st.markdown(f"**→ `{name}`**")
            if args:
                self._st.code(_preview(args), language="json")

    def log_tool_result(self, name: str, result: Any) -> None:
        self.steps.append({"event": "result", "tool": name, "result": result})
        if self._st is not None:
            with self._st.expander(f"Result · {name}", expanded=False):
                self._st.json(result if isinstance(result, (dict, list)) else {"value": result})

    def log_final_decision(self, action: str, refund_amount: float, reasoning: str) -> None:
        self.decision = {
            "predicted_action": action,
            "refund_amount": refund_amount,
            "reasoning": reasoning,
        }
        if self._st is not None:
            self._st.success(f"Decision: `{action}` · refund ${float(refund_amount):.2f}")
            if reasoning:
                self._st.caption(reasoning)

    def show_tools_called_table(self, tools_called: list[str]) -> None:
        if self._st is None or not tools_called:
            return
        import pandas as pd

        self._st.markdown("#### Tools invoked")
        self._st.dataframe(
            pd.DataFrame(
                {"#": list(range(1, len(tools_called) + 1)), "tool": tools_called}
            ),
            hide_index=True,
            width="stretch",
        )
