"""Module containing schemas."""

from __future__ import annotations

from pydantic import BaseModel, field_validator

RATE_CODE_LEN = 3


class CommonResponse(BaseModel):
    """Common response class."""

    success: bool
    code: str | None
    message: str


class ConvertRequest(BaseModel):
    """Request body of convert endpoint."""

    amount: float
    source: str
    target: str

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v: str) -> str:
        """Validate source code."""
        if len(v) != RATE_CODE_LEN:
            msg = "Source code should be 3 length."
            raise ValueError(msg)
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v: str) -> str:
        """Validate target code."""
        if len(v) != RATE_CODE_LEN:
            msg = "Target code should be 3 length."
            raise ValueError(msg)
        return v


class ConvertResponse(BaseModel):
    """Response of covnert endpoint."""

    amount: float
    source: str
    target: str
    result: float
