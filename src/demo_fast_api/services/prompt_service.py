from pathlib import Path

class PromptService:
    def __init__(self):
        self.prompts_path = (
            Path(__file__).resolve().parent.parent/"prompts"
        )

    def get_chat_prompt(self, version: str) -> str:
        prompts_path =  (
            self.prompts_path
            / "chat"
            / f"{version}.txt"
        )

        if not prompts_path.exists:
            raise FileNotFoundError(f"Chat prompt not found : {version}")

        return prompts_path.read_text(encoding="utf-8")

