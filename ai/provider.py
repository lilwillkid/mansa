class AIProvider:
    def generate_response(self, messages):
        raise NotImplementedError(
            "AI providers must implement generate_response()."
        )