"""Unit tests for ServiceRecord schemas (no DB, no endpoints)."""

from datetime import date
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.service_record import ServiceRecordCreate


def test_service_record_create_valid():
    """Valid data creates ServiceRecordCreate successfully."""
    vehicle_id = uuid4()
    data = {
        "vehicle_id": vehicle_id,
        "service_type": "oil_change",
        "mileage": 120000,
        "service_date": date(2026, 2, 1),
        "notes": "Full synthetic 5W-30.",
    }
    record = ServiceRecordCreate(**data)
    assert record.vehicle_id == vehicle_id
    assert record.service_type == "oil_change"
    assert record.mileage == 120000
    assert record.service_date == date(2026, 2, 1)
    assert record.notes == "Full synthetic 5W-30."


def test_service_record_create_invalid_mileage_negative():
    """Negative mileage raises ValidationError."""
    vehicle_id = uuid4()
    with pytest.raises(ValidationError):
        ServiceRecordCreate(
            vehicle_id=vehicle_id,
            service_type="oil_change",
            mileage=-1,
            service_date=date(2026, 2, 1),
        )
