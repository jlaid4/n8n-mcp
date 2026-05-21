"""
combat.py - Turn-based tactical combat for Nova City RPG
Handles all fight encounters, including Port Sons gang members.
"""

import random
import time
from typing import Optional


# ── Enemy Class ────────────────────────────────────────

class Enemy:
    """A single combat opponent with its own stats and loot table."""

    def __init__(self, name: str, hp: int, attack: int, defense: int,
                 xp_reward: int, loot: Optional[list] = None, description: str = ""):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.xp_reward = xp_reward
        self.loot = loot or []
        self.description = description
        self.status_effects: list[str] = []  # e.g. "stunned", "weakened"

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        """Applies damage reduced by half of defense. Returns actual damage dealt."""
        actual = max(1, amount - self.defense // 2)
        self.hp = max(0, self.hp - actual)
        return actual

    def deal_damage(self) -> int:
        """Returns the damage this enemy deals this turn, with small variance."""
        return max(1, self.attack + random.randint(-3, 3))

    def apply_status(self, effect: str):
        if effect not in self.status_effects:
            self.status_effects.append(effect)

    def clear_status(self, effect: str):
        if effect in self.status_effects:
            self.status_effects.remove(effect)

    def hp_bar(self, width: int = 15) -> str:
        filled = int((self.hp / self.max_hp) * width)
        return "█" * filled + "░" * (width - filled)


# ── Predefined Enemies ─────────────────────────────────

def make_port_grunt() -> Enemy:
    return Enemy(
        name="Port Sons Grunt",
        hp=random.randint(35, 50),
        attack=random.randint(8, 12),
        defense=random.randint(2, 4),
        xp_reward=30,
        loot=["Burner Phone Fragment"],
        description="A young enforcer in a Port Sons jacket. Nervous eyes, fast hands.",
    )


def make_port_lieutenant() -> Enemy:
    return Enemy(
        name="Port Sons Lieutenant",
        hp=random.randint(60, 75),
        attack=random.randint(12, 16),
        defense=random.randint(4, 7),
        xp_reward=60,
        loot=["Encrypted Note", "Port Sons Insignia"],
        description="A hardened enforcer with a scar across his jaw. He has done this before.",
    )


def make_tariq() -> Enemy:
    """Tariq only turns hostile if the player forces the issue."""
    return Enemy(
        name="Tariq (Port Sons Enforcer)",
        hp=55,
        attack=13,
        defense=5,
        xp_reward=50,
        loot=["Warehouse Key", "Tariq's Confession"],
        description="A stocky man who looks like he regrets every decision that led here.",
    )


def make_final_guard() -> Enemy:
    return Enemy(
        name="Halabi's Personal Guard",
        hp=80,
        attack=15,
        defense=8,
        xp_reward=80,
        loot=["Access Card"],
        description="Ex-military. Professional. Dangerous.",
    )


# ── Combat Actions ─────────────────────────────────────

ATTACK        = "attack"
DEFEND        = "defend"
SKILL_STRIKE  = "skill_strike"
STEALTH_HIT   = "stealth_hit"
INTIMIDATE    = "intimidate"
FLEE          = "flee"


def _print_combat_status(player, enemy: Enemy):
    """Renders both fighters' current state."""
    print("\n" + "─" * 52)
    print(f"  {player.name:<22} HP: {player.hp:>3}/{player.max_hp}")
    print(f"  {enemy.name:<22} HP: [{enemy.hp_bar()}] {enemy.hp}/{enemy.max_hp}")
    if enemy.status_effects:
        print(f"  Enemy status: {', '.join(enemy.status_effects)}")
    print("─" * 52)


def _get_player_action(player, can_flee: bool) -> str:
    """Builds the action menu from available skills and returns the chosen action."""
    print("\n  Actions:")
    actions: list[tuple[str, str]] = [
        (ATTACK, "Attack — Basic strike"),
        (DEFEND, "Defend — Reduce incoming damage this turn"),
    ]

    if player.skills["combat"].level >= 2:
        actions.append((SKILL_STRIKE,
                        f"Combat Strike — Heavy hit (Combat Lv.{player.skills['combat'].level})"))

    if player.skills["stealth"].level >= 2:
        actions.append((STEALTH_HIT,
                        f"Stealth Strike — Bypass defense (Stealth Lv.{player.skills['stealth'].level})"))

    if player.skills["investigation"].level >= 2:
        actions.append((INTIMIDATE, "Intimidate — Weaken enemy's resolve"))

    if can_flee:
        actions.append((FLEE, "Flee — Attempt to escape"))

    for i, (_, label) in enumerate(actions, 1):
        print(f"  [{i}] {label}")

    while True:
        try:
            choice = int(input("\n  > ").strip())
            if 1 <= choice <= len(actions):
                return actions[choice - 1][0]
        except (ValueError, KeyboardInterrupt):
            pass
        print("  Invalid choice.")


def _resolve_player_action(action: str, player, enemy: Enemy,
                            currently_defending: bool) -> tuple[str, bool]:
    """
    Applies the player's action to the enemy.
    Returns (result_message, is_now_defending_next_turn).
    """
    next_defending = False

    if action == ATTACK:
        dmg = random.randint(8, 15) + player.skills["combat"].level * 2
        if "stunned" in enemy.status_effects:
            dmg = int(dmg * 1.5)
            enemy.clear_status("stunned")
        actual = enemy.take_damage(dmg)
        msg = f"  You strike {enemy.name} for {actual} damage."

    elif action == DEFEND:
        msg = "  You take a defensive stance. Incoming damage halved this turn."
        next_defending = True

    elif action == SKILL_STRIKE:
        lvl = player.skills["combat"].level
        dmg = random.randint(14, 22) + lvl * 3
        crit = random.random() < 0.2
        if crit:
            dmg = int(dmg * 1.5)
        actual = enemy.take_damage(dmg)
        crit_text = " CRITICAL!" if crit else ""
        msg = f"  Combat Strike!{crit_text} {actual} damage to {enemy.name}."

    elif action == STEALTH_HIT:
        # Temporarily zeroes defense so the hit bypasses armor
        dmg = random.randint(15, 24) + player.skills["stealth"].level * 2
        saved_defense, enemy.defense = enemy.defense, 0
        actual = enemy.take_damage(dmg)
        enemy.defense = saved_defense
        msg = f"  Stealth Strike — you find an opening. {actual} damage, ignoring armor."

    elif action == INTIMIDATE:
        chance = 0.3 + player.skills["investigation"].level * 0.1
        if random.random() < chance:
            enemy.apply_status("weakened")
            enemy.attack = max(1, enemy.attack - 4)
            msg = f"  You stare down {enemy.name}. They falter — weakened!"
        else:
            msg = f"  {enemy.name} doesn't flinch. Your words have no effect."

    else:
        msg = "FLEE"

    return msg, next_defending


# ── Main Combat Loop ───────────────────────────────────

def run_combat(player, enemy: Enemy, can_flee: bool = True) -> dict:
    """
    Runs a full turn-based combat encounter.

    Returns a result dict:
        outcome   : 'victory' | 'defeat' | 'fled'
        xp_gained : int
        loot      : list[str]
        turns     : int
    """
    print(f"\n  ⚔  COMBAT: {player.name}  vs  {enemy.name}")
    print(f"  {enemy.description}")
    time.sleep(0.5)

    defending = False
    turn = 0

    while player.is_alive() and enemy.is_alive():
        turn += 1
        _print_combat_status(player, enemy)

        # ── Player turn ──
        action = _get_player_action(player, can_flee)

        if action == FLEE:
            flee_chance = 0.45 + player.skills["stealth"].level * 0.05
            if random.random() < flee_chance:
                print("\n  You slip away into the shadows.")
                return {"outcome": "fled", "xp_gained": 0, "loot": [], "turns": turn}
            else:
                print(f"\n  {enemy.name} blocks your escape!")
                continue

        msg, defending = _resolve_player_action(action, player, enemy, defending)
        print(f"\n{msg}")

        if not enemy.is_alive():
            break

        # ── Enemy turn ──
        time.sleep(0.4)

        if "stunned" in enemy.status_effects:
            print(f"  {enemy.name} is stunned and loses their turn!")
            enemy.clear_status("stunned")
        else:
            raw_dmg = enemy.deal_damage()
            if "weakened" in enemy.status_effects:
                raw_dmg = int(raw_dmg * 0.7)
            if defending:
                raw_dmg = max(1, raw_dmg // 2)
                print(f"  {enemy.name} attacks — blocked! {raw_dmg} damage gets through.")
            else:
                print(f"  {enemy.name} attacks! {raw_dmg} damage.")
            player.take_damage(raw_dmg)
            defending = False

        # Medkit prompt when critically low
        if player.hp < player.max_hp * 0.25 and player.has_item("Medkit"):
            print(f"\n  [HP critical! Use Medkit? 1=Yes / 2=No]")
            try:
                if int(input("  > ")) == 1:
                    player.remove_item("Medkit")
                    player.heal(40)
                    print(f"  Medkit used. HP restored to {player.hp}.")
            except ValueError:
                pass

    # ── Resolve outcome ──
    if player.is_alive():
        print(f"\n  Victory! {enemy.name} is down.")

        xp_msgs = player.gain_xp(enemy.xp_reward)
        for m in xp_msgs:
            print(f"  {m}")

        gained_loot = []
        for item in enemy.loot:
            player.add_item(item)
            gained_loot.append(item)
            print(f"  Found: {item}")

        # Small chance to improve combat skill after a fight
        if random.random() < 0.3:
            if player.skills["combat"].improve():
                print(f"  Combat skill improved! Now Lv.{player.skills['combat'].level}")

        input("\n  [Press ENTER to continue...]")
        return {"outcome": "victory", "xp_gained": enemy.xp_reward,
                "loot": gained_loot, "turns": turn}

    else:
        print(f"\n  You've been defeated by {enemy.name}...")
        input("\n  [Press ENTER to continue...]")
        return {"outcome": "defeat", "xp_gained": 0, "loot": [], "turns": turn}
