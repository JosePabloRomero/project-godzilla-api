from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MultiCloudPayload(BaseModel):
    """Hybrid payload received by the multicloud integration endpoint."""

    cliente: dict[str, Any] = Field(
        ...,
        description="Client data block.",
    )
    podcast: dict[str, Any] = Field(
        ...,
        description="Podcast data block.",
    )
    vehicle_id: UUID | None = Field(
        default=None,
        description="Optional vehicle id to resolve first.",
    )

    model_config = ConfigDict(extra="allow")
