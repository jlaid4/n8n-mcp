"""
player.py - Character system for Nova City RPG
Handles player stats, leveling, skills, and inventory.
"""

import random

# XP required to reach each level (index = level)
LEVEL_XP_THRESHOLDS = [0, 100, 250, 450, 700, 1000]


class Skill:
    """A single player skill with a numeric level and derived bonus."""

    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level

    def __repr__(self):
        return f"{self.name} Lv.{self.level}"

    def get_bonus(self) -> int:
        """Flat bonus added to d20 skill checks."""
        return (self.level - 1) * 5

    def improve(self) -> bool:
        """Raises skill by 1. Returns True if successful."""
        if self.level < 10:
            self.level += 1
            return True
        return False


class Player:
    """
    The player character.
    Tracks vitals, skills, inventory, story flags, and case notes.
    """

    def __init__(self, name: str):
        self.name = name
        self.level = 1
        self.xp = 0

        self.max_hp = 100
        self.hp = self.max_hp

        self.skills = {
            "combat":        Skill("Combat"),
            "stealth":       Skill("Stealth"),
            "investigation": Skill("Investigation"),
        }

        self.inventory: list[str] = []
        self.flags: dict = {}     # Boolean story-state flags
        self.notes: list[str] = []  # Case notes gathered during play

    # ── Vitals ─────────────────────────────────────────

    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

    # ── Progression ────────────────────────────────────

    def gain_xp(self, amount: int) -> list[str]:
        """Awards XP, triggers level-ups. Returns list of status messages."""
        messages = [f"+{amount} XP"]
        self.xp += amount

        while (self.level < len(LEVEL_XP_THRESHOLDS) - 1
               and self.xp >= LEVEL_XP_THRESHOLDS[self.level]):
            self._level_up()
            messages.append(f"LEVEL UP! Now Level {self.level}!")

        return messages

    def _level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = min(self.max_hp, self.hp + 20)

    # ── Skill Checks ───────────────────────────────────

    def skill_check(self, skill_name: str, difficulty: int) -> tuple[bool, int, int]:
        """
        d20 + skill bonus vs difficulty.
        Returns (success, total_roll, difficulty).
        """
        skill = self.skills.get(skill_name.lower())
        if not skill:
            return False, 0, difficulty

        roll = random.randint(1, 20) + skill.get_bonus()
        return roll >= difficulty, roll, difficulty

    # ── Inventory ──────────────────────────────────────

    def add_item(self, item: str):
        self.inventory.append(item)

    def has_item(self, item: str) -> bool:
        return item in self.inventory

    def remove_item(self, item: str) -> bool:
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    # ── Story Flags ────────────────────────────────────

    def set_flag(self, flag: str, value=True):
        self.flags[flag] = value

    def get_flag(self, flag: str, default=False):
        return self.flags.get(flag, default)

    # ── Display ────────────────────────────────────────

    def show_status(self):
        """Prints a compact status card."""
        filled = int((self.hp / self.max_hp) * 20)
        hp_bar = "█" * filled + "░" * (20 - filled)

        print("\n" + "─" * 48)
        print(f"  {self.name}  │  Level {self.level}  │  XP: {self.xp}")
        print(f"  HP: [{hp_bar}] {self.hp}/{self.max_hp}")
        print(f"  Skills: {' | '.join(str(s) for s in self.skills.values())}")
        if self.inventory:
            print(f"  Inventory: {', '.join(self.inventory)}")
        print("─" * 48)

    def show_notes(self):
        """Prints collected case notes."""
        if not self.notes:
            print("  [No notes yet]")
        else:
            for i, note in enumerate(self.notes, 1):
                print(f"  {i}. {note}")
