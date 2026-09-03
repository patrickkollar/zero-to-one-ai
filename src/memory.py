"""
Memory layer for Job Needle Finder.

Memory represents what the system knows.
Storage represents where that knowledge persists.

Keeping those responsibilities separate lets us change
the storage technology without changing the behavior of
the memory layer.
"""

from dataclasses import dataclass, field

from storage import Storage


@dataclass
class Decision:
    job_id: str
    decision: str
    reason: str


@dataclass
class Memory:
    storage: Storage = field(default_factory=Storage)

    decisions: list[Decision] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)

    def __post_init__(self):
        self._load()

    def _load(self):
        """Load persistent knowledge into working memory."""

        self.decisions = [
            Decision(
                job_id=job_id,
                decision=decision,
                reason=reason,
            )
            for job_id, decision, reason
            in self.storage.get_decisions()
        ]

    def is_excluded(self, job: dict) -> bool:
        """Check whether a job has already been rejected."""

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
        """Record feedback in both memory and persistent storage."""

        record = Decision(
            job_id=job["id"],
            decision=decision,
            reason=reason,
        )

        self.decisions.append(record)

        self.storage.save_decision(
            job_id=job["id"],
            decision=decision,
            reason=reason,
        )

    def add_preference(self, preference: str):
        """Add a preference to the system's knowledge."""

        if preference not in self.preferences:
            self.preferences.append(preference)

            self.storage.save_preference(preference)

    def add_exclusion(self, exclusion: str):
        """Add a hard exclusion to persistent memory."""

        if exclusion not in self.exclusions:
            self.exclusions.append(exclusion)

            self.storage.save_exclusion(exclusion)
