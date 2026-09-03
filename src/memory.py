"""
Memory layer for Job Needle Finder.

The memory layer turns human feedback into persistent state.

This is the difference between:

    "I don't like this job."

and:

    "The system should know why this type of job is not a fit."
"""

from dataclasses import dataclass, field


@dataclass
class Decision:
    job_id: str
    decision: str
    reason: str


@dataclass
class Memory:
    """
    Persistent knowledge accumulated through human feedback.
    """

    decisions: list[Decision] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)

    def is_excluded(self, job: dict) -> bool:
        """
        Determine whether the opportunity should be skipped
        based on previously established knowledge.
        """

        job_id = job.get("id")

        return any(
            decision.job_id == job_id
            and decision.decision == "reject"
            for decision in self.decisions
        )

    def record_decision(
        self,
        job: dict,
        decision: str,
        reason: str,
    ):
        """
        Store human feedback so future runs can use it.
        """

        self.decisions.append(
            Decision(
                job_id=job["id"],
                decision=decision,
                reason=reason,
            )
        )

    def add_preference(self, preference: str):
        """
        Add a newly discovered preference.
        """

        if preference not in self.preferences:
            self.preferences.append(preference)

    def add_exclusion(self, exclusion: str):
        """
        Add a new hard exclusion.
        """

        if exclusion not in self.exclusions:
            self.exclusions.append(exclusion)
