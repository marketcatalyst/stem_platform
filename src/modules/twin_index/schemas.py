from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class SurveyAssetInput(BaseModel):
    """
    Validates data packets captured during rapid on-site asset inventory surveys.
    Enforces strict typing to guarantee computation integrity across the math engines.
    """

    asset_type_id: UUID = Field(
        ..., description="Unique reference matching our pre-seeded Asset Taxonomy."
    )
    quantity: int = Field(
        ..., ge=1, description="Number of active units deployed on-site."
    )
    average_kw_rating: float = Field(
        ..., gt=0.0, description="Nameplate power rating of the equipment class."
    )
    duty_cycle_hours_per_week: float = Field(
        ..., gt=0.0, le=168.0, description="Weekly operational runtime limits."
    )

    @field_validator("duty_cycle_hours_per_week")
    @classmethod
    def validate_weekly_hours(cls, value: float) -> float:
        if value > 168.0:
            raise ValueError(
                "Operational timeline profile cannot exceed total hours in a week (168 hours)."
            )
        return value


class RoughTwinAssessmentPayload(BaseModel):
    """
    Unified evaluation packet binding a specific client site to an un-metered inventory array.
    """

    site_id: UUID = Field(
        ..., description="Target site reference within the isolated tenant data plane."
    )
    assets: list[SurveyAssetInput] = Field(
        ..., description="List of un-metered assets observed on-site."
    )
