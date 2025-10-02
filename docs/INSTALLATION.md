# Installation Guide - Mitsuba 3 Render Studio

## 📋 Prerequisites

- **Python 3.8+** (3.10 or 3.11 recommended)
- **Windows 10/11** (64-bit)
- **Git** (for cloning repository)
- **~500MB free disk space** (for dependencies)

## 🚀 Quick Installation (Recommended)

### Step 1: Run the Setup Script

Simply run the automated setup script:

```powershell
.\setup_environment.ps1
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Verify installation
- ✅ Launch the GUI

### Step 2: Launch the GUI (After Setup)

```powershell
.\launch_gui.ps1
```

That's it! 🎉

---

## 🛠️ Manual Installation (Alternative)

If you prefer manual setup or the automated script doesn't work:

### Step 1: Create Virtual Environment

```powershell
# Navigate to project directory
cd path\to\Mitsuba3-Learning-Demos

# Create virtual environment
python -m venv mitsuba_venv
```

### Step 2: Activate Virtual Environment

```powershell
# Activate the virtual environment
.\mitsuba_venv\Scripts\Activate.ps1
```

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- **mitsuba** (3.0+) - Core rendering engine
- **PyQt6** (6.4+) - GUI framework
- **numpy** (1.20+) - Numerical computing
- **matplotlib** (3.3+) - Plotting
- **Pillow** (8.0+) - Image processing
- **loguru** (0.6+) - Logging

### Step 5: Verify Installation

```powershell
python -c "import mitsuba; import PyQt6; import loguru; print('✅ All dependencies installed!')"
```

### Step 6: Launch GUI

```powershell
python launch_gui.py
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'PyQt6'"

**Solution:**
```powershell
# Activate virtual environment first
.\mitsuba_venv\Scripts\Activate.ps1

# Install PyQt6 specifically
pip install PyQt6>=6.4.0

# Verify
python -c "import PyQt6; print('PyQt6 installed!')"
```

### Issue: "ModuleNotFoundError: No module named 'mitsuba'"

**Solution:**
```powershell
# Install Mitsuba 3
pip install mitsuba

# If that fails, try:
pip install --upgrade mitsuba
```

### Issue: Virtual environment activation fails

**Error:** "Execution policies"

**Solution:**
```powershell
# Allow script execution for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try activating again
.\mitsuba_venv\Scripts\Activate.ps1
```

### Issue: Slow installation

**Solution:** Use faster package resolver:
```powershell
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --prefer-binary
```

### Issue: GUI doesn't launch

**Check:**
1. Virtual environment is activated: `(mitsuba_venv)` should appear in prompt
2. All dependencies installed: Run verification command above
3. Python version: `python --version` (should be 3.8+)

---

## 📦 Dependency Details

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| mitsuba | ≥3.0.0 | Physically-based rendering engine |
| PyQt6 | ≥6.4.0 | GUI framework (dark theme) |
| numpy | ≥1.20.0 | Array operations, math |
| matplotlib | ≥3.3.0 | Optional plotting |
| Pillow | ≥8.0.0 | Image loading/saving |
| loguru | ≥0.6.0 | Beautiful logging |

### System Requirements

- **RAM:** 4GB minimum, 8GB+ recommended
- **CPU:** Multi-core recommended for rendering
- **GPU:** Optional (Mitsuba can use CUDA/OptiX if available)

---

## 🎯 Verification Checklist

After installation, verify everything works:

- [ ] Virtual environment created: `mitsuba_venv/` folder exists
- [ ] Virtual environment activates: `.\mitsuba_venv\Scripts\Activate.ps1`
- [ ] Dependencies installed: `pip list` shows all packages
- [ ] Python imports work: All verification commands pass
- [ ] GUI launches: `python launch_gui.py` opens window
- [ ] Rendering works: Try "Basic Scene" tab

---

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** - Most common issues covered above
2. **Check dependencies:** `pip list | Select-String -Pattern "mitsuba|PyQt6|loguru"`
3. **Reinstall virtual environment:**
   ```powershell
   # Delete old environment
   Remove-Item -Recurse -Force mitsuba_venv
   
   # Create fresh environment
   python -m venv mitsuba_venv
   .\mitsuba_venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. **Check Python version:**
   ```powershell
   python --version  # Should be 3.8+
   ```

---

## 🎓 Next Steps

After successful installation:

1. **Launch GUI:** `.\launch_gui.ps1`
2. **Read User Guide:** See `GUI_USER_GUIDE.md`
3. **Try Examples:** Start with "🔮 Basic Scene" tab
4. **Learn Rendering:** See `gui_examples/README.md`
5. **Experiment:** Adjust parameters and render!

Happy rendering! 🎨✨
