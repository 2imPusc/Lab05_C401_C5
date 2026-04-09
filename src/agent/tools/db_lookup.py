"""Tool tra cứu database: hướng dẫn sửa chữa + trạm gần nhất."""

import json
import math
from pathlib import Path
from langchain_core.tools import tool

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_json(filename: str) -> list:
    with open(_DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Khoảng cách (km) giữa 2 tọa độ."""
    R = 6371 # cái này là bán kính trung bình của Trái Đất (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


@tool
def search_troubleshoot(query: str) -> str:
    """Tìm hướng dẫn xử lý sự cố xe VinFast từ knowledge base.
    Truyền vào mô tả vấn đề, trả về hướng dẫn step-by-step."""
    kb = _load_json("troubleshoot_kb.json")
    query_lower = query.lower()

    best_match = None
    best_score = 0

    # loop qua tất cả loại vấn đề trong troubleshoot_kb.json
    # từng vấn đề đều có keyword. Vấn đề nào match nhiều keyword trong query nhất,
    # thì classifier là vấn đề đó
    for entry in kb:
        score = sum(1 for kw in entry["keywords"] if kw in query_lower)
        if score > best_score:
            best_score = score
            best_match = entry

    if best_match:
        return (
            f"**[{best_match['id']}] {best_match['issue']}** (Mức độ: {best_match['severity']})\n\n"
            f"{best_match['guide']}\n\n"
            f"_Nguồn: {best_match['id']} — {best_match['issue']}_"
        )
    return "Không tìm thấy hướng dẫn phù hợp trong cơ sở dữ liệu. Vui lòng mô tả chi tiết hơn hoặc gọi hotline 1900-23-23-89."


# Kiếm 3 trạm sạc gần nhất rồi trả lại
@tool
def find_nearest_stations(latitude: float, longitude: float, service_type: str = "all") -> str:
    """Tìm trạm sạc/bảo hành/cứu hộ VinFast gần nhất.
    latitude, longitude: tọa độ người dùng.
    service_type: 'sạc', 'bảo hành', 'cứu hộ', hoặc 'all'."""
    stations = _load_json("stations.json")

    if service_type != "all":
        stations = [s for s in stations if service_type in s["type"]]

    for s in stations:
        s["distance_km"] = round(_haversine(latitude, longitude, s["lat"], s["lon"]), 1)

    stations.sort(key=lambda s: s["distance_km"])
    top3 = stations[:3]

    if not top3:
        return "Không tìm thấy trạm phù hợp gần bạn."

    result = "**Trạm gần nhất:**\n\n"
    for i, s in enumerate(top3, 1):
        result += (
            f"{i}. **{s['name']}**\n"
            f"   📍 {s['address']}\n"
            f"   📞 {s['phone']}\n"
            f"   🕐 {s['hours']}\n"
            f"   📏 Cách bạn: {s['distance_km']} km\n"
            f"   🔧 Dịch vụ: {', '.join(s['type'])}\n\n"
        )
    return result
