"""
Scoring engine.

The reasoning layer evaluates the job across several dimensions.
This module applies the configured weights and produces the final
opportunity score.

This separation is important:

    LLM = judgment about each dimension
    Scoring engine = deterministic math
    Workflow = orchestration
"""


def calculate_score(
    dimension_scores: dict[str, float],
    scoring_model: dict,
) -> float:
    """
    Calculate a weighted score from 0-100.

    Each dimension score should be between 0 and 100.
    """

    dimensions = scoring_model["dimensions"]

    weighted_total = 0.0

    for dimension, configuration in dimensions.items():

        weight = configuration["weight"]
        score = dimension_scores.get(dimension, 0)

        weighted_total += score * weight

    return round(weighted_total, 1)


def get_recommendation(
    score: float,
    scoring_model: dict,
) -> str:
    """Convert a score into the configured recommendation."""

    thresholds = scoring_model["thresholds"]

    if score >= thresholds["exceptional"]:
        return "exceptional"

    if score >= thresholds["pursue"]:
        return "pursue"

    if score >= thresholds["investigate"]:
        return "investigate"

    if score >= thresholds["watch"]:
        return "watch"

    return "reject"
