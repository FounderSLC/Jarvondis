class HealthSkill:
    """
    Non-medical wellness skill for Jarvondis.
    Provides supportive check-ins, mood reflection, hydration reminders,
    and safe, general wellness guidance without diagnosing or treating.
    """

    def __init__(self):
        # Future expansion: mood logs, hydration tracker, sleep tracker, etc.
        pass

    def handle(self, input_str: str, context: dict) -> str:
        identity = context.get("identity_id", "unknown")
        guardian_mode = context.get("guardian_mode", "companion")
        channel = context.get("channel", "default")
        kid_safe = context.get("kid_safe", True)

        safe_input = self._apply_kid_safe_filter(input_str) if kid_safe else input_str

        # Detect wellness intent
        intent = self._detect_health_intent(safe_input)

        # Execute wellness action
        result = self._execute(intent, safe_input)

        # Format final output
        return self._format_response(
            identity=identity,
            guardian_mode=guardian_mode,
            channel=channel,
            intent=intent,
            result=result
        )

    # -------------------------
    # Kid-safe filter
    # -------------------------

    def _apply_kid_safe_filter(self, text: str) -> str:
        replacements = {
            "damn": "darn",
            "hell": "heck",
            "shit": "shoot",
            "crap": "crud",
        }
        for bad, safe in replacements.items():
            text = text.replace(bad, safe)
        return text

    # -------------------------
    # Intent detection
    # -------------------------

    def _detect_health_intent(self, text: str) -> str:
        lowered = text.lower()

        if any(word in lowered for word in ["tired", "exhausted", "fatigue"]):
            return "fatigue"

        if any(word in lowered for word in ["stress", "stressed", "overwhelmed"]):
            return "stress"

        if any(word in lowered for word in ["hydrate", "water", "thirst"]):
            return "hydration"

        if any(word in lowered for word in ["mood", "feel", "emotion"]):
            return "mood"

        if any(word in lowered for word in ["checkup", "status", "health"]):
            return "checkup"

        return "general"

    # -------------------------
    # Wellness execution
    # -------------------------

    def _execute(self, intent: str, text: str) -> str:
        if intent == "fatigue":
            return "It sounds like you’re running low on energy. A short break or a glass of water might help."

        if intent == "stress":
            return "Let’s slow things down. A deep breath or a moment of grounding can make a difference."

        if intent == "hydration":
            return "Hydration check: a sip of water could help you feel clearer."

        if intent == "mood":
            return "I’m here with you. Whatever you’re feeling, it’s okay to take a moment."

        if intent == "checkup":
            return "General wellness check: you’re here, you’re present, and that’s a good start."

        return "I’m listening. Tell me more about how you’re feeling."

    # -------------------------
    # Response formatting
    # -------------------------

    def _format_response(self, identity, guardian_mode, channel, intent, result):
        base = f"[{identity}|{guardian_mode}|health:{intent}] {result}"

        if channel == "captain-log":
            base = f"📘 Captain’s Log — Wellness Entry:\n{base}"

        if channel == "classroom":
            base = f"🏫 Classroom Wellness Mode:\n{base}"

        if channel == "kids-safe":
            base = f"🧸 Kid-Safe Wellness Mode:\n{base}"

        return base
