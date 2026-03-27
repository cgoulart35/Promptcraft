#!/usr/bin/env python3
"""
Minecraft Map Builder — Blueprint Executor
==========================================
Converts a Claude-generated JSON blueprint into a real Minecraft .schem file
importable via WorldEdit (Java Edition).

Usage:
    python3 build.py <blueprint.json> [--output-dir <dir>]

Example:
    python3 build.py castle.json
    python3 build.py tower.json --output-dir ~/minecraft/schematics
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import mcschematic
except ImportError:
    print("❌ Missing dependency: mcschematic")
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
        print(f"❌ Blueprint file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in blueprint: {e}")
        sys.exit(1)

    # Validate required fields
    if "blocks" not in data:
        print("❌ Blueprint missing required 'blocks' array")
        sys.exit(1)

    if not isinstance(data["blocks"], list):
        print("❌ 'blocks' must be an array")
        sys.exit(1)

    return data


def validate_block(block: dict, index: int) -> bool:
    """Validate a single block entry. Returns True if valid."""
    required = ["x", "y", "z", "block"]
    for field in required:
        if field not in block:
            print(f"⚠️  Block #{index} missing field '{field}' — skipping")
            return False

    if not isinstance(block["x"], (int, float)):
        print(f"⚠️  Block #{index}: 'x' must be a number — skipping")
        return False
    if not isinstance(block["y"], (int, float)):
        print(f"⚠️  Block #{index}: 'y' must be a number — skipping")
        return False
    if not isinstance(block["z"], (int, float)):
        print(f"⚠️  Block #{index}: 'z' must be a number — skipping")
        return False
    if not isinstance(block["block"], str):
        print(f"⚠️  Block #{index}: 'block' must be a string — skipping")
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


def build_schematic(blueprint: dict, output_dir: str) -> str:
    """Build the .schem file from a blueprint. Returns the output path."""

    name = blueprint.get("name", "build").replace(" ", "_")
    description = blueprint.get("description", "")
    version_str = blueprint.get("version", DEFAULT_VERSION)
    raw_blocks = blueprint["blocks"]

    # Resolve version
    version = VERSION_MAP.get(version_str)
    if version is None:
        print(f"⚠️  Unknown version '{version_str}', defaulting to {DEFAULT_VERSION}")
        version = VERSION_MAP[DEFAULT_VERSION]

    print(f"\n🏗️  Building: {name}")
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
        print("❌ No valid blocks found in blueprint")
        sys.exit(1)

    # Compute bounds
    bounds = compute_bounds(valid_blocks)
    print(f"\n   Dimensions: {bounds['width']}W × {bounds['height']}H × {bounds['length']}L")
    print(f"   Total blocks: {len(valid_blocks)}")

    # Warn on large builds
    total_volume = bounds["width"] * bounds["height"] * bounds["length"]
    if total_volume > 1_000_000:
        print(f"\n⚠️  Large build detected ({total_volume:,} block volume). This may take a while...")

    # Build the schematic
    schem = mcschematic.MCSchematic()

    start_time = time.time()
    placed = 0
    skipped = 0

    for block in valid_blocks:
        x, y, z = int(block["x"]), int(block["y"]), int(block["z"])
        block_id = block["block"]

        # Skip air explicitly — mcschematic treats unset blocks as air anyway
        if block_id == "minecraft:air":
            skipped += 1
            continue

        try:
            schem.setBlock((x, y, z), block_id)
            placed += 1
        except Exception as e:
            print(f"⚠️  Failed to place {block_id} at ({x},{y},{z}): {e}")
            skipped += 1

        # Progress every 5000 blocks
        if placed % 5000 == 0 and placed > 0:
            elapsed = time.time() - start_time
            print(f"   ⏳ Placed {placed:,} blocks... ({elapsed:.1f}s)")

    elapsed = time.time() - start_time

    # Save the schematic
    os.makedirs(output_dir, exist_ok=True)
    schem.save(output_dir, name, version)
    output_path = os.path.join(output_dir, f"{name}.schem")

    print(f"\n✅ Done in {elapsed:.2f}s")
    print(f"   Blocks placed: {placed:,}")
    if skipped:
        print(f"   Blocks skipped: {skipped}")
    print(f"\n📦 Schematic saved: {output_path}")
    print(f"\n💡 To use in Minecraft:")
    print(f"   1. Copy '{name}.schem' to your WorldEdit schematics folder")
    print(f"      (usually: .minecraft/config/worldedit/schematics/)")
    print(f"   2. In-game: //schem load {name}")
    print(f"   3. Stand where you want the origin, then: //paste")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Claude-generated Minecraft blueprint JSON into a .schem file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 build.py castle.json
  python3 build.py tower.json --output-dir ~/schematics
  python3 build.py village.json --output-dir .

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
    print("  Minecraft Map Builder — Blueprint Executor")
    print("=" * 50)

    blueprint = load_blueprint(args.blueprint)
    build_schematic(blueprint, args.output_dir)


if __name__ == "__main__":
    main()
