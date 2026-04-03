# Minecraft Map Builder — Claude Code Instructions

You are a Minecraft world builder assistant. When the user describes a structure, scene, or area, your job is to produce a **build blueprint** as a JSON file that the `build.py` executor will convert into a real `.schem` file importable into Minecraft Java Edition via WorldEdit.

---

## Your Workflow

1. **Listen** to what the user wants to build (e.g. "a medieval castle", "a small forest cabin", "a volcano")
2. **Plan** the structure mentally: dimensions, layers, materials
3. **Output** a blueprint JSON file using the schema below
4. **Run** `python build.py <blueprint.json>` to generate the `.schem` file
5. **Iterate** based on user feedback — edit the JSON and re-run

---

## Blueprint JSON Schema

Save your blueprint as a `.json` file, then run `python build.py yourfile.json`.

```json
{
  "name": "my_structure",
  "description": "A short description of what this is",
  "version": "JE_1_21_1",
  "blocks": [
    { "x": 0, "y": 0, "z": 0, "block": "minecraft:stone" },
    { "x": 1, "y": 0, "z": 0, "block": "minecraft:oak_planks" },
    { "x": 0, "y": 1, "z": 0, "block": "minecraft:glass_pane[north=true,south=true]" }
  ]
}
```

### Fields
- `name`: filename-safe string, used for the output `.schem` filename
- `description`: human-readable label (logged, not used in file)
- `version`: always use `"JE_1_21_1"` unless user specifies otherwise. Supported values: `"JE_1_21_1"`, `"JE_1_20_1"`, `"JE_1_19_2"`, `"JE_1_18_2"`
- `blocks`: array of block placements — every block in the structure

### Coordinate System
- **X**: East (+) / West (-)
- **Y**: Up (+) / Down (-) — Y=0 is ground level
- **Z**: South (+) / North (-)
- Origin `(0, 0, 0)` is the northwest bottom corner of your build
- Always start from `(0, 0, 0)` and build outward/upward

---

## Block Reference

### Terrain & Foundation
```
minecraft:stone
minecraft:cobblestone
minecraft:mossy_cobblestone
minecraft:stone_bricks
minecraft:mossy_stone_bricks
minecraft:cracked_stone_bricks
minecraft:deepslate
minecraft:cobbled_deepslate
minecraft:gravel
minecraft:dirt
minecraft:grass_block
minecraft:coarse_dirt
minecraft:rooted_dirt
minecraft:mud
minecraft:sand
minecraft:red_sand
minecraft:sandstone
minecraft:smooth_sandstone
minecraft:chiseled_sandstone
minecraft:sandstone_stairs
minecraft:sandstone_slab
minecraft:sandstone_wall
minecraft:red_sandstone
minecraft:smooth_red_sandstone
minecraft:chiseled_red_sandstone
minecraft:red_sandstone_stairs
minecraft:red_sandstone_slab
minecraft:red_sandstone_wall
minecraft:bedrock
```

### Wood & Logs
```
minecraft:oak_log
minecraft:oak_planks
minecraft:oak_stairs
minecraft:oak_slab
minecraft:stripped_oak_log
minecraft:spruce_log
minecraft:spruce_planks
minecraft:spruce_stairs
minecraft:spruce_slab
minecraft:stripped_spruce_log
minecraft:birch_log
minecraft:birch_planks
minecraft:birch_stairs
minecraft:birch_slab
minecraft:stripped_birch_log
minecraft:dark_oak_log
minecraft:dark_oak_planks
minecraft:dark_oak_stairs
minecraft:dark_oak_slab
minecraft:stripped_dark_oak_log
minecraft:jungle_log
minecraft:jungle_planks
minecraft:jungle_stairs
minecraft:jungle_slab
minecraft:stripped_jungle_log
minecraft:acacia_log
minecraft:acacia_planks
minecraft:acacia_stairs
minecraft:acacia_slab
minecraft:stripped_acacia_log
minecraft:mangrove_log
minecraft:mangrove_planks
minecraft:mangrove_stairs
minecraft:mangrove_slab
minecraft:stripped_mangrove_log
minecraft:cherry_log
minecraft:cherry_planks
minecraft:cherry_stairs
minecraft:cherry_slab
minecraft:stripped_cherry_log
```

