from enum import Enum
import json
import sys
from time import sleep
from typing import Literal
from anthropic import Anthropic, RateLimitError
from dotenv import load_dotenv
from openai import OpenAI
from function_schema import get_function_schema
from tools import tools, get_route, choose_song_from_playlist, publish_tweet, send_message_to_contact, create_new_playlist
import os
import logging

logging.basicConfig(level=logging.WARN)

load_dotenv()

anthropic_client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

model = os.getenv("DEFAULT_MODEL")


class AIGateway:
    def __init__(self, provider: Literal['claude', 'openai'] = 'claude', system_prompt: list[dict] | str = ""):
        self.provider = provider
        self.messages = []
        self.selected_model = model
        self.system_prompt = system_prompt
        self.tools = self._generate_tools_schema(tools)
        if provider == 'claude':
            self.client = Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError("Unsupported AI provider")

    def get_client(self):
        if self.provider == "claude":
            if self.selected_model == "claude-3-5-sonnet-20240620":
                return self.client.beta.prompt_caching
        return self.client

    def complete(self, prompt="", system_prompt: str | list[str] = "", **kwargs):
        if self.provider == 'claude':
            try:
                response = self.get_client().messages.create(
                    model=self.selected_model,
                    messages=self.messages,
                    system=self.system_prompt,  # type: ignore
                    **kwargs
                )
                return response
            except RateLimitError as e:
                if self.selected_model == "claude-3-5-sonnet-20240620":
                    logging.error(e)
                    logging.warning(
                        "You have hit your rate limit, switching to Haiku....")
                    self.selected_model = "claude-3-haiku-20240307"
                logging.info("Please wait...")
                sleep(5)
                logging.info("Back online")
                response = self.get_client().messages.create(
                    model=self.selected_model,
                    messages=self.messages,
                    system=self.system_prompt,  # type: ignore
                    **kwargs
                )
                return response

        else:
            raise ValueError("Unsupported AI provider")

    def create_message_with_tools(self, **kwargs):
        if self.provider == 'claude':
            return self.complete(
                tools=self.tools,
                system_prompt=self.system_prompt,  # type: ignore
                max_tokens=500,
                temperature=0
            )
        else:
            raise ValueError("Unsupported AI provider")

    # Sometimes multiple tools are called in one content block. This function makes sure to process them all.
    def handle_tool_use(self, response):
        for content_item in response.content:
            if content_item.type == "tool_use":
                tool_use = content_item
                tool_input = tool_use.input
                tool_name = tool_use.name
                result = globals()[tool_name](**tool_input)  # type: ignore
                logging.info("==============TOOL RESULT===========")
                logging.info(json.dumps(result, indent=2))
                self.messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                            "content": str(result)
                    }]
                })
                anthropic_tool_response = self.create_message_with_tools(
                    messages=self.messages,
                    max_tokens=500,
                    temperature=0
                )
                print(anthropic_tool_response.content[0].text)
                self.messages.append({
                    "role": "assistant",
                    "content": anthropic_tool_response.content
                })
                if anthropic_tool_response.stop_reason == "tool_use":
                    self.handle_tool_use(anthropic_tool_response)

    # private method which creates the json schema to match the function definition.
    def _generate_tools_schema(self, tools):
        return [get_function_schema(tool, format=self.provider)
                for tool in tools]

# Usage:
# ai_gateway = AIGateway('openai')
# client = ai_gateway.get_client()
# completion = ai_gateway.complete("Hello, how are you?", system_prompt="You are a helpful assistant.")
# tool_response = ai_gateway.tool_call(
#     messages=[{"role": "user", "content": "What's the weather like?"}],
#     tools=[{"type": "function", "function": {"name": "get_weather", "description": "Get the weather", "parameters": {"type": "object", "properties": {}}}}]
# )
