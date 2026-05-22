"""
Nova City RPG — Single-file edition
A terminal detective RPG spanning four chapters.

Conceived by Romuald Czlonkowski — www.aiadvisors.pl/en
"""

import os
import sys
import time
import random
from typing import Optional


# ═══════════════════════════════════════════════════════
#  PLAYER SYSTEM  (player.py)
# ═══════════════════════════════════════════════════════

# XP required to reach each level (index = level)
LEVEL_XP_THRESHOLDS = [0, 100, 250, 450, 700, 1000]


class Skill:
    """A single player skill with a numeric level and derived d20 bonus."""

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

        self.inventory = []
        self.flags = {}      # Boolean story-state flags
        self.notes = []      # Case notes gathered during play

    # ── Vitals ─────────────────────────────────────────

    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

    # ── Progression ────────────────────────────────────

    def gain_xp(self, amount: int) -> list:
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

    def skill_check(self, skill_name: str, difficulty: int):
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
        print(f"  {self.name}  |  Level {self.level}  |  XP: {self.xp}")
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


# ═══════════════════════════════════════════════════════
#  STORY SYSTEM  (story.py)
# ═══════════════════════════════════════════════════════

def slow_print(text: str, delay: float = 0.025):
    """Streams text character by character for atmospheric effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_speaker(speaker: str, text: str, delay: float = 0.02):
    """Formats a line of spoken dialogue."""
    print(f"\n  {speaker}:")
    slow_print(f'  "{text}"', delay)


def print_narration(text: str, delay: float = 0.025):
    """Prints narrative description."""
    slow_print(f"\n  [{text}]", delay)


def print_header(title: str):
    """Prints a chapter or scene header."""
    width = 55
    print("\n" + "═" * width)
    print(f"  {title}".center(width))
    print("═" * width + "\n")


def get_choice(options: list, prompt: str = "Your choice") -> int:
    """
    Displays numbered choices and returns the 0-based index of the selection.
    Loops until valid input.
    """
    print()
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")

    while True:
        try:
            raw = input(f"\n  {prompt} > ").strip()
            idx = int(raw)
            if 1 <= idx <= len(options):
                return idx - 1
        except (ValueError, KeyboardInterrupt):
            pass
        print(f"  Enter a number from 1 to {len(options)}.")


# ── Chapter 1 — Karim's Mother ─────────────────────────

def scene_karims_mother(player) -> str:
    """
    Opening scene: Mrs. Mansour hires the player to find her son Karim.
    The chosen approach (direct / gentle / professional) affects
    early clue availability and story flags.
    Returns one of: 'direct', 'gentle', 'professional'.
    """
    print_header("CHAPTER 1 — A MOTHER'S PLEA")

    print_narration(
        "The Port District, Nova City. Late night. A cramped apartment above a fish market. "
        "The woman at the door has the hollow eyes of someone who hasn't slept in days."
    )

    print_speaker("Mrs. Mansour", "They told me you help people. People the police won't touch.")
    print_speaker(player.name, "Who told you that?")
    print_speaker(
        "Mrs. Mansour",
        "It doesn't matter. My son Karim — seventeen years old — he's been missing three days. "
        "I found this in his room."
    )

    print_narration("She holds out a crumpled Port Sons gang tag. A scorpion stamped in black ink.")

    print_speaker(player.name, "How long has he been running with them?")
    print_speaker(
        "Mrs. Mansour",
        "He isn't — he wasn't. The neighborhood changes people. "
        "El-Aqrab, they call him. The Scorpion. He runs the Port Sons. "
        "He takes boys like Karim and makes them... do things."
    )

    print_narration("She steadies herself.")

    print_speaker("Mrs. Mansour", "I can pay. Not much. But I can pay.")

    print("\n  How do you respond?")
    choice = get_choice([
        '"Keep your money. Tell me everything you know about El-Aqrab." (Direct)',
        '"We\'ll find him. Start from the beginning — when did you last see Karim?" (Gentle)',
        '"I\'ll need a retainer up front. This sounds dangerous." (Professional)',
    ])

    approaches = ["direct", "gentle", "professional"]
    chosen = approaches[choice]

    if chosen == "direct":
        print_speaker(player.name, "Keep your money. Tell me everything about El-Aqrab.")
        print_speaker(
            "Mrs. Mansour",
            "Straightforward. Good. No one knows his real name. "
            "He runs everything through his lieutenants."
        )
        player.set_flag("approach_direct", True)
        player.notes.append("El-Aqrab's true identity is unknown — even to most of his own gang.")

    elif chosen == "gentle":
        print_speaker(player.name, "We'll find him. Start from the beginning — when did you last see Karim?")
        print_speaker(
            "Mrs. Mansour",
            "Thursday morning. He seemed nervous. He had a burner phone I'd never seen before."
        )
        player.set_flag("approach_gentle", True)
        player.notes.append("Karim had an unknown burner phone before he disappeared.")

    else:
        print_speaker(player.name, "I'll need a retainer. This sounds dangerous.")
        print_speaker("Mrs. Mansour", "I have two hundred. It's everything I have.")
        print_speaker(player.name, "That'll do. Now tell me about the last time you saw him.")
        player.add_item("200 Dinars")
        player.set_flag("approach_professional", True)
        player.notes.append("Client: Mrs. Mansour. Missing son: Karim (17). Port Sons tag found in his room.")

    print_narration(
        "She talks for an hour. By the end you have a neighborhood, a warehouse number, "
        "and the sinking feeling that Karim isn't the only missing boy in the Port District."
    )

    player.notes.append("El-Aqrab controls the Port District docks. Last known sighting: Warehouse 7.")

    input("\n  [Press ENTER to continue...]")
    return chosen


# ── Chapter 2 — Nova Partnership ───────────────────────

def scene_nova_partnership(player) -> bool:
    """
    Scene where the player meets Nova and negotiates a partnership.
    Returns True if the player accepts the alliance.
    """
    print_header("CHAPTER 2 — THE FIXER")

    print_narration(
        "The Anchor Bar. Noon. A woman in a worn leather jacket sits across from you. "
        "A dossier sits on the table between you. She got here before you. That's telling."
    )

    print_speaker("Nova", "You're poking around Port Sons territory. Brave or stupid, I haven't decided.")
    print_speaker(player.name, "Who are you?")
    print_speaker(
        "Nova",
        "Someone who's been working El-Aqrab's case for six months. "
        "Someone who knows you hit the same dead end I did at Warehouse 7."
    )

    print_narration("She slides the dossier across. Crime scene photos. Three missing teenagers.")

    print_speaker(
        "Nova",
        "El-Aqrab is smart. He never appears in public — his lieutenants handle everything. "
        "But I have a contact inside Port Sons, a man named Tariq. "
        "He'll only talk if we come together. Less suspicious."
    )

    print("\n  She wants to partner up. Your call.")
    choice = get_choice([
        '"You have six months on me. I\'m in." (Accept)',
        '"I work alone. How do I know I can trust you?" (Skeptical)',
        '"What\'s your angle — what do you actually get from this?" (Probe motives)',
    ])

    if choice == 0:
        print_speaker(player.name, "You've got six months on me. I'm in.")
        print_speaker("Nova", "Good. No heroics. We get the information and we get out.")
        player.set_flag("nova_partner", True)
        player.set_flag("nova_trust", 2)
        player.add_item("Nova's Dossier")
        player.notes.append("NOVA: Undercover investigator. Has contact 'Tariq' inside Port Sons.")
        print_narration("Nova trusts you immediately. Whether that's confidence or desperation, you're not sure.")

    elif choice == 1:
        print_speaker(player.name, "I work alone. How do I know I can trust you?")
        print_speaker(
            "Nova",
            "You don't. But Tariq won't meet with a solo operator he's never heard of. "
            "I'm your introduction. After that, do what you want."
        )

        sub = get_choice([
            "Fair enough. One meeting, then we reassess.",
            "No deal. I'll find another way to Tariq.",
        ])

        if sub == 0:
            print_speaker(player.name, "Fair enough. One meeting, then we see where we stand.")
            player.set_flag("nova_partner", True)
            player.set_flag("nova_trust", 1)
            player.add_item("Nova's Dossier")
            player.notes.append("NOVA: Provisional alliance. Trust is earned, not given.")
        else:
            print_speaker(player.name, "No deal.")
            print_speaker("Nova", "Your funeral. When you hit a wall — and you will — I'll be at this bar.")
            player.set_flag("nova_partner", False)
            print_narration("You walk out alone. Harder road, but yours.")
            input("\n  [Press ENTER to continue...]")
            return False

    else:
        print_speaker(player.name, "What's your angle? What do you actually get from this?")
        print_speaker(
            "Nova",
            "El-Aqrab killed my informant. A kid named Hassan. Seventeen years old. "
            "I want El-Aqrab in cuffs, or I want him dead. I don't particularly care which."
        )
        print_narration("The honesty is brutal. You believe her.")
        print_speaker(player.name, "Then we want the same thing.")
        player.set_flag("nova_partner", True)
        player.set_flag("nova_trust", 3)
        player.add_item("Nova's Dossier")
        player.notes.append("NOVA: Personal stake — El-Aqrab murdered her informant Hassan (17). Highly motivated.")

    print_narration("You spend the next hour comparing notes. The shape of the case begins to emerge.")
    input("\n  [Press ENTER to continue...]")
    return player.get_flag("nova_partner")


# ── Chapter 4 — Final Confrontation ────────────────────

def scene_final_confrontation(player, el_aqrab_identity: str) -> bool:
    """
    Final confrontation: the player faces El-Aqrab in his office.
    el_aqrab_identity is the name the player deduced from the evidence board.
    Returns True if the player brings him to justice.
    """
    print_header("CHAPTER 4 — THE SCORPION'S LAIR")

    print_narration(
        "The Port Authority building. Top floor. A man with the title 'Harbor Commissioner' "
        "sits behind a mahogany desk. He looks up when you enter. "
        "His expression doesn't change. That tells you everything."
    )

    commissioner_name = "Commissioner Halabi"
    correctly_identified = any(
        keyword in el_aqrab_identity.lower()
        for keyword in ["nasser", "halabi", "commissioner"]
    )

    if correctly_identified:
        print_narration("He sees the recognition in your eyes. No point in pretending.")
        print_speaker(commissioner_name, "You figured it out. I wondered who eventually would.")
    else:
        print_speaker(commissioner_name, "Can I help you?")
        print_speaker(player.name, "You can turn yourself in. El-Aqrab.")
        print_narration("The polite expression vanishes.")

    print_speaker(
        commissioner_name,
        "El-Aqrab. I haven't heard that name said to my face in years. "
        "You've been busy. The evidence board — yes, I know. "
        "My people saw you at the docks. At Tariq's apartment."
    )

    print_narration("Two guards enter behind you. The door clicks shut.")

    print("\n  You're outnumbered and he knows it. How do you play this?")

    options = [
        '"It\'s over, Halabi. Nova has copies at three separate locations." (Bluff)',
        '"The boys — Karim and the others — where are they?" (Focus on the mission)',
    ]

    if player.has_item("Recorder"):
        options.append('"This entire conversation is broadcasting live." (Use recorder)')

    if player.get_flag("nova_partner"):
        options.append("Wait for Nova's signal — she's already in position. (Trust the plan)")

    choice = get_choice(options)
    selected = options[choice]
    success = False

    if "Bluff" in selected:
        print_speaker(
            player.name,
            "It's over, Halabi. Nova has copies of everything at three separate locations."
        )
        succeeded, roll, target = player.skill_check("investigation", 12)
        if succeeded or player.get_flag("full_evidence"):
            print_speaker(commissioner_name, "...You're bluffing.")
            print_speaker(player.name, "Try me.")
            print_narration("A long silence. Halabi raises his hands slowly.")
            success = True
        else:
            print_speaker(commissioner_name, "Empty words. Take them.")
            print_narration("The guards move. You fight your way out the hard way.")
            success = False

    elif "Focus on the mission" in selected:
        print_speaker(player.name, "The boys — Karim and the others — where are they?")
        print_speaker(
            commissioner_name,
            "Unharmed. I'm not a monster. They're leverage, not victims."
        )
        print_speaker(
            player.name,
            "Then prove it. Let them go and I'll give you 24 hours before I go to the press."
        )
        succeeded, _, _ = player.skill_check("investigation", 10)
        if succeeded:
            print_speaker(
                commissioner_name,
                "You'd actually walk away from the biggest story in Nova City?"
            )
            print_speaker(player.name, "I want the boys home. After that, we'll see.")
            print_narration("Halabi considers. It's a lie. He doesn't know that.")
            success = True
        else:
            print_speaker(commissioner_name, "I don't believe you.")
            success = False

    elif "recorder" in selected.lower():
        print_speaker(player.name, "This entire conversation is broadcasting live.")
        print_narration("You hold up the recorder. Halabi's composure fractures.")
        print_speaker(commissioner_name, "You — how did you—")
        print_speaker(player.name, "Anything you do now is on camera. Live.")
        print_narration("The guards look at each other. Neither wants to be on that recording.")
        success = True

    else:
        # Nova's plan
        print_narration("You hold Halabi's gaze and wait. Three seconds. Then the fire alarm.")
        print_speaker("Nova", "[Over earpiece] — go. Police are ninety seconds out. Evidence package delivered.")
        print_speaker(player.name, "Hear that? Your guards can stay and be arrested, or they can leave now.")
        print_narration("They choose survival over loyalty.")
        success = True

    # Epilogue
    if success:
        print_narration("\nThree hours later. Harbor Commissioner Nasser Halabi is in police custody.")
        print_narration("Karim Mansour is home. So are eleven other boys.")
        print_narration("El-Aqrab — the Scorpion — will not sting again.")

        if player.get_flag("nova_partner"):
            print_speaker("Nova", "We did it. Hassan would have liked you.")
            print_speaker(player.name, "What will you do now?")
            print_speaker("Nova", "There's always another El-Aqrab. You?")
            print_speaker(player.name, "Same answer.")

        print_speaker("Mrs. Mansour", "Thank you. Thank you for bringing him home.")
        print_narration("Some cases don't have clean endings. This one did. You'll take it.")

    else:
        print_narration("Halabi's men take you down. You wake up in the harbor, bruised and cold.")
        print_narration("But Nova got the evidence out. The story breaks the next morning.")
        print_narration("El-Aqrab tries to flee. He doesn't make it to the airport.")
        print_narration("The boys come home. It's a win — just not a clean one.")

    input("\n  [Press ENTER to finish...]")
    return success


# ═══════════════════════════════════════════════════════
#  COMBAT SYSTEM  (combat.py)
# ═══════════════════════════════════════════════════════

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
        self.status_effects = []  # e.g. "stunned", "weakened"

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


# ── Combat Action Constants ─────────────────────────────

ATTACK       = "attack"
DEFEND       = "defend"
SKILL_STRIKE = "skill_strike"
STEALTH_HIT  = "stealth_hit"
INTIMIDATE   = "intimidate"
FLEE         = "flee"


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
    actions = [
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


def _resolve_player_action(action: str, player, enemy: Enemy, currently_defending: bool):
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


def run_combat(player, enemy: Enemy, can_flee: bool = True) -> dict:
    """
    Runs a full turn-based combat encounter.
    Returns a result dict with keys: outcome, xp_gained, loot, turns.
    outcome is one of: 'victory', 'defeat', 'fled'.
    """
    print(f"\n  COMBAT: {player.name}  vs  {enemy.name}")
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


# ═══════════════════════════════════════════════════════
#  INVESTIGATION SYSTEM  (investigation.py)
# ═══════════════════════════════════════════════════════

class Clue:
    """
    A single piece of evidence on the board.
    'connections' holds IDs of clues that this one points toward.
    """

    def __init__(self, clue_id: str, title: str, description: str,
                 category: str, connections: Optional[list] = None,
                 unlocked: bool = False):
        self.id = clue_id
        self.title = title
        self.description = description
        self.category = category    # person | location | document | object
        self.connections = connections or []
        self.unlocked = unlocked
        self.analyzed = False

    def __repr__(self):
        if self.analyzed:
            marker = "v"
        elif self.unlocked:
            marker = "?"
        else:
            marker = "."
        return f"[{marker}] {self.title}"


# ── Master Clue Database ───────────────────────────────

CLUE_DATABASE = {
    "c01": Clue("c01", "Port Sons Gang Tag",
                "Scorpion insignia, hand-stamped — not printed. A craftsman's mark.",
                "object", ["c04", "c08"], unlocked=True),

    "c02": Clue("c02", "Karim's Burner Phone",
                "Pre-paid. Three contacts saved: 'Dock Boss', 'Night Shift', 'The Commissioner'.",
                "object", ["c05", "c09"]),

    "c03": Clue("c03", "Warehouse 7 Ledger",
                "Every third shipment carries a secondary manifest labeled "
                "'Port Authority Approved'. Each one signed with the initials N.H.",
                "document", ["c06", "c09"]),

    "c04": Clue("c04", "Tariq's Testimony",
                "Tariq says El-Aqrab 'speaks like an educated man' and is never seen "
                "without gloves. He has Port Authority clearance to move through the docks freely.",
                "person", ["c07", "c09"]),

    "c05": Clue("c05", "Phone Tower Records",
                "The 'Commissioner' number on Karim's phone was dialed from the "
                "Port Authority Building, 5th floor, three times in the past week.",
                "document", ["c09"]),

    "c06": Clue("c06", "Customs Stamp Analysis",
                "The secondary manifests bear an official Port Authority wet stamp. "
                "Only the Harbor Commissioner holds stamp authority.",
                "document", ["c09"]),

    "c07": Clue("c07", "Leather Shop Receipt",
                "A shop near the docks: 'Commissioner Halabi orders custom lambskin "
                "gloves every six months. Always pays cash. Never leaves a name, "
                "but the face is unmistakable.'",
                "person", ["c09"]),

    "c08": Clue("c08", "Tattoo Removal Record",
                "A private clinic note from 2019: Nasser Halabi had a scorpion tattoo "
                "removed from his left wrist. Paid in cash — not through insurance.",
                "person", ["c09"]),

    "c09": Clue("c09", "Identity: El-Aqrab",
                "Harbor Commissioner Nasser Halabi IS El-Aqrab. He runs the Port Sons "
                "from behind official cover, invisible to anyone who only looks at the gang.",
                "person", []),
}

# Clues that become available at the start of each chapter
CHAPTER_CLUES = {
    1: ["c01"],
    2: ["c02", "c03", "c04"],
    3: ["c05", "c06", "c07", "c08"],
    4: ["c09"],
}

# Skill check difficulty per clue
CLUE_DIFFICULTY = {
    "c01": 8,  "c02": 10, "c03": 12,
    "c04": 10, "c05": 11, "c06": 11,
    "c07": 9,  "c08": 13, "c09": 15,
}


class EvidenceBoard:
    """
    The player's investigation workspace.
    Tracks which clues are discovered, analyzed, and connected.
    """

    def __init__(self, player):
        self.player = player
        # Deep-copy each clue so runtime state is isolated from the master database
        self.clues = {
            cid: Clue(c.id, c.title, c.description, c.category,
                      list(c.connections), c.unlocked)
            for cid, c in CLUE_DATABASE.items()
        }

    def add_clue(self, clue_id: str):
        if clue_id in self.clues:
            self.clues[clue_id].unlocked = True

    def get_unlocked(self) -> list:
        return [c for c in self.clues.values() if c.unlocked]

    def get_analyzed(self) -> list:
        return [c for c in self.clues.values() if c.analyzed]

    def evidence_count_against_target(self, target: str = "c09") -> int:
        """How many analyzed clues directly point to the identity clue."""
        return sum(1 for c in self.get_analyzed() if target in c.connections)

    def can_solve(self) -> bool:
        """True once the player has analyzed enough evidence to make a deduction."""
        return self.evidence_count_against_target("c09") >= 3

    def display(self):
        """Renders the full evidence board to the terminal."""
        unlocked = self.get_unlocked()
        locked_count = sum(1 for c in self.clues.values() if not c.unlocked)

        print("\n" + "=" * 58)
        print("  EVIDENCE BOARD -- Nova City Investigation")
        print("=" * 58)

        if not unlocked:
            print("  [Board is empty — gather evidence first]")
        else:
            categories = {
                "person":   "PERSONS OF INTEREST",
                "document": "DOCUMENTS",
                "object":   "PHYSICAL EVIDENCE",
                "location": "LOCATIONS",
            }
            for cat_key, cat_label in categories.items():
                cat_clues = [c for c in unlocked if c.category == cat_key]
                if not cat_clues:
                    continue
                print(f"\n  {cat_label}:")
                for clue in cat_clues:
                    print(f"    {clue}")
                    if clue.analyzed:
                        linked = [
                            self.clues[cid].title
                            for cid in clue.connections
                            if cid in self.clues
                            and self.clues[cid].unlocked
                            and cid != "c09"
                        ]
                        if linked:
                            print(f"       -> Links to: {', '.join(linked)}")

        evidence_count = self.evidence_count_against_target("c09")
        print(f"\n  Threads pointing to El-Aqrab: {evidence_count}/4")
        print(f"  Undiscovered leads: {locked_count}")

        if self.can_solve():
            print("\n  *** SUFFICIENT EVIDENCE TO MAKE A DEDUCTION ***")

        print("=" * 58)

    def analyze_clue(self, clue_id: str) -> Optional[str]:
        """
        Attempts a deep analysis of the given clue via an Investigation check.
        On success, marks the clue analyzed and unlocks connected clues.
        Returns a text result, or None if the clue doesn't exist.
        """
        clue = self.clues.get(clue_id)
        if not clue or not clue.unlocked:
            return None

        if clue.analyzed:
            return f"You've already fully analyzed: {clue.title}"

        difficulty = CLUE_DIFFICULTY.get(clue_id, 10)
        success, roll, target = self.player.skill_check("investigation", difficulty)

        if success:
            clue.analyzed = True
            # Unlock clues this one points toward (but not the final deduction clue)
            for connected_id in clue.connections:
                if connected_id != "c09":
                    self.clues[connected_id].unlocked = True

            result = f"  Insight: {clue.description}"

            if random.random() < 0.25:
                if self.player.skills["investigation"].improve():
                    result += (f"\n  [Investigation skill improved to "
                               f"Lv.{self.player.skills['investigation'].level}]")
            return result
        else:
            return (f"  You study '{clue.title}' carefully, but the significance escapes you. "
                    f"(Roll: {roll} vs Difficulty: {target})")


def scene_evidence_collection(player, chapter: int) -> EvidenceBoard:
    """
    Returns the player's persistent EvidenceBoard, unlocking clues
    appropriate for the given chapter.
    """
    if not hasattr(player, "_evidence_board"):
        player._evidence_board = EvidenceBoard(player)

    board = player._evidence_board
    for clue_id in CHAPTER_CLUES.get(chapter, []):
        board.add_clue(clue_id)

    return board


def run_investigation_scene(player, board: EvidenceBoard, chapter: int) -> bool:
    """
    Interactive investigation loop for the given chapter.
    Player can analyze clues, review notes, or attempt the final deduction.
    Returns True if meaningful progress was made this session.
    """
    print_header(f"CHAPTER {chapter} — EVIDENCE BOARD")

    if chapter == 2:
        print_narration(
            "You spread your notes across the table. Between Tariq's information "
            "and what Nova pulled from the docks, the board is filling up."
        )
    elif chapter == 3:
        print_narration(
            "The picture is nearly complete. One more clear thread and you'll "
            "have enough to name El-Aqrab with certainty."
        )

    progress_made = False

    while True:
        board.display()

        unlocked = board.get_unlocked()
        unanalyzed = [c for c in unlocked if not c.analyzed]

        options = []
        if unanalyzed:
            options.append("Analyze a clue")
        options.append("Review case notes")

        if chapter >= 3 and board.can_solve():
            options.append("Make the deduction — name El-Aqrab")

        options.append("Continue the story")

        choice = get_choice(options)
        selected = options[choice]

        if selected == "Analyze a clue":
            print("\n  Which clue?")
            clue_titles = [c.title for c in unanalyzed] + ["Cancel"]
            clue_choice = get_choice(clue_titles)

            if clue_choice < len(unanalyzed):
                result = board.analyze_clue(unanalyzed[clue_choice].id)
                if result:
                    slow_print(f"\n{result}", 0.025)
                    progress_made = True
            input("\n  [Press ENTER...]")

        elif selected == "Review case notes":
            print("\n  CASE NOTES:")
            player.show_notes()
            input("\n  [Press ENTER...]")

        elif "name El-Aqrab" in selected:
            solved = run_deduction_puzzle(player, board)
            return solved

        else:
            break

    return progress_made


def run_deduction_puzzle(player, board: EvidenceBoard) -> bool:
    """
    The climactic deduction: the player must type El-Aqrab's real name.
    Returns True if the answer is correct.
    """
    print("\n" + "=" * 58)
    print("  THE DEDUCTION")
    print("=" * 58)

    print_narration(
        "You step back from the board. The threads connect. You can see the shape of it — "
        "someone with port access, official cover, and the ability to vanish behind a title."
    )

    slow_print("\n  Who is El-Aqrab? Enter the suspect's name:")
    analyzed_count = len(board.get_analyzed())
    if analyzed_count >= 4:
        print("  (Hint: The initials N.H. appear on the warehouse ledger.)")
    elif analyzed_count >= 2:
        print("  (Hint: Who holds Port Authority stamp authority?)")
    else:
        print("  (Hint: Review every clue on the board — the answer is there.)")

    answer = input("\n  Your answer: ").strip().lower()

    correct_answers = [
        "nasser halabi", "halabi", "commissioner halabi",
        "nasser", "harbor commissioner", "the commissioner",
        "commissioner nasser halabi",
    ]

    if any(a in answer for a in correct_answers):
        print("\n  *** CORRECT ***")
        slow_print(
            "  Harbor Commissioner Nasser Halabi. El-Aqrab. The Scorpion.\n"
            "  N.H. on the ledger. Exclusive stamp authority. The tattoo removal.\n"
            "  The custom gloves. The phone contact labelled 'The Commissioner'.\n"
            "  Every road in the Port District leads to the man who runs the docks.",
            0.028
        )

        board.add_clue("c09")
        board.clues["c09"].unlocked = True
        board.clues["c09"].analyzed = True
        player.notes.append("EL-AQRAB IDENTIFIED: Harbor Commissioner Nasser Halabi.")

        xp_msgs = player.gain_xp(100)
        for msg in xp_msgs:
            print(f"  {msg}")

        if player.skills["investigation"].improve():
            print(f"  Investigation mastered! Lv.{player.skills['investigation'].level}")

        input("\n  [Press ENTER to confront him...]")
        return True

    else:
        print(f"\n  You write '{answer}' on the board... but something doesn't fit.")
        slow_print("  The evidence points somewhere else. Review the connections.", 0.028)
        input("\n  [Press ENTER to return to the board...]")
        return False


# ═══════════════════════════════════════════════════════
#  MAIN GAME LOOP  (main.py)
# ═══════════════════════════════════════════════════════

def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass


def print_title():
    print("\n" + "=" * 70)
    print("  NOVA CITY".center(70))
    print("  A Nova City Investigation".center(70))
    print("=" * 70)
    print()
    print("  Conceived by Romuald Czlonkowski -- www.aiadvisors.pl/en".center(70))
    print()


def show_intro():
    print("─" * 65)
    slow_print("  Nova City. Population: 2.3 million. Port District: forgotten.", 0.028)
    slow_print("  The Port Sons gang controls the docks. No one asks questions.", 0.028)
    slow_print("  El-Aqrab — The Scorpion — is the name no one says out loud.", 0.028)
    slow_print("  Someone has to.", 0.028)
    print("─" * 65)
    time.sleep(0.4)


def show_ending(won: bool, player):
    print("\n" + "=" * 60)
    print("  CASE CLOSED" if won else "  GAME OVER")
    print("=" * 60)
    player.show_status()
    print()

    if won:
        slow_print("  El-Aqrab is behind bars. The Port District breathes again.", 0.028)
        slow_print("  Karim Mansour is home. Eleven other boys too.", 0.028)
        slow_print("  Nova City is a little less rotten than it was yesterday.", 0.028)
    else:
        slow_print("  The Scorpion wins this round.", 0.028)
        slow_print("  But stories like this don't end — they pause.", 0.028)

    print("\n" + "=" * 60)


# ── Character Creation ─────────────────────────────────

def create_character() -> Player:
    """Handles name input and initial skill point allocation."""
    print("─" * 55)
    print("  Create your character")
    print("─" * 55)

    while True:
        name = input("  Enter your name: ").strip()
        if name:
            break
        print("  A detective needs a name.")

    player = Player(name)

    print(f"\n  {name}. You have 3 skill points to distribute.")
    print("  Skills: [1] Combat   [2] Stealth   [3] Investigation")
    print()

    points = 3
    while points > 0:
        print(f"  Current -- {' | '.join(str(s) for s in player.skills.values())}")
        print(f"  Points remaining: {points}")
        try:
            choice = int(input("  Improve which skill? > ").strip())
            if choice == 1:
                player.skills["combat"].improve()
                points -= 1
            elif choice == 2:
                player.skills["stealth"].improve()
                points -= 1
            elif choice == 3:
                player.skills["investigation"].improve()
                points -= 1
            else:
                print("  Enter 1, 2, or 3.")
        except ValueError:
            print("  Enter 1, 2, or 3.")

    player.show_status()
    return player


# ── Chapter 1 — A Mother's Plea ────────────────────────

def chapter_one(player):
    """
    Introduce the case through Karim's mother.
    First combat encounter on the docks.
    """
    print_header("CHAPTER 1 — A MOTHER'S PLEA")

    scene_karims_mother(player)

    board = scene_evidence_collection(player, chapter=1)

    print_narration("You study the gang tag she gave you. It's a starting point.")
    run_investigation_scene(player, board, chapter=1)

    print_header("CHAPTER 1 — THE DOCKS, NIGHT")
    print_narration(
        "You follow the trail to Warehouse Row. A Port Sons grunt spots you "
        "before you can slip past. There is no talking your way out of this one."
    )

    grunt = make_port_grunt()
    result = run_combat(player, grunt, can_flee=True)

    if result["outcome"] == "defeat":
        print_narration("You wake up bruised but alive — they didn't want to kill you. Yet.")
        player.hp = max(20, player.hp)
    elif result["outcome"] == "victory" and "Burner Phone Fragment" in result["loot"]:
        player.notes.append("Found a burner phone fragment — same make as Karim's phone.")
        board.add_clue("c02")

    player.show_status()
    print("\n  Chapter 1 complete.")
    input("  [Press ENTER for Chapter 2...]")


# ── Chapter 2 — The Fixer ──────────────────────────────

def chapter_two(player):
    """
    Meet Nova, decide on partnership.
    Encounter Tariq — by persuasion or force.
    Deepen the investigation.
    """
    player.heal(30)

    has_partner = scene_nova_partnership(player)

    board = scene_evidence_collection(player, chapter=2)

    print_header("CHAPTER 2 — TARIQ'S APARTMENT")

    if has_partner:
        print_narration(
            "Nova leads you to Tariq's apartment in the industrial quarter. "
            "When he opens the door and sees two of you, something shifts in his face."
        )
    else:
        print_narration(
            "You track Tariq to his apartment. He opens the door and immediately "
            "tries to slam it shut. You get a foot in."
        )

    print("\n  How do you handle Tariq?")
    tariq_options = [
        "Reason with him — you need information, not a body",
        "Show him the evidence you already have — let him see the walls closing in",
    ]
    if has_partner:
        tariq_options.append("Let Nova take the lead — she knows him")
    tariq_options.append("Take him down — information by force if necessary")

    tariq_choice = get_choice(tariq_options)

    if tariq_choice == len(tariq_options) - 1:
        print_narration("Tariq reaches for something under the counter. No more talking.")
        tariq = make_tariq()
        result = run_combat(player, tariq, can_flee=False)

        if result["outcome"] == "defeat":
            player.hp = max(15, player.hp)
            print_narration("He got the better of you — but you overheard enough before blacking out.")

        if "Tariq's Confession" in result.get("loot", []):
            board.add_clue("c04")
            board.add_clue("c03")

    else:
        if tariq_choice == 0:
            print_narration("Tariq eyes you for a long moment. Then he sits down. 'What do you want?'")
            player.notes.append("Tariq is frightened of El-Aqrab — willing to talk if he feels safe.")

        elif tariq_choice == 1:
            slow_print("\n  You lay out what you know. Tariq's face goes pale.")
            print_narration("'How did you — fine. I'll tell you what I can. But I'm gone after this.'")

        else:
            print_narration(
                "Nova steps forward. She and Tariq speak quietly for a moment. "
                "Whatever she said, it worked."
            )
            player.set_flag("nova_helped_tariq", True)

        board.add_clue("c04")
        board.add_clue("c03")
        print_narration("Tariq talks for twenty minutes. The shape of El-Aqrab's operation becomes clearer.")

    run_investigation_scene(player, board, chapter=2)

    player.show_status()
    print("\n  Chapter 2 complete.")
    input("  [Press ENTER for Chapter 3...]")


# ── Chapter 3 — Warehouse 7 ────────────────────────────

def chapter_three(player):
    """
    Infiltrate Warehouse 7 for physical evidence.
    Multiple entry approaches with different combat consequences.
    """
    player.heal(25)

    print_header("CHAPTER 3 — WAREHOUSE 7")
    print_narration(
        "Nova intercepts a shipping manifest. Secondary cargo moves through "
        "Warehouse 7 tonight. If physical evidence connecting El-Aqrab exists, it's there."
    )

    if player.hp < 50:
        player.add_item("Medkit")
        print_narration("Nova hands you a medkit. 'Don't be a hero.'")

    print("\n  How do you enter the warehouse?")
    approach = get_choice([
        "Stealth — wait for a gap in patrols (Stealth check, DC 13)",
        "Distraction — trigger a fire alarm two blocks away (Investigation check, DC 11)",
        "Direct — walk in through the front and deal with whatever you find",
    ])

    entry_success = False

    if approach == 0:
        success, roll, target = player.skill_check("stealth", 13)
        if success:
            slow_print(f"\n  You ghost through the shadows. No one sees you. (Roll: {roll})", 0.022)
            entry_success = True
            player.notes.append("Warehouse 7: Accessed via stealth — south loading dock, 11 pm.")
        else:
            slow_print(f"\n  A guard catches movement. (Roll: {roll} vs DC {target})", 0.022)

    elif approach == 1:
        success, roll, target = player.skill_check("investigation", 11)
        if success:
            slow_print(f"\n  The alarm clears the floor. Four minutes. (Roll: {roll})", 0.022)
            entry_success = True
        else:
            slow_print(f"\n  The alarm doesn't trigger. Guards are on edge. (Roll: {roll})", 0.022)

    else:
        print_narration("Three grunts step out from the loading bay. They were expecting trouble.")

    if not entry_success:
        grunt = make_port_grunt()
        result1 = run_combat(player, grunt)
        if result1["outcome"] == "defeat":
            player.hp = max(15, player.hp)

        if player.is_alive():
            print_narration("A lieutenant steps out from the back office. He has seen everything.")
            lieutenant = make_port_lieutenant()
            result2 = run_combat(player, lieutenant, can_flee=False)

            if result2["outcome"] == "defeat":
                player.hp = max(10, player.hp)
            elif "Encrypted Note" in result2.get("loot", []):
                player.notes.append("Encrypted note from Warehouse 7: 'N.H. confirms next shipment.'")

    print_narration(
        "In the warehouse office: shipping ledgers, stamped manifests, "
        "a burner phone still warm."
    )

    board = scene_evidence_collection(player, chapter=3)
    player.set_flag("warehouse_evidence", True)

    if not player.has_item("Recorder"):
        player.add_item("Recorder")
        print_narration("You pocket a small digital recorder from the desk. Could be useful.")

    run_investigation_scene(player, board, chapter=3)

    if board.clues["c09"].analyzed:
        player.set_flag("identity_known", True)
        player.set_flag("full_evidence", True)
        print_narration("You know who El-Aqrab is. Now you have to prove it — or confront him directly.")
    else:
        print_narration("You have most of the picture. The final piece will surface at the confrontation.")

    player.show_status()
    print("\n  Chapter 3 complete.")
    input("  [Press ENTER for the final chapter...]")


# ── Chapter 4 — The Scorpion's Lair ───────────────────

def chapter_four(player) -> bool:
    """
    Final chapter: confront El-Aqrab in the Port Authority building.
    Returns True if the player wins.
    """
    player.heal(50)

    print_header("CHAPTER 4 — THE SCORPION'S LAIR")

    if not player.get_flag("identity_known"):
        print_narration(
            "Before confronting anyone, you need to be certain. "
            "Nova spreads the evidence one final time."
        )
        board = getattr(player, "_evidence_board", scene_evidence_collection(player, 3))

        if board.can_solve():
            solved = run_deduction_puzzle(player, board)
            if solved:
                player.set_flag("identity_known", True)
        else:
            # Failsafe: grant the identity so the player is never stuck
            print_narration(
                "The evidence paints one clear picture. "
                "Harbor Commissioner Nasser Halabi. El-Aqrab. You're certain."
            )
            player.set_flag("identity_known", True)
            player.notes.append("EL-AQRAB IDENTIFIED: Harbor Commissioner Nasser Halabi.")

    print_narration(
        "The Port Authority building. Security is tighter than usual — "
        "Halabi knows someone is close. His personal guard stands at the elevator."
    )

    approach = get_choice([
        "Fight through the guard",
        "Use official credentials (requires Nova's Dossier or Access Card)",
        "Use the recorder as a distraction",
    ])

    if approach == 0:
        guard = make_final_guard()
        result = run_combat(player, guard, can_flee=False)
        if result["outcome"] == "defeat":
            player.hp = max(10, player.hp)
            print_narration("Beaten but not stopped. You drag yourself up. It ends tonight.")

    elif approach == 1:
        if player.has_item("Nova's Dossier") or player.has_item("Access Card"):
            success, roll, _ = player.skill_check("investigation", 10)
            if success:
                print_narration("You talk your way past. Confident, purposeful, invisible.")
            else:
                print_narration("The guard isn't buying it. You'll have to go through him.")
                guard = make_final_guard()
                run_combat(player, guard, can_flee=False)
        else:
            print_narration("You don't have the right credentials. Direct approach.")
            guard = make_final_guard()
            run_combat(player, guard, can_flee=False)

    else:
        if player.has_item("Recorder"):
            print_narration(
                "You play back Tariq's voice through the recorder down the hall. "
                "The guard moves to investigate. You take the stairs."
            )
        else:
            print_narration("No recorder. Direct approach.")
            guard = make_final_guard()
            run_combat(player, guard, can_flee=False)

    if not player.is_alive():
        print_narration("You never reach his office. The case dies here.")
        return False

    identity_guess = "Nasser Halabi"
    if not player.get_flag("identity_known"):
        identity_guess = input("\n  Last chance — who is El-Aqrab? ").strip()

    return scene_final_confrontation(player, identity_guess)


# ── Entry Point ─────────────────────────────────────────

def main():
    clear_screen()
    print_title()

    player = create_character()
    input("\n  [Press ENTER to begin...]")

    clear_screen()
    show_intro()
    input("  [Press ENTER to start the investigation...]")

    chapters = [chapter_one, chapter_two, chapter_three, chapter_four]
    won = False

    for i, chapter_fn in enumerate(chapters, 1):
        clear_screen()
        try:
            if i == 4:
                won = chapter_fn(player)
            else:
                chapter_fn(player)
        except (KeyboardInterrupt, EOFError):
            print("\n\n  [Game interrupted]")
            sys.exit(0)

    clear_screen()
    show_ending(won, player)
    print()


if __name__ == "__main__":
    main()
