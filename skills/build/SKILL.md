---
name: build
description: Generates a Minecraft structure from a natural language description and outputs a real .schem file, automatically copied to the user's WorldEdit schematics folder. Trigger on any Minecraft building request — "/promptcraft:build a castle", "make me a village", "build a dungeon", etc.
argument-hint: <describe what you want to build>
disable-model-invocation: false
---

# Promptcraft — /promptcraft:build

The user wants to build something in Minecraft. Turn their description into a `.schem` file in their WorldEdit schematics folder, ready to paste in-game.

## What $ARGUMENTS contains

The user's full natural language description — everything after `/promptcraft:build`. Examples:
- `"a medieval castle with a moat, 40x40, dark stone"`
- `"small cozy forest cabin with a fireplace"`
- `"egyptian pyramid, hollow inside, 30 blocks tall"`

---

## Step 1 — Read the block reference

Read `CLAUDE.md` in the project root. It contains the full block vocabulary, coordinate system, style palettes, and building strategies. Do this before planning anything.

---

## Step 2 — Plan the build

Decide:
- **Style** — which palette fits? (Medieval, Rustic, Modern, Nether, Elven, Egyptian — or derive your own)
- **Size** — Small (7–15³), Medium (15–40³), Large (40–100³)
- **Structure** — layers, key features, interior details
- **Materials** — specific blocks for walls, floor, roof, accents, lighting

Tell the user your plan in 2–3 sentences before writing any code.

If the description is vague, ask one clarifying question at most (style, scale, or specific feature), then proceed.

---

## Step 3 — Write a generator script

Always write a Python generator script for anything non-trivial — never hand-write a JSON block array.

**Save the script to `output/<name>_generator.py`.** Always create the output directory first:

```python
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

blocks = []

def fill_rect(x1, y, z1, x2, z2, block):
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            blocks.append({"x": x, "y": y, "z": z, "block": block})

def hollow_rect(x1, y, z1, x2, z2, block):
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            if x == x1 or x == x2 or z == z1 or z == z2:
                blocks.append({"x": x, "y": y, "z": z, "block": block})

def fill_box(x1, y1, z1, x2, y2, z2, block):
    for y in range(y1, y2 + 1):
        fill_rect(x1, y, z1, x2, z2, block)

def hollow_box(x1, y1, z1, x2, y2, z2, block):
    for y in range(y1, y2 + 1):
        hollow_rect(x1, y, z1, x2, z2, block)

def fill_circle(cx, y, cz, radius, block):
    """Fill a solid circle at height y."""
    for x in range(cx - radius, cx + radius + 1):
        for z in range(cz - radius, cz + radius + 1):
            if (x - cx) ** 2 + (z - cz) ** 2 <= radius ** 2:
                blocks.append({"x": x, "y": y, "z": z, "block": block})

def hollow_circle(cx, y, cz, radius, block):
    """Place only the perimeter of a circle at height y."""
    if radius == 0:
        blocks.append({"x": cx, "y": y, "z": cz, "block": block})
        return
    for x in range(cx - radius, cx + radius + 1):
        for z in range(cz - radius, cz + radius + 1):
            dist_sq = (x - cx) ** 2 + (z - cz) ** 2
            if (radius - 1) ** 2 < dist_sq <= radius ** 2:
                blocks.append({"x": x, "y": y, "z": z, "block": block})

def pitched_roof(x1, z1, x2, z2, y_base, block_stair, block_cap):
    """Build a gable roof with ridge running east-west (X axis).
    North slope uses facing=north stairs, south slope uses facing=south.
    Ridge is capped with full blocks."""
    width_z = z2 - z1 + 1
    half = width_z // 2
    for layer in range(half):
        y = y_base + layer
        # North slope
        for x in range(x1, x2 + 1):
            blocks.append({"x": x, "y": y, "z": z1 + layer,
                           "block": f"{block_stair}[facing=north,half=bottom]"})
        # South slope
        for x in range(x1, x2 + 1):
            blocks.append({"x": x, "y": y, "z": z2 - layer,
                           "block": f"{block_stair}[facing=south,half=bottom]"})
    # Ridge cap — fill the center to close the peak
    if width_z % 2 == 1:
        # Odd width: single center row of full blocks
        ridge_z = z1 + half
        for x in range(x1, x2 + 1):
            blocks.append({"x": x, "y": y_base + half, "z": ridge_z, "block": block_cap})
    # Even width: the two innermost stair rows face each other with high sides meeting —
    # they already form a complete peak, no cap block needed.

# ... build logic here ...

blueprint = {
    "name": "<name>",
    "description": "<description>",
    "version": "JE_1_21_1",
    "blocks": blocks
}

output_file = os.path.join(OUTPUT_DIR, "<name>.json")
with open(output_file, "w") as f:
    json.dump(blueprint, f, indent=2)

print(f"Blueprint saved: {output_file} ({len(blocks)} blocks)")
```

---

## Step 4 — Run the generator

```bash
python output/<name>_generator.py
```

Confirm `output/<name>.json` was created and how many blocks it contains.

---

## Step 5 — Run build.py

```bash
python build.py output/<name>.json
```

`build.py` will:
- Validate the blueprint
- Generate the `.schem` → `output/<name>.schem`
- Auto-copy to the user's WorldEdit schematics folder (if `config.json` is set)
- Print the in-game commands

---

## Step 6 — Report back

Tell the user:
- What was built and its dimensions
- That the `.schem` is ready and was copied to their schematics folder
- The in-game commands:
  ```
  //schem load <name>
  //paste -a
  ```
- Offer to iterate: "Want me to adjust anything — size, style, add features?"

---

## Quality bar

- **Interior detail** — not just hollow shells. Add floors, lighting, furniture, ladders.
- **Material variation** — mix mossy/cracked/regular stone, alternate log types, etc.
- **Entrances** — doors need frames, arches, or steps.
- **Lived-in details** — flower pots, torches, barrels, crafting tables.

## Pre-build checklist

Before generating the final blueprint, verify each item:

- [ ] **Roof has no gaps** — ridge line filled with full blocks or top slabs, stair orientations are correct
- [ ] **Every torch has support** — floor torch on solid block below, wall_torch facing away from its wall
- [ ] **Every ladder is flush** — facing points toward a solid wall block
- [ ] **Doors have both halves** — lower + upper with matching facing/hinge
- [ ] **Beds have both parts** — head + foot with correct facing
- [ ] **Windows look right** — glass panes have connection states set (`east=true,west=true` etc.)
- [ ] **Leaves have `persistent=true`** — without it, leaves decay and vanish in-game within minutes
- [ ] **No block conflicts** — ladder holes cut through floors, torches not overwritten by later blocks
- [ ] **Placement order** — foundation → walls → roof → openings → doors → floor holes → ladders → furniture → lighting → decorations
- [ ] **At least 2-3 materials** — no single-material walls; mix in accent blocks
- [ ] **Lighting coverage** — no large dark interior areas; place torches/lanterns every 6-8 blocks

---

## Coordinate reminder

- Origin `(0,0,0)` = northwest bottom corner
- X = East (+), Y = Up (+), Z = South (+)
- Y=0 is ground level — build upward from there
- Always `//paste -a` to strip air and blend into terrain
