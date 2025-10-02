# 🚀 Quick Start Guide - Mitsuba 3 Render Studio

## ⚡ First Time Setup (One Command!)| Action | Command |
|--------|---------|  
| **Setup** | `.\scripts\setup_environment.ps1` |
| **Launch GUI** | `.\scripts\launch_gui.ps1` |``powershell
.\setup_environment.ps1
```

**That's it!** This installs everything and launches the GUI.

---

## 🎨 Daily Usage

### Launch GUI
```powershell
.\scripts\launch_gui.ps1
```

### Or Manually
```powershell
# Activate environment
.\mitsuba_venv\Scripts\Activate.ps1

# Launch GUI
python launch_gui.py
```

---

## 🎓 Learning Path

### Beginner (Start Here!)
1. Launch GUI → `.\launch_gui.ps1`
2. Click **"🔮 Basic Scene"** tab
3. Click **"🎨 Render Scene"** button
4. Experiment with parameters!

### Intermediate
5. Try **"💎 Materials Showcase"** - See 5 materials
6. Try **"💡 Lighting Techniques"** - Professional lighting

### Advanced
7. Try **"🔬 Glass & Transparency"** - Caustics!
8. Try **"📦 Cornell Box"** - Global illumination

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'PyQt6'"

**Fix:**
```powershell
.\mitsuba_venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Virtual environment not found"

**Fix:**
```powershell
.\setup_environment.ps1
```

### GUI won't launch

**Fix:**
```powershell
# Delete old environment
Remove-Item -Recurse -Force mitsuba_venv

# Run setup again
.\setup_environment.ps1
```

---

## 📚 More Help

- **Installation Issues:** See `docs/INSTALLATION.md`
- **GUI Usage:** See `docs/gui/USER_GUIDE.md`
- **Learning Examples:** See `docs/examples/GUI_EXAMPLES.md`
- **All Documentation:** See `README.md`

---

## 🎯 Key Commands

| Action | Command |
|--------|---------|
| **Setup** | `.\setup_environment.ps1` |
| **Launch GUI** | `.\launch_gui.ps1` |
| **Activate Env** | `.\mitsuba_venv\Scripts\Activate.ps1` |
| **Install Deps** | `pip install -r requirements.txt` |
| **Verify** | `python -c "import PyQt6; import mitsuba"` |

---

**Happy Rendering!** 🎨✨
