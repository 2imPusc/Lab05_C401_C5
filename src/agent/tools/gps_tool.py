"""Tool lấy vị trí GPS (mock)."""

import random
from langchain_core.tools import tool

# Một số vị trí mẫu tại Việt Nam
_MOCK_LOCATIONS = {
    "hanoi": {"lat": 21.0285, "lon": 105.8542, "display": "Hà Nội, gần Hoàn Kiếm"},
    "hcm": {"lat": 10.7769, "lon": 106.7009, "display": "TP.HCM, gần Quận 1"},
    "danang": {"lat": 16.0544, "lon": 108.2022, "display": "Đà Nẵng, gần cầu Rồng"},
}


def get_mock_location() -> dict:
    """Trả về vị trí mock ngẫu nhiên (simulate GPS)."""
    loc = random.choice(list(_MOCK_LOCATIONS.values()))
    return {
        "lat": loc["lat"] + random.uniform(-0.01, 0.01),
        "lon": loc["lon"] + random.uniform(-0.01, 0.01),
        "display": loc["display"],
        "source": "GPS (tự động)",
    }


@tool
def get_current_location() -> str:
    """Lấy vị trí hiện tại của người dùng từ GPS.
    Trả về tọa độ và địa chỉ ước tính."""
    loc = get_mock_location()
    return (
        f"📍 Vị trí hiện tại: {loc['display']}\n"
        f"Tọa độ: {loc['lat']:.4f}, {loc['lon']:.4f}\n"
        f"Nguồn: {loc['source']}"
    )
