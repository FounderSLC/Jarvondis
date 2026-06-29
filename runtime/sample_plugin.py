class PantherPlugin:
    """
    Example Panther-OS plugin.
    """

    def run(self, command: str, context: dict) -> str:
        identity = context.get("identity_id", "unknown")
        guardian_mode = context.get("guardian_mode", "companion")

        return (
            f"[{identity}|{guardian_mode}|plugin:sample] "
            f"Executed sample plugin command: '{command}'"
        )
