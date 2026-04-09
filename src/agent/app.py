"""VinFast Rescue AI — Streamlit App Entry Point."""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from config import APP_TITLE, APP_ICON, ISSUE_OPTIONS
from ui.chat_ui import AppState, init_session_state, reset_session, set_state, add_message, get_messages
from ui.components import (
    render_option_selector,
    render_classification_result,
    render_info_confirmation,
    render_rescue_proposal,
    render_rescue_confirmed,
    render_rescue_cancelled,
)
from core.classifier import classify_issue
from core.react_agent import create_react_agent_executor, run_react_agent
from core.rescue_agent import auto_collect_info, find_rescue_service, format_rescue_proposal

# ── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
)

# ── Custom CSS ───────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stButton"] > button {
        height: 80px;
        font-size: 1.1rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: all 0.2s ease;
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #1a73e8;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.15);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ── Init ─────────────────────────────────────────────
init_session_state()

# ── Sidebar ──────────────────────────────────────────
with st.sidebar:
    st.markdown(f"# {APP_TITLE}")
    st.markdown("---")
    st.markdown(
        "Trợ lý AI hỗ trợ xử lý sự cố xe VinFast.\n\n"
        "**Hai chế độ:**\n"
        "- 🔧 **Tự xử lý** — Chat với AI để troubleshoot\n"
        "- 🚨 **Cứu hộ** — Gọi đội cứu hộ nhanh chóng"
    )
    st.markdown("---")

    current_state = st.session_state.app_state
    state_labels = {
        AppState.SELECT_ISSUE: "⏳ Chọn vấn đề",
        AppState.CLASSIFYING: "🔄 Đang phân loại...",
        AppState.SELF_SERVICE_CHAT: "💬 Chat troubleshoot",
        AppState.RESCUE_COLLECT_INFO: "📋 Thu thập thông tin",
        AppState.RESCUE_CONFIRM_INFO: "✅ Xác nhận thông tin",
        AppState.RESCUE_PROPOSAL: "🚨 Đề xuất cứu hộ",
        AppState.RESCUE_CONFIRMED: "✅ Đã gửi yêu cầu",
        AppState.RESCUE_CANCELLED: "❌ Đã hủy",
    }
    st.markdown(f"**Trạng thái:** {state_labels.get(current_state, current_state)}")

    st.markdown("---")
    if st.button("🔄 Bắt đầu lại", use_container_width=True):
        reset_session()
        st.rerun()

    st.markdown("---")
    st.caption("📞 Hotline: 1900-23-23-89\n\n⚠️ Đây là prototype demo")

# ── Main Content ─────────────────────────────────────
st.markdown(f"# {APP_TITLE}")

state = st.session_state.app_state

# ─── State: SELECT_ISSUE ─────────────────────────────
if state == AppState.SELECT_ISSUE:
    st.markdown("Xin chào! Tôi là trợ lý AI của VinFast. Hãy cho tôi biết bạn đang gặp vấn đề gì.")
    st.markdown("")

    selected = render_option_selector()

    if selected:
        st.session_state.selected_issue = selected
        issue_label = ISSUE_OPTIONS[selected]["label"]
        add_message("user", f"Tôi gặp vấn đề: {issue_label}")
        set_state(AppState.CLASSIFYING)
        st.rerun()

# ─── State: CLASSIFYING ──────────────────────────────
elif state == AppState.CLASSIFYING:
    issue_option = st.session_state.selected_issue
    issue_label = ISSUE_OPTIONS[issue_option]["label"]

    # Hiển thị chat history
    for msg in get_messages():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    with st.spinner("🔄 Đang phân loại sự cố..."):
        classification = classify_issue(issue_option)
        st.session_state.classification = classification

    if classification["severity"] == "self_serviceable":
        add_message("assistant",
            f"🔧 **Đánh giá:** Vấn đề này có thể tự xử lý.\n\n"
            f"_{classification['reason']}_\n\n"
            f"Hãy mô tả chi tiết hơn để tôi hướng dẫn bạn nhé!"
        )
        set_state(AppState.SELF_SERVICE_CHAT)
    else:
        add_message("assistant",
            f"🚨 **Đánh giá:** Cần hỗ trợ cứu hộ chuyên nghiệp.\n\n"
            f"_{classification['reason']}_\n\n"
            f"Tôi sẽ thu thập thông tin để gọi cứu hộ cho bạn."
        )
        set_state(AppState.RESCUE_COLLECT_INFO)

    st.rerun()

