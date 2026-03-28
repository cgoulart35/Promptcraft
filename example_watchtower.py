#!/usr/bin/env python3
"""
Example: Medieval Watchtower Generator
Generates a blueprint JSON for a 7x7 medieval stone watchtower, 18 blocks tall,
with battlements, windows, a wooden floor interior, and a torch-lit entrance.

Run: python example_watchtower.py
Then: python build.py output/watchtower.json
"""

import json
import os

blocks = []

def add(x, y, z, block):
    blocks.append({"x": x, "y": y, "z": z, "block": block})

def fill_rect(x1, y, z1, x2, z2, block):
    """Fill a solid rectangle at height y."""
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            add(x, y, z, block)

def hollow_rect(x1, y, z1, x2, z2, block):
    """Place only the perimeter of a rectangle at height y."""
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            if x == x1 or x == x2 or z == z1 or z == z2:
                add(x, y, z, block)

W = 7  # Width (X)
D = 7  # Depth (Z)
H = 18 # Height

# ─── Y=0: Stone foundation floor ───────────────────────────────
fill_rect(0, 0, 0, W-1, D-1, "minecraft:stone_bricks")

# ─── Y=1–14: Hollow walls ──────────────────────────────────────
wall_block = "minecraft:stone_bricks"
accent_block = "minecraft:mossy_stone_bricks"

for y in range(1, H - 3):
    for x in range(W):
        for z in range(D):
            if x == 0 or x == W-1 or z == 0 or z == D-1:
                # Alternate mossy stones for texture every 3 layers
                b = accent_block if y % 4 == 0 and (x + z) % 3 == 0 else wall_block
                add(x, y, z, b)

# ─── Y=5: Interior wooden floor ────────────────────────────────
for x in range(1, W - 1):
    for z in range(1, D - 1):
        add(x, 5, z, "minecraft:oak_planks")

# ─── Y=10: Second interior floor ───────────────────────────────
for x in range(1, W - 1):
    for z in range(1, D - 1):
        add(x, 10, z, "minecraft:spruce_planks")

# ─── Doorway: Y=1–2, center of north wall (z=0) ────────────────
door_x = W // 2  # x=3
add(door_x, 1, 0, "minecraft:air")
add(door_x, 2, 0, "minecraft:air")
# Door frame
add(door_x - 1, 1, 0, "minecraft:stone_brick_stairs[facing=east,half=bottom]")
add(door_x + 1, 1, 0, "minecraft:stone_brick_stairs[facing=west,half=bottom]")
# Torches flanking the entrance (outside)
add(door_x - 1, 2, 0, "minecraft:torch")
add(door_x + 1, 2, 0, "minecraft:torch")

# ─── Windows: Y=7 and Y=12 on each wall ────────────────────────
window_ys = [7, 12]
for y in window_ys:
    # North wall (z=0): center window
    add(W // 2, y, 0, "minecraft:air")
    # South wall (z=D-1): center window
    add(W // 2, y, D - 1, "minecraft:air")
    # West wall (x=0): center window
    add(0, y, D // 2, "minecraft:air")
    # East wall (x=W-1): center window
    add(W - 1, y, D // 2, "minecraft:air")

# ─── Y=15–17: Battlements ──────────────────────────────────────
battlement_y = H - 3
hollow_rect(0, battlement_y, 0, W-1, D-1, "minecraft:stone_bricks")

# Merlons (raised parts) — every other block on the top
for y in range(battlement_y + 1, battlement_y + 3):
    for x in range(W):
        for z in range(D):
            on_edge = (x == 0 or x == W-1 or z == 0 or z == D-1)
            is_merlon = (x + z) % 2 == 0
            if on_edge and is_merlon:
                add(x, y, z, "minecraft:stone_bricks")

# Corner pillars (always solid)
for y in range(battlement_y, battlement_y + 3):
    for cx, cz in [(0, 0), (0, D-1), (W-1, 0), (W-1, D-1)]:
        add(cx, y, cz, "minecraft:stone_bricks")

# ─── Interior torches on walls ─────────────────────────────────
torch_positions = [
    (1, 6, 1), (W-2, 6, 1), (1, 6, D-2), (W-2, 6, D-2),
    (1, 11, 1), (W-2, 11, 1), (1, 11, D-2), (W-2, 11, D-2),
]
for tx, ty, tz in torch_positions:
    add(tx, ty, tz, "minecraft:torch")

# ─── Ladder on north wall interior (x=1, z=1 to 5) ────────────
for ly in range(1, H - 3):
    add(1, ly, 1, "minecraft:ladder[facing=south]")

# ─── Output blueprint ──────────────────────────────────────────
blueprint = {
    "name": "watchtower",
    "description": f"Medieval stone watchtower -- {W}x{D} base, {H} blocks tall, with battlements, windows, and interior floors",
    "version": "JE_1_21_1",
    "blocks": blocks
}

os.makedirs("output", exist_ok=True)
output_file = "output/watchtower.json"
with open(output_file, "w") as f:
    json.dump(blueprint, f, indent=2)

print(f"Blueprint generated: {output_file}")
print(f"   Total blocks: {len(blocks)}")
print(f"   Dimensions: {W}W x {H}H x {D}D")
print(f"\nNext step: python build.py {output_file}")
