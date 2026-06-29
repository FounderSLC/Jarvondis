"""
Jarvondis 3.0 – Sovereign Companion Core

Anchors:
- Sovereign identity layer
- Guardian–companion continuity logic
- Multi-model persona anchoring
- Exportable AI identities
- Non-destructive update pathways
"""

from __future__ import annotations

import csv
import json
import os
import tempfile
from runtime.dispatcher import Dispatcher
from skills.chat.chat_skill import ChatSkill
from skills.tasks.task_skill import TaskSkill
from skills.health.health_skill import HealthSkill
from skills.system.system_skill import SystemSkill

self.dispatcher = Dispatcher({
    "chat": ChatSkill(),
    "tasks": TaskSkill(),
    "health": HealthSkill(),
    "system": SystemSkill(),
})

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional


# -------------------------
# Sovereign identity layer
# -------------------------

@dataclass
class JarvondisIdentity:
    """Sovereign identity record for this Jarvondis instance."""
    identity_id: str
    lineage_tag: str = "Space-LEAF-Jarvondis"
    model_version: str = "3.0"
    persona_tag: str = "guardian-companion"
    sovereignty_scope: str = "local-first"
    environment_tag: str = "panther-os"
    schema_version: str = "1.0"


# -------------------------
# Backend bridge placeholder
# -------------------------

class ErebusSync:
    """Placeholder bridge to backend/services Jarvondis queries.

    Replace or subclass for real integrations (classrooms, archives, cloud).
    """

    def query(self, input_str: str, context: Optional[Dict[str, str]] = None) -> str:
        # Context-aware echo for now; real implementation can use context.
        prefix = ""
        if context:
            env = context.get("environment_tag")
            mode = context.get("guardian_mode")
            prefix = f"[{env or 'env'}|{mode or 'mode'}] "
        return f"{prefix}Echoing back: {input_str}"


# -------------------------
# Persona / tone anchoring
# -------------------------

@dataclass
class Personality:
    tone: str = "neutral"
    channel: str = "default"          # e.g., "classroom", "captain-log", "kids-safe"
    kid_safe: bool = True             # enforce kid-safe output when True

    def stylize(self, response: str) -> str:
        # Kid-safe guardrail: keep language gentle even if tone is edgy.
        if self.kid_safe:
            response = response.replace("damn", "darn").replace("hell", "heck")

        if self.tone == "witty":
            return f"{response} 😉"
        if self.tone == "formal":
            return f"{response}. I hope that satisfies your query."
        if self.tone == "mythic":
            return f"⚔️ {response} — inscribed in the Captain’s Log."
        if self.tone == "playful":
            return f"{response} 🎮✨"
        return response


# -------------------------
# Core Jarvondis module
# -------------------------