# ─── State: SELF_SERVICE_CHAT ────────────────────────
elif state == AppState.SELF_SERVICE_CHAT:
    # Hiển thị chat history
    for msg in get_messages():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Tạo agent nếu chưa có
    if st.session_state.agent_executor is None:
        st.session_state.agent_executor = create_react_agent_executor()

    # Chat input
    if user_input := st.chat_input("Mô tả chi tiết vấn đề của bạn..."):
        add_message("user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)

        # Build LangChain chat history
        lc_history = []
        for msg in get_messages()[:-1]:  # exclude latest user message
            if msg["role"] == "user":
                lc_history.append(HumanMessage(content=msg["content"]))
            else:
                lc_history.append(AIMessage(content=msg["content"]))

        with st.chat_message("assistant"):
            with st.spinner("Đang suy nghĩ..."):
                response = run_react_agent(
                    st.session_state.agent_executor,
                    user_input,
                    lc_history,
                )
            st.markdown(response)
            add_message("assistant", response)

# ─── State: RESCUE_COLLECT_INFO ──────────────────────
elif state == AppState.RESCUE_COLLECT_INFO:
    for msg in get_messages():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    with st.spinner("📡 Đang tự động thu thập thông tin vị trí và xe..."):
        info = auto_collect_info()
        st.session_state.rescue_info = info

    set_state(AppState.RESCUE_CONFIRM_INFO)
    st.rerun()

# ─── State: RESCUE_CONFIRM_INFO ──────────────────────
elif state == AppState.RESCUE_CONFIRM_INFO:
    for msg in get_messages():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    info = st.session_state.rescue_info
    render_info_confirmation(info)

    st.markdown("---")
    st.markdown("Thông tin trên có chính xác không?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Chính xác", key="info_correct", type="primary", use_container_width=True):
            add_message("user", "Thông tin chính xác.")
            set_state(AppState.RESCUE_PROPOSAL)
            st.rerun()
    with col2:
        if st.button("✏️ Nhập lại", key="info_manual", use_container_width=True):
            st.session_state.show_manual_form = True

    # Form nhập tay
    if st.session_state.get("show_manual_form", False):
        st.markdown("### Nhập thông tin thủ công")
        with st.form("manual_info_form"):
            manual_address = st.text_input("Địa chỉ / vị trí hiện tại", placeholder="VD: 191 Bà Triệu, Hà Nội")
            manual_plate = st.text_input("Biển số xe", placeholder="VD: 30A-123.45")
            manual_model = st.selectbox("Model xe", ["VF 5 Plus", "VF e34", "VF 6", "VF 7", "VF 8 Plus", "VF 9", "Khác"])
            submitted = st.form_submit_button("Xác nhận", type="primary")

            if submitted:
                st.session_state.rescue_info = {
                    "location": {
                        "lat": 21.0115, "lon": 105.8490,
                        "display": manual_address or "Hà Nội",
                        "source": "Nhập thủ công",
                    },
                    "vehicle": {
                        "model": manual_model, "year": 2024,
                        "plate": manual_plate, "vin": "N/A",
                        "color": "N/A", "battery_health": "N/A",
                        "last_service": "N/A",
                    },
                }
                st.session_state.show_manual_form = False
                add_message("user", f"Đã nhập thông tin: {manual_address}, xe {manual_model} biển {manual_plate}")
                set_state(AppState.RESCUE_PROPOSAL)
                st.rerun()

# ─── State: RESCUE_PROPOSAL ──────────────────────────
elif state == AppState.RESCUE_PROPOSAL:
    for msg in get_messages():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    info = st.session_state.rescue_info
    issue_option = st.session_state.selected_issue
    issue_label = ISSUE_OPTIONS[issue_option]["label"]

    # Tìm dịch vụ cứu hộ
    if st.session_state.rescue_service is None:
        with st.spinner("🔍 Đang tìm đội cứu hộ gần nhất..."):
            rescue = find_rescue_service(
                info["location"]["lat"],
                info["location"]["lon"],
                issue_label,
            )
            st.session_state.rescue_service = rescue
            proposal_text = format_rescue_proposal(info, rescue, issue_label)
            st.session_state.rescue_proposal_text = proposal_text
            add_message("assistant", proposal_text)
            st.rerun()
    else:
        # Hiển thị đề xuất
        choice = render_rescue_proposal(st.session_state.rescue_proposal_text)
        if choice == "yes":
            set_state(AppState.RESCUE_CONFIRMED)
            add_message("user", "✅ Đồng ý gọi cứu hộ.")
            st.rerun()
        elif choice == "no":
            set_state(AppState.RESCUE_CANCELLED)
            add_message("user", "❌ Không gọi cứu hộ.")
            st.rerun()

# ─── State: RESCUE_CONFIRMED ─────────────────────────
elif state == AppState.RESCUE_CONFIRMED:
    for msg in get_messages():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    render_rescue_confirmed()

# ─── State: RESCUE_CANCELLED ─────────────────────────
elif state == AppState.RESCUE_CANCELLED:
    for msg in get_messages():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    render_rescue_cancelled()
