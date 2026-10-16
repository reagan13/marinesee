from io import BytesIO

import numpy as np
from PIL import Image

from dataset_contract import TRAINABLE_SPECIES
from serve_identify import identify_payload


def _jpeg() -> bytes:
    frame = np.full((256, 256, 3), (190, 170, 150), dtype=np.uint8)
    frame[30:230, 118:138] = (30, 150, 40)
    buf = BytesIO()
    Image.fromarray(frame).save(buf, format="JPEG")
    return buf.getvalue()


def test_empty_body() -> None:
    status, payload = identify_payload(b"")
    assert status == 400
    assert payload["success"] is False


def test_too_large() -> None:
    status, payload = identify_payload(b"x" * (8 * 1024 * 1024 + 1))
    assert status == 413
    assert payload["success"] is False


def test_unreadable_bytes_stay_an_error() -> None:
    status, payload = identify_payload(b"not-an-image")
    assert status == 400
    assert payload["success"] is False
    assert "slug" not in payload.get("data", {})


def test_photo_returns_a_trainable_species_and_a_percent() -> None:
    status, payload = identify_payload(_jpeg())
    assert status == 200
    assert payload["success"] is True
    data = payload["data"]
    assert data["slug"] in TRAINABLE_SPECIES
    assert 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["low_confidence"], bool)
    again, _ = identify_payload(_jpeg())
    assert again == 200


if __name__ == "__main__":
    test_empty_body()
    test_too_large()
    test_unreadable_bytes_stay_an_error()
    test_photo_returns_a_trainable_species_and_a_percent()
    print("ok")
