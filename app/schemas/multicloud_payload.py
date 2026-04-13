from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.vehicle import VehicleCreate


class MultiCloudPayload(BaseModel):
    """Payload envelope received from API #1 and enriched before forwarding."""

    api1_payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Opaque JSON received from API #1 (can be nested/dynamic).",
    )
    vehicle_seed: VehicleCreate | None = Field(
        default=None,
        description="Optional vehicle attributes to find/create a Vehicle entity.",
    )
    vehicle: dict[str, Any] | None = Field(
        default=None,
        description="Reserved slot for the injected Vehicle payload before forwarding.",
    )

    model_config = ConfigDict(extra="allow")
