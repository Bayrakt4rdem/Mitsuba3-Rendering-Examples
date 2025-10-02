# File Organization Plan

## New Directory Structure

```
Mitsuba_trials/
├── docs/                          # All documentation
│   ├── gui/                      # GUI-specific documentation
│   │   ├── USER_GUIDE.md        # How to use the GUI
│   │   ├── IMPLEMENTATION_SUMMARY.md
│   │   ├── EXAMPLES_UPDATE_SUMMARY.md
│   │   └── ARCHITECTURE.md      # GUI code architecture
│   ├── examples/                # Example documentation
│   │   ├── GUI_EXAMPLES.md     # GUI examples (lighting, glass, etc.)
│   │   └── CLI_EXAMPLES.md     # Command-line examples
│   ├── INSTALLATION.md          # Installation guide
│   ├── QUICKSTART.md           # Quick start guide
│   ├── LEARNING_ROADMAP.md     # Learning path
│   ├── PROJECT_SUMMARY.md      # Project overview
│   └── STRUCTURE.md            # Code structure
│
├── scripts/                      # All executable scripts
│   ├── setup_environment.ps1   # Automated setup (PowerShell)
│   ├── setup_environment.bat   # Automated setup (Batch)
│   ├── launch_gui.ps1          # GUI launcher
│   ├── run_demo.ps1            # Run all demos
│   └── run_examples.ps1        # Run CLI examples
│
├── gui/                          # GUI source code
├── gui_examples/                # GUI scene generators
├── examples/                    # CLI example scripts
├── assets/                      # Images, icons
├── README.md                    # Main project README
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # License file
├── requirements.txt             # Python dependencies
└── launch_gui.py               # Main GUI entry point
```

## Files to Move

### GUI Documentation → `docs/gui/`
- `GUI_USER_GUIDE.md` → `docs/gui/USER_GUIDE.md`
- `GUI_IMPLEMENTATION_SUMMARY.md` → `docs/gui/IMPLEMENTATION_SUMMARY.md`
- `GUI_EXAMPLES_UPDATE_SUMMARY.md` → `docs/gui/EXAMPLES_UPDATE_SUMMARY.md`
- `gui/README.md` → `docs/gui/ARCHITECTURE.md`

### Example Documentation → `docs/examples/`
- `gui_examples/README.md` → `docs/examples/GUI_EXAMPLES.md`
- `examples/README.md` → `docs/examples/CLI_EXAMPLES.md`

### General Documentation → `docs/`
- `INSTALLATION.md` → `docs/INSTALLATION.md`
- `QUICKSTART.md` → `docs/QUICKSTART.md`

### Scripts → `scripts/`
- `setup_environment.ps1` → `scripts/setup_environment.ps1`
- `setup_environment.bat` → `scripts/setup_environment.bat`
- `launch_gui.ps1` → `scripts/launch_gui.ps1`
- `run_demo.ps1` → `scripts/run_demo.ps1`
- `examples/run_demo.ps1` → `scripts/run_examples.ps1`

## Files to Keep in Root
- `README.md` - Main entry point
- `CONTRIBUTING.md` - For contributors
- `LICENSE` - License file
- `requirements.txt` - Dependencies
- `launch_gui.py` - Main Python entry point
- `.gitignore` - Git configuration

## Benefits

1. **Cleaner Root Directory** - Only essential files visible
2. **Organized Documentation** - Easy to find relevant docs
3. **Centralized Scripts** - All launchers in one place
4. **Better Navigation** - Logical grouping by purpose
5. **Easier Maintenance** - Clear separation of concerns
