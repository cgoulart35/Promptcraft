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

try:
    import mcschematic
except ImportError:
    print("ERROR: Missing dependency: mcschematic")
    print("   Run: pip install mcschematic")
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

    return True


def compute_bounds(blocks: list) -> dict:
    """Compute bounding box of all block positions."""
    xs = [b["x"] for b in blocks]
    ys = [b["y"] for b in blocks]
    zs = [b["z"] for b in blocks]
    return {
        "min_x": min(xs), "max_x": max(xs),
        "min_y": min(ys), "max_y": max(ys),
        "min_z": min(zs), "max_z": max(zs),
        "width":  max(xs) - min(xs) + 1,
        "height": max(ys) - min(ys) + 1,
        "length": max(zs) - min(zs) + 1,
    }


def build_schematic(blueprint: dict, output_dir: str, config: dict) -> str:
    """Build the .schem file from a blueprint. Returns the output path."""

    name = blueprint.get("name", "build").replace(" ", "_")
    description = blueprint.get("description", "")
    version_str = blueprint.get("version", DEFAULT_VERSION)
    raw_blocks = blueprint["blocks"]

    # Resolve version
    version = VERSION_MAP.get(version_str)
    if version is None:
        print(f"WARNING: Unknown version '{version_str}', defaulting to {DEFAULT_VERSION}")
        version = VERSION_MAP[DEFAULT_VERSION]

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

    # Compute bounds
    bounds = compute_bounds(valid_blocks)
    print(f"\n   Dimensions: {bounds['width']}W x {bounds['height']}H x {bounds['length']}L")
    print(f"   Total blocks: {len(valid_blocks)}")

    # Warn on large builds
    total_volume = bounds["width"] * bounds["height"] * bounds["length"]
    if total_volume > 1_000_000:
        print(f"\nWARNING: Large build detected ({total_volume:,} block volume). This may take a while...")

    # Build the schematic
    schem = mcschematic.MCSchematic()

    start_time = time.time()
    placed = 0
    skipped = 0

    for block in valid_blocks:
        x, y, z = int(block["x"]), int(block["y"]), int(block["z"])
        block_id = block["block"]

        # Skip air explicitly -- mcschematic treats unset blocks as air anyway
        if block_id == "minecraft:air":
            skipped += 1
            continue

        try:
            schem.setBlock((x, y, z), block_id)
            placed += 1
        except Exception as e:
            print(f"WARNING: Failed to place {block_id} at ({x},{y},{z}): {e}")
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
