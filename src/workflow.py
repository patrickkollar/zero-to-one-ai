"""
Job Needle Finder workflow.

This module orchestrates the system:

    Search
       ↓
    Evaluate
       ↓
    Filter
       ↓
    Rank
       ↓
    Present
       ↓
    Learn

The workflow owns execution.
The LLM owns interpretation and reasoning.
"""

from evaluate import evaluate_job


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

    # 1. Search for current opportunities
    jobs = search_client.search(
        candidate_profile=candidate_profile
    )

    evaluated = []

    # 2. Evaluate each opportunity
    for job in jobs:

        # 3. Check existing memory before spending
        #    reasoning effort on something already rejected.
        if memory.is_excluded(job):
            continue

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

    # 4. Rank the surviving opportunities
    evaluated.sort(
        key=lambda item: item["evaluation"].score,
        reverse=True,
    )

    # 5. Return the highest-value opportunities
    return evaluated
