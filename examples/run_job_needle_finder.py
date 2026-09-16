"""
Run the Job Needle Finder end-to-end.

The workflow:

    Load
      ↓
    Hard Filters
      ↓
    LLM Evaluation
      ↓
    Deterministic Scoring
      ↓
    Ranking
      ↓
    Results

The reasoning engine can be switched between a local mock and
the real OpenAI implementation.
"""

from src.config_loader import load_yaml
from src.job_loader import load_jobs
from src.llm import OpenAIClient
from src.memory import Memory
from src.schemas import LLMEvaluation
from src.workflow import run_job_search


class MockLLM:
    """
    Local reasoning engine used for development and testing.

    This allows the entire workflow to be tested without
    making API calls.
    """

    def __init__(self, evaluations: dict[str, LLMEvaluation]):
        self.evaluations = evaluations

    def generate(self, prompt: str) -> LLMEvaluation:
        """Return a predefined evaluation based on the job in the prompt."""

        for job_name, evaluation in self.evaluations.items():
            if job_name in prompt:
                return evaluation

        return self.evaluations["default"]


def build_mock_llm() -> MockLLM:
    """Build the deterministic reasoning engine used for local testing."""

    return MockLLM(
        evaluations={
            "Reporting & Analytics": LLMEvaluation(
                dimension_scores={
                    "actual_work": 45,
                    "seniority_and_scope": 85,
                    "transferability": 60,
                    "compensation": 85,
                    "work_model": 100,
                },
                reasoning=(
                    "The role is primarily reporting and analytics "
                    "rather than business operations leadership."
                ),
                strengths=["Executive reporting"],
                concerns=["Reporting-heavy scope"],
            ),
            "Manager, Operations": LLMEvaluation(
                dimension_scores={
                    "actual_work": 70,
                    "seniority_and_scope": 45,
                    "transferability": 75,
                    "compensation": 55,
                    "work_model": 100,
                },
                reasoning=(
                    "The operational work is relevant but the level "
                    "and scope appear below the target."
                ),
                strengths=["Operations management"],
                concerns=["Likely too junior"],
            ),
            "Helix Bio": LLMEvaluation(
                dimension_scores={
                    "actual_work": 92,
                    "seniority_and_scope": 90,
                    "transferability": 85,
                    "compensation": 95,
                    "work_model": 100,
                },
                reasoning=(
                    "The functional work strongly transfers despite "
                    "the unfamiliar industry."
                ),
                strengths=[
                    "Business transformation",
                    "Operating model design",
                    "Cross-functional leadership",
                ],
                concerns=["Limited direct biotechnology experience"],
            ),
            "Director, Customer Operations": LLMEvaluation(
                dimension_scores={
                    "actual_work": 96,
                    "seniority_and_scope": 95,
                    "transferability": 95,
                    "compensation": 95,
                    "work_model": 100,
                },
                reasoning=(
                    "The role closely matches the candidate's target "
                    "scope and operating experience."
                ),
                strengths=[
                    "Customer operations",
                    "Operating model design",
                    "Cross-functional transformation",
                ],
                concerns=[],
            ),
            "default": LLMEvaluation(
                dimension_scores={
                    "actual_work": 95,
                    "seniority_and_scope": 92,
                    "transferability": 95,
                    "compensation": 90,
                    "work_model": 100,
                },
                reasoning=(
                    "The role strongly aligns with business operations "
                    "leadership and transformation experience."
                ),
                strengths=[
                    "Business operations",
                    "Strategic planning",
                    "Operational transformation",
                ],
                concerns=[],
            ),
        }
    )


class JobSearchClient:
    """
    Adapter that makes the local job dataset look like a search service.

    Later this can be replaced by a real job-search provider without
    changing the workflow.
    """

    def search(self, candidate_profile: dict) -> list[dict]:
        """Return the current job dataset."""

        return load_jobs()


def print_results(results: list[dict], filtered_jobs: list[dict]):
    """Display the results of one Job Needle Finder run."""

    print()
    print("FILTERED OPPORTUNITIES")
    print("======================")

    for item in filtered_jobs:
        job = item["job"]

        print(
            f"- {job['title']} — {job['company']}"
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


def main(use_real_llm: bool = False):
    """Run one complete Job Needle Finder cycle."""

    candidate_profile = load_yaml(
        "config/candidate_profile.example.yaml"
    )

    scoring_model = load_yaml(
        "config/scoring_model.yaml"
    )

    memory = Memory()

    search_client = JobSearchClient()

    if use_real_llm:
        llm_client = OpenAIClient(
            model="gpt-5.6-luna"
        )
    else:
        llm_client = build_mock_llm()

    results, filtered_jobs = run_job_search(
        search_client=search_client,
        llm_client=llm_client,
        candidate_profile=candidate_profile,
        scoring_model=scoring_model,
        memory=memory,
    )

    print_results(
        results=results,
        filtered_jobs=filtered_jobs,
    )


if __name__ == "__main__":
    main()