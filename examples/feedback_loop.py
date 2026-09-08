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

    # Check persistent memory before doing any work.
    if memory.is_excluded(job):
        print("Found existing decision in memory.")
        print()
        print(f"Job: {job['title']}")
        print(f"Company: {job['company']}")
        print("Status: EXCLUDED")
        print()
        print("Skipping evaluation.")
        print("The system remembers the previous decision.")

    else:
        # The AI recommends the opportunity.
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

        print()
        print("Decision saved to persistent memory.")