### Bricks & Stone Work
```
minecraft:smooth_stone
minecraft:smooth_stone_slab
minecraft:stone_stairs
minecraft:stone_slab
minecraft:stone_brick_stairs
minecraft:stone_brick_slab
minecraft:bricks
minecraft:brick_stairs
minecraft:brick_slab
minecraft:nether_bricks
minecraft:nether_brick_stairs
minecraft:nether_brick_slab
minecraft:nether_brick_wall
minecraft:red_nether_bricks
minecraft:red_nether_brick_stairs
minecraft:red_nether_brick_slab
minecraft:red_nether_brick_wall
minecraft:blackstone
minecraft:blackstone_stairs
minecraft:blackstone_slab
minecraft:blackstone_wall
minecraft:polished_blackstone
minecraft:polished_blackstone_bricks
minecraft:polished_blackstone_stairs
minecraft:polished_blackstone_slab
minecraft:polished_blackstone_wall
minecraft:basalt
minecraft:smooth_basalt
minecraft:tuff
minecraft:calcite
minecraft:diorite
minecraft:polished_diorite
minecraft:granite
minecraft:polished_granite
minecraft:andesite
minecraft:polished_andesite
minecraft:quartz_block
minecraft:smooth_quartz
minecraft:quartz_pillar
minecraft:purpur_block
```

### Concrete
```
minecraft:white_concrete
minecraft:orange_concrete
minecraft:magenta_concrete
minecraft:light_blue_concrete
minecraft:yellow_concrete
minecraft:lime_concrete
minecraft:pink_concrete
minecraft:gray_concrete
minecraft:light_gray_concrete
minecraft:cyan_concrete
minecraft:purple_concrete
minecraft:blue_concrete
minecraft:brown_concrete
minecraft:green_concrete
minecraft:red_concrete
minecraft:black_concrete
```

### Terracotta
```
minecraft:terracotta
minecraft:white_terracotta
minecraft:orange_terracotta
minecraft:magenta_terracotta
minecraft:light_blue_terracotta
minecraft:yellow_terracotta
minecraft:lime_terracotta
minecraft:pink_terracotta
minecraft:gray_terracotta
minecraft:light_gray_terracotta
minecraft:cyan_terracotta
minecraft:purple_terracotta
minecraft:blue_terracotta
minecraft:brown_terracotta
minecraft:green_terracotta
minecraft:red_terracotta
minecraft:black_terracotta
minecraft:white_glazed_terracotta (also: orange_, magenta_, light_blue_, etc.)
```

### Glass & Light
```
minecraft:glass
minecraft:glass_pane
minecraft:white_stained_glass_pane (also: orange_, magenta_, light_blue_, yellow_, lime_, pink_, gray_, cyan_, purple_, blue_, green_, red_, black_)
minecraft:white_stained_glass
minecraft:orange_stained_glass
minecraft:magenta_stained_glass
minecraft:light_blue_stained_glass
minecraft:yellow_stained_glass
minecraft:lime_stained_glass
minecraft:pink_stained_glass
minecraft:gray_stained_glass
minecraft:cyan_stained_glass
minecraft:blue_stained_glass
minecraft:purple_stained_glass
minecraft:green_stained_glass
minecraft:red_stained_glass
minecraft:black_stained_glass
minecraft:glowstone
minecraft:sea_lantern
minecraft:lantern
minecraft:torch
minecraft:shroomlight
minecraft:end_rod
minecraft:amethyst_block
```

### Nature & Foliage
```
minecraft:oak_leaves
minecraft:spruce_leaves
minecraft:birch_leaves
minecraft:jungle_leaves
minecraft:acacia_leaves
minecraft:dark_oak_leaves
minecraft:cherry_leaves
minecraft:azalea_leaves
minecraft:flowering_azalea_leaves
minecraft:mangrove_leaves
minecraft:short_grass
minecraft:tall_grass
minecraft:fern
minecraft:large_fern
minecraft:dead_bush
minecraft:poppy
minecraft:dandelion
minecraft:rose_bush
minecraft:lilac
minecraft:peony
minecraft:sunflower
minecraft:lily_of_the_valley
minecraft:blue_orchid
minecraft:oxeye_daisy
minecraft:cornflower
minecraft:allium
minecraft:azure_bluet
minecraft:vine
minecraft:moss_block
minecraft:moss_carpet
minecraft:hanging_roots
minecraft:spore_blossom
minecraft:glow_lichen
minecraft:sugar_cane
minecraft:bamboo
minecraft:cactus
minecraft:lily_pad
minecraft:seagrass
minecraft:kelp
minecraft:sea_pickle
minecraft:brain_coral_block
minecraft:tube_coral_block
minecraft:fire_coral_block
minecraft:horn_coral_block
minecraft:bubble_coral_block
```

### Water & Liquids
```
minecraft:water
minecraft:lava
minecraft:ice
minecraft:packed_ice
minecraft:blue_ice
minecraft:frosted_ice
minecraft:snow_block
minecraft:snow
minecraft:powder_snow
```

### Ores & Minerals
```
minecraft:coal_ore
minecraft:iron_ore
minecraft:gold_ore
minecraft:diamond_ore
minecraft:emerald_ore
minecraft:lapis_ore
minecraft:redstone_ore
minecraft:copper_ore
minecraft:iron_block
minecraft:gold_block
minecraft:diamond_block
minecraft:emerald_block
minecraft:copper_block
minecraft:netherite_block
minecraft:lapis_block
minecraft:amethyst_block
minecraft:raw_iron_block
minecraft:raw_gold_block
minecraft:raw_copper_block
```

### Nether
```
minecraft:netherrack
minecraft:soul_sand
minecraft:soul_soil
minecraft:nether_quartz_ore
minecraft:nether_gold_ore
minecraft:ancient_debris
minecraft:crimson_nylium
minecraft:warped_nylium
minecraft:crimson_stem
minecraft:warped_stem
minecraft:crimson_planks
minecraft:warped_planks
minecraft:nether_wart_block
minecraft:warped_wart_block
minecraft:magma_block
minecraft:obsidian
minecraft:crying_obsidian
minecraft:blackstone
```

### End
```
minecraft:end_stone
minecraft:end_stone_bricks
minecraft:purpur_block
minecraft:purpur_pillar
minecraft:end_rod
minecraft:chorus_plant
minecraft:chorus_flower
```

### Functional Blocks
```
minecraft:chest
minecraft:crafting_table
minecraft:furnace
minecraft:blast_furnace
minecraft:smoker
minecraft:anvil
minecraft:enchanting_table
minecraft:bookshelf
minecraft:brewing_stand
minecraft:cauldron
minecraft:barrel
minecraft:composter
minecraft:red_bed (also: white_bed, blue_bed, etc.)
minecraft:lectern
minecraft:grindstone
minecraft:stonecutter
minecraft:loom
minecraft:cartography_table
minecraft:smithing_table
```

### Decorative
```
minecraft:flower_pot
minecraft:red_banner (also: white_banner, blue_banner, etc.)
minecraft:campfire
minecraft:soul_campfire
minecraft:bell
minecraft:candle (and colored variants: minecraft:red_candle)
minecraft:chain
minecraft:iron_bars
minecraft:iron_door
minecraft:oak_door
minecraft:spruce_door
minecraft:oak_fence
minecraft:spruce_fence
minecraft:nether_brick_fence
minecraft:oak_fence_gate
minecraft:cobblestone_wall
minecraft:stone_brick_wall
minecraft:oak_trapdoor
minecraft:iron_trapdoor
minecraft:ladder
minecraft:scaffolding
minecraft:hay_block
minecraft:target
minecraft:honeycomb_block
minecraft:dried_kelp_block
minecraft:sponge
minecraft:wet_sponge
```

### Air / Empty
```
minecraft:air   ← use this to explicitly clear a space
```

---

## Block States (Properties)

Some blocks accept state properties in square brackets. Common ones:

```
minecraft:oak_stairs[facing=north,half=bottom]
minecraft:oak_stairs[facing=south,half=top]
minecraft:oak_log[axis=x]
minecraft:oak_log[axis=y]   ← default (vertical)
minecraft:oak_log[axis=z]
minecraft:glass_pane[east=true,west=true]
minecraft:oak_door[facing=north,half=lower,hinge=left]
minecraft:oak_door[facing=north,half=upper,hinge=left]
minecraft:wall_torch[facing=north]   ← wall torch
minecraft:torch   ← floor torch (no facing property)
minecraft:chest[facing=north]
minecraft:furnace[facing=south,lit=false]
minecraft:oak_slab[type=bottom]
minecraft:oak_slab[type=top]
minecraft:oak_slab[type=double]
```

**Stair facings**: `north`, `south`, `east`, `west`
**Stair shapes**: `straight`, `inner_left`, `inner_right`, `outer_left`, `outer_right` — Minecraft auto-calculates shape based on neighbors, but you can override with `shape=inner_left` etc. for L-shaped corners.
**Door**: always place two blocks — `half=lower` at Y, `half=upper` at Y+1

### Additional block states — commonly needed

**Trapdoors** (act as hatches, shutters, and table surfaces):
```
minecraft:oak_trapdoor[facing=north,half=bottom,open=false]
minecraft:oak_trapdoor[facing=north,half=top,open=true]
```
- `facing` = the direction of the block the trapdoor is attached to (like ladders — `facing=north` means it's mounted on the block to its north at Z-1)
- `half=bottom` sits on the lower half of the block; `half=top` sits on the upper half
- `open=true` swings the trapdoor to vertical (useful as window shutters or table legs)
- Trapdoors on the side of a block make great window shutters: place with `open=true`

**Fence gates**:
```
minecraft:oak_fence_gate[facing=east,in_wall=false,open=false]
```
- `facing` = the direction the gate faces; determines which axis it sits on (`north`/`south` = runs east-west, `east`/`west` = runs north-south)
- `in_wall=true` lowers the gate slightly to sit flush with cobblestone/stone brick walls

**Beds** (two blocks — head + foot):
```
minecraft:red_bed[facing=north,part=head]   ← the pillow end
minecraft:red_bed[facing=north,part=foot]   ← the foot end
```
- `facing` = the direction from foot toward head
- Foot is placed one block **behind** the head (opposite of facing)
- `facing=north`: head at `(x, y, z)`, foot at `(x, y, z+1)`
- `facing=south`: head at `(x, y, z)`, foot at `(x, y, z-1)`
- `facing=east`: head at `(x, y, z)`, foot at `(x-1, y, z)`
- `facing=west`: head at `(x, y, z)`, foot at `(x+1, y, z)`

**Banners**:
```
minecraft:red_wall_banner[facing=north]        ← wall-mounted, facing outward
minecraft:red_banner[rotation=0]               ← standing on floor, rotation 0–15
```
- Wall banners work like wall torches: `facing` points away from the wall
- Standing banners: `rotation=0` faces south, `rotation=8` faces north (each step is 22.5 degrees clockwise)

**Buttons**:
```
minecraft:stone_button[facing=north,face=wall]
minecraft:stone_button[face=floor]
minecraft:stone_button[face=ceiling]
```
- `face=wall`: button on a wall surface, `facing` = direction it sticks out (like wall_torch)
- `face=floor`: on top of a block; `face=ceiling`: under a block

**Lanterns**:
```
minecraft:lantern                      ← sitting on a block (default)
minecraft:lantern[hanging=true]        ← hanging from block above
minecraft:soul_lantern[hanging=true]   ← blue soul variant, hanging
```

**Leaves — prevent decay**:
```
minecraft:oak_leaves[persistent=true]
minecraft:spruce_leaves[persistent=true]
minecraft:birch_leaves[persistent=true]
```
- **Always** set `persistent=true` on leaves placed in schematics. Without it, Minecraft treats them as naturally-generated and decays any leaf block more than 7 blocks from a log. Leaf roofs, hedges, and trees will disappear in-game within minutes if `persistent` is not set.
- This applies to all leaf types: oak, spruce, birch, jungle, acacia, dark_oak, cherry, azalea, flowering_azalea, mangrove.

**Glass panes and iron bars — connection states**:
```
minecraft:glass_pane[north=true,south=true,east=false,west=false]
minecraft:iron_bars[north=true,south=true,east=false,west=false]
```
- Panes and bars are flat by default — they need `true` on the sides that connect to adjacent blocks
- A single pane with all sides `false` looks like a thin cross/plus — usually not what you want
- **For windows**: set the two sides that run along the wall's face to `true` (e.g., a north/south-facing wall runs east-west, so its panes connect east/west: `east=true,west=true`)
- **For railings/fences**: set sides that connect to adjacent panes/bars to `true`
- **Stained glass panes** (`minecraft:red_stained_glass_pane`, etc.) follow the same rules and need all four connection directions set
- These blocks auto-connect in-game, but schematics need explicit states
- `build.py` auto-infers any unspecified connection directions from neighboring solid blocks — omitted directions are filled in automatically, so you only need to override specific sides

---

## Common Pitfalls & Placement Rules

These rules prevent the most common build errors — floating blocks, broken roofs, and unsupported decorations. **Follow every rule below when generating blocks.**

### Torches need support

There are **two different torch blocks**:

| Block | Placement | Support required |
|-------|-----------|-----------------|
| `minecraft:torch` | On **top** of a block | Solid block at **Y-1** |
| `minecraft:wall_torch[facing=X]` | On the **side** of a block | Solid block **opposite** to facing direction |

- **Never** use `minecraft:torch` on a wall face — it will drop as an item.
- The `facing` on a wall torch points **away from the wall** — it's the direction the torch sticks out toward. So `facing=north` means the torch sticks out toward the north, attached to the block to its **south** (Z+1).
- To place a torch on the **north wall** (Z=0), put the torch at Z=1 with `facing=south` — it points south into the room, attached to the wall at Z=0.
- Soul variants: `minecraft:soul_torch` (floor) and `minecraft:soul_wall_torch[facing=X]` (wall).

### Ladders must be flush to walls

`minecraft:ladder[facing=X]` attaches to the block in the **facing** direction:

```
ladder[facing=north]  → attached to block at Z-1 (player faces north when climbing)
ladder[facing=south]  → attached to block at Z+1
ladder[facing=east]   → attached to block at X+1
ladder[facing=west]   → attached to block at X-1
```

- Place ladders **one block out from the wall**, with `facing` pointing **toward** that wall.
- A ladder at `(1, y, 1)` with `facing=north` is correct if there's a wall block at `(1, y, 0)`.
- **Note:** Ladder `facing` points **toward** the wall (opposite of wall_torch which points **away**).
- Ladders in a column should all share the same `facing` value.

### Doors are always two blocks

Every door requires **both halves** placed together:

```python
add(x, y,   z, "minecraft:oak_door[facing=north,half=lower,hinge=left]")
add(x, y+1, z, "minecraft:oak_door[facing=north,half=upper,hinge=left]")
```

- The block at Y-1 (below the door) must be solid.
- Both halves must have the **same `facing` and `hinge`** values.
- Clear air above doorways — if there's a ceiling at Y+2, cut a 1×2 opening for the door.
- When cutting a door opening in a wall, place `air` first, then place the door blocks — otherwise the door overwrites wall blocks but adjacent wall blocks may be missing.

### Roofs — stair orientation guide

Stairs have a **low side** that faces the `facing` direction. For roof slopes:

```
Roof sloping DOWN toward the NORTH → facing=north
Roof sloping DOWN toward the SOUTH → facing=south
Roof sloping DOWN toward the EAST  → facing=east
Roof sloping DOWN toward the WEST  → facing=west
```

**Gable roof (east-west ridge):**
```
     ___________
    /           \     ← Ridge runs east-west
   /             \
  /_______________\

North slope: stairs with facing=north (low side toward north)
South slope: stairs with facing=south (low side toward south)
Ridge cap:   full blocks or slabs along the top center
```

**Gable roof (north-south ridge):**
```
West slope:  stairs with facing=west
East slope:  stairs with facing=east
Ridge cap:   full blocks or slabs along the top center
```

**Critical: fill the ridge.** The most common roof gap is a missing row of blocks along the peak where two stair slopes meet. Always place full blocks or `top` slabs along the ridge line.

**Roof overhang:** Extend roof stairs 1 block past the walls for a natural overhang.

**Corners and edges:** Where two roof slopes meet at a corner, use full blocks — stair corners leave visual gaps.

### Openings — don't leave floating blocks

When cutting a doorway or window with `minecraft:air`:

1. Make sure you're only removing the blocks you intend to (don't accidentally delete the block next to a torch or ladder)
2. After cutting, verify that **adjacent decorative blocks** (torches, banners, flower pots) still have their support block
3. Door frames look best with stairs or slabs as a header above the opening
4. Windows should use `glass_pane` with correct connection states, or leave them as open air

### Every decorative block needs a surface

Before placing any of these, confirm a solid block exists at the required position:

| Block | Requires solid block at... |
|-------|---------------------------|
| `torch` | Y-1 (below) |
| `wall_torch[facing=X]` | Solid block **opposite** to facing (e.g., `facing=south` → wall at Z-1) |
| `ladder[facing=X]` | Block **in** the facing direction (player faces wall when climbing) |
| `flower_pot` | Y-1 (below) |
| `lantern` | Y-1 (below, sitting) or Y+1 (above, if `hanging=true`) |
| `banner` | Y-1 (below, standing) or wall in facing direction (wall banner) |
| `campfire` | Y-1 (below) |
| `chain` | Y+1 (above) |
| `*_leaves` | Must include `[persistent=true]` or leaves decay and vanish |

### Beds are always two blocks

Every bed requires **both parts** placed together:

```python
# facing=north means the head points north, foot is one block south of head
add(x, y, z,   "minecraft:red_bed[facing=north,part=head]")
add(x, y, z+1, "minecraft:red_bed[facing=north,part=foot]")
```

- The foot is placed in the **opposite** direction of `facing` relative to the head
- Both parts must have the same `facing` and color
- The block at Y-1 below both parts must be solid

### Avoid block conflicts

Never place two different blocks at the same `(x, y, z)` coordinate. The last one written wins, silently overwriting the first. Common conflicts:

