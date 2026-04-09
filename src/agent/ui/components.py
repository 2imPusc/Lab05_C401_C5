"""Streamlit UI components cho VinFast Rescue AI."""

import streamlit as st
from config import ISSUE_OPTIONS


def render_option_selector() -> int | None:
    """Hiển thị 4 nút chọn vấn đề (grid 2x2). Trả về option đã chọn hoặc None."""
    st.markdown("### Bạn gặp vấn đề gì?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            ISSUE_OPTIONS[1]["label"],
            key="opt_1",
            use_container_width=True,
            type="secondary",
        ):
            return 1
        if st.button(
            ISSUE_OPTIONS[3]["label"],
            key="opt_3",
            use_container_width=True,
            type="secondary",
        ):
            return 3

    with col2:
        if st.button(
            ISSUE_OPTIONS[2]["label"],
            key="opt_2",
            use_container_width=True,
            type="secondary",
        ):
            return 2
        if st.button(
            ISSUE_OPTIONS[4]["label"],
            key="opt_4",
            use_container_width=True,
            type="secondary",
        ):
            return 4

    return None


def render_classification_result(result: dict, issue_label: str):
    """Hiển thị kết quả phân loại."""
    severity = result["severity"]
    reason = result["reason"]

    if severity == "self_serviceable":
        st.info(f"🔧 **Đánh giá:** Vấn đề này có thể tự xử lý.\n\n_{reason}_")
    else:
        st.warning(f"🚨 **Đánh giá:** Cần hỗ trợ cứu hộ chuyên nghiệp.\n\n_{reason}_")


def render_info_confirmation(info: dict):
    """Hiển thị card xác nhận thông tin (vị trí + xe)."""
    loc = info["location"]
    v = info["vehicle"]

    st.markdown("### 📋 Xác nhận thông tin")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"**📍 Vị trí**\n\n"
            f"{loc['display']}\n\n"
            f"`{loc['lat']:.4f}, {loc['lon']:.4f}`\n\n"
            f"_Nguồn: {loc['source']}_"
        )

    with col2:
        st.markdown(
            f"**🚗 Thông tin xe**\n\n"
            f"{v['model']} ({v['year']})\n\n"
            f"Biển số: `{v['plate']}`\n\n"
            f"Pin: {v['battery_health']}"
        )


def render_rescue_proposal(proposal_text: str):
    """Hiển thị đề xuất cứu hộ."""
    st.markdown(proposal_text)
    st.markdown("---")
    st.markdown("### Bạn có muốn gọi cứu hộ không?")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        yes = st.button("✅ Có, gọi ngay", key="rescue_yes", type="primary", use_container_width=True)
    with col2:
        no = st.button("❌ Không", key="rescue_no", use_container_width=True)

    if yes:
        return "yes"
    if no:
        return "no"
    return None


def render_rescue_confirmed():
    """Hiển thị xác nhận đã gửi yêu cầu cứu hộ."""
    st.success(
        "## ✅ Đã gửi yêu cầu cứu hộ!\n\n"
        "Đội cứu hộ VinFast sẽ liên hệ bạn trong vòng **2 phút**.\n\n"
        "📞 Nếu cần hỗ trợ gấp, gọi ngay: **1900-23-23-89**\n\n"
        "_Hãy ở yên tại vị trí an toàn và bật đèn hazard._"
    )


def render_rescue_cancelled():
    """Hiển thị khi user từ chối cứu hộ."""
    st.info(
        "Đã hủy yêu cầu cứu hộ.\n\n"
        "Bạn có thể quay lại chọn vấn đề khác hoặc gọi hotline **1900-23-23-89** bất cứ lúc nào."
    )


def render_low_confidence():
    """Hiển thị UI khi AI không đủ tin cậy để chẩn đoán."""
    st.warning(
        "🤔 **Tôi chưa thể chẩn đoán chính xác sự cố của bạn.**\n\n"
        "_Mô tả hiện tại chưa đủ thông tin kỹ thuật để xác định nguyên nhân. "
        "Vì lý do an toàn, tôi khuyên bạn nên liên hệ kỹ thuật viên._"
    )

    st.markdown("### Bạn muốn làm gì tiếp?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📞 Nối máy kỹ thuật viên", key="lc_technician", type="primary", use_container_width=True):
            return "technician"
    with col2:
        if st.button("💬 Thử mô tả lại", key="lc_retry", use_container_width=True):
            return "retry"

    return None


def render_csat_rating() -> int | None:
    """Hiển thị widget đánh giá CSAT 1-5 sao."""
    st.markdown("---")
    st.markdown("### ⭐ Đánh giá trải nghiệm")
    st.markdown("Bạn hài lòng với hỗ trợ của AI như thế nào?")

    cols = st.columns(5)
    for i, col in enumerate(cols, 1):
        with col:
            if st.button(f"{'⭐' * i}", key=f"csat_{i}", use_container_width=True):
                return i
    return None
