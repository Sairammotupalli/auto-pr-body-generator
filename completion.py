from prompt import Prompt
from uuid import uuid4
import logging
from enum import Enum
from cachetools import TTLCache
import time

# Set up cache and OpenAI rate limit checker
cache = TTLCache(maxsize=100, ttl=3600)  # Cache size and TTL as required

class Completion:
    class State(Enum):
        UNCOMPLETE = "UNCOMPLETE"
        COMPLETED = "COMPLETED"

    def __init__(self, prompt: Prompt, openai_client):
        self._id = f"hash(prompt)-{uuid4()}"
        self._openai_client = openai_client
        self._prompt = prompt
        self._state = self.State.UNCOMPLETE
        self._result = ""

    def check_rate_limit(self):
        response = self._openai_client.Usage.retrieve()
        return response["data"]["usage"]["rate_limit"]

    def _complete_prompt(self) -> str:
        if self._prompt.text in cache:
            return cache[self._prompt.text]

        while True:
            if self.check_rate_limit() > 0:
                try:
                    response = self._openai_client.Completion.create(
                        model="gpt-3.5-turbo", prompt=self._prompt.text, max_tokens=1024
                    )
                    result_text = response.choices[0].text
                    cache[self._prompt.text] = result_text  # Cache the result
                    return result_text
                except openai.error.RateLimitError:
                    print("Rate limit exceeded. Retrying...")
                    time.sleep(10)
            else:
                print("Waiting for rate limit reset...")
                time.sleep(60)

    def complete(self):
        logging.info(f"completion_{self.id} - Completing prompt...")
        logging.info(f"completion_{self.id} - prompt to complete: {self._prompt}")
        self._result = self._complete_prompt()
        self._state = self.State.COMPLETED
        logging.info(f"completion_{self.id} - Complete")
        logging.info(f"completion_{self.id} - Result: {self.result}")

    @property
    def id(self):
        return self._id

    @property
    def result(self):
        return self._result

    @property
    def state(self):
        return self._state
