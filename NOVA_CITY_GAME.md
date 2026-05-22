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

A living investigation board tracks every clue you discover across the four chapters. Clues link to each other — analyze one and it unlocks others. When you have enough threads, you attempt the **final deduction**: type the name of El-Aqrab to crack the case.

| Clue | What it reveals |
|------|----------------|
| Port Sons Gang Tag | Hand-crafted — points to a person with a craftsman's past |
| Karim's Burner Phone | A contact listed only as "The Commissioner" |
| Warehouse 7 Ledger | Secondary manifests signed with initials *N.H.* |
| Tattoo Removal Record | A scorpion tattoo, removed in 2019, paid in cash |
| Leather Shop Receipt | Custom gloves, ordered by name |
| Phone Tower Records | Calls traced to the 5th floor of the Port Authority building |

### ⚔️ Tactical Turn-Based Combat

Every fight is a decision, not just a dice roll. Available actions:

| Action | Requirement | Effect |
|--------|-------------|--------|
| **Attack** | Always available | Reliable damage |
| **Defend** | Always available | Halve incoming damage this turn |
| **Combat Strike** | Combat Lv.2 | Heavy hit with 20% crit chance |
| **Stealth Strike** | Stealth Lv.2 | Bypasses enemy armor entirely |
| **Intimidate** | Investigation Lv.2 | Applies *Weakened* — reduces enemy attack |
| **Flee** | When allowed | Success scales with Stealth skill |

Enemies carry status effects: *weakened* enemies hit softer, *stunned* enemies lose their next turn.

### 🎭 Branching Dialogue & Story Choices

Every major scene offers meaningful choices with real consequences:

- **Mrs. Mansour scene** — your approach (Direct / Gentle / Professional) changes your starting clues and what she tells you
- **Nova partnership** — three paths ranging from full trust to outright refusal, each affecting the finale
- **Tariq encounter** — reason with him, show him evidence, let Nova lead, or take him down by force
- **Final confrontation** — 2 to 4 options depending on what you've collected and who's on your side

### 📊 RPG Character System

Three skills, each with real mechanical weight:

| Skill | Combat effect | Exploration effect |
|-------|--------------|-------------------|
| **Combat** | +damage, unlocks Combat Strike | — |
| **Stealth** | Unlocks Stealth Strike, better flee | Warehouse infiltration DC 13 |
| **Investigation** | Unlocks Intimidate | Clue analysis rolls, distraction DC 11 |

- Allocate **3 free skill points** at character creation
- Earn XP from victories and deductions — level up to raise max HP
- Skills can improve mid-game through combat outcomes and successful clue analysis

---

## How to Play

### Option 1 — Run Locally

Requires Python 3.9 or higher. No external packages needed.

```bash
# Clone the repository
git clone https://github.com/jlaid4/n8n-mcp.git
cd n8n-mcp

# Run the game
python3 main.py
```

### Option 2 — Online Compiler (Phone / No Setup)

For online compilers like [replit.com](https://replit.com) or [programiz.com](https://www.programiz.com/python-programming/online-compiler/) that cannot import multiple files:

1. Open **`nova_city.py`** in this repository
2. Copy the entire file
3. Paste into any online Python compiler
4. Run — no setup required

### Gameplay Tips

- **Invest in Investigation early** — the evidence board is the core of the game; high Investigation dramatically improves clue analysis rolls
- **Do not skip the evidence board** — clues analyzed in Chapter 2 unlock new clues in Chapter 3
- **The deduction accepts several answers:** `halabi`, `nasser`, `nasser halabi`, `commissioner halabi` all register as correct
- **Combat defeats keep you alive** — you are set to minimum HP and the story continues; the only real endings are in the final confrontation

---

## Chapter Overview

| Chapter | Location | Key Events |
|---------|----------|------------|
| **1 — A Mother's Plea** | Port District apartment → Warehouse Row | Meet Mrs. Mansour, open the case, first combat |
| **2 — The Fixer** | The Anchor Bar → Tariq's apartment | Meet Nova, decide on partnership, interrogate Tariq |
| **3 — Warehouse 7** | Industrial docks | Infiltrate for physical evidence, near-complete deduction |
| **4 — The Scorpion's Lair** | Port Authority Building | Final guard, confront El-Aqrab, multiple resolution paths |

---

## File Structure

```
nova_city.py        ← Single-file version (online compilers / phone)
main.py             ← Game entry point (modular version)
player.py           ← Character: stats, skills, inventory, XP system
story.py            ← Dialogue scenes and branching narrative
combat.py           ← Turn-based combat engine and enemy definitions
investigation.py    ← Evidence Board, clue analysis, deduction puzzle
```

---

## Credits

**Lead Game Designer & Developer:** Omar

Conceived by Romuald Członkowski — [www.aiadvisors.pl/en](https://www.aiadvisors.pl/en)
