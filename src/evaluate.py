"""
Job opportunity evaluator.

The reasoning layer evaluates the opportunity across the dimensions
defined by the scoring model.

The LLM provides judgments.
The scoring engine applies the weights.
The workflow orchestrates the process.
"""

from dataclasses import dataclass
from typing import Any, Dict

from src.scoring import calculate_score, get_recommendation


@dataclass
class Evaluation:
    score: float
    recommendation: str
    reasoning: str
    strengths: list[str]
    concerns: list[str]
    dimension_scores: Dict[str, float]


def build_evaluation_prompt(
    job: Dict[str, Any],
    candidate_profile: Dict[str, Any],
    scoring_model: Dict[str, Any],
) -> str:
    """
    Build the structured decision problem supplied to the reasoning model.
    """

    return f"""
Evaluate this job opportunity against the candidate profile.

CANDIDATE:
{candidate_profile}

EVALUATION MODEL:
{scoring_model}

JOB:
{job}

Return structured results containing:

1. Scores from 0-100 for each evaluation dimension:
   - actual_work
   - seniority_and_scope
   - transferability
   - compensation
   - work_model

2. Why the opportunity fits

3. Concerns or gaps

4. The strongest reason this candidate should pursue it

5. The strongest reason they should not

Evaluate the actual work described in the job,
not simply the title.

Distinguish between:
- hard requirements
- preferred qualifications
- transferable experience
- genuine gaps

Do not invent information that is not present in the job posting.

Do not calculate a final weighted score.
The scoring engine will do that separately.
"""


def evaluate_job(
    job: Dict[str, Any],
    candidate_profile: Dict[str, Any],
    scoring_model: Dict[str, Any],
    llm_client,
) -> Evaluation:
    """
    Evaluate a job using the reasoning layer and deterministic scorer.
    """

    prompt = build_evaluation_prompt(
        job,
        candidate_profile,
        scoring_model,
    )

    response = llm_client.generate(prompt)

    dimension_scores = response["dimension_scores"]

    score = calculate_score(
        dimension_scores=dimension_scores,
        scoring_model=scoring_model,
    )

    recommendation = get_recommendation(
        score=score,
        scoring_model=scoring_model,
    )

    return Evaluation(
        score=score,
        recommendation=recommendation,
        reasoning=response["reasoning"],
        strengths=response["strengths"],
        concerns=response["concerns"],
        dimension_scores=dimension_scores,
    )