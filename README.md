# MageMaker

**Mage: The Ascension 20th Anniversary Edition Character Creator**

A native GTK4/Adwaita application for Arch Linux to create and manage Mage: The Ascension 20th Anniversary Edition characters.

## Author

**TraydMarkk**

## Features

- **Three-Panel Layout**
  - Left sidebar: Character file browser for saved characters
  - Center panel: Full character editor with all traits
  - Right sidebar: Progress tracker with dot/point counters

- **Three Character Creation Modes**
  - **Creation Mode**: Initial character creation with dot distribution tracking
  - **Freebie Point Mode**: Spend freebie points to customize your character
  - **XP Mode**: Track and spend experience points for character advancement

- **Complete M20 Character Sheet Support**
  - Comprehensive Backgrounds list
  - Merits and Flaws from both M20 core and Book of Secrets
  - Core traits: Arete, Willpower, Quintessence, Paradox
  - Focus elements: Paradigm, Practice, Instruments
  - Full faction support: Traditions, Technocratic Union, Disparates

- **Save/Load System**
  - Characters saved as readable Markdown files with .M20 extension
  - Automatic character discovery in save folder
  - Export to plain text (.txt) for printing

## Requirements

- Arch Linux (or other Linux distribution)
- Python 3.10+
- GTK4
- libadwaita

## Installation

### Install Dependencies (Arch Linux)

```bash
sudo pacman -S python gtk4 libadwaita python-gobject
```

### Run the Application

**Quick launch (from project directory):**
```bash
./launch.sh
```

**Or run directly:**
```bash
cd /path/to/MageMaker
python -m magemaker.gui
```

**Or install as a package:**
```bash
pip install -e .
magemaker
```

## Usage

1. **New Character**: Click "New Character" in the left sidebar
2. **Fill in Details**: Use the center panel to set all character traits
3. **Track Progress**: The right sidebar shows remaining dots/points
4. **Set Priorities**: Assign primary/secondary/tertiary for Attributes and Abilities
5. **Advance Modes**: Click "Advance to Freebie Mode" when creation dots are spent
6. **Save**: Click "Save" to store your character as a .M20 file
7. **Export**: Click "Export TXT" to create a printable text file

## Character Storage

Characters are saved to: `characters/` folder in the directory where MageMaker is run from.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This is a fan-made tool for use with the Mage: The Ascension tabletop roleplaying game. Mage: The Ascension is © Paradox Interactive.


