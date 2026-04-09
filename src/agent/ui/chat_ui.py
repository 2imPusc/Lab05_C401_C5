"""Chat UI logic — quản lý session state và state machine."""

import streamlit as st
from enum import Enum


class AppState(str, Enum):
    SELECT_ISSUE = "select_issue"
    CLASSIFYING = "classifying"
    LOW_CONFIDENCE = "low_confidence"
    SELF_SERVICE_CHAT = "self_service_chat"
    RESCUE_COLLECT_INFO = "rescue_collect_info"
    RESCUE_CONFIRM_INFO = "rescue_confirm_info"
    RESCUE_PROPOSAL = "rescue_proposal"
    RESCUE_CONFIRMED = "rescue_confirmed"
    RESCUE_CANCELLED = "rescue_cancelled"


def init_session_state():
    """Khởi tạo session state nếu chưa có."""
    defaults = {
        "app_state": AppState.SELECT_ISSUE,
        "selected_issue": None,
        "issue_description": "",
        "classification": None,
        "chat_history": [],
        "messages": [],
        "agent_executor": None,
        "rescue_info": None,
        "rescue_service": None,
        "rescue_proposal_text": None,
        "correction_count": 0,
        "csat_rating": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session():
    """Reset toàn bộ state."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()


def set_state(new_state: AppState):
    """Chuyển state."""
    st.session_state.app_state = new_state


def add_message(role: str, content: str):
    """Thêm message vào chat history."""
    st.session_state.messages.append({"role": role, "content": content})


def get_messages() -> list:
    """Lấy toàn bộ messages."""
    return st.session_state.messages
