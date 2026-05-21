"""
investigation.py - Evidence Board puzzle system for Nova City RPG
Players collect clues, analyze them to reveal connections, and
eventually deduce El-Aqrab's true identity.
"""

import random
from typing import Optional


# ── Clue Definition ────────────────────────────────────

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
        self.category = category          # person | location | document | object
        self.connections = connections or []
        self.unlocked = unlocked
        self.analyzed = False

    def __repr__(self):
        if self.analyzed:
            marker = "✓"
        elif self.unlocked:
            marker = "?"
        else:
            marker = "░"
        return f"[{marker}] {self.title}"


# ── Master Clue Database ───────────────────────────────

CLUE_DATABASE: dict[str, Clue] = {
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
CHAPTER_CLUES: dict[int, list[str]] = {
    1: ["c01"],
    2: ["c02", "c03", "c04"],
    3: ["c05", "c06", "c07", "c08"],
    4: ["c09"],
}

# Skill check difficulty per clue
CLUE_DIFFICULTY: dict[str, int] = {
    "c01": 8, "c02": 10, "c03": 12,
    "c04": 10, "c05": 11, "c06": 11,
    "c07": 9,  "c08": 13, "c09": 15,
}


# ── Evidence Board ─────────────────────────────────────

class EvidenceBoard:
    """
    The player's investigation workspace.
    Tracks which clues are discovered, analyzed, and connected.
    """

    def __init__(self, player):
        self.player = player
        # Deep-copy each clue so runtime state is isolated
        self.clues: dict[str, Clue] = {
            cid: Clue(c.id, c.title, c.description, c.category,
                      list(c.connections), c.unlocked)
            for cid, c in CLUE_DATABASE.items()
        }

    def add_clue(self, clue_id: str):
        if clue_id in self.clues:
            self.clues[clue_id].unlocked = True

    def get_unlocked(self) -> list[Clue]:
        return [c for c in self.clues.values() if c.unlocked]

    def get_analyzed(self) -> list[Clue]:
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

        print("\n" + "═" * 58)
        print("  EVIDENCE BOARD — Nova City Investigation")
        print("═" * 58)

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
                            print(f"       ↳ Links to: {', '.join(linked)}")

        evidence_count = self.evidence_count_against_target("c09")
        print(f"\n  Threads pointing to El-Aqrab: {evidence_count}/4")
        print(f"  Undiscovered leads: {locked_count}")

        if self.can_solve():
            print("\n  *** SUFFICIENT EVIDENCE TO MAKE A DEDUCTION ***")

        print("═" * 58)

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
            # Unlock clues this one points toward (but not the final deduction)
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


# ── Investigation Scene ────────────────────────────────

def scene_evidence_collection(player, chapter: int) -> "EvidenceBoard":
    """
    Returns the player's persistent EvidenceBoard, unlocking clues
    that are appropriate for the given chapter.
    """
    if not hasattr(player, "_evidence_board"):
        player._evidence_board = EvidenceBoard(player)

    board: EvidenceBoard = player._evidence_board
    for clue_id in CHAPTER_CLUES.get(chapter, []):
        board.add_clue(clue_id)

    return board


def run_investigation_scene(player, board: EvidenceBoard, chapter: int) -> bool:
    """
    Interactive investigation loop for the given chapter.
    Player can analyze clues, review notes, or attempt the final deduction.
    Returns True if meaningful progress was made this session.
    """
    # Deferred import avoids circular dependency
    from story import print_header, print_narration, get_choice, slow_print

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

        options: list[str] = []
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


# ── Final Deduction Puzzle ─────────────────────────────

def run_deduction_puzzle(player, board: EvidenceBoard) -> bool:
    """
    The climactic deduction: the player must type El-Aqrab's real name.
    Returns True if the answer is correct.
    """
    from story import print_narration, slow_print

    print("\n" + "═" * 58)
    print("  THE DEDUCTION")
    print("═" * 58)

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
