"""
Hard filters for job opportunities.

Hard filters are deterministic rules that can eliminate an
opportunity before the reasoning layer spends effort evaluating it.

This is intentionally separate from scoring.

A job can be a perfect functional match and still be impossible
because it violates a non-negotiable requirement.
"""


def apply_hard_filters(
    jobs: list[dict],
    memory,
    candidate_profile: dict,
) -> tuple[list[dict], list[dict]]:
    """
    Separate jobs into eligible and filtered-out opportunities.

    Returns:
        eligible_jobs
        filtered_jobs
    """

    eligible = []
    filtered = []

    preferred_work_models = candidate_profile["candidate"][
        "preferred_work_model"
    ]

    for job in jobs:

        # Previously rejected jobs should never be reconsidered.
        if memory.is_excluded(job):
            filtered.append(
                {
                    "job": job,
                    "reason": "Previously rejected",
                }
            )
            continue

        # If remote is a hard requirement, eliminate jobs that
        # explicitly require an incompatible work model.
        if (
            "Remote" in preferred_work_models
            and job["work_model"].lower() == "on-site"
        ):
            filtered.append(
                {
                    "job": job,
                    "reason": "Work model does not meet requirements",
                }
            )
            continue

        eligible.append(job)

    return eligible, filtered