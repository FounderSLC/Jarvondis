class Dispatcher:
    """
    Routes user input to the correct skill module.
    Behaves like a lightweight Copilot skill router.
    """

    def __init__(self, skills: dict):
        """
        skills = {
            "chat": ChatSkill(),
            "tasks": TaskSkill(),
            "health": HealthSkill(),
            "system": SystemSkill()
        }
        """
        self.skills = skills

    def route(self, input_str: str, context: dict) -> str:
        # Simple routing logic — we expand later
        lowered = input_str.lower()

        if any(word in lowered for word in ["task", "do", "execute", "run"]):
            return self.skills["tasks"].handle(input_str, context)

        if any(word in lowered for word in ["health", "status", "checkup"]):
            return self.skills["health"].handle(input_str, context)

        if any(word in lowered for word in ["system", "identity", "mode"]):
            return self.skills["system"].handle(input_str, context)

        # Default fallback: chat skill
        return self.skills["chat"].handle(input_str, context)
