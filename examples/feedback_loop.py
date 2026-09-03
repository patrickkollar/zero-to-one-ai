"""
Illustrative example of the human feedback loop.

The important behavior:

    AI recommendation
          ↓
    Human response
          ↓
    Persistent memory
          ↓
    Better future decisions

This example uses fake jobs and fake feedback.
"""

from src.memory import Memory


def process_feedback(memory: Memory, job: dict, feedback: dict):
    """
    Convert human feedback into system state.
    """

    decision = feedback["decision"]
    reason = feedback["reason"]

    memory.record_decision(
        job=job,
        decision=decision,
        reason=reason,
    )

    print(f"Recorded: {decision}")
    print(f"Reason: {reason}")


if __name__ == "__main__":

    memory = Memory()

    job = {
        "id": "example-001",
        "title": "Senior Manager, Operations",
        "company": "Example Corp",
    }

    # The AI recommended the opportunity.
    print("AI recommendation:")
    print("Score: 87")
    print("Recommendation: pursue")
    print()

    # The human provides feedback.
    feedback = {
        "decision": "reject",
        "reason": "Role is primarily reporting and analytics.",
    }

    process_feedback(
        memory=memory,
        job=job,
        feedback=feedback,
    )

    # A future run can now use that decision.
    print()
    print("Future search:")
    print(f"Excluded: {memory.is_excluded(job)}")
