# ⛏️ Promptcraft

**Describe it. Build it.**

A Claude Code plugin that turns natural language into real Minecraft worlds. Tell Claude what you want to build — a medieval castle, a jungle temple, an underwater city — and get a `.schem` file pasted directly into your WorldEdit schematics folder.

> Built for [Claude Code](https://claude.ai/code) · Outputs WorldEdit-compatible `.schem` files · Java Edition

---

## How It Works

```
You:          /promptcraft:build a dark fantasy castle with a moat, nether brick, 40x40
                          ↓
Claude Code:  Plans the structure, writes a generator script, runs it
                          ↓
              Runs build.py → outputs castle.schem → copies to your schematics folder
                          ↓
You:          //schem load castle   then   //paste -a
```

No GUI. No web app. Just Claude Code, your terminal, and Minecraft.

---

<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <img src="https://github.com/user-attachments/assets/e2be3fd6-4c4e-4eb3-9a22-f8824b15b4db" style="width: 32%;" />
  <img src="https://github.com/user-attachments/assets/7a368419-86e1-4853-9061-13a7bce62540" style="width: 32%;" />
  <img src="https://github.com/user-attachments/assets/66cdcf01-b5a5-42bf-9d7d-15dd2e8d3b9b" style="width: 32%;" />
</div>

---

## Requirements

- [Claude Code](https://claude.ai/code) installed
- Python 3.8+
- Minecraft Java Edition with [WorldEdit](https://enginehub.org/worldedit/) mod installed

> `mcschematic` (the Python library that writes `.schem` files) is installed automatically by `/promptcraft:setup`.

---

## Installation

### 1. Add the Promptcraft marketplace

In Claude Code, add this repository as a marketplace:

```
/plugin marketplace add cgoulart35/Promptcraft
```

### 2. Install the plugin

```
/plugin install promptcraft@promptcraft
```

### 3. Run first-time setup

```
/promptcraft:setup
```

Setup will:
- Verify Python 3.8+ is available
- Install the `mcschematic` dependency
- Ask for your WorldEdit schematics folder path and write `config.json`
- Run a test build to confirm everything works end to end

You can re-run `/promptcraft:setup` at any time to update your config or fix a broken install.

---

## Usage

Once setup is complete, describe what you want to build:

```
/promptcraft:build a rustic forest cabin, spruce wood, fireplace inside
/promptcraft:build an Egyptian pyramid, sandstone, hollow, 30 blocks tall
/promptcraft:build a nether fortress outpost with a lava moat
/promptcraft:build a floating sky island with a small house and waterfalls
```

Claude will:
1. Plan the structure (style, dimensions, materials)
2. Write and run a Python generator script → `output/<name>.json`
3. Run `build.py` → `output/<name>.schem`
4. Auto-copy the `.schem` to your WorldEdit schematics folder

Then in Minecraft:

```
//schem load <name>
//paste -a
```

(`-a` strips air blocks so the structure blends into your terrain)

---

## Example Prompts

```
"A medieval stone keep, 20x20, inner courtyard, torches and battlements"
"A rustic forest cabin, spruce wood, cozy interior with a fireplace"
"An Egyptian pyramid, sandstone, 30 blocks tall, hollow interior"
"A floating sky island with a small house on top and waterfalls"
"A nether fortress outpost, blackstone and nether brick, lava moat"
"A modern glass-and-quartz office building, 20x20, 15 floors"
"A ruined stone temple overgrown with vines and moss"
```

---

## Try the Demo

A working watchtower example is included:

```bash
python example_watchtower.py        # generates output/watchtower.json
python build.py output/watchtower.json   # outputs output/watchtower.schem
```

---

## Project Structure

```
Promptcraft/
├── .claude-plugin/
│   ├── marketplace.json        ← Marketplace metadata
│   └── plugin.json             ← Plugin manifest
├── .github/
│   └── FUNDING.yml             ← Sponsorship links
├── skills/
│   ├── build/SKILL.md          ← /promptcraft:build <description>
│   └── setup/SKILL.md          ← /promptcraft:setup
├── CLAUDE.md                   ← Teaches Claude Minecraft's block vocabulary and building strategies
├── build.py                    ← Executor: JSON blueprint → .schem file
├── example_watchtower.py       ← Demo generator
├── config.json                 ← Your local WorldEdit path (gitignored, created by /setup)
├── requirements.txt            ← mcschematic
└── output/                     ← All generated files land here (gitignored)
```

---

## Style Palettes

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

- [ ] Terrain generation (hills, rivers, cliffs under structures)
- [ ] Biome-aware builds (auto-match surrounding biome)
- [ ] Interior furnishing (chests, crafting tables, beds placed contextually)
- [ ] Village generation (multiple buildings + connecting paths)
- [ ] Dungeon generation with loot tables
- [ ] Bedrock Edition support

---

## Contributing

PRs welcome. If you build something cool with Promptcraft, open an issue and show it off.

---

## License

All rights reserved. This project is not currently licensed for redistribution or commercial use.

---

*Built with [Claude Code](https://claude.ai/code) · [promptcraft.dev](https://promptcraft.dev) · [@promptcraft](https://x.com/promptcraft)*
