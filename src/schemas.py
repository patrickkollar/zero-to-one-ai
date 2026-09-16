"""
Data structures used by the Job Needle Finder.

Schemas define the contract between different parts of the system.
"""

from pydantic import BaseModel


class DimensionScores(BaseModel):
    """
    Scores for each evaluation dimension.
    """

    actual_work: float
    seniority_and_scope: float
    transferability: float
    compensation: float
    work_model: float


class LLMEvaluation(BaseModel):
    """
    Structured judgment returned by the reasoning layer.
    """

    dimension_scores: DimensionScores
    reasoning: str
    strengths: list[str]
    concerns: list[str]