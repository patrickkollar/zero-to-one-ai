"""
Job Needle Finder workflow.

The workflow orchestrates the system:

    Load
      ↓
    Hard Filters
      ↓
    Evaluate
      ↓
    Rank
      ↓
    Present

The workflow owns execution.
The LLM owns interpretation and reasoning.
Memory owns what the system has learned.
Hard filters enforce non-negotiable rules.
"""

from src.evaluate import evaluate_job
from src.filters import apply_hard_filters


def run_job_search(
    search_client,
    llm_client,
    candidate_profile,
    scoring_model,
    memory,
):
    """
    Execute one complete job-search cycle.
    """

    # 1. Load current opportunities.
    jobs = search_client.search(
        candidate_profile=candidate_profile
    )

    # 2. Apply deterministic rules before invoking
    #    the reasoning layer.
    eligible_jobs, filtered_jobs = apply_hard_filters(
        jobs=jobs,
        memory=memory,
        candidate_profile=candidate_profile,
    )

    evaluated = []

    # 3. Evaluate only opportunities that survived
    #    the hard filters.
    for job in eligible_jobs:

        evaluation = evaluate_job(
            job=job,
            candidate_profile=candidate_profile,
            scoring_model=scoring_model,
            llm_client=llm_client,
        )

        evaluated.append(
            {
                "job": job,
                "evaluation": evaluation,
            }
        )

    # 4. Rank the surviving opportunities.
    evaluated.sort(
        key=lambda item: item["evaluation"].score,
        reverse=True,
    )

    # 5. Return both evaluated and filtered opportunities.
    return evaluated, filtered_jobs