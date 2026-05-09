from dataclasses import dataclass


@dataclass
class AIInsight:
    regime: str
    confidence: float
    sentiment_score: float


class AIModel:
    """Optional AI layer. Stubbed for easy replacement with LSTM/Transformer pipelines."""

    def classify_regime(self, volatility: float, trend_strength: float) -> AIInsight:
        if trend_strength > 0.6 and volatility < 0.4:
            return AIInsight("bull", 0.75, 0.2)
        if trend_strength < 0.3 and volatility > 0.7:
            return AIInsight("bear", 0.70, -0.4)
        return AIInsight("sideways", 0.55, 0.0)

    def directional_probability(self) -> float:
        # Placeholder for medium-term directional model.
        return 0.62
