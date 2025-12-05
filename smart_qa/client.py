import os
import json
import logging
import functools
from google import genai
from typing import Dict, Any
from .custom_exceptions import LLMAPIError
from dotenv import load_dotenv


load_dotenv()


class LLMClient:
    def __init__(self) -> None:
        """Load API key and configure genai"""
        self.client = genai.Client()

#           -  _  =  +
    # def _make_request(self, *args):
        
    
    
    def ask(self, text:str, question:str):
        prompt = """
        
        """
        
        
        
        
    # TODO: Add caching decorator here?
    def summarize(self, text: str) -> str:
        # ...
        pass

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extracts entities and returns a dictionary."""
        # TODO: Prompt for JSON output and parse it safely
        pass