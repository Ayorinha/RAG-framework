"""Tests for the OpenAI generator."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ragframework.base import Chunk
from ragframework.exceptions import GeneratorError
from ragframework.generator.openai import OpenAIGenerator


def test_generate_returns_openai_response() -> None:
    generator = OpenAIGenerator(api_key="test-key")

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "The answer is 42."

    with patch.object(
        generator._client.chat.completions,
        "create",
        return_value=mock_response,
    ) as mock_create:
        result = generator.generate(
            "What is the answer?",
            [Chunk(id="1", content="The answer is 42.")],
        )

    assert result == "The answer is 42."
    mock_create.assert_called_once()


def test_generate_formats_context() -> None:
    generator = OpenAIGenerator(api_key="test-key")

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "RAG uses retrieved context."

    with patch.object(
        generator._client.chat.completions,
        "create",
        return_value=mock_response,
    ) as mock_create:
        generator.generate(
            "What is RAG?",
            [
                Chunk(id="1", content="RAG retrieves relevant information."),
                Chunk(id="2", content="RAG then generates an answer."),
            ],
        )

    call_kwargs = mock_create.call_args.kwargs
    user_message = call_kwargs["messages"][1]["content"]

    assert "[Chunk 1]" in user_message
    assert "RAG retrieves relevant information." in user_message
    assert "[Chunk 2]" in user_message
    assert "RAG then generates an answer." in user_message


def test_generate_uses_custom_configuration() -> None:
    generator = OpenAIGenerator(
        model="custom-model",
        api_key="test-key",
        system_prompt="Use only the supplied context.",
        max_tokens=100,
    )

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Answer."

    with patch.object(
        generator._client.chat.completions,
        "create",
        return_value=mock_response,
    ) as mock_create:
        generator.generate("Question?", [])

    call_kwargs = mock_create.call_args.kwargs

    assert call_kwargs["model"] == "custom-model"
    assert call_kwargs["max_tokens"] == 100
    assert call_kwargs["messages"][0]["content"] == "Use only the supplied context."


def test_generate_uses_api_key_from_environment() -> None:
    with (
        patch.dict("os.environ", {"OPENAI_API_KEY": "environment-key"}),
        patch("ragframework.generator.openai.OpenAI") as mock_openai,
    ):
        OpenAIGenerator()

    mock_openai.assert_called_once_with(api_key="environment-key")


def test_generate_raises_generator_error_on_api_failure() -> None:
    generator = OpenAIGenerator(api_key="test-key")

    with patch.object(
        generator._client.chat.completions,
        "create",
        side_effect=RuntimeError("API unavailable"),
    ), pytest.raises(GeneratorError, match="OpenAI generation failed"):
        generator.generate("Question?", [])


def test_generate_raises_generator_error_for_empty_response() -> None:
    generator = OpenAIGenerator(api_key="test-key")

    mock_response = MagicMock()
    mock_response.choices[0].message.content = ""

    with patch.object(
        generator._client.chat.completions,
        "create",
        return_value=mock_response,
    ), pytest.raises(GeneratorError, match="empty response"):
        generator.generate("Question?", [])
