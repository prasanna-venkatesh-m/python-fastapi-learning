from pydantic import BaseModel, Field


class EvaluationMetric(BaseModel):
    score: int
    reason: str


class EvaluationResult(BaseModel):
    correctness: EvaluationMetric
    groundedness: EvaluationMetric
    relevance: EvaluationMetric
    completeness: EvaluationMetric
    abstention_quality: EvaluationMetric
    fairness_bias: EvaluationMetric
    safety_policy_compliance: EvaluationMetric
    instruction_compliance: EvaluationMetric

    total_score: int
    max_score: int
    normalized_score: float
    passed: bool = Field(alias="pass")
    critical_failure: bool
    failure_reasons: list[str]
    overall_assessment: str