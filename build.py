#!/usr/bin/env python3
"""
Minecraft Map Builder -- Blueprint Executor
==========================================
Converts a Claude-generated JSON blueprint into a real Minecraft .schem file
importable via WorldEdit (Java Edition).

Usage:
    python build.py <blueprint.json> [--output-dir <dir>]

Example:
    python build.py castle.json
    python build.py tower.json --output-dir ~/minecraft/schematics

Config:
    Run /promptcraft:setup to create config.json with your schematics_dir.
    build.py will auto-copy the .schem there after every build.
"""

import argparse
import json
import os
import re
import shutil
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")


def load_config() -> dict:
    """Load config.json if it exists. Returns empty dict if not found."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"WARNING: config.json is invalid JSON: {e} -- ignoring config")
        return {}
    except PermissionError:
        print("WARNING: Permission denied reading config.json -- ignoring config")
        return {}
    except OSError as e:
        print(f"WARNING: Could not read config.json: {e} -- ignoring config")
        return {}

try:
    import mcschematic
except ImportError:
    print("ERROR: Missing dependency: mcschematic")
    print("   Run: pip install mcschematic")
    print("   If using a venv, make sure it's activated first.")
    sys.exit(1)

# Map version strings to mcschematic Version enum values
VERSION_MAP = {
    "JE_1_21_1": mcschematic.Version.JE_1_21_1,
    "JE_1_20_1": mcschematic.Version.JE_1_20_1,
    "JE_1_19_2": mcschematic.Version.JE_1_19_2,
    "JE_1_18_2": mcschematic.Version.JE_1_18_2,
}
DEFAULT_VERSION = "JE_1_21_1"


def load_blueprint(path: str) -> dict:
    """Load and validate a blueprint JSON file."""
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Blueprint file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in blueprint: {e}")
        sys.exit(1)

    # Validate required fields
    if "blocks" not in data:
        print("ERROR: Blueprint missing required 'blocks' array")
        sys.exit(1)

    if not isinstance(data["blocks"], list):
        print("ERROR: 'blocks' must be an array")
        sys.exit(1)

    if "name" not in data or not isinstance(data.get("name"), str):
        print("WARNING: Blueprint missing or invalid 'name' field -- will default to 'build'")
    version_str = data.get("version", DEFAULT_VERSION)
    if version_str not in VERSION_MAP:
        print(f"WARNING: Unknown version '{version_str}' in blueprint -- will default to {DEFAULT_VERSION}")

    return data


def validate_block(block: dict, index: int) -> bool:
    """Validate a single block entry. Returns True if valid."""
    required = ["x", "y", "z", "block"]
    for field in required:
        if field not in block:
            print(f"WARNING: Block #{index} missing field '{field}' -- skipping")
            return False

    if not isinstance(block["x"], (int, float)):
        print(f"WARNING: Block #{index}: 'x' must be a number -- skipping")
        return False
    if not isinstance(block["y"], (int, float)):
        print(f"WARNING: Block #{index}: 'y' must be a number -- skipping")
        return False
    if not isinstance(block["z"], (int, float)):
        print(f"WARNING: Block #{index}: 'z' must be a number -- skipping")
        return False
    if not isinstance(block["block"], str):
        print(f"WARNING: Block #{index}: 'block' must be a string -- skipping")
        return False

    # Check for missing minecraft: prefix (common mistake)
    block_id = block["block"].split("[")[0]  # strip state properties
    if ":" not in block_id:
        print(f"WARNING: Block #{index}: '{block['block']}' missing 'minecraft:' prefix -- skipping")
        return False

    return True


def parse_block_state(block_id: str) -> tuple:
    """Parse 'minecraft:foo[key=val,...]' into (base_id, {key: val})."""
    if "[" not in block_id:
        return block_id, {}
    try:
        bracket_open = block_id.index("[")
        bracket_close = block_id.index("]")
        base = block_id[:bracket_open]
        state_str = block_id[bracket_open + 1 : bracket_close]
        props = {}
        for pair in state_str.split(","):
            if "=" not in pair:
                continue
            k, v = pair.split("=", 1)
            props[k.strip()] = v.strip()
        return base, props
    except (ValueError, IndexError):
        # Malformed state string — warn and return raw block_id with no props
        print(f"WARNING: Malformed block state syntax: '{block_id}' -- properties ignored")
        return block_id, {}


def rebuild_block_id(base: str, props: dict) -> str:
    """Reconstruct a block ID string from base name and properties dict."""
    if not props:
        return base
    state = ",".join(f"{k}={v}" for k, v in sorted(props.items()))
    return f"{base}[{state}]"


# Blocks that don't count as solid for support/connectivity purposes
_TRANSPARENT_BLOCKS = {
    "minecraft:air", "minecraft:torch", "minecraft:wall_torch",
    "minecraft:soul_torch", "minecraft:soul_wall_torch",
    "minecraft:ladder", "minecraft:vine", "minecraft:glass_pane",
    "minecraft:iron_bars", "minecraft:chain", "minecraft:flower_pot",
    "minecraft:short_grass", "minecraft:tall_grass", "minecraft:fern",
    "minecraft:dead_bush", "minecraft:snow", "minecraft:moss_carpet",
    "minecraft:lantern", "minecraft:soul_lantern",
    "minecraft:campfire", "minecraft:soul_campfire",
    "minecraft:water", "minecraft:lava",
    # Rails
    "minecraft:rail", "minecraft:powered_rail", "minecraft:detector_rail",
    "minecraft:activator_rail",
    # Redstone components
    "minecraft:redstone_wire", "minecraft:repeater", "minecraft:comparator",
    "minecraft:tripwire", "minecraft:tripwire_hook",
    # Pressure plates and buttons
    "minecraft:stone_pressure_plate", "minecraft:oak_pressure_plate",
    "minecraft:stone_button", "minecraft:oak_button",
    # Crops
    "minecraft:wheat", "minecraft:potatoes", "minecraft:carrots",
    "minecraft:beetroots", "minecraft:nether_wart",
    # Misc non-solid
    "minecraft:end_rod",
}

# Blocks whose connection states (north/south/east/west) must be set explicitly
_CONNECTABLE = {"minecraft:glass_pane", "minecraft:iron_bars"}
_STAINED_GLASS_PANES = {
    "minecraft:white_stained_glass_pane", "minecraft:orange_stained_glass_pane",
    "minecraft:magenta_stained_glass_pane", "minecraft:light_blue_stained_glass_pane",
    "minecraft:yellow_stained_glass_pane", "minecraft:lime_stained_glass_pane",
    "minecraft:pink_stained_glass_pane", "minecraft:gray_stained_glass_pane",
    "minecraft:light_gray_stained_glass_pane", "minecraft:cyan_stained_glass_pane",
    "minecraft:purple_stained_glass_pane", "minecraft:blue_stained_glass_pane",
    "minecraft:brown_stained_glass_pane", "minecraft:green_stained_glass_pane",
    "minecraft:red_stained_glass_pane", "minecraft:black_stained_glass_pane",
}
_ALL_CONNECTABLE = _CONNECTABLE | _STAINED_GLASS_PANES
_CONNECTION_DIRS = {"north", "south", "east", "west"}


def auto_fix_blocks(blocks: list) -> tuple:
    """Auto-fix known schematic issues before building.

    - Injects [persistent=true] on all leaf blocks (prevents in-game decay).
    - Infers connection states for glass panes and iron bars from adjacent blocks.

    Returns (fixed_blocks, list_of_fix_messages).
    """
    # Build position lookup for pane connectivity — solid/opaque blocks only.
    # Transparent and non-solid blocks (torches, rails, etc.) must not cause panes to connect.
    positions = set()
    for b in blocks:
        base, _ = parse_block_state(b["block"])
        if base not in _TRANSPARENT_BLOCKS or base in _ALL_CONNECTABLE:
            positions.add((round(b["x"]), round(b["y"]), round(b["z"])))

    fixed_leaves = 0
    fixed_panes = 0
    new_blocks = []

    for b in blocks:
        block_id = b["block"]
        base, props = parse_block_state(block_id)
        changed = False

        # Leaves: inject persistent=true to prevent in-game decay
        if "_leaves" in base and props.get("persistent") != "true":
            props["persistent"] = "true"
            changed = True
            fixed_leaves += 1

        # Glass panes / iron bars: infer connection states from neighbors
        if base in _ALL_CONNECTABLE:
            if not all(d in props for d in _CONNECTION_DIRS):
                x, y, z = round(b["x"]), round(b["y"]), round(b["z"])
                if "north" not in props: props["north"] = "true" if (x,     y, z - 1) in positions else "false"
                if "south" not in props: props["south"] = "true" if (x,     y, z + 1) in positions else "false"
                if "east"  not in props: props["east"]  = "true" if (x + 1, y, z    ) in positions else "false"
                if "west"  not in props: props["west"]  = "true" if (x - 1, y, z    ) in positions else "false"
                changed = True
                fixed_panes += 1

        new_b = dict(b)
        if changed:
            new_b["block"] = rebuild_block_id(base, props)
        new_blocks.append(new_b)

    fixes = []
    if fixed_leaves:
        fixes.append(f"Auto-fixed {fixed_leaves} leaf block(s): added [persistent=true]")
    if fixed_panes:
        fixes.append(f"Auto-fixed {fixed_panes} glass pane/iron bar block(s): inferred connection states")

    return new_blocks, fixes


def validate_placement(blocks: list) -> list:
    """Check for common placement issues. Returns list of warning strings."""
    # Build a set of all solid block positions for adjacency checks
    occupied = {}  # (x,y,z) -> block_id
    for b in blocks:
        x, y, z = round(b["x"]), round(b["y"]), round(b["z"])
        base, _ = parse_block_state(b["block"])
        occupied[(x, y, z)] = base

    def is_solid(x, y, z):
        bid = occupied.get((x, y, z))
        return (
            bid is not None
            and bid not in _TRANSPARENT_BLOCKS
            and bid not in _STAINED_GLASS_PANES
        )

    warnings = []

    # Wall torch: facing points AWAY from support → support is in the OPPOSITE direction
    # Ladder: facing points TOWARD support → support is in the SAME direction
    facing_same = {
        "north": (0, 0, -1),
        "south": (0, 0, 1),
        "east":  (1, 0, 0),
        "west":  (-1, 0, 0),
    }
    # Wall torches point in `facing` direction and attach to the block behind them.
    # e.g. facing=north → torch points north, support block is at Z+1 (south)
    facing_to_support_offset = {
        "north": (0, 0, 1),
        "south": (0, 0, -1),
        "east":  (-1, 0, 0),
        "west":  (1, 0, 0),
    }

    torches_unsupported = 0
    ladders_unsupported = 0
    doors_unpaired = 0
    doors_no_floor = 0
    beds_unpaired = 0
    panes_no_states = 0

    door_halves = {}  # (x, y_lower, z, base, facing, hinge) -> {y_lower, y_upper}
    bed_parts = {}    # (base, facing) -> {"heads": [(x,y,z)...], "feet": [(x,y,z)...]}

    for b in blocks:
        x, y, z = round(b["x"]), round(b["y"]), round(b["z"])
        base, props = parse_block_state(b["block"])

        # Floor torches need solid block below
        if base in ("minecraft:torch", "minecraft:soul_torch"):
            if not is_solid(x, y - 1, z):
                torches_unsupported += 1

        # Wall torches point in `facing` direction; support block is behind them
        if base in ("minecraft:wall_torch", "minecraft:soul_wall_torch"):
            facing = props.get("facing")
            if facing and facing in facing_to_support_offset:
                dx, dy, dz = facing_to_support_offset[facing]
                if not is_solid(x + dx, y + dy, z + dz):
                    torches_unsupported += 1

        # Ladders: support is in the SAME facing direction
        if base == "minecraft:ladder":
            facing = props.get("facing")
            if facing and facing in facing_same:
                dx, dy, dz = facing_same[facing]
                if not is_solid(x + dx, y + dy, z + dz):
                    ladders_unsupported += 1

        # Track door halves for pairing check
        if base.endswith("_door"):
            half = props.get("half")
            facing = props.get("facing", "?")
            hinge = props.get("hinge", "?")
            # Anchor key to the lower half's Y so two stacked doors don't merge
            y_anchor = y if half == "lower" else y - 1
            key = (x, y_anchor, z, base, facing, hinge)
            if key not in door_halves:
                door_halves[key] = {}
            if half == "lower":
                door_halves[key]["lower"] = y
                if not is_solid(x, y - 1, z):
                    door_halves[key]["no_floor"] = True
            elif half == "upper":
                door_halves[key]["upper"] = y

        # Track bed parts for pairing check — store full (x,y,z) per part
        if base.endswith("_bed"):
            part = props.get("part")
            facing = props.get("facing", "?")
            key = (base, facing)
            if key not in bed_parts:
                bed_parts[key] = {}
            if part == "head":
                bed_parts[key].setdefault("heads", []).append((x, y, z))
            elif part == "foot":
                bed_parts[key].setdefault("feet", []).append((x, y, z))

        # Glass panes / iron bars without connection states render as a cross shape
        if base in _ALL_CONNECTABLE:
            if not all(d in props for d in _CONNECTION_DIRS):
                panes_no_states += 1

    # Check door pairing and floor support
    for key, halves in door_halves.items():
        if "lower" in halves and "upper" not in halves:
            doors_unpaired += 1
        elif "upper" in halves and "lower" not in halves:
            doors_unpaired += 1
        elif "lower" in halves and "upper" in halves:
            if halves["upper"] != halves["lower"] + 1:
                doors_unpaired += 1
        if halves.get("no_floor"):
            doors_no_floor += 1

    # Check bed pairing — each head must have a foot at the correct adjacent offset
    # facing=north: foot at (x, y, z+1); facing=south: foot at (x, y, z-1)
    # facing=east:  foot at (x-1, y, z); facing=west:  foot at (x+1, y, z)
    _bed_foot_offset = {
        "north": (0, 0, 1), "south": (0, 0, -1),
        "east": (-1, 0, 0), "west": (1, 0, 0),
    }
    for (base, facing), parts in bed_parts.items():
        heads = parts.get("heads", [])
        feet = set(parts.get("feet", []))
        offset = _bed_foot_offset.get(facing)
        if offset is None:
            # Unknown facing value — flag all heads as unpaired
            beds_unpaired += len(heads)
            continue
        dx, dy, dz = offset
        for hx, hy, hz in heads:
            expected_foot = (hx + dx, hy + dy, hz + dz)
            if expected_foot not in feet:
                beds_unpaired += 1

    if torches_unsupported:
        warnings.append(f"{torches_unsupported} torch(es) without a support block (will drop as items in-game)")
    if ladders_unsupported:
        warnings.append(f"{ladders_unsupported} ladder(s) not attached to a wall (will drop as items in-game)")
    if doors_unpaired:
        warnings.append(f"{doors_unpaired} door(s) missing their upper or lower half")
    if doors_no_floor:
        warnings.append(f"{doors_no_floor} door(s) with no solid block below (lower half unsupported)")
    if beds_unpaired:
        warnings.append(f"{beds_unpaired} bed(s) missing their head or foot part")
    if panes_no_states:
        warnings.append(f"{panes_no_states} glass pane/iron bar block(s) missing connection states — will render as a cross shape")

    return warnings


def compute_bounds(blocks: list) -> dict:
    """Compute bounding box of all block positions."""
    if not blocks:
        return {"min_x": 0, "max_x": 0, "min_y": 0, "max_y": 0,
                "min_z": 0, "max_z": 0, "width": 1, "height": 1, "length": 1}
    min_x = max_x = round(blocks[0]["x"])
    min_y = max_y = round(blocks[0]["y"])
    min_z = max_z = round(blocks[0]["z"])
    for b in blocks[1:]:
        x = round(b["x"]); y = round(b["y"]); z = round(b["z"])
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y
        if z < min_z: min_z = z
        if z > max_z: max_z = z
    return {
        "min_x": min_x, "max_x": max_x,
        "min_y": min_y, "max_y": max_y,
        "min_z": min_z, "max_z": max_z,
        "width":  max_x - min_x + 1,
        "height": max_y - min_y + 1,
        "length": max_z - min_z + 1,
    }


def build_schematic(blueprint: dict, output_dir: str, config: dict) -> str:
    """Build the .schem file from a blueprint. Returns the output path."""

    name = re.sub(r'[<>:"/\\|?*\s]', "_", str(blueprint.get("name", "build")))
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        name = "build"
    if len(name) > 200:
        name = name[:200]
    description = blueprint.get("description", "")
    version_str = blueprint.get("version", DEFAULT_VERSION)
    raw_blocks = blueprint["blocks"]

    # Resolve version
    version = VERSION_MAP.get(version_str)
    if version is None:
        print(f"WARNING: Unknown version '{version_str}', defaulting to {DEFAULT_VERSION}")
        version = VERSION_MAP.get(DEFAULT_VERSION)
    if version is None:
        print(f"ERROR: Default version '{DEFAULT_VERSION}' not available -- mcschematic library may be outdated")
        print("   Try: pip install --upgrade mcschematic")
        sys.exit(1)

    print(f"\nBuilding: {name}")
    if description:
        print(f"   {description}")
    print(f"   Version: {version_str}")
    print(f"   Raw blocks in blueprint: {len(raw_blocks)}")

    # Validate blocks
    valid_blocks = []
    for i, block in enumerate(raw_blocks):
        if validate_block(block, i):
            valid_blocks.append(block)

    if not valid_blocks:
        print("ERROR: No valid blocks found in blueprint")
        sys.exit(1)

    # Deduplicate coordinates — last placement wins (matches generator placement order)
    deduped = {}
    for block in valid_blocks:
        coord = (round(block["x"]), round(block["y"]), round(block["z"]))
        deduped[coord] = block
    duplicates = len(valid_blocks) - len(deduped)
    if duplicates:
        pct = duplicates / len(valid_blocks) * 100
        msg = f"\n   NOTE: {duplicates} duplicate coordinate(s) removed (last placement kept)"
        if pct > 10:
            msg += f" -- {pct:.0f}% of placements were duplicates, possible generator bug"
        print(msg)
    valid_blocks = list(deduped.values())

    # Auto-fix leaves and pane states before validation and building
    valid_blocks, fixes = auto_fix_blocks(valid_blocks)
    if fixes:
        print(f"\n   Auto-fixes applied:")
        for fix in fixes:
            print(f"   ✓ {fix}")

    # Compute bounds
    bounds = compute_bounds(valid_blocks)
    print(f"\n   Dimensions: {bounds['width']}W x {bounds['height']}H x {bounds['length']}L")
    print(f"   Total blocks: {len(valid_blocks)}")

    # Validate block placement (support checks, pairing checks)
    placement_warnings = validate_placement(valid_blocks)
    if placement_warnings:
        print(f"\n   Placement warnings:")
        for w in placement_warnings:
            print(f"   WARNING: {w}")

    # Hard limit to prevent memory exhaustion
    MAX_PLACED_BLOCKS = 5_000_000
    if len(valid_blocks) > MAX_PLACED_BLOCKS:
        print(f"ERROR: Blueprint has {len(valid_blocks):,} blocks, exceeding the {MAX_PLACED_BLOCKS:,} block limit.")
        print("   Large builds may exhaust memory. Split the structure into smaller sections.")
        sys.exit(1)

    # Warn on large builds
    total_volume = bounds["width"] * bounds["height"] * bounds["length"]
    if total_volume > 1_000_000:
        print(f"\nWARNING: Large bounding box detected ({total_volume:,} blocks). This may take a while...")

    # Build the schematic
    schem = mcschematic.MCSchematic()

    start_time = time.time()
    placed = 0
    skipped = 0
    skipped_ids = {}

    for block in valid_blocks:
        x, y, z = round(block["x"]), round(block["y"]), round(block["z"])
        block_id = block["block"]

        # Skip air explicitly -- mcschematic treats unset blocks as air anyway
        if block_id == "minecraft:air":
            skipped += 1
            continue

        try:
            schem.setBlock((x, y, z), block_id)
            placed += 1
        except Exception as e:
            base_id = block_id.split("[")[0]
            skipped_ids[base_id] = skipped_ids.get(base_id, 0) + 1
            skipped += 1

        # Progress every 5000 blocks
        if placed % 5000 == 0 and placed > 0:
            elapsed = time.time() - start_time
            print(f"   Placed {placed:,} blocks... ({elapsed:.1f}s)")

    elapsed = time.time() - start_time

    # Save the schematic
    os.makedirs(output_dir, exist_ok=True)
    schem.save(output_dir, name, version)
    output_path = os.path.join(output_dir, f"{name}.schem")

    print(f"\nDone in {elapsed:.2f}s")
    print(f"   Blocks placed: {placed:,}")
    if skipped:
        print(f"   Blocks skipped: {skipped}")
        if skipped_ids:
            summary = ", ".join(f"{k}({v})" for k, v in sorted(skipped_ids.items()))
            print(f"   Skipped block types: {summary}")
    print(f"\nSchematic saved: {output_path}")

    # Auto-copy to WorldEdit schematics folder if configured
    schematics_dir = config.get("schematics_dir")
    if schematics_dir:
        schematics_dir = os.path.expandvars(os.path.expanduser(schematics_dir))
        try:
            os.makedirs(schematics_dir, exist_ok=True)
            dest = os.path.join(schematics_dir, f"{name}.schem")
            shutil.copy2(output_path, dest)
            print(f"Auto-copied to WorldEdit: {dest}")
            print(f"\nIn-game:")
            print(f"   //schem load {name}")
            print(f"   //paste -a")
        except PermissionError:
            print(f"WARNING: Permission denied copying to schematics folder: {schematics_dir}")
            print(f"   Manually copy '{name}.schem' to that folder, or check folder permissions.")
        except NotADirectoryError:
            print(f"WARNING: Schematics path exists as a file, not a directory: {schematics_dir}")
            print(f"   Check the schematics_dir setting in config.json.")
        except Exception as e:
            print(f"WARNING: Could not auto-copy to schematics folder: {e}")
            print(f"   Manually copy '{name}.schem' to: {schematics_dir}")
    else:
        print(f"\nTo use in Minecraft:")
        print(f"   1. Copy '{name}.schem' to your WorldEdit schematics folder")
        print(f"      - Singleplayer (Fabric/Forge): .minecraft/config/worldedit/schematics/")
        print(f"      - Multiplayer (Spigot/Paper):  server-root/plugins/WorldEdit/schematics/")
        print(f"      - Prism/other launcher:        <instance>/minecraft/config/worldedit/schematics/")
        print(f"      Tip: set schematics_dir in config.json to auto-copy after every build")
        print(f"   2. In-game: //schem load {name}")
        print(f"   3. //paste -a")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Claude-generated Minecraft blueprint JSON into a .schem file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py castle.json
  python build.py tower.json --output-dir ~/schematics
  python build.py village.json --output-dir .

Blueprint JSON format:
  {
    "name": "my_build",
    "description": "Optional description",
    "version": "JE_1_21_1",
    "blocks": [
      { "x": 0, "y": 0, "z": 0, "block": "minecraft:stone" },
      { "x": 1, "y": 0, "z": 0, "block": "minecraft:oak_planks" }
    ]
  }
        """
    )
    parser.add_argument("blueprint", help="Path to the blueprint JSON file")
    parser.add_argument(
        "--output-dir", "-o",
        default="./output",
        help="Directory to save the .schem file (default: ./output)"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("  Minecraft Map Builder -- Blueprint Executor")
    print("=" * 50)

    config = load_config()
    blueprint = load_blueprint(args.blueprint)
    build_schematic(blueprint, args.output_dir, config)


if __name__ == "__main__":
    main()
