class SystemSkill:
    """
    System-level skill for Jarvondis.
    Handles identity introspection, mode/status queries, and simple mode changes.
    """

    def __init__(self):
        # Future: hook into config files, OS, remote control surfaces, etc.
        pass

    def handle(self, input_str: str, context: dict) -> str:
        identity_id = context.get("identity_id", "unknown")
        lineage_tag = context.get("lineage_tag", "")
        model_version = context.get("model_version", "")
        guardian_mode = context.get("guardian_mode", "companion")
        channel = context.get("channel", "default")
        environment_tag = context.get("environment_tag", "")
        schema_version = context.get("schema_version", "")

        lowered = input_str.lower()

        if "identity" in lowered or "who are you" in lowered:
            result = self._describe_identity(
                identity_id,
                lineage_tag,
                model_version,
                environment_tag,
                schema_version,
            )
        elif "mode" in lowered or "status" in lowered:
            result = self._describe_mode(guardian_mode, channel)
        elif "schema" in lowered:
            result = self._describe_schema(schema_version)
        else:
            result = "System skill: I can describe identity, mode, and schema. Try asking about identity or mode."

        return self._format_response(
            identity_id=identity_id,
            guardian_mode=guardian_mode,
            channel=channel,
            result=result,
        )

    # -------------------------
    # Descriptions
    # -------------------------

    def _describe_identity(
        self,
        identity_id: str,
        lineage_tag: str,
        model_version: str,
        environment_tag: str,
        schema_version: str,
    ) -> str:
        return (
            f"Identity: {identity_id}\n"
            f"Lineage: {lineage_tag}\n"
            f"Model version: {model_version}\n"
            f"Environment: {environment_tag}\n"
            f"Schema version: {schema_version}"
        )

    def _describe_mode(self, guardian_mode: str, channel: str) -> str:
        return (
            f"Guardian mode: {guardian_mode}\n"
            f"Channel: {channel}\n"
            f"Role: operating as a multi-skill companion."
        )

    def _describe_schema(self, schema_version: str) -> str:
        return f"Current memory/identity schema version: {schema_version}"

    # -------------------------
    # Formatting
    # -------------------------

    def _format_response(self, identity_id: str, guardian_mode: str, channel: str, result: str) -> str:
        base = f"[{identity_id}|{guardian_mode}|system] {result}"

        if channel == "captain-log":
            base = f"📘 Captain’s Log — System Entry:\n{base}"
        elif channel == "classroom":
            base = f"🏫 Classroom System Mode:\n{base}"
        elif channel == "kids-safe":
            base = f"🧸 Kid-Safe System Mode:\n{base}"

        return base