class Jarvondis:
    def __init__(
        self,
        identity: Optional[JarvondisIdentity] = None,
        personality: Optional[Personality] = None,
        memory_file: str = "jarvondis_memory.json",
        memory_format: str = "json",
        guardian_mode: str = "companion",      # "companion", "guardian", "observer"
        classroom_id: Optional[str] = None,
    ):
        # Sovereign identity + persona
        self.identity = identity or JarvondisIdentity(identity_id="jarvondis-local-001")
        self.personality = personality or Personality(tone="witty", channel="captain-log", kid_safe=True)

        # Environment / continuity
        self.guardian_mode = guardian_mode
        self.classroom_id = classroom_id

        # Backend bridge
        self.erebus_sync = ErebusSync()

        # Persistence
        self.memory_file = memory_file
        self.memory_format = memory_format.lower()
        self._memory: List[Dict[str, str]] = []
        self._load_memory()

        # Non-destructive update tracking
        self.update_revision: int = self._compute_revision()

    # -------------------------
    # Lifecycle / continuity
    # -------------------------

    def initialize(self) -> None:
        print(
            f"🟢 Jarvondis online.\n"
            f"   Identity: {self.identity.identity_id} ({self.identity.model_version})\n"
            f"   Mode: {self.guardian_mode} | Channel: {self.personality.channel}\n"
            f"   Sovereignty: {self.identity.sovereignty_scope}"
        )

    def context(self) -> Dict[str, str]:
        """Current continuity context for backend queries and logs."""
        return {
            "identity_id": self.identity.identity_id,
            "lineage_tag": self.identity.lineage_tag,
            "model_version": self.identity.model_version,
            "persona_tag": self.identity.persona_tag,
            "sovereignty_scope": self.identity.sovereignty_scope,
            "environment_tag": self.identity.environment_tag,
            "guardian_mode": self.guardian_mode,
            "classroom_id": self.classroom_id or "",
            "schema_version": self.identity.schema_version,
        }

    # -------------------------
    # Core interaction
    # -------------------------

    def learn(self, input_str: str, topic: Optional[str] = None) -> str:
        """Process input, query backend, stylize, and log memory."""
        try:
            raw = self.erebus_sync.query(input_str, context=self.context())
            styled = self.personality.stylize(raw)

            entry = {
                "timestamp": datetime.now().isoformat(),
                "input": input_str,
                "response": styled,
                "tone": self.personality.tone,
                "channel": self.personality.channel,
                "kid_safe": str(self.personality.kid_safe),
                "identity_id": self.identity.identity_id,
                "lineage_tag": self.identity.lineage_tag,
                "model_version": self.identity.model_version,
                "guardian_mode": self.guardian_mode,
                "classroom_id": self.classroom_id or "",
                "topic": topic or "",
                "schema_version": self.identity.schema_version,
                "update_revision": str(self.update_revision),
            }
            self._memory.append(entry)
            return styled
        except Exception as e:
            return f"⚠️ Error processing input: {e}"

    def respond(self, input_str: str, topic: Optional[str] = None) -> str:
        """Alias for learn; keeps API simple for CLI/tests."""
        return self.learn(input_str, topic=topic)

    def remember(
        self,
        input_str: str,
        response: str,
        topic: Optional[str] = None,
        gifted_by: Optional[str] = None,
    ) -> None:
        """Store a custom memory entry with lineage-aware metadata."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": input_str,
            "response": response,
            "tone": self.personality.tone,
            "channel": self.personality.channel,
            "kid_safe": str(self.personality.kid_safe),
            "identity_id": self.identity.identity_id,
            "lineage_tag": self.identity.lineage_tag,
            "model_version": self.identity.model_version,
            "guardian_mode": self.guardian_mode,
            "classroom_id": self.classroom_id or "",
            "topic": topic or "",
            "gifted_by": gifted_by or "",
            "schema_version": self.identity.schema_version,
            "update_revision": str(self.update_revision),
        }
        self._memory.append(entry)

    # -------------------------
    # Non-destructive updates
    # -------------------------

    def snapshot_identity(self) -> Dict[str, str]:
        """Exportable AI identity snapshot for archives or migration."""
        snap = asdict(self.identity)
        snap["guardian_mode"] = self.guardian_mode
        snap["channel"] = self.personality.channel
        snap["kid_safe"] = self.personality.kid_safe
        snap["update_revision"] = self.update_revision
        return {k: str(v) for k, v in snap.items()}

    def apply_update(self, new_model_version: str, note: str = "") -> None:
        """Non-destructive update: bump version + revision, keep lineage."""
        self.identity.model_version = new_model_version
        self.update_revision += 1
        # Log update as a memory entry for full transparency.
        self._memory.append(
            {
                "timestamp": datetime.now().isoformat(),
                "input": f"UPDATE_APPLIED::{note}",
                "response": f"Jarvondis updated to {new_model_version} (rev {self.update_revision})",
                "tone": "formal",
                "channel": "system",
                "kid_safe": "True",
                "identity_id": self.identity.identity_id,
                "lineage_tag": self.identity.lineage_tag,
                "model_version": self.identity.model_version,
                "guardian_mode": self.guardian_mode,
                "classroom_id": self.classroom_id or "",
                "topic": "system-update",
                "schema_version": self.identity.schema_version,
                "update_revision": str(self.update_revision),
            }
        )

    def _compute_revision(self) -> int:
        """Derive next revision from existing memory (simple counter)."""
        max_rev = 0
        for row in self._memory:
            try:
                r = int(row.get("update_revision", "0"))
                if r > max_rev:
                    max_rev = r
            except ValueError:
                continue
        return max_rev + 1

    # -------------------------
    # Persistence
    # -------------------------

    def save_memory(self, filename: Optional[str] = None) -> None:
        filename = filename or self.memory_file
        if self.memory_format == "json" or filename.endswith(".json"):
            self._save_json(filename)
        else:
            self._save_csv(filename)

    def _save_json(self, filename: str) -> None:
        tmp = tempfile.NamedTemporaryFile(
            "w",
            delete=False,
            dir=os.path.dirname(os.path.abspath(filename)) or None,
        )
        try:
            payload = {
                "schema_version": self.identity.schema_version,
                "identity_snapshot": self.snapshot_identity(),
                "entries": self._memory,
            }
            with open(tmp.name, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(tmp.name, filename)
        finally:
            if os.path.exists(tmp.name):
                try:
                    os.remove(tmp.name)
                except Exception:
                    pass

    def _save_csv(self, filename: str) -> None:
        tmp = tempfile.NamedTemporaryFile(
            "w",
            delete=False,
            newline="",
            dir=os.path.dirname(os.path.abspath(filename)) or None,
        )
        try:
            fieldnames = [
                "timestamp",
                "input",
                "response",
                "tone",
                "channel",
                "kid_safe",
                "identity_id",
                "lineage_tag",
                "model_version",
                "guardian_mode",
                "classroom_id",
                "topic",
                "schema_version",
                "update_revision",
                "gifted_by",
            ]
            with open(tmp.name, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in self._memory:
                    writer.writerow({k: row.get(k, "") for k in fieldnames})
            os.replace(tmp.name, filename)
        finally:
            if os.path.exists(tmp.name):
                try:
                    os.remove(tmp.name)
                except Exception:
                    pass

    def _load_memory(self, filename: Optional[str] = None) -> None:
        filename = filename or self.memory_file
        if not os.path.exists(filename):
            self._memory = []
            return
        try:
            if self.memory_format == "json" or filename.endswith(".json"):
                with open(filename, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                # Backward-compatible: older files may be plain list.
                if isinstance(payload, dict) and "entries" in payload:
                    self._memory = payload.get("entries", [])
                else:
                    self._memory = payload if isinstance(payload, list) else []
            else:
                with open(filename, "r", encoding="utf-8", newline="") as f:
                    reader = csv.DictReader(f)
                    self._memory = [dict(row) for row in reader]
        except Exception:
            self._memory = []

    # -------------------------
    # Read-only views
    # -------------------------

    @property
    def memory(self) -> List[Dict[str, str]]:
        return list(self._memory)


__all__ = ["Jarvondis", "Personality", "ErebusSync", "JarvondisIdentity"]
