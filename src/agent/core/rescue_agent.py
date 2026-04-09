"""Rescue Agent cho nhánh 'phức tạp hơn' — flow lấy info → đề xuất cứu hộ."""

import random
from tools.gps_tool import get_mock_location
from tools.vehicle_info import get_mock_vehicle
from tools.db_lookup import _load_json, _haversine


def auto_collect_info() -> dict:
    """Tự động thu thập thông tin user (GPS + xe). Mock data."""
    location = get_mock_location()
    vehicle = get_mock_vehicle()
    return {
        "location": location,
        "vehicle": vehicle,
    }


def find_rescue_service(lat: float, lon: float, issue_type: str) -> dict:
    """Tìm dịch vụ cứu hộ phù hợp nhất."""
    stations = _load_json("stations.json")
    rescue_stations = [s for s in stations if "cứu hộ" in s["type"]]

    for s in rescue_stations:
        s["distance_km"] = round(_haversine(lat, lon, s["lat"], s["lon"]), 1)

    rescue_stations.sort(key=lambda s: s["distance_km"])

    if not rescue_stations:
        return None

    best = rescue_stations[0]

    # Ước tính chi phí dựa trên khoảng cách + loại sự cố
    base_cost = {
        "Hết pin / hết xăng": 500_000,
        "Hỏng máy / lỗi kỹ thuật": 800_000,
        "Tai nạn / va chạm": 1_200_000,
        "Thủng lốp": 400_000,
    }
    cost = base_cost.get(issue_type, 600_000)
    cost += int(best["distance_km"] * 15_000)  # 15k/km

    # ETA ước tính
    eta_minutes = max(15, int(best["distance_km"] * 2.5) + random.randint(5, 15))

    return {
        "station": best,
        "cost": cost,
        "cost_display": f"{cost:,.0f} VNĐ",
        "eta_minutes": eta_minutes,
        "eta_display": f"~{eta_minutes} phút",
    }


def format_rescue_proposal(info: dict, rescue: dict, issue_type: str) -> str:
    """Format đề xuất cứu hộ để hiển thị cho user."""
    v = info["vehicle"]
    loc = info["location"]
    s = rescue["station"]

    return (
        f"## 📋 Thông tin yêu cầu cứu hộ\n\n"
        f"**Xe:** {v['model']} ({v['year']}) — Biển số: {v['plate']}\n\n"
        f"**Vị trí:** {loc['display']} ({loc['lat']:.4f}, {loc['lon']:.4f})\n\n"
        f"**Sự cố:** {issue_type}\n\n"
        f"---\n\n"
        f"## 🚨 Đề xuất dịch vụ cứu hộ\n\n"
        f"**Đội cứu hộ:** {s['name']}\n\n"
        f"**Khoảng cách:** {s['distance_km']} km\n\n"
        f"**Chi phí ước tính:** {rescue['cost_display']}\n\n"
        f"**Thời gian dự kiến:** {rescue['eta_display']}\n\n"
        f"**Hotline:** {s['phone']}"
    )
