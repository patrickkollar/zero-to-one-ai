"""
Job opportunity evaluator.

This module demonstrates the reasoning layer of the system.
The LLM receives:
    1. The candidate profile
    2. The evaluation model
    3. A job opportunity

It returns a structured assessment.

No personal candidate information belongs in this public example.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Evaluation:
    score: float
    recommendation: str
    reasoning: str
    strengths: list[str]
    concerns: list[str]


def build_evaluation_prompt(
    job: Dict[str, Any],
    candidate_profile: Dict[str, Any],
    scoring_model: Dict[str, Any],
) -> str:
    """
    Build the context supplied to the reasoning model.

    The important design principle:
    the model does not receive an arbitrary question.
    It receives a structured decision problem.
    """

    return f"""
Evaluate this job opportunity against the candidate profile.

CANDIDATE:
{candidate_profile}

EVALUATION MODEL:
{scoring_model}

JOB:
{job}

Return:

1. Overall score from 0-100
2. Recommendation:
   - exceptional
   - pursue
   - investigate
   - watch
   - reject
3. Why this opportunity fits
4. Concerns or gaps
5. The strongest reason this candidate should pursue it
6. The strongest reason they should not

Evaluate the actual work described in the job,
not simply the title.

Distinguish between:
- hard requirements
- preferred qualifications
- transferable experience
- genuine gaps

Do not invent information that is not present in the job posting.
"""


def evaluate_job(
    job: Dict[str, Any],
    candidate_profile: Dict[str, Any],
    scoring_model: Dict[str, Any],
    llm_client,
) -> Evaluation:
    """
    Send the structured decision problem to an LLM.

    The specific LLM provider is intentionally injected rather
    than hard-coded. This keeps the reasoning layer separate
    from the workflow.
    """

    prompt = build_evaluation_prompt(
        job,
        candidate_profile,
        scoring_model,
    )

    response = llm_client.generate(prompt)

    return Evaluation(
        score=response["score"],
        recommendation=response["recommendation"],
        reasoning=response["reasoning"],
        strengths=response["strengths"],
        concerns=response["concerns"],
    )
