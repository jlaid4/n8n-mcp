"""
story.py - Dialogue and narrative system for Nova City RPG
Provides branching dialogue trees and the three key story scenes.
"""

import sys
import time


# ── Output Helpers ─────────────────────────────────────

def slow_print(text: str, delay: float = 0.025):
    """Streams text character by character for atmospheric effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_speaker(speaker: str, text: str, delay: float = 0.02):
    """Formats a line of spoken dialogue."""
    print(f"\n  \033[1m{speaker}:\033[0m")
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


def get_choice(options: list[str], prompt: str = "Your choice") -> int:
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
    The player's chosen approach (direct / gentle / professional) affects
    early clue availability and flags.
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
