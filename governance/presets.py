from dataclasses import dataclass

@dataclass(frozen=True)
class GovernancePreset:
    name: str
    clarity_threshold: float
    risk_threshold: float
    description: str

PRESETS = {
    "Defensive": GovernancePreset(
        "Defensive", 84.0, 46.0,
        "High caution, tight tolerance."
    ),
    "Balanced": GovernancePreset(
        "Balanced", 75.0, 62.0,
        "Standard caution, normal tolerance."
    ),
    "Aggressive": GovernancePreset(
        "Aggressive", 66.0, 78.0,
        "Higher tolerance (still synthetic)."
    ),
}
