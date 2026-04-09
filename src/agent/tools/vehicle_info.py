"""Tool lấy thông tin xe (mock)."""

import random
from langchain_core.tools import tool

_MOCK_VEHICLES = [
    {
        "vin": "VF8-2024-HN-001234",
        "plate": "30A-123.45",
        "model": "VF 8 Plus",
        "year": 2024,
        "color": "Xanh Neptune",
        "battery_health": "92%",
        "last_service": "2025-12-15",
    },
    {
        "vin": "VF5-2025-SG-005678",
        "plate": "51G-678.90",
        "model": "VF 5 Plus",
        "year": 2025,
        "color": "Trắng Pristine",
        "battery_health": "98%",
        "last_service": "2026-01-20",
    },
    {
        "vin": "VFe34-2024-DN-009012",
        "plate": "43A-345.67",
        "model": "VF e34",
        "year": 2024,
        "color": "Đỏ Crimson",
        "battery_health": "87%",
        "last_service": "2025-11-03",
    },
]


def get_mock_vehicle() -> dict:
    """Trả về thông tin xe mock."""
    return random.choice(_MOCK_VEHICLES)


@tool
def get_vehicle_info(user_id: str = "current_user") -> str:
    """Lấy thông tin xe VinFast của người dùng từ hệ thống.
    Trả về VIN, biển số, model, tình trạng pin."""
    v = get_mock_vehicle()
    return (
        f"🚗 **Thông tin xe:**\n"
        f"- Model: {v['model']} ({v['year']})\n"
        f"- Biển số: {v['plate']}\n"
        f"- VIN: {v['vin']}\n"
        f"- Màu: {v['color']}\n"
        f"- Tình trạng pin: {v['battery_health']}\n"
        f"- Bảo dưỡng gần nhất: {v['last_service']}"
    )
