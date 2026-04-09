"""ReAct Agent cho nhánh 'tự xử được' — chat troubleshoot với tools."""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE, REACT_AGENT_PROMPT
from tools.db_lookup import search_troubleshoot, find_nearest_stations
from tools.gps_tool import get_current_location


def create_react_agent_executor():
    """Tạo ReAct agent với tools tra cứu DB + GPS."""

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    tools = [search_troubleshoot, find_nearest_stations, get_current_location]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=REACT_AGENT_PROMPT,
    )

    return agent


def run_react_agent(agent, user_input: str, chat_history: list) -> str:
    """Chạy agent với input và history, trả về response text."""
    messages = list(chat_history) + [HumanMessage(content=user_input)]

    result = agent.invoke({"messages": messages})

    # Lấy message cuối cùng từ AI
    ai_messages = [
        m for m in result["messages"]
        if isinstance(m, AIMessage) and m.content
    ]

    if ai_messages:
        return ai_messages[-1].content
    return "Xin lỗi, tôi không thể xử lý yêu cầu này. Vui lòng gọi hotline 1900-23-23-89."
