# Nova City RPG 🏙️⚓

> *"El-Aqrab — The Scorpion — is the name no one says out loud. Someone has to."*

A gritty, text-based detective RPG set in the criminal underworld of Nova City's forgotten Port District. Four chapters. Branching choices. A mystery that runs deeper than a missing teenager.

---

## The Story

Karim Mansour is seventeen years old and has been missing for three days.

His mother comes to you with nothing but a crumpled gang tag — a scorpion, hand-stamped in black ink — and the name everyone in the Port District whispers but never says aloud: **El-Aqrab**. The Scorpion. The man who rebuilt the **Port Sons** gang from a street crew into a shadow empire that controls every shipment, every dock worker, and every official who looks the other way.

Karim is not the first boy to disappear. He will not be the last — unless you stop it.

Your investigation pulls you into a web of smuggled manifests, encrypted phones, and a city where the most dangerous criminals wear the cleanest suits. Along the way you cross paths with **Nova**, a sharp-edged investigator who has been hunting El-Aqrab for six months and lost an informant to him. She has leads you don't. You have angles she hasn't tried. The question is whether you can trust each other long enough to finish this.

El-Aqrab's real identity is unknown — even to most of his own gang. Somewhere in the evidence you collect is the answer. You'll have to find it before he finds you.

---

## Key Features

### 🗂️ Evidence Board & Investigation Puzzles
A living investigation board tracks every clue you discover across the four chapters. Clues link to each other — analyze one and it unlocks others. When you have enough threads, you can attempt the **final deduction**: type the name of El-Aqrab to crack the case. Get it wrong and you go back to the board.

| Clue | What it reveals |
|------|----------------|
| Port Sons Gang Tag | Hand-crafted — points to a person with a craftsman's past |
| Karim's Burner Phone | A contact listed only as "The Commissioner" |
| Warehouse 7 Ledger | Secondary manifests signed with initials *N.H.* |
| Tattoo Removal Record | A scorpion tattoo, removed in 2019, paid in cash |
| Leather Shop Receipt | Custom gloves, ordered by name |
| ...and more | Each unlocked by successful Investigation checks |

### ⚔️ Tactical Turn-Based Combat
Every fight is a decision, not a dice roll. Choose from:
- **Attack** — reliable damage
- **Defend** — halve incoming damage for one turn
- **Combat Strike** — heavy hit with crit chance (unlocked at Combat Lv.2)
- **Stealth Strike** — bypasses enemy armor entirely (unlocked at Stealth Lv.2)
- **Intimidate** — applies *Weakened* status, reducing enemy attack (unlocked at Investigation Lv.2)
- **Flee** — success chance scales with your Stealth skill

Enemies have their own status system. A *weakened* enemy hits softer; a *stunned* one loses their next turn. Use the environment.

### 🎭 Branching Dialogue & Story Choices
Every major scene has meaningful choices that change what information you get, which items you carry into later chapters, and how characters respond to you.

- How you approach Mrs. Mansour changes your early clue set
- Whether you partner with Nova (and how much she trusts you) changes your options in the finale
- How you handle Tariq — reason, evidence, or force — has different consequences
- The final confrontation has 2–4 options depending on your inventory and flags

### 📊 RPG Character System
| Stat | Effect |
|------|--------|
| **Combat** | Bonus damage, unlocks Combat Strike at Lv.2 |
| **Stealth** | Better flee chance, unlocks Stealth Strike at Lv.2, helps Warehouse infiltration |
| **Investigation** | Better skill checks on clues, unlocks Intimidate at Lv.2, helps evidence analysis |

- Start with **3 free skill points** to build your detective
- Earn XP from combat victories and successful deductions
- Skills can improve mid-game through combat and investigation successes
- Level up to increase max HP

---

## How to Play

### Option 1 — Run Locally (Recommended)

Requires Python 3.9 or higher. No external packages needed.

```bash
# Clone the repository
git clone https://github.com/jlaid4/n8n-mcp.git
cd n8n-mcp

# Run the modular version
python3 main.py
```

### Option 2 — Single File (Online Compiler / Phone)

For online compilers (replit.com, programiz.com, etc.) that cannot import multiple files:

1. Open `nova_city.py` in this repository
2. Copy the entire file
3. Paste it into any online Python compiler
4. Run it — no setup required

### Gameplay Tips

- **Invest in Investigation early** — the evidence board is the heart of the game and high Investigation skill dramatically improves your clue analysis success rate
- **Don't skip the evidence board** — clues you analyze in Chapter 2 unlock new clues in Chapter 3
- **The deduction answer** accepts several forms: `halabi`, `nasser`, `nasser halabi`, `commissioner halabi` all work
- **You cannot truly lose** — even a combat defeat keeps you at minimum HP and the story continues. The only real endings are in the final confrontation

---

## Chapter Overview

| Chapter | Location | What Happens |
|---------|----------|-------------|
| **1 — A Mother's Plea** | Port District apartment → Warehouse Row docks | Meet Mrs. Mansour, receive the case, first combat encounter |
| **2 — The Fixer** | The Anchor Bar → Tariq's apartment | Meet Nova, decide on partnership, interrogate Tariq |
| **3 — Warehouse 7** | Industrial docks | Infiltrate the warehouse, gather physical evidence, near-complete deduction |
| **4 — The Scorpion's Lair** | Port Authority Building | Final guard encounter, confront El-Aqrab, multiple resolution paths |

---

## File Structure

```
nova_city.py        ← Single-file version (for online compilers)
main.py             ← Game entry point (modular version)
player.py           ← Character class: stats, skills, inventory, XP
story.py            ← Dialogue scenes and branching narrative
combat.py           ← Turn-based combat engine and enemy definitions
investigation.py    ← Evidence Board, clue analysis, deduction puzzle
```

---

## Credits

**Lead Game Designer & Developer:** Omar

Conceived by Romuald Członkowski — [www.aiadvisors.pl/en](https://www.aiadvisors.pl/en)
