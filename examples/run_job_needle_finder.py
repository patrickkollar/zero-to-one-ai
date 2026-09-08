"""
Run the Job Needle Finder end-to-end.

This example connects the major pieces of the system:

    Jobs
      ↓
    Configuration
      ↓
    Memory
      ↓
    Hard Filters
      ↓
    Evaluation
      ↓
    Deterministic Scoring
      ↓
    Ranking
      ↓
    Results

The reasoning engine is mocked for now.
We will replace it with a real LLM later.
"""

from src.config_loader import load_yaml
from src.job_loader import load_jobs
from src.memory import Memory
from src.workflow import run_job_search


class MockLLM:
    """
    Temporary reasoning engine.

    The mock returns dimension-level judgments.
    The scoring engine then applies the configured weights.
    """

    def generate(self, prompt: str) -> dict:

        if "Reporting & Analytics" in prompt:
            return {
                "dimension_scores": {
                    "actual_work": 45,
                    "seniority_and_scope": 85,
                    "transferability": 60,
                    "compensation": 85,
                    "work_model": 100,
                },
                "reasoning": "The role is primarily reporting and analytics rather than business operations leadership.",
                "strengths": ["Executive reporting"],
                "concerns": ["Reporting-heavy scope"],
            }

        if "Manager, Operations" in prompt:
            return {
                "dimension_scores": {
                    "actual_work": 70,
                    "seniority_and_scope": 45,
                    "transferability": 75,
                    "compensation": 55,
                    "work_model": 100,
                },
                "reasoning": "The operational work is relevant but the level and scope appear below the target.",
                "strengths": ["Operations management"],
                "concerns": ["Likely too junior"],
            }

        if "Helix Bio" in prompt:
            return {
                "dimension_scores": {
                    "actual_work": 92,
                    "seniority_and_scope": 90,
                    "transferability": 85,
                    "compensation": 95,
                    "work_model": 100,
                },
                "reasoning": "The functional work strongly transfers despite the unfamiliar industry.",
                "strengths": [
                    "Business transformation",
                    "Operating model design",
                    "Cross-functional leadership",
                ],
                "concerns": ["Limited direct biotechnology experience"],
            }

        if "Director, Customer Operations" in prompt:
            return {
                "dimension_scores": {
                    "actual_work": 96,
                    "seniority_and_scope": 95,
                    "transferability": 95,
                    "compensation": 95,
                    "work_model": 100,
                },
                "reasoning": "The role closely matches the candidate's target scope and operating experience.",
                "strengths": [
                    "Customer operations",
                    "Operating model design",
                    "Cross-functional transformation",
                ],
                "concerns": [],
            }

        return {
            "dimension_scores": {
                "actual_work": 95,
                "seniority_and_scope": 92,
                "transferability": 95,
                "compensation": 90,
                "work_model": 100,
            },
            "reasoning": "The role strongly aligns with business operations leadership and transformation experience.",
            "strengths": [
                "Business operations",
                "Strategic planning",
                "Operational transformation",
            ],
            "concerns": [],
        }


class JobSearchClient:
    """Adapter that makes the local job dataset look like a search service."""

    def search(self, candidate_profile: dict) -> list[dict]:
        return load_jobs()


if __name__ == "__main__":

    candidate_profile = load_yaml(
        "config/candidate_profile.example.yaml"
    )

    scoring_model = load_yaml(
        "config/scoring_model.yaml"
    )

    memory = Memory()

    search_client = JobSearchClient()
    llm_client = MockLLM()

    results, filtered_jobs = run_job_search(
        search_client=search_client,
        llm_client=llm_client,
        candidate_profile=candidate_profile,
        scoring_model=scoring_model,
        memory=memory,
    )

    print()
    print("FILTERED OPPORTUNITIES")
    print("=====================")

    for item in filtered_jobs:
        print(
            f"- {item['job']['title']} — "
            f"{item['job']['company']}"
        )
        print(
            f"  Reason: {item['reason']}"
        )

    print()
    print("JOB NEEDLE FINDER")
    print("=================")
    print()

    for index, result in enumerate(results, start=1):

        job = result["job"]
        evaluation = result["evaluation"]

        print(
            f"{index}. {job['title']} — {job['company']}"
        )

        print(
            f"   Score: {evaluation.score}"
        )

        print(
            f"   Recommendation: "
            f"{evaluation.recommendation.upper()}"
        )

        print(
            f"   Why: {evaluation.reasoning}"
        )

        print("   Dimensions:")

        for dimension, score in evaluation.dimension_scores.items():
            print(
                f"      {dimension}: {score}"
            )

        if evaluation.concerns:
            print(
                f"   Concern: "
                f"{evaluation.concerns[0]}"
            )

        print()