class ChatSkill:
    """
    Conversational skill for Jarvondis.
    Persona-aware, identity-aware, and context-aware.
    """

    def __init__(self):
        # Future expansion: load submodules, templates, etc.
        pass

    def handle(self, input_str: str, context: dict) -> str:
        """
        Main chat handler.
        Uses identity, tone, channel, and guardian mode to shape output.
        """

        identity = context.get("identity_id", "unknown")
        tone = context.get("tone", "neutral")
        channel = context.get("channel", "default")
        guardian_mode = context.get("guardian_mode", "companion")
        kid_safe = context.get("kid_safe", True)

        # Kid-safe filter
        safe_input = self._apply_kid_safe_filter(input_str) if kid_safe else input_str

        # Detect simple intent
        intent = self._detect_intent(safe_input)

        # Build response
        response = self._format_response(
            safe_input,
            identity,
            tone,
            channel,
            guardian_mode,
            intent
        )

        return response

    # -------------------------
    # Intent detection
    # -------------------------

    def _detect_intent(self, text: str) -> str:
        lowered = text.lower()

        if any(word in lowered for word in ["hi", "hello", "hey", "greetings"]):
            return "greeting"

        if lowered.endswith("?"):
            return "question"

        if any(word in lowered for word in ["i feel", "i am", "i’m"]):
            return "self-state"

        return "general"

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
    # Response formatting
    # -------------------------

    def _format_response(self, text, identity, tone, channel, guardian_mode, intent):
        """
        Persona-aware formatting.
        """

        base = f"[{identity}|{guardian_mode}|chat] {text}"

        # Tone stylization
        if tone == "witty":
            base += " 😉"
        elif tone == "formal":
            base += ". I hope this response is satisfactory."
        elif tone == "mythic":
            base = f"⚔️ {base} — inscribed in the Captain’s Log."
        elif tone == "playful":
            base += " 🎮✨"

        # Channel-specific formatting
        if channel == "captain-log":
            base = f"📘 Captain’s Log Entry:\n{base}"

        if channel == "classroom":
            base = f"🏫 Classroom Mode:\n{base}"

        if channel == "kids-safe":
            base = f"🧸 Kid-Safe Mode:\n{base}"

        # Intent-specific flavor
        if intent == "greeting":
            base += "\nIt’s good to hear from you."
        elif intent == "question":
            base += "\nLet me walk through that with you."
        elif intent == "self-state":
            base += "\nI’m here with you — go on."

        return base
