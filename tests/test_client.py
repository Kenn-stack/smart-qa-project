import pytest
from google.genai.types import Error

from smart_qa.client import LLMClient


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def make_error(status=500, message="Error"):
    return Error(status=status, message=message)


# ------------------------------------------------------------
# generate_content tests
# ------------------------------------------------------------

def test_generate_content_success(mocker):
    """Client.models.generate_content returns text successfully."""
    mock_method = mocker.patch(
        "google.genai.models.ModelsService.generate_content"
    )
    mock_method.return_value = mocker.Mock(text="Hello world!")

    client = LLMClient()
    result = client.generate_content("Hello")

    assert result == "Hello world!"
    mock_method.assert_called_once()


def test_generate_content_error(mocker):
    """Errors from the API should propagate upward."""
    mock_method = mocker.patch(
        "google.genai.models.ModelsService.generate_content"
    )
    mock_method.side_effect = make_error(429, "Rate limit")

    client = LLMClient()

    with pytest.raises(Error):
        client.generate_content("Hello")


# ------------------------------------------------------------
# chat tests
# ------------------------------------------------------------

def test_chat_create_success(mocker):
    """Chat responses should return text field."""
    mock_chat = mocker.patch(
        "google.genai.chats.ChatsService.create"
    )

    mock_chat.return_value = mocker.Mock(text="Response message")

    client = LLMClient()
    result = client.chat("Hello", history=[])

    assert result == "Response message"
    mock_chat.assert_called_once()


def test_chat_create_error(mocker):
    mock_chat = mocker.patch(
        "google.genai.chats.ChatsService.create"
    )

    mock_chat.side_effect = make_error(400, "Bad request")

    client = LLMClient()

    with pytest.raises(Error):
        client.chat("Hello", history=[])


# ------------------------------------------------------------
# extract tests
# ------------------------------------------------------------

def test_extract_calls_generate_content(mocker):
    mock_gen = mocker.patch(
        "google.genai.models.ModelsService.generate_content"
    )

    mock_gen.return_value = mocker.Mock(text='{"name": "Ekene"}')

    client = LLMClient()
    result = client.extract("My name is Ekene.")

    assert result == {"name": "Ekene"}
    mock_gen.assert_called_once()


def test_extract_invalid_json_returns_none(mocker):
    mock_gen = mocker.patch(
        "google.genai.models.ModelsService.generate_content"
    )

    mock_gen.return_value = mocker.Mock(text="not json")

    client = LLMClient()
    result = client.extract("Something")

    assert result is None


# ------------------------------------------------------------
# summarize tests
# ------------------------------------------------------------

def test_summarize_calls_generate_content(mocker):
    mock_gen = mocker.patch(
        "google.genai.models.ModelsService.generate_content"
    )
    mock_gen.return_value = mocker.Mock(text="Summary text")

    client = LLMClient()
    result = client.summarize("Full long text")

    assert result == "Summary text"
    mock_gen.assert_called_once()


def test_summarize_error(mocker):
    mock_gen = mocker.patch(
        "google.genai.models.ModelsService.generate_content"
    )
    mock_gen.side_effect = make_error(503, "Unavailable")

    client = LLMClient()

    with pytest.raises(Error):
        client.summarize("Full text")


# ------------------------------------------------------------
# Prompt-based QA tests
# ------------------------------------------------------------

def test_answer_question_calls_generate_content(mocker):
    mock_gen = mocker.patch(
        "google.genai.models.ModelsService.generate_content"
    )
    mock_gen.return_value = mocker.Mock(text="The answer is 42.")

    client = LLMClient()
    result = client.answer_question("What is X?", context="X is 42.")

    assert "42" in result
    mock_gen.assert_called_once()


def test_answer_question_handles_missing_answer(mocker):
    mock_gen = mocker.patch(
        "google.genai.models.ModelsService.generate_content"
    )
    mock_gen.return_value = mocker.Mock(text="I don't know")

    client = LLMClient()
    result = client.answer_question("?", context="No answer")

    assert result.lower().strip() == "i don't know"
