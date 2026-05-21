"""
main.py - Nova City RPG entry point
Runs the game from Chapter 1 through Chapter 4, connecting
player, story, combat, and investigation systems.

Conceived by Romuald Członkowski — www.aiadvisors.pl/en
"""

import os
import sys
import time


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_title():
    banner = r"""
    ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗      ██████╗██╗████████╗██╗   ██╗
    ████╗  ██║██╔═══██╗██║   ██║██╔══██╗    ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝
    ██╔██╗ ██║██║   ██║██║   ██║███████║    ██║     ██║   ██║    ╚████╔╝
    ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║    ██║     ██║   ██║     ╚██╔╝
    ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║    ╚██████╗██║   ██║      ██║
    ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝     ╚═════╝╚═╝   ╚═╝      ╚═╝
    """
    print(banner)
    print("                       A Nova City Investigation")
    print()
    print("      Conceived by Romuald Członkowski — www.aiadvisors.pl/en")
    print()


def show_intro():
    from story import slow_print
    print("─" * 65)
    slow_print("  Nova City. Population: 2.3 million. Port District: forgotten.", 0.028)
    slow_print("  The Port Sons gang controls the docks. No one asks questions.", 0.028)
    slow_print("  El-Aqrab — The Scorpion — is the name no one says out loud.", 0.028)
    slow_print("  Someone has to.", 0.028)
    print("─" * 65)
    time.sleep(0.4)


def show_ending(won: bool, player):
    from story import slow_print
    print("\n" + "═" * 60)
    print("  CASE CLOSED" if won else "  GAME OVER")
    print("═" * 60)
    player.show_status()
    print()

    if won:
        slow_print("  El-Aqrab is behind bars. The Port District breathes again.", 0.028)
        slow_print("  Karim Mansour is home. Eleven other boys too.", 0.028)
        slow_print("  Nova City is a little less rotten than it was yesterday.", 0.028)
    else:
        slow_print("  The Scorpion wins this round.", 0.028)
        slow_print("  But stories like this don't end — they pause.", 0.028)

    print("\n" + "═" * 60)


# ── Character Creation ─────────────────────────────────

def create_character():
    """Handles name input and initial skill point allocation."""
    from player import Player
    from story import slow_print

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
        print(f"  Current — {' | '.join(str(s) for s in player.skills.values())}")
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
    from story import print_header, print_narration, scene_karims_mother
    from combat import run_combat, make_port_grunt
    from investigation import scene_evidence_collection, run_investigation_scene

    print_header("CHAPTER 1 — A MOTHER'S PLEA")

    # Opening dialogue
    scene_karims_mother(player)

    # Initialize the evidence board with chapter-1 clues
    board = scene_evidence_collection(player, chapter=1)

    print_narration("You study the gang tag she gave you. It's a starting point.")
    run_investigation_scene(player, board, chapter=1)

    # First combat: docks patrol
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
    from story import (print_header, print_narration, get_choice,
                       scene_nova_partnership, slow_print)
    from combat import run_combat, make_tariq
    from investigation import scene_evidence_collection, run_investigation_scene

    player.heal(30)

    has_partner = scene_nova_partnership(player)

    board = scene_evidence_collection(player, chapter=2)

    # Tariq encounter
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
        # Force approach triggers combat
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
        # Persuasion approach
        if tariq_choice == 0:
            print_narration("Tariq eyes you for a long moment. Then he sits down. 'What do you want?'")
            player.notes.append("Tariq is frightened of El-Aqrab — willing to talk if he feels safe.")

        elif tariq_choice == 1:
            slow_print("\n  You lay out what you know. Tariq's face goes pale.")
            print_narration("'How did you — fine. I'll tell you what I can. But I'm gone after this.'")

        else:
            # Nova leads
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
    Multiple entry approaches — each with different combat consequences.
    """
    from story import print_header, print_narration, get_choice, slow_print
    from combat import run_combat, make_port_grunt, make_port_lieutenant
    from investigation import scene_evidence_collection, run_investigation_scene

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
    from story import print_header, print_narration, get_choice, scene_final_confrontation
    from combat import run_combat, make_final_guard
    from investigation import scene_evidence_collection, run_deduction_puzzle

    player.heal(50)

    print_header("CHAPTER 4 — THE SCORPION'S LAIR")

    # Last chance to name El-Aqrab if not done yet
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
            # Failsafe: grant identity so the player isn't stuck
            print_narration(
                "The evidence paints one clear picture. "
                "Harbor Commissioner Nasser Halabi. El-Aqrab. You're certain."
            )
            player.set_flag("identity_known", True)
            player.notes.append("EL-AQRAB IDENTIFIED: Harbor Commissioner Nasser Halabi.")

    # Approach the office — guard in the way
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

    # Final confrontation dialogue
    identity_guess = "Nasser Halabi"  # Default — player has confirmed this by now
    if not player.get_flag("identity_known"):
        identity_guess = input("\n  Last chance — who is El-Aqrab? ").strip()

    return scene_final_confrontation(player, identity_guess)


# ── Main ───────────────────────────────────────────────

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
