import json
import logging
import os
import time
from functools import lru_cache
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
# from google.genai.resources.chats import ChatSession

from .custom_exceptions import JSONParseError, MaxRetriesExceeded

load_dotenv()

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for making calls to llm model"""
    def __init__(self) -> None:
        """Load API key and configure genai"""
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def _make_request(self, **kwargs):
        """Makes an API request with automatic retries for rate limits."""
        MAX_RETRIES = 3
        backoff_factor = 2

        logger.info("Commencing API call to Gemini")
        for attempt in range(MAX_RETRIES):
            logger.info(f"Attempt {attempt} initialized...")
            try:
                response = self.client.models.generate_content(**kwargs)
                response = response.text
                return response
            except errors.APIError as err:
                logger.warning(
                    {
                        "status": f"{err.status_code}",
                        "message": f"{err.message}. Retrying...",
                    }
                )
                if 500 <= err.status_code < 600 or err.status_code in (429, 403):
                    sleep_time = backoff_factor * (2**attempt)
                    logger.warning(
                        f"{err.message}. {err.status_code}. Retrying in {sleep_time:.1f}s ..."
                    )
                    time.sleep(sleep_time)
                    continue

            except ConnectionError:
                sleep_time = backoff_factor * (2**attempt)
                logger.warning(f"There is a problem with your internet connection. Retrying in {sleep_time:.1f}s ...")
                time.sleep(sleep_time)
                continue

            # except errors.GenAIException as err:
            #     logger.error(f"{err.message}. {err.status_code}")

        raise MaxRetriesExceeded(
            "There was an error in making the request. Check logs for details"
        )

    @lru_cache
    def create_chat(self, text):
        """Creates a Chat instance for the user to interact with. Tobe used with the 'ask' flow."""
        chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=f"""
                                        Answer questions only with information explicitly found in the provided text.
                                        If the answer is not directly stated in the text, reply only: ‘I don’t know.’
                                        Do not guess or infer beyond the text.

                                        TEXT:
                                            {text}
                                        """
            ),
        )

        return chat

    def ask(self, question: str, chat):
        """makes request to the llm using a Chat instance"""
        MAX_RETRIES = 3
        backoff_factor = 2

        logger.info("Commencing API call to Gemini")
        for attempt in range(MAX_RETRIES):
            logger.info(f"Attempt {attempt} initialized...")
            try:
                response = chat.send_message(question)
                response = response.text
                return response
            except errors.GenAIAPIError as err:
                logger.warning(
                    {
                        "status": f"{err.status_code}",
                        "message": f"{err.message}. Retrying...",
                    }
                )
                if 500 <= err.status_code < 600 or err.status_code in (429, 403):
                    sleep_time = backoff_factor * (2**attempt)
                    logger.warning(
                        f"{err.message}. {err.status_code}. Retrying in {sleep_time:.1f}s ..."
                    )
                    time.sleep(sleep_time)
                    continue

            except errors.GenAIException as err:
                sleep_time = backoff_factor * (2**attempt)
                logger.warning(f"{err.message}. Retrying in {sleep_time:.1f}s ...")
                time.sleep(sleep_time)
                continue

        raise MaxRetriesExceeded(
            "There was an error in making the request. Check logs for details"
        )

    @lru_cache
    def summarize(self, text: str) -> str:
        print("summarizing...")
        response = self._make_request(
            model="gemini-2.5-flash",
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction="""
                                        You will be given a text. Your task is to produce a concise summary that captures the most important ideas, events, and arguments from the text.
                                        Focus only on what is explicitly stated — no assumptions or external information.

                                        Your summary must:
                                        -Be clear and concise
                                        -Preserve all major points
                                        -Highlight key ideas, facts, or arguments
                                        -Avoid minor details, examples, or filler content
                                        -Use bullet points if they improve clarity (optional)
                                        -Do not add opinions or interpretations that are not in the text.
                                        """
            ),
        )
        # response = response.text
        return response

    @lru_cache
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extracts entities and returns a dictionary."""
        response = self._make_request(
            model="gemini-2.5-flash",
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction="""
                                        You will be given a text. Extract only explicit facts stated word-for-word in the text.
                                        Do not infer, guess, interpret, or fill in missing details.
                                        If a piece of information is not directly stated, do not include it.

                                        Return the extracted facts as a JSON dictionary using only key–value pairs that come directly from the text.

                                        Values must be taken exactly from the text (no rephrasing).

                                        If nothing factual is found, return {}.

                                        Do not include code fences, backticks, comments, or explanations.
                                        Return a JSON object only.
                                        """
            ),
        )
        print(response)
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            raise JSONParseError("There was an error in parsing the json response")
        return response
