"""PDPA compliance tests for API-layer utilities."""
from __future__ import annotations

import pytest


@pytest.fixture
def sample_consent_record() -> dict[str, str | None]:
    return {
        "user_id": "user-123",
        "consented_at": "2025-11-01T10:00:00Z",
        "revoked_at": None,
    }


def test_require_consent_raises_for_missing_record() -> None:
    """API must block access when no consent record is present."""
    from src.apps.api.app import pdpa  # noqa: PLC0415

    with pytest.raises(pdpa.ConsentMissingError):
        pdpa.require_consent(None)


def test_require_consent_allows_active_consent(sample_consent_record: dict[str, str | None]) -> None:
    """Active consent records should pass without raising."""
    from src.apps.api.app import pdpa  # noqa: PLC0415

    pdpa.require_consent(sample_consent_record)


@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("user@example.com", "***@example.com"),
        ("นายกสมาคม@thai.co.th", "***@thai.co.th"),
    ],
)
def test_mask_email_hides_local_part(email: str, expected: str) -> None:
    """Email masking must hide all characters before the domain."""
    from src.apps.api.app import pdpa  # noqa: PLC0415

    assert pdpa.mask_email(email) == expected


@pytest.mark.parametrize(
    ("latitude", "longitude", "expected"),
    [
        (13.756331, 100.501765, (13.756, 100.502)),
        (51.507351, -0.127758, (51.507, -0.128)),
    ],
)
def test_round_gps_three_decimals(latitude: float, longitude: float, expected: tuple[float, float]) -> None:
    """GPS coordinates must round to three decimals before storage/logging."""
    from src.apps.api.app import pdpa  # noqa: PLC0415

    assert pdpa.round_gps(latitude, longitude) == expected