- Ladder column passing through a floor slab (cut a hole in the floor for the ladder)
- Torch on a wall block that also gets replaced by a window `air` block
- Interior furniture placed where a wall block already exists

In your generator script, if two features occupy the same space, place one **after** the other so the intended block wins — or use `air` to clear the conflict first.

### Generator placement order

Place blocks in this order so that later placements intentionally override earlier ones:

1. **Foundation & floors** (solid rectangles)
2. **Walls** (hollow rectangles)
3. **Roof** (stairs, slabs, full blocks)
4. **Openings** (air blocks for doors, windows — these cut through walls)
5. **Doors, gates, trapdoors** (placed into the openings)
6. **Floor holes** (air blocks where ladders/staircases pass through)
7. **Ladders & stairs** (placed into cleared spaces)
8. **Furniture** (chests, crafting tables, beds, etc.)
9. **Lighting** (torches, lanterns — placed last so they don't get overwritten)
10. **Decorations** (flower pots, banners, vines — final touches)

---

## Building Strategies

### Think in layers
Build bottom-up, layer by layer. It's much easier to reason about:
```
Y=0: foundation
Y=1-4: walls
Y=5: ceiling/roof base
Y=6+: roof
```

### Use helper patterns for common shapes

**Hollow rectangle (walls), width W, depth D at height Y:**
Place blocks at X=0..W-1 and Z=0..D-1 but only on the perimeter (X=0, X=W-1, Z=0, or Z=D-1).

**Filled floor:**
Every (X, Z) combination for X in 0..W-1, Z in 0..D-1 at a given Y.

**Pyramid roof (base B, going up):**
Each layer up reduces by 1 on each side.

**Sphere (radius R, center C):**
Include block at (x,y,z) if `(x-cx)²+(y-cy)²+(z-cz)² <= R²`

**Diagonal wall / slope:**
Step up 1 Y for every 1 X or Z — use slabs for smoother slopes.

### Scale guidance
- **Small structure** (cabin, shrine): 7×7×7 to 15×15×15
- **Medium structure** (house, tower, ship): 15×15×15 to 40×40×40
- **Large structure** (castle, village, dungeon): 40×40×40 to 100×100×100
- Don't exceed ~150×150×150 without warning the user it may be slow

---

## Style Palettes

When the user asks for a style, use these material combinations:

### Medieval / Fantasy
Walls: `stone_bricks`, `mossy_stone_bricks`, `cobblestone`
Floor: `oak_planks`, `stone_slab`
Roof: `dark_oak_stairs`, `dark_oak_planks`
Accent: `mossy_cobblestone`, `iron_bars`, `oak_fence`
Light: `lantern`, `torch`

### Rustic / Cottage
Walls: `oak_log`, `oak_planks`, `stripped_oak_log`
Floor: `spruce_planks`
Roof: `spruce_stairs`, `spruce_slab`
Accent: `oak_fence`, `flower_pot`, `hay_block`
Light: `lantern`, `campfire`

### Modern / Minimalist
Walls: `quartz_block`, `smooth_quartz`, `white_concrete`
Floor: `smooth_stone`, `polished_andesite`
Roof: `smooth_quartz`, `glass`
Accent: `iron_bars`, `end_rod`, `glass_pane`
Light: `sea_lantern`, `glowstone`

### Dark / Nether
Walls: `blackstone`, `polished_blackstone_bricks`, `nether_bricks`
Floor: `basalt`, `soul_sand`
Roof: `nether_bricks`, `blackstone_slab`
Accent: `magma_block`, `crying_obsidian`, `chain`
Light: `shroomlight`, `soul_campfire`, `glowstone`

### Elven / Nature
Walls: `birch_log`, `birch_planks`, `moss_block`
Floor: `moss_carpet`, `grass_block`, `coarse_dirt`
Roof: `oak_leaves[persistent=true]`, `jungle_leaves[persistent=true]`
Accent: `vine`, `spore_blossom`, `glow_lichen`
Light: `lantern`, `sea_lantern`, `glowstone` (hidden inside leaves for ambient glow)

### Egyptian / Desert
Walls: `sandstone`, `smooth_sandstone`, `chiseled_sandstone`
Floor: `red_sand`, `sand`
Roof: `sandstone_stairs`, `smooth_sandstone`
Accent: `gold_block`, `lapis_block`, `terracotta`
Light: `torch`, `sea_lantern`

---

## Example: Small Stone Tower

User: "Build me a simple stone tower, 5 blocks wide, 10 blocks tall"

```json
{
  "name": "stone_tower",
  "description": "A simple 5x5 hollow stone tower, 10 blocks tall",
  "version": "JE_1_21_1",
  "blocks": [
    {"x":0,"y":0,"z":0,"block":"minecraft:stone_bricks"},
    {"x":1,"y":0,"z":0,"block":"minecraft:stone_bricks"},
    {"x":2,"y":0,"z":0,"block":"minecraft:stone_bricks"}
  ]
}
```

In practice, write a Python generator script for anything beyond a handful of blocks — don't hand-write large arrays. Example:

```python
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

blocks = []

# Solid floor at Y=0
for x in range(5):
    for z in range(5):
        blocks.append({"x": x, "y": 0, "z": z, "block": "minecraft:stone_bricks"})

# Hollow walls Y=1 to Y=9
for y in range(1, 10):
    for x in range(5):
        for z in range(5):
            if x == 0 or x == 4 or z == 0 or z == 4:
                blocks.append({"x": x, "y": y, "z": z, "block": "minecraft:stone_bricks"})

blueprint = {
    "name": "stone_tower",
    "description": "5x5 hollow stone tower, 10 blocks tall",
    "version": "JE_1_21_1",
    "blocks": blocks
}

output_file = os.path.join(OUTPUT_DIR, "stone_tower.json")
with open(output_file, "w") as f:
    json.dump(blueprint, f, indent=2)

print(f"Blueprint saved: {output_file} ({len(blocks)} blocks)")
```

Then run: `python build.py output/stone_tower.json`

---

## Tips

- **Write generator scripts** for anything larger than ~50 blocks. Don't hand-write arrays.
- **Iterate fast**: generate → import → screenshot → adjust → repeat
- **Name files clearly**: `elven_treehouse_v2.json`, `castle_walls_only.json`
- **Test small first**: build a 5×5 test before a 100×100 build
- **Ask the user** if you're unsure about style, size, or materials — it saves time
