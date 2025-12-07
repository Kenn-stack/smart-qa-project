# tests/test_client.py
import json
import pytest
from google.genai import errors
from smart_qa.client import LLMClient
from smart_qa.custom_exceptions import JSONParseError, MaxRetriesExceeded


# -------------------------------------------------------------------
# MAKE REQUEST (INTERNAL) — RETRIES + SUCCESS
# -------------------------------------------------------------------
def test_make_request_success(mocker, llm_client):
    mock = mocker.patch(
        "google.genai.models.Models.generate_content",
        return_value=mocker.Mock(text="OK!")
    )

    result = llm_client._make_request(model="x", contents="y")
    assert result == "OK!"
    assert mock.call_count == 1


def test_make_request_retries_then_success(mocker, llm_client):
    # First two calls raise 429, last one succeeds
    error = errors.APIError(429, {"message":"Rate limit"})

    mock = mocker.patch(
        "google.genai.models.Models.generate_content",
        side_effect=[error, error, mocker.Mock(text="finally")]
    )

    result = llm_client._make_request(model="x", contents="y")
    assert result == "finally"
    assert mock.call_count == 3


def test_make_request_exceeds_max_retries(mocker, llm_client):
    error = errors.APIError(500, {"message":"Server error"})

    mocker.patch(
        "google.genai.models.Models.generate_content",
        side_effect=[error, error, error]
    )

    with pytest.raises(MaxRetriesExceeded):
        llm_client._make_request(model="x", contents="y")


# -------------------------------------------------------------------
# SUMMARIZE — CACHE + RETURN VALUE
# -------------------------------------------------------------------
def test_summarize_cached(mocker, llm_client):
    mock = mocker.patch(
        "google.genai.models.Models.generate_content",
        return_value=mocker.Mock(text="Summary!")
    )

    text = "Hello world"
    r1 = llm_client.summarize(text)
    r2 = llm_client.summarize(text)

    assert r1 == "Summary!"
    assert r2 == "Summary!"
    assert mock.call_count == 1  # cached!


# -------------------------------------------------------------------
# CREATE CHAT — CACHE
# -------------------------------------------------------------------
def test_create_chat_cached(mock_chat_create, llm_client):
    fake_chat = object()
    mock_chat_create.return_value = fake_chat

    text = "Sample"
    c1 = llm_client.create_chat(text)
    c2 = llm_client.create_chat(text)

    assert c1 is fake_chat
    assert c2 is fake_chat
    assert mock_chat_create.call_count == 1


# -------------------------------------------------------------------
# ASK — RETRIES
# -------------------------------------------------------------------
def test_ask_retry_success(mocker, llm_client):
    fake_chat = mocker.Mock()

    error = errors.APIError(429, {"message":"Rate limit"})
    fake_chat.send_message.side_effect = [
        error,
        mocker.Mock(text="Answer")
    ]

    result = llm_client.ask("Q", fake_chat)
    assert result == "Answer"
    assert fake_chat.send_message.call_count == 2


def test_ask_retry_failure(mocker, llm_client):
    fake_chat = mocker.Mock()

    error = errors.APIError(500, {"message":"Server error"})
    fake_chat.send_message.side_effect = [error, error, error]

    with pytest.raises(MaxRetriesExceeded):
        llm_client.ask("Q", fake_chat)


# -------------------------------------------------------------------
# EXTRACT ENTITIES — VALID JSON + CACHE
# -------------------------------------------------------------------
def test_extract_entities_valid_json(mocker, llm_client):
    mocker.patch(
        "google.genai.models.Models.generate_content",
        return_value=mocker.Mock(text='{"name": "Ekene"}')
    )

    result = llm_client.extract_entities("text")
    assert result == {"name": "Ekene"}


def test_extract_entities_cached(mocker, llm_client):
    mock = mocker.patch(
        "google.genai.models.Models.generate_content",
        return_value=mocker.Mock(text='{"age": 8}')
    )

    t = "My name is Ekene"
    r1 = llm_client.extract_entities(t)
    r2 = llm_client.extract_entities(t)

    assert r1 == {"age": 8}
    assert r2 == {"age": 8}
    assert mock.call_count == 1  # cached!


# -------------------------------------------------------------------
# EXTRACT ENTITIES — BAD JSON → RAISE JSONParseError
# -------------------------------------------------------------------
def test_extract_entities_bad_json(mocker, llm_client):
    mocker.patch(
        "google.genai.models.Models.generate_content",
        return_value=mocker.Mock(text="NOT JSON")
    )

    with pytest.raises(JSONParseError):
        llm_client.extract_entities("text")
