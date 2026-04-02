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

# ═══════════════════════════════════════════════════════════════
# Phase 1: Foundation & Floors
# ═══════════════════════════════════════════════════════════════

# Y=0: Stone foundation floor
fill_rect(0, 0, 0, W-1, D-1, "minecraft:stone_bricks")

# Y=5: Interior wooden floor (skip ladder hole at x=1,z=1)
for x in range(1, W - 1):
    for z in range(1, D - 1):
        if not (x == 1 and z == 1):
            add(x, 5, z, "minecraft:oak_planks")

# Y=10: Second interior floor (skip ladder hole at x=1,z=1)
for x in range(1, W - 1):
    for z in range(1, D - 1):
        if not (x == 1 and z == 1):
            add(x, 10, z, "minecraft:spruce_planks")

# ═══════════════════════════════════════════════════════════════
# Phase 2: Walls
# ═══════════════════════════════════════════════════════════════

wall_block = "minecraft:stone_bricks"
accent_block = "minecraft:mossy_stone_bricks"

for y in range(1, H - 3):
    for x in range(W):
        for z in range(D):
            if x == 0 or x == W-1 or z == 0 or z == D-1:
                # Mossy accent: every 4th layer (y % 4) on every 3rd diagonal position ((x+z) % 3)
                b = accent_block if y % 4 == 0 and (x + z) % 3 == 0 else wall_block
                add(x, y, z, b)

# ═══════════════════════════════════════════════════════════════
# Phase 3: Battlements (roof)
# ═══════════════════════════════════════════════════════════════

battlement_y = H - 3  # Y=15

# Battlement floor (solid so players can walk on top)
fill_rect(0, battlement_y, 0, W-1, D-1, "minecraft:stone_bricks")
# Cut ladder exit hole — matches the ladder column at (1,1)
add(1, battlement_y, 1, "minecraft:air")

# Merlons (raised parts) — every other block on the top
# Corners are always solid (merlon or not) to avoid gaps
corners = {(0, 0), (0, D-1), (W-1, 0), (W-1, D-1)}
for y in range(battlement_y + 1, battlement_y + 3):
    for x in range(W):
        for z in range(D):
            on_edge = (x == 0 or x == W-1 or z == 0 or z == D-1)
            is_corner = (x, z) in corners
            is_merlon = (x + z) % 2 == 0
            if on_edge and (is_merlon or is_corner):
                add(x, y, z, "minecraft:stone_bricks")

# ═══════════════════════════════════════════════════════════════
# Phase 4: Openings (doors, windows — air blocks cut through walls)
# ═══════════════════════════════════════════════════════════════

# Doorway: Y=1–2, center of north wall (z=0)
door_x = W // 2  # x=3
add(door_x, 1, 0, "minecraft:air")
add(door_x, 2, 0, "minecraft:air")

# Windows: Y=7 and Y=12 on each wall
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

# ═══════════════════════════════════════════════════════════════
# Phase 5: Door frames & structural details
# ═══════════════════════════════════════════════════════════════

# Door frame stairs
add(door_x - 1, 1, 0, "minecraft:stone_brick_stairs[facing=east,half=bottom]")
add(door_x + 1, 1, 0, "minecraft:stone_brick_stairs[facing=west,half=bottom]")

# Door (facing=south: player enters from outside/north, faces south into the tower)
add(door_x, 1, 0, "minecraft:oak_door[facing=south,half=lower,hinge=left]")
add(door_x, 2, 0, "minecraft:oak_door[facing=south,half=upper,hinge=left]")

# ═══════════════════════════════════════════════════════════════
# Phase 6: Floor holes & ladder column
# ═══════════════════════════════════════════════════════════════

# Ladder column at (x=1, z=1), climbing full tower height
# (Floor holes at x=1,z=1 already skipped in Phase 1)
# facing=north → ladder attached to wall at z=0 (the north wall)
# Extend to battlement_y so player can exit at the top (battlement floor hole cut below)
for ly in range(1, H - 2):
    add(1, ly, 1, "minecraft:ladder[facing=north]")

# ═══════════════════════════════════════════════════════════════
# Phase 7: Furniture (interior details)
# ═══════════════════════════════════════════════════════════════

# Ground floor (Y=1): storage area
add(W-2, 1, D-2, "minecraft:chest[facing=west]")
add(W-2, 1, D-3, "minecraft:barrel")

# First floor (Y=6, on top of oak floor at Y=5): living area
add(W-2, 6, D-2, "minecraft:crafting_table")
add(W-2, 6, 1, "minecraft:furnace[facing=west,lit=false]")

# Second floor (Y=11, on top of spruce floor at Y=10): quarters
add(W-2, 11, D-2, "minecraft:chest[facing=west]")

# ═══════════════════════════════════════════════════════════════
# Phase 8: Lighting (placed late so nothing overwrites them)
# ═══════════════════════════════════════════════════════════════

# Entrance torches (inside, on north wall surface)
# facing=south → torch sticks south into room, attached to north wall (z=0)
add(door_x - 1, 3, 1, "minecraft:wall_torch[facing=south]")
add(door_x + 1, 3, 1, "minecraft:wall_torch[facing=south]")

# Interior wall torches — placed on inner face of walls, facing inward
# facing=south → attached to north wall (z=0), torch at z=1
# facing=north → attached to south wall (z=D-1), torch at z=D-2
wall_torches = [
    # Floor 1 (above Y=5 floor)
    # Note: (1,y,1) is the ladder column — use west wall instead
    (1, 7, 2, "east"), (W-2, 7, 1, "south"),       # west wall / north wall
    (1, 7, D-2, "north"), (W-2, 7, D-2, "north"),   # south wall
    # Floor 2 (above Y=10 floor)
    (1, 12, 2, "east"), (W-2, 12, 1, "south"),
    (1, 12, D-2, "north"), (W-2, 12, D-2, "north"),
]
for tx, ty, tz, facing in wall_torches:
    add(tx, ty, tz, f"minecraft:wall_torch[facing={facing}]")

# Ground floor torch (floor torch on solid foundation)
add(W-2, 1, 1, "minecraft:torch")

# ═══════════════════════════════════════════════════════════════
# Output blueprint
# ═══════════════════════════════════════════════════════════════

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
