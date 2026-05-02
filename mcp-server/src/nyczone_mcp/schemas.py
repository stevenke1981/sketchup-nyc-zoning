"""Pydantic I/O schemas for MCP tools."""
from __future__ import annotations

from pydantic import BaseModel, Field


class QueryBuildingsInput(BaseModel):
    min_lon: float = Field(..., description="West longitude")
    min_lat: float = Field(..., description="South latitude")
    max_lon: float = Field(..., description="East longitude")
    max_lat: float = Field(..., description="North latitude")
    limit: int = Field(500, ge=1, le=5000)


class QueryZoningInput(BaseModel):
    lon: float
    lat: float


class QueryPlutoInput(BaseModel):
    bbl: str = Field(..., description="10-digit Borough-Block-Lot")


class SearchAddressInput(BaseModel):
    address: str = Field(..., description="NYC street address")


class BoroughStatsInput(BaseModel):
    borough: str = Field(
        ..., description="manhattan | brooklyn | queens | bronx | statenisland"
    )
