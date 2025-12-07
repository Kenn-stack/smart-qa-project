# tests/conftest.py
import pytest
from smart_qa.client import LLMClient


@pytest.fixture
def mock_generate_content(mocker):
    """Mock for client.models.generate_content"""
    return mocker.patch("google.genai.models.ModelsService.generate_content")


@pytest.fixture
def mock_chat_send(mocker):
    """Mock chat.send_message"""
    return mocker.patch("google.genai.resources.chats.ChatSession.send_message")


@pytest.fixture
def mock_chat_create(mocker):
    """Mock client.chats.create"""
    return mocker.patch("google.genai.chats.ChatsService.create")


@pytest.fixture
def llm_client():
    """Real instance so we can test caching."""
    return LLMClient()
