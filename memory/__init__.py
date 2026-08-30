"""
Memory Module — Persistent Case Memory for the Dispute Resolution Agent.

Provides cross-case learning and customer history tracking:
- Stores past case decisions and reasoning traces
- Tracks customer fraud patterns across interactions
- Enables the agent to "remember" previous encounters
"""

from memory.case_memory import CaseMemory
