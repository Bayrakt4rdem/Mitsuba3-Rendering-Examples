# Mitsuba 3 Demo Examples

This directory contains all the demo Python files for learning Mitsuba 3.

## 🎯 Examples Overview

### 00_quick_start.py ⚡
**Difficulty:** Setup  
**Time:** 5 minutes  
**Purpose:** Verify installation and ensure everything works

Checks all dependencies and renders a simple test scene. **Run this first!**

```powershell
python examples/00_quick_start.py
```

---

### 01_basic_scene.py 🎈
**Difficulty:** Beginner  
**Time:** 15 minutes  
**Purpose:** Learn fundamental concepts

Your first real render! Creates a simple scene with a red sphere, ground plane, and point light.

**Key Concepts:**
- Scene structure
- Basic shapes (sphere, rectangle)
- Materials (BSDF)
- Camera setup with look_at()
- Simple lighting

```powershell
python examples/01_basic_scene.py
```

---

### 02_materials_showcase.py 🎨
**Difficulty:** Intermediate  
**Time:** 30 minutes  
**Purpose:** Explore different material types

Renders 5 spheres with different materials side-by-side for comparison.

**Materials Covered:**
1. Diffuse (matte red)
2. Conductor (smooth gold)
3. RoughConductor (rough copper)
4. Dielectric (clear glass)
5. Plastic (blue plastic)

```powershell
python examples/02_materials_showcase.py
```

---

### 03_lighting_techniques.py 💡
**Difficulty:** Intermediate  
**Time:** 45 minutes  
**Purpose:** Master lighting setups

Compares 6 different lighting configurations to show their effects.

**Lighting Types:**
1. Point light (hard shadows)
2. Area light (soft shadows)
3. Directional light (sun-like)
4. Three-point lighting (professional)
5. Environment lighting (sky dome)
6. Colored lights (artistic)

```powershell
python examples/03_lighting_techniques.py
```

---

### 04_advanced_scene.py 🏆
**Difficulty:** Advanced  
**Time:** 60 minutes  
**Purpose:** Combine all techniques

A complex scene with multiple objects, materials, and professional lighting setup.

**Features:**
- 5 different material spheres
- Multiple walls with colors
- Three-point + ambient lighting
- High-quality render settings
- Professional composition

```powershell
python examples/04_advanced_scene.py
```

---

### 05_cornell_box.py 📦
**Difficulty:** Intermediate  
**Time:** 45 minutes  
**Purpose:** Understand global illumination

The famous Cornell Box - a classic computer graphics benchmark scene.

**Demonstrates:**
- Global illumination
- Color bleeding (red/green walls)
- Indirect lighting
- Soft shadows from area light
- Light transport simulation

```powershell
python examples/05_cornell_box.py
```

---

## 🚀 Running the Examples

### Prerequisites

1. **Activate virtual environment:**
   ```powershell
   .\mitsuba_venv\Scripts\Activate.ps1
   ```

2. **Install dependencies (if not already done):**
   ```powershell
   pip install -r requirements.txt
   ```

### Run Individual Examples

```powershell
# From project root
python examples/00_quick_start.py
python examples/01_basic_scene.py
# etc...
```

### Using the Launcher Script

```powershell
# Interactive menu
.\run_demo.ps1
```

## 📊 Render Times & Quality

| Example | Resolution | SPP | Render Time* |
|---------|-----------|-----|--------------|
| Quick Start | 256×256 | 16 | ~5s |
| Basic Scene | 512×512 | 64 | ~10s |
| Materials | 800×400 | 128 | ~60s |
| Lighting | 600×600 | 64 | ~30s each |
| Advanced | 1024×768 | 256 | ~2-5min |
| Cornell Box | 512×512 | 256 | ~1-2min |

*Approximate times on modern CPU. Your results may vary.

## 🎓 Learning Path

### Recommended Order

1. **Start here:** `00_quick_start.py` - Verify setup
2. **Basics:** `01_basic_scene.py` - Learn fundamentals
3. **Materials:** `02_materials_showcase.py` - Explore surfaces
4. **Cornell Box:** `05_cornell_box.py` - See global illumination
5. **Lighting:** `03_lighting_techniques.py` - Master lights
6. **Advanced:** `04_advanced_scene.py` - Put it all together

### Alternative Path (Faster)

1. `00_quick_start.py` - Setup
2. `01_basic_scene.py` - Basics
3. `05_cornell_box.py` - Key concepts
4. Experiment on your own!

## 🔧 Customization Tips

### Quick Experiments

All examples are designed to be modified! Try:

**Change Colors:**
```python
'reflectance': {'type': 'rgb', 'value': [0.8, 0.1, 0.1]}  # Red
'reflectance': {'type': 'rgb', 'value': [0.1, 0.1, 0.8]}  # Blue
```

**Move Camera:**
```python
'to_world': mi.ScalarTransform4f.look_at(
    origin=[5, 5, 10],  # Try different positions
    target=[0, 0, 0],
    up=[0, 1, 0]
)
```

**Adjust Quality:**
```python
'sample_count': 16,   # Fast preview
'sample_count': 256,  # High quality
```

**Change Light Intensity:**
```python
'intensity': {'type': 'spectrum', 'value': 100.0}  # Brighter
'intensity': {'type': 'spectrum', 'value': 20.0}   # Dimmer
```

## 📁 Output

All rendered images are saved to the `output/` directory with descriptive filenames:
- `01_basic_scene.png`
- `02_materials_showcase.png`
- `03_lighting_01_point_light.png`
- etc.

## 🐛 Troubleshooting

### Import Error
```
ImportError: No module named 'mitsuba'
```
**Solution:** Activate the virtual environment first.

### Slow Rendering
**Solution:** Reduce quality settings for faster previews:
- Lower `sample_count` (16-32)
- Reduce resolution
- Decrease `max_depth`

### Dark Images
**Solution:** Increase light intensity or add more lights.

## 📚 Learn More

- **Documentation:** See [docs/README.md](../docs/README.md)
- **Roadmap:** See [docs/LEARNING_ROADMAP.md](../docs/LEARNING_ROADMAP.md)
- **Main README:** See [../README.md](../README.md)

## 💡 Next Steps

After completing these examples:
1. Modify existing demos
2. Combine techniques
3. Create your own scenes
4. Load 3D models
5. Add texture maps
6. Explore advanced features

---

**Happy rendering!** 🎨✨
