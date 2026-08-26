import json
import urllib.request
import urllib.error

from ai.provider import AIProvider
from config import AI_MODEL


class LocalProvider(AIProvider):
    def __init__(
        self,
        model_name=AI_MODEL,
        base_url="http://localhost:11434"
    ):
        self.model_name = model_name
        self.base_url = base_url

    def generate_response(self, messages):
        data = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
        }

        request_data = json.dumps(data).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=request_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(request) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            return result["message"]["content"]

        except urllib.error.URLError:
            return (
                "I couldn't reach the local AI server. "
                "Make sure Ollama is running."
            )

        except KeyError:
            return (
                "The local AI server responded, but I couldn't "
                "understand its response."
            )