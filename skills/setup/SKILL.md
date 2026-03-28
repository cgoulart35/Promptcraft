---
name: setup
description: Sets up the Promptcraft environment. Installs Python dependencies, creates or updates config.json with the user's WorldEdit schematics path, and validates everything works end to end. Safe to run multiple times — re-running will update your config or repair a broken install.
disable-model-invocation: false
---

# Promptcraft — /promptcraft:setup

Walk the user through setup in order. This skill is idempotent — each step checks the current state before acting, so it's safe to run multiple times.

---

## Step 1 — Check Python version

```bash
python --version
```

Promptcraft requires Python 3.8 or higher. If the version is lower or `python` is not found:
- Tell the user to install Python from https://www.python.org/downloads/
- Stop here until they fix it.

---

## Step 2 — Install dependencies

```bash
python -m pip install mcschematic
```

This is idempotent — pip will skip the install if mcschematic is already up to date.

If pip fails (permissions error), try:
```bash
python -m pip install --user mcschematic
```

---

## Step 3 — Verify the install

```bash
python -c "import mcschematic; print('mcschematic OK')"
```

If this fails, tell the user exactly what went wrong. Common fix: `python -m pip install --upgrade mcschematic`.

---

## Step 4 — Configure the WorldEdit schematics path

Check if `config.json` already exists:

```bash
cat config.json
```

**If config.json exists and has a non-empty `schematics_dir`:**

Tell the user:
```
config.json found. Current schematics path:
  <current path>

Is this still correct? (yes to keep it, or paste a new path to update)
```

Wait for their response. If they confirm, keep it. If they give a new path, update config.json.

**If config.json doesn't exist or `schematics_dir` is empty:**

Tell the user:

```
No WorldEdit schematics path configured yet. Let's set that up.

Your schematics folder depends on your launcher and OS:

  Prism Launcher (Windows):
    C:\Users\YOU\AppData\Roaming\PrismLauncher\instances\<instance>\minecraft\config\worldedit\schematics

  Vanilla Minecraft (Windows):
    C:\Users\YOU\AppData\Roaming\.minecraft\config\worldedit\schematics

  Vanilla Minecraft (Mac):
    ~/Library/Application Support/minecraft/config/worldedit/schematics

  Vanilla Minecraft (Linux):
    ~/.minecraft/config/worldedit/schematics

  Spigot / Paper server:
    /path/to/server/plugins/WorldEdit/schematics

Not sure where yours is? See the WorldEdit docs:
  https://worldedit.enginehub.org/en/latest/usage/files/#schematics

What is your WorldEdit schematics folder path?
```

Wait for the user's answer, then write `config.json`:

```json
{
  "schematics_dir": "<their path>"
}
```

---

## Step 5 — Validate the schematics path

Check that the path exists:

```bash
# Windows
dir "<schematics_dir>"

# Mac / Linux
ls "<schematics_dir>"
```

If it doesn't exist, tell the user:

```
That folder doesn't exist yet. WorldEdit creates it automatically the first time
you save a schematic in-game. Either:
  - Load Minecraft once and let WorldEdit create it, then re-run /promptcraft:setup
  - Or create it manually now

Promptcraft will still work — it creates the folder if missing — but confirm
the path is correct before continuing.
```

Ask the user if they want to continue anyway or fix the path first.

---

## Step 6 — Run a test build

Run the included demo to confirm everything works end to end:

```bash
python example_watchtower.py
python build.py output/watchtower.json
```

Confirm:
- `output/watchtower.json` was generated
- `output/watchtower.schem` was created
- The `.schem` was auto-copied to the user's schematics folder (if config is set)

If anything fails, diagnose and fix it before continuing.

---

## Step 7 — Done

Tell the user:

```
✅ Promptcraft is ready!

Setup summary:
  Python:            <version>
  mcschematic:       installed
  WorldEdit folder:  <schematics_dir>
  Test build:        output/watchtower.schem ✓

To build something, run:
  /promptcraft:build <describe what you want>

Examples:
  /promptcraft:build a small medieval watchtower with battlements
  /promptcraft:build a cozy forest cabin with a fireplace inside
  /promptcraft:build an Egyptian pyramid, hollow, 30 blocks tall

Then in Minecraft:
  //schem load <name>
  //paste -a
```
