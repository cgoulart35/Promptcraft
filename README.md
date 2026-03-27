# ⛏️ Promptcraft

**Describe it. Build it.**

A Claude Code plugin that turns natural language into real Minecraft worlds. Tell Claude what you want to build — a medieval castle, a jungle temple, an underwater city — and get a `.schem` file you can paste directly into Minecraft.

> Built for [Claude Code](https://claude.ai/code) · Outputs WorldEdit-compatible `.schem` files · Java Edition 1.21.1

---

## How It Works

Promptcraft gives Claude Code a complete Minecraft building vocabulary — blocks, palettes, coordinate systems, and building strategies — so it can reason about 3D space and generate real structures.

```
You: "Build me a dark fantasy castle with a moat, 40x40, nether brick walls"
         ↓
Claude Code reads CLAUDE.md, plans the structure layer by layer
         ↓
Writes a Python generator → runs build.py → outputs castle.schem
         ↓
You paste it into Minecraft with WorldEdit
```

No GUI. No web app. Just Claude Code, your terminal, and Minecraft.

---

## Requirements

- [Claude Code](https://claude.ai/code) installed and running
- Python 3.8+
- `mcschematic` Python library
- Minecraft Java Edition with [WorldEdit](https://enginehub.org/worldedit/) mod

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/Promptcraft.git
cd Promptcraft

# 2. Install the Python dependency
pip install mcschematic

# 3. Open Claude Code in this folder
claude
```

That's it. Claude will automatically read `CLAUDE.md` on startup and know how to build Minecraft structures.

---

## Usage

Once Claude Code is running in the Promptcraft folder, just describe what you want:

```
> Build me a small medieval watchtower, stone brick, 7x7 base, 18 blocks tall
  with battlements and interior floors
```

Claude will:
1. Plan the structure and write a generator script
2. Run `python3 build.py yourstructure.json`
3. Save a `.schem` file to `./output/`

Then in Minecraft:
```
# Copy the .schem to your WorldEdit schematics folder:
# .minecraft/config/worldedit/schematics/

//schem load watchtower
//paste
```

---

## Example Prompts

```
"A rustic forest cabin, spruce wood, cozy interior with a fireplace"
"An Egyptian pyramid, sandstone, 30 blocks tall, hollow interior with traps"
"A floating sky island with a small house on top and waterfalls"
"A nether fortress outpost, blackstone and nether brick, lava moat"
"A modern glass-and-quartz office building, 20x20, 15 floors"
"An underwater coral reef village with dome buildings"
"A ruined stone temple overgrown with vines and moss"
```

---

## Try the Demo

A working example is included — a full medieval watchtower:

```bash
python3 example_watchtower.py   # generates watchtower.json
python3 build.py watchtower.json  # outputs ./output/watchtower.schem
```

---

## Project Structure

```
Promptcraft/
├── CLAUDE.md               ← The brain: teaches Claude how to build in Minecraft
├── build.py                ← Executor: JSON blueprint → .schem file
├── example_watchtower.py   ← Demo generator
└── output/                 ← Generated .schem files go here
```

---

## Style Palettes

Promptcraft ships with 6 built-in style palettes Claude can use:

| Style | Vibe | Key Materials |
|---|---|---|
| **Medieval** | Stone keeps, castles | Stone bricks, mossy cobblestone, dark oak |
| **Rustic** | Cozy cabins, farms | Oak logs, spruce planks, hay bales |
| **Modern** | Glass towers, minimal | Quartz, smooth stone, glass panes |
| **Dark / Nether** | Fortresses, dungeons | Blackstone, nether brick, magma |
| **Elven** | Nature, treehouses | Birch, moss, flowering azalea |
| **Egyptian** | Deserts, pyramids | Sandstone, gold, terracotta |

Or just describe your own — Claude will figure out the materials.

---

## Roadmap

- [ ] Terrain generation (hills, rivers, cliffs)
- [ ] Biome-aware builds (auto-match surrounding biome)
- [ ] Interior furnishing (chests, crafting tables, beds placed contextually)
- [ ] Village generation (multiple buildings + paths)
- [ ] Dungeon generation with loot tables
- [ ] Bedrock Edition support

---

## Contributing

PRs welcome. If you build something cool with Promptcraft, open an issue and show it off — we'd love to feature community builds.

---

## License

MIT — build whatever you want with it.

---

*Built with [Claude Code](https://claude.ai/code) · [promptcraft.dev](https://promptcraft.dev) · [@promptcraft](https://x.com/promptcraft)*
