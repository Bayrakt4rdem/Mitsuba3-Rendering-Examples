# Mitsuba 3 Learning Demos 🎨✨

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Mitsuba](https://img.shields.io/badge/Mitsuba-3.0+-green.svg)](https://www.mitsuba-renderer.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

> **Comprehensive learning environment for Mitsuba 3 with progressive demos covering materials, lighting, and global illumination.**

A collection of well-documented, educational examples to help you learn physically-based rendering with Mitsuba 3. Perfect for beginners and intermediate users!

![Example Renders](https://img.shields.io/badge/Examples-6_Demos-brightgreen.svg)
![Documentation](https://img.shields.io/badge/Docs-Comprehensive-blue.svg)

## 🌟 What You'll Learn

- **Fundamentals**: Scene structure, cameras, basic shapes
- **Materials**: Diffuse, metallic, glass, plastic surfaces
- **Lighting**: Point lights, area lights, environment lighting
- **Global Illumination**: Color bleeding, indirect lighting
- **Professional Techniques**: Three-point lighting, composition

## 🚀 Quick Start

### ⚡ Automated Setup (Easiest!)

Run the automated setup script - it handles everything:

```powershell
.\setup.ps1
```

**Or use the full path:**

```powershell
.\scripts\setup_environment.ps1
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies (Mitsuba, PyQt6, etc.)
- ✅ Verify installation
- ✅ Launch the GUI

**That's it! One command!** 🎉

---

### 🛠️ Manual Installation (Alternative)

If you prefer manual setup:

```powershell
# 1. Create virtual environment
python -m venv mitsuba_venv

# 2. Activate it
.\mitsuba_venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch GUI
python launch_gui.py
```

For detailed troubleshooting, see **[Installation Guide](docs/INSTALLATION.md)**

---

### 🎨 Launch the GUI

After installation, launch anytime with:

```powershell
.\launch.ps1
```

**Or use the full path:**

```powershell
.\scripts\launch_gui.ps1
```

### 🎨 GUI Features

The GUI provides an intuitive interface for learning Mitsuba 3:

**Features:**
- 🎛️ Interactive parameter controls
- 📊 Real-time progress tracking
- 🖼️ Built-in image viewer
- 📝 Integrated log console
- 🌑 Professional dark theme
- 🎓 Progressive learning path

**5 Scene Tabs:**
1. 🔮 **Basic Scene** - Fundamentals
2. 💎 **Materials Showcase** - 5 materials compared
3. 💡 **Lighting Techniques** - Professional setups
4. 🔬 **Glass & Transparency** - IOR, caustics
5. 📦 **Cornell Box** - Global illumination

**2 Experimental Tabs (WIP):**
6. 🎨 **Custom Mesh** ⚠️ - Load OBJ/PLY/STL files (partially functional)
7. 🔄 **Inverse Rendering** ℹ️ - Educational info + variant checker (examples in CLI)

> ⚠️ **Note:** Custom Mesh and Inverse Rendering tabs are work-in-progress. See [TODO.md](TODO.md) for known issues and implementation status.

**See:** [GUI User Guide](docs/gui/USER_GUIDE.md) for detailed usage instructions.

---

### 💻 Command Line Examples (Alternative)

### 1. Clone or Download

```bash
git clone https://github.com/Bayrakt4rdem/Mitsuba3-Learning-Demos.git
cd Mitsuba3-Learning-Demos
```

### 2. Set Up Environment

```powershell
# Create virtual environment
python -m venv mitsuba_venv

# Activate it (Windows PowerShell)
.\mitsuba_venv\Scripts\Activate.ps1

# Linux/macOS
source mitsuba_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Installation

```powershell
python examples/00_quick_start.py
```

You should see a test render! ✨

### 4. Start Learning

```powershell
# Your first scene
python examples/01_basic_scene.py

# Or use the interactive launcher
cd examples
.\run_demo.ps1
```

## 📚 Demo Examples

| File | Level | Time | What You'll Learn |
|------|-------|------|-------------------|
| [`00_quick_start.py`](examples/00_quick_start.py) | Setup | 5 min | Verify installation |
| [`01_basic_scene.py`](examples/01_basic_scene.py) | Beginner | 15 min | Fundamentals, first render |
| [`02_materials_showcase.py`](examples/02_materials_showcase.py) | Intermediate | 30 min | 5 material types |
| [`03_lighting_techniques.py`](examples/03_lighting_techniques.py) | Intermediate | 45 min | 6 lighting setups |
| [`04_advanced_scene.py`](examples/04_advanced_scene.py) | Advanced | 60 min | Complex composition |
| [`05_cornell_box.py`](examples/05_cornell_box.py) | Classic | 45 min | Global illumination |

**See [examples/README.md](examples/README.md) for detailed descriptions.**

## 📖 Documentation

### Quick Links
- 📘 **[Quickstart Guide](docs/QUICKSTART.md)** - 5-minute setup guide
- 🔧 **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup & troubleshooting
- 🎓 **[Learning Roadmap](docs/LEARNING_ROADMAP.md)** - Complete 7-phase learning path
- 🎨 **[GUI User Guide](docs/gui/USER_GUIDE.md)** - How to use the GUI application
- 💡 **[GUI Examples](docs/examples/GUI_EXAMPLES.md)** - Interactive scene examples explained
- 💻 **[CLI Examples](docs/examples/CLI_EXAMPLES.md)** - Command-line demo descriptions

### Project Information
- 📋 **[Project Summary](docs/PROJECT_SUMMARY.md)** - Complete project overview
- 🏗️ **[Code Structure](docs/STRUCTURE.md)** - Codebase organization
- 🗂️ **[File Organization](docs/FILE_ORGANIZATION.md)** - Directory structure
- 🤝 **[Contributing](CONTRIBUTING.md)** - How to contribute

**See [docs/README.md](docs/README.md) for complete documentation index.**

## 🎯 Learning Path

### For Complete Beginners

1. Run `00_quick_start.py` to verify setup
2. Study `01_basic_scene.py` - understand scene structure
3. Experiment: change colors, move camera, adjust lights
4. Read the [Learning Roadmap](docs/LEARNING_ROADMAP.md)

### For Intermediate Users

1. Complete beginner path
2. Explore `02_materials_showcase.py` - see different surfaces
3. Master `03_lighting_techniques.py` - lighting is crucial!
4. Study `05_cornell_box.py` - understand global illumination

### For Advanced Learning

1. Complete intermediate path
2. Analyze `04_advanced_scene.py` - complex scenes
3. Create your own scenes from scratch
4. Experiment with advanced features (textures, volumes, etc.)

## 🎨 What is Mitsuba 3?

Mitsuba 3 is a research-oriented rendering system for physically-based rendering:

- ✅ **Physically Accurate**: Implements real light transport
- ✅ **Fast**: C++ core with Python bindings
- ✅ **Flexible**: Multiple rendering algorithms
- ✅ **Modern**: Supports differentiable rendering
- ✅ **Well-Documented**: Extensive documentation and examples

**Use cases:** Research, education, product visualization, artistic rendering, benchmarking

## 🛠️ Requirements

- **Python** 3.8 or higher
- **Operating System**: Windows, Linux, or macOS
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Multi-core recommended for faster rendering

## 📁 Project Structure

```
Mitsuba3-Learning-Demos/
├── examples/              # All demo Python files
│   ├── 00_quick_start.py
│   ├── 01_basic_scene.py
│   ├── 02_materials_showcase.py
│   ├── 03_lighting_techniques.py
│   ├── 04_advanced_scene.py
│   ├── 05_cornell_box.py
│   └── README.md          # Examples documentation
├── docs/                  # Documentation
│   ├── .local/            # Your personal notes (not committed)
│   ├── LEARNING_ROADMAP.md
│   ├── PROJECT_SUMMARY.md
│   ├── GITHUB_PUSH_GUIDE.md
│   └── README.md
├── assets/                # Images, diagrams (if added)
├── output/                # Rendered images (auto-created)
├── mitsuba_venv/          # Virtual environment (not committed)
├── requirements.txt       # Python dependencies
├── run_demo.ps1           # Interactive launcher script
├── README.md              # This file
├── LICENSE                # MIT + Mitsuba attribution
├── CONTRIBUTING.md        # Contribution guidelines
└── .gitignore             # Git ignore rules
```

## 🎓 Key Concepts Covered

### Materials (BSDFs)
- **Diffuse**: Matte surfaces (chalk, paper, unpolished wood)
- **Conductor**: Metals (gold, copper, aluminum, silver)
- **Rough Conductor**: Brushed metals with surface roughness
- **Dielectric**: Transparent materials (glass, water, diamond)
- **Plastic**: Glossy coating over diffuse base

### Lighting
- **Point Lights**: Omnidirectional, hard shadows
- **Area Lights**: Surface emitters, soft shadows
- **Directional Lights**: Parallel rays (sun-like)
- **Environment Maps**: Sky dome lighting
- **Three-Point Setup**: Professional lighting technique

### Rendering Concepts
- **Path Tracing**: Physically accurate light simulation
- **Global Illumination**: Indirect lighting and light bounces
- **Color Bleeding**: Light carrying color between surfaces
- **Samples Per Pixel**: Quality vs speed tradeoff
- **Ray Depth**: Maximum light bounces

## 💡 Customization Examples

All demos are designed to be modified! Try these experiments:

```python
# Change material color
'reflectance': {'type': 'rgb', 'value': [0.8, 0.1, 0.1]}  # Red
'reflectance': {'type': 'rgb', 'value': [0.1, 0.8, 0.1]}  # Green

# Move camera
origin=[5, 5, 10]  # Further away
origin=[2, 1, 3]   # Closer

# Adjust render quality
'sample_count': 16,   # Fast preview
'sample_count': 256,  # High quality

# Change light intensity
'intensity': {'type': 'spectrum', 'value': 50.0}   # Dimmer
'intensity': {'type': 'spectrum', 'value': 200.0}  # Brighter
```

## 🐛 Troubleshooting

### Import Error: No module named 'mitsuba'
**Solution**: Activate virtual environment first
```powershell
.\mitsuba_venv\Scripts\Activate.ps1
```

### Rendering is Slow
**Solution**: Reduce quality for previews
- Lower `sample_count` to 16-32
- Reduce resolution (256×256)
- Decrease `max_depth` to 4

### Images are Too Dark
**Solution**: Increase lighting
- Higher `intensity` values
- Add more light sources
- Increase `radiance` for area lights

### Python Version Error
**Solution**: Use Python 3.8 or higher
```bash
python --version
```

## 🌐 Resources

### Mitsuba 3
- **Documentation**: https://mitsuba.readthedocs.io/
- **GitHub**: https://github.com/mitsuba-renderer/mitsuba3
- **Website**: https://www.mitsuba-renderer.org/
- **Gallery**: https://www.mitsuba-renderer.org/gallery.html

### Learning Materials
- **Computer Graphics Principles**: Learn ray tracing fundamentals
- **PBR Theory**: Understand physically-based rendering
- **Blender**: Practice 3D concepts visually
- **ShaderToy**: Experiment with real-time graphics

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ways to contribute:
- 🐛 Report bugs
- 💡 Suggest improvements
- 📝 Improve documentation
- 🎨 Add new examples
- 🔧 Fix issues

## � Project Structure

```
Mitsuba3-Learning-Demos/
├── docs/                          # 📚 All documentation
│   ├── gui/                      # GUI-specific docs
│   ├── examples/                 # Example documentation
│   ├── INSTALLATION.md           # Setup guide
│   ├── QUICKSTART.md            # Quick start
│   └── README.md                 # Documentation index
│
├── scripts/                       # 🚀 Launcher scripts
│   ├── setup_environment.ps1    # Automated setup
│   ├── launch_gui.ps1           # GUI launcher
│   └── run_examples.ps1         # Run CLI examples
│
├── gui/                          # 🎨 GUI application
│   ├── core/                    # Main window, rendering
│   ├── tabs/                    # Scene tab modules
│   └── widgets/                 # Reusable UI components
│
├── gui_examples/                 # 💡 GUI scene generators
│   ├── basic_scene.py           # Fundamentals
│   ├── materials_showcase.py    # Material comparison
│   ├── lighting_techniques.py   # Professional lighting
│   ├── glass_demo.py            # Glass & transparency
│   └── cornell_box.py           # Global illumination
│
├── examples/                     # 💻 CLI demo scripts
│   ├── 00_quick_start.py        # Installation check
│   ├── 01_basic_scene.py        # First render
│   ├── 02_materials_showcase.py # Materials
│   ├── 03_lighting_techniques.py# Lighting
│   ├── 04_advanced_scene.py     # Complex scenes
│   └── 05_cornell_box.py        # Classic scene
│
├── setup.ps1                     # 🔧 Quick setup wrapper
├── launch.ps1                    # ▶️ Quick launch wrapper
├── launch_gui.py                # Main GUI entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

**See [docs/FILE_ORGANIZATION.md](docs/FILE_ORGANIZATION.md) for detailed explanations.**

---

## �📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

**Note**: This project uses Mitsuba 3, which is licensed under the BSD 3-Clause License. See LICENSE for full attribution.

## 🙏 Acknowledgments

- **Mitsuba Team** ([Realistic Graphics Lab, EPFL](https://rgl.epfl.ch/)) - For creating Mitsuba 3
- **Cornell University** - For the classic Cornell Box scene
- **Computer Graphics Community** - For inspiration and knowledge sharing

## ⭐ Show Your Support

If you find this project helpful:
- Give it a ⭐ on GitHub
- Share it with others learning rendering
- Contribute your own examples
- Provide feedback and suggestions

##  Contact & Support

- **Issues**: [GitHub Issues](https://github.com/Bayrakt4rdem/Mitsuba3-Learning-Demos/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Bayrakt4rdem/Mitsuba3-Learning-Demos/discussions)

## 🗺️ Roadmap

Future additions (contributions welcome!):
- [ ] 3D model loading examples (OBJ, PLY)
- [ ] Texture mapping demos
- [ ] Volumetric rendering (fog, smoke)
- [ ] Animation examples
- [ ] Subsurface scattering demo
- [ ] HDR environment map examples
- [ ] Batch rendering scripts
- [ ] Video tutorials
- [ ] Interactive Jupyter notebooks

---

**Ready to start?** Run `python examples/00_quick_start.py` and begin your rendering journey! 🚀

**Questions?** Check the [docs/](docs/) folder or open an issue!

**Happy Rendering!** 🎨✨
