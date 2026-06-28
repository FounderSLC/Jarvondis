class ChatSkill:
    """Default conversational skill."""

    def handle(self, input_str: str, context: dict) -> str:
        identity = context.get("identity_id", "unknown")
        tone = context.get("tone", "neutral")
        return f"[{identity}|chat|{tone}] {input_str}"
