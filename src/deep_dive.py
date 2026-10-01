"""
Deep Dive analysis for a selected job opportunity.

The Deep Dive is a second-stage reasoning step that happens only
when the user requests more detail on a specific opportunity.
"""

from typing import Any, Dict

from src.schemas import DeepDiveAnalysis


def build_deep_dive_prompt(
    job: Dict[str, Any],
    candidate_profile: Dict[str, Any],
    initial_evaluation,
) -> str:
    """
    Build a concise second-stage analysis for a selected job.
    """

    return f"""
Perform a focused second-stage analysis of this job opportunity
against the candidate profile.

The initial evaluation has already determined the overall fit
and scores. Do not simply repeat that analysis.

CANDIDATE:
{candidate_profile}

JOB:
{job}

INITIAL EVALUATION:
Overall score: {initial_evaluation.score}
Recommendation: {initial_evaluation.recommendation}

Reasoning:
{initial_evaluation.reasoning}

Strengths:
{initial_evaluation.strengths}

Concerns:
{initial_evaluation.concerns}

Dimension scores:
{initial_evaluation.dimension_scores}

Return four sections:

1. WHY THIS FITS

Identify the 3-5 strongest reasons the candidate's actual
experience aligns with the actual work in this role.

Focus on substantive alignment, not keyword matching.

2. WHERE IT DOESN'T FIT

Identify the 3-5 most meaningful gaps, mismatches, risks,
or unknowns.

Distinguish genuine gaps from information that simply isn't
provided in the job description.

3. WHAT TO INVESTIGATE

Identify the 4-6 most useful questions the candidate should
answer before investing significant time in the opportunity.

Focus on things such as:
- organizational scope
- decision authority
- team size
- reporting structure
- responsibilities
- compensation
- workload
- travel
- remote expectations
- organizational maturity
- technical expectations

Only identify questions that are reasonable based on the
available information.

4. BOTTOM LINE

Provide a concise 2-4 sentence conclusion.

Summarize the overall fit and identify the most important
unknowns the candidate should resolve.

Do not tell the candidate whether they should apply.

Do not invent facts about the candidate or employer.

Do not assume experience that is not present in the candidate
profile.

Do not simply restate the job description.

Keep the analysis concise and decision-oriented.
"""


def deep_dive_job(
    job: Dict[str, Any],
    candidate_profile: Dict[str, Any],
    initial_evaluation,
    llm_client,
) -> DeepDiveAnalysis:
    """
    Generate a detailed Deep Dive analysis for one selected job.
    """

    prompt = build_deep_dive_prompt(
        job=job,
        candidate_profile=candidate_profile,
        initial_evaluation=initial_evaluation,
    )

    return llm_client.generate_deep_dive(prompt)