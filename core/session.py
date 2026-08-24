class Session:
    def __init__(self):
        self.command_history = []
        self.current_mode = None

    def add_command(self, command):
        self.command_history.append(command)

    def set_mode(self, mode):
        self.current_mode = mode

    def get_history(self):
        if not self.command_history:
            return "No commands have been entered yet."

        return "\n".join(
            f"{index + 1}. {command}"
            for index, command in enumerate(self.command_history)
        )

    def get_current_mode(self):
        if self.current_mode is None:
            return "No active mode."

        return f"Current mode: {self.current_mode}"