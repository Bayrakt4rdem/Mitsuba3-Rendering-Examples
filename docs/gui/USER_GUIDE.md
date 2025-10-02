# Mitsuba 3 Render Studio - User Guide

## 🎨 Welcome

Mitsuba 3 Render Studio is a professional PyQt6-based GUI that makes learning and experimenting with Mitsuba 3 rendering easy and intuitive. No need to write code - just adjust sliders and see the results!

## 🚀 Getting Started

### Launch the Application

**Windows PowerShell:**
```powershell
.\launch_gui.ps1
```

**Or directly:**
```powershell
python launch_gui.py
```

The launcher will automatically:
- Activate your virtual environment
- Check for missing dependencies
- Install them if needed
- Launch the GUI

## 🖥️ Interface Overview

### Main Window Layout

```
┌─────────────────────────────────────────────────────────┐
│  [🏠 Home] [🔮 Basic Scene] [📦 Cornell Box]          │
├──────────────────────────────┬──────────────────────────┤
│                              │ ┌──────────────────────┐ │
│                              │ │   Output Viewer      │ │
│    Scene Parameters          │ │  (Rendered Images)   │ │
│    and Controls              │ └──────────────────────┘ │
│                              │ ┌──────────────────────┐ │
│                              │ │   Log Viewer         │ │
│    [🎨 Render Scene]         │ │  (Terminal Console)  │ │
│                              │ └──────────────────────┘ │
└──────────────────────────────┴──────────────────────────┘
```

### Key Components

1. **Tab Bar** (Top)
   - Switch between different scenes
   - Drag tabs to reorder
   - Home tab for global settings

2. **Parameter Panel** (Left)
   - Adjust scene parameters
   - Real-time validation
   - Tooltips for guidance

3. **Output Viewer** (Top Right)
   - View rendered images
   - Zoom and pan
   - Save images
   - Open output folder

4. **Log Console** (Bottom Right)
   - Color-coded messages
   - Auto-scroll option
   - Clear logs button
   - Shows render progress

5. **Render Controls** (Bottom)
   - Render button
   - Progress bar
   - Cancel button

## 📋 Step-by-Step Workflow

### 1. Configure Global Settings

Click the **🏠 Home** tab:

- **Resolution**: Set default image size (e.g., 800×600)
- **Samples per Pixel**: Quality vs. speed (256 = good, 512+ = better)
- **Rendering Variant**: Backend (use `scalar_rgb` by default)
- **Auto-scroll Logs**: Keep latest messages visible

Click **Apply Settings** to save.

### 2. Select a Scene

Click on a scene tab (listed in order of difficulty):

1. **🔮 Basic Scene**: Simple sphere with customizable material (BEGINNER)
2. **� Materials**: Compare 5 different material types (BEGINNER-INTERMEDIATE)
3. **💡 Lighting**: Professional lighting techniques (INTERMEDIATE)
4. **🔬 Glass**: Transparent materials and caustics (ADVANCED)
5. **📦 Cornell Box**: Global illumination demo (ADVANCED)

### 3. Adjust Parameters

Each scene has its own controls:

#### Basic Scene Parameters

**Sphere Properties:**
- `Radius`: Size of the sphere (0.1 - 5.0)
- `Position X/Y/Z`: Move the sphere around
  - X: Left (-) / Right (+)
  - Y: Back (-) / Front (+)
  - Z: Down (-) / Up (+)

**Material Properties:**
- `Material Type`: Choose surface type
  - **Diffuse**: Matte, non-reflective
  - **Plastic**: Glossy paint-like
  - **Conductor**: Metallic (copper-like)
  - **Dielectric**: Glass, transparent
- `Roughness`: Surface smoothness (0=mirror, 100=rough)
- `Color R/G/B`: RGB color sliders (0-100)

**Camera Settings:**
- `Distance`: How far camera is from scene

#### Materials Showcase Parameters

**Lighting:**
- `Light Intensity`: Overall brightness (5-100)
- `Light Height`: Position of area light (2-8m)

**Material Adjustments:**
- `Conductor Roughness`: Metallic surface smoothness (0=mirror, 50=brushed)
- `Plastic Roughness`: Plastic coating smoothness
- `Glass IOR`: Index of refraction (1.5=standard glass)

**Scene Settings:**
- `Sphere Spacing`: Distance between material spheres
- `Sphere Radius`: Size of each demo sphere

**Scene Layout:** Five spheres showing:
1. Red diffuse (matte)
2. Blue plastic (glossy)
3. Gold conductor (metallic)
4. Clear dielectric (glass)
5. Aluminum rough conductor (brushed metal)

#### Lighting Techniques Parameters

**Lighting Setup:**
- `Lighting Technique`: Choose from:
  - **Three-Point:** Balanced studio (key+fill+rim)
  - **Dramatic:** Single strong side light
  - **Soft:** Large area lights, even illumination
  - **Rim:** Strong backlight, silhouette effect
  - **Top:** Overhead mysterious lighting

**Light Intensities:**
- `Key Light`: Main light strength (5-100)
- `Fill Light`: Shadow-filling light (0-50)
- `Rim/Back Light`: Edge separation light (0-100)

**Light Position:**
- `Light Height`: Vertical position (1-10m)
- `Light Distance`: Distance from subject (2-15m)

**Subject:**
- `Object Type`: Sphere, cube, or both
- `Material`: Diffuse, plastic, or metal

**Scene Settings:**
- `Background`: Brightness level (0=black, 100=white)

#### Glass & Transparency Parameters

**Glass Object:**
- `Glass Shape`: 
  - **Sphere:** Beautiful lens caustics
  - **Cube:** Flat refraction patterns
  - **Cylinder:** Line caustics
  - **Wine Glass:** Complex hollow geometry

**Glass Properties:**
- `Index of Refraction (IOR)`: Light bending amount
  - 1.0 = Air (no bending)
  - 1.33 = Water
  - 1.5 = Standard glass
  - 1.9 = Dense glass
  - 2.42 = Diamond

**Glass Tint:**
- `Red/Green/Blue Tint`: Color absorption (100=clear, <100=tinted)

**Lighting:**
- `Light Intensity`: Brightness (5-50)
- `Light Height`: Vertical position affects caustics (2-8m)

**Background:**
- `Background Type`:
  - **White:** Best for seeing caustics
  - **Checker:** Shows refraction distortion
  - **Gradient:** Atmospheric effect
- `Show Caustic Plane`: Toggle white receiving plane

**Important:** Glass scenes need 512+ SPP for clean caustics!

#### Cornell Box Parameters

**Box Settings:**
- `Box Size`: Scale of entire room

**Lighting:**
- `Light Intensity`: Brightness (1-50)
- `Light Size`: Area light dimensions

**Wall Colors:**
- Left wall (traditionally red)
- Right wall (traditionally green)
- Adjust RGB components individually

**Scene Objects:**
- `Sphere Size`: Metallic sphere
- `Box Size`: White diffuse cube

### 4. Render the Scene

1. Click **🎨 Render Scene** button
2. Watch progress bar fill up (0% → 100%)
3. See log messages in console:
   - 🎨 Starting render
   - Loading scene...
   - Rendering with path integrator
   - Post-processing...
   - ✅ Render complete!

### 5. View Results

**Automatically displayed in Output Viewer:**
- Image shows immediately
- Filename and resolution shown below
- Buttons become active:
  - `Save As...`: Export to different location
  - `Open Folder`: Open output directory in Explorer
  - `Fit to Window`: Toggle fit/actual size

### 6. Iterate and Experiment

- Adjust parameters
- Render again
- Compare results
- Learn how parameters affect the image!

## 🎛️ Advanced Features

### Draggable Tabs

- Click and hold a tab
- Drag to new position
- Release to drop
- Reorder based on your workflow

### Resizable Panels

**Horizontal Splitter** (Parameters ↔ Viewers):
- Hover over divider
- Cursor changes to resize arrow
- Drag left/right to adjust
- Give more space to parameters or viewers

**Vertical Splitter** (Output ↔ Logs):
- Hover between output and log panels
- Drag up/down
- Maximize whichever you need

### Log Console Features

**Auto-scroll:**
- Toggle with button
- ON: Always shows latest
- OFF: Stay at current position (for reviewing old logs)

**Clear Logs:**
- Click `Clear Logs` button
- Removes all messages
- Fresh start

**Color Codes:**
- 🟢 Green: Success/info
- 🟡 Yellow: Warning
- 🔴 Red: Error
- 🔵 Cyan: Debug info

### Image Viewer Features

**Fit to Window:**
- ON: Image scales to fit viewer
- OFF: Shows actual pixel size
- Useful for checking details

**Zoom:**
- Use scroll wheel (when Fit=OFF)
- Pan by dragging

**Save Options:**
- Click `Save As...`
- Choose location and filename
- Supports PNG format

## ⚙️ Tips & Tricks

### Performance

**Faster Renders:**
- Lower Samples per Pixel (128 or less)
- Smaller resolution (400×300)
- Use `scalar_rgb` variant

**Higher Quality:**
- More SPP (512, 1024, or higher)
- Larger resolution (1920×1080+)
- More patience! 😊

### Material Tips

**Diffuse Materials:**
- Best for learning basics
- Fast to render
- No complex lighting interactions

**Conductor (Metal):**
- Reflects environment
- Works with area lights
- Adjust roughness for polished/brushed look

**Dielectric (Glass):**
- Transparent materials
- Slowest to render
- Beautiful but requires more SPP

**Plastic:**
- Good middle ground
- Glossy highlights
- Colorful diffuse base

### Lighting Tips

**Cornell Box:**
- Increase SPP for smooth color bleeding
- Small light = sharp shadows
- Large light = soft shadows
- High intensity = bright, low = moody

**Basic Scene:**
- Light is above the sphere
- Experiment with sphere position
- Move sphere up (Z+) for dramatic shadows

### Color Selection

**Using RGB Sliders:**
- Red=100, G=0, B=0 → Pure red
- R=G=B=50 → Medium gray
- R=G=B=100 → White
- R=G=B=0 → Black

**Material Color:**
- Only affects diffuse and plastic
- Conductor uses physical metal properties
- Dielectric is transparent (color ignored)

## 🐛 Troubleshooting

### GUI Won't Start

**Error: "Virtual environment not found"**
```powershell
python -m venv mitsuba_venv
.\mitsuba_venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Error: "Import PyQt6 could not be resolved"**
```powershell
pip install PyQt6
```

**Error: "Import mitsuba could not be resolved"**
```powershell
pip install mitsuba
```

### Rendering Issues

**"Render already in progress"**
- Wait for current render to finish
- Or click Cancel

**"LLVM API initialization failed"**
- This is normal! Just a warning
- Mitsuba falls back to scalar backend
- Doesn't affect results

**Black/Dark Images:**
- Increase light intensity
- Check object isn't too far from light
- Increase SPP for global illumination

**Noisy Images:**
- Increase Samples per Pixel
- More SPP = smoother
- Cornell Box needs 512+ for clean results

**Slow Renders:**
- Reduce resolution
- Lower SPP
- Simplify scene parameters
- Close other applications

### Display Issues

**Image Not Showing:**
- Check log for errors
- Verify render completed (100%)
- Try toggling "Fit to Window"

**Can't Resize Panels:**
- Hover exactly on divider line
- Cursor should change shape
- If stuck, restart GUI

**Logs Not Scrolling:**
- Check "Auto-scroll" is ON
- Click button to toggle
- Manually scroll to bottom

## 📁 File Locations

**Rendered Images:**
```
output/
├── basic_scene.png
├── cornell_box.png
└── ...
```

**Log Files:**
```
logs/
├── mitsuba_gui_2025-10-02.log
├── mitsuba_gui_2025-10-02.log.zip
└── ...
```

**Configuration:**
- Global settings stored in memory
- Not persisted between sessions (yet!)
- Set defaults in Home tab each time

## 🎓 Learning Path

### Beginner (30 minutes)

1. ✅ Launch GUI
2. ✅ Render Basic Scene (defaults)
3. ✅ Change sphere color
4. ✅ Try different materials
5. ✅ Adjust sphere position

### Intermediate (1 hour)

1. ✅ Master material types
2. ✅ Experiment with roughness
3. ✅ Render Cornell Box
4. ✅ Adjust wall colors
5. ✅ Compare light intensities

### Advanced (2+ hours)

1. ✅ Understand SPP impact
2. ✅ Optimize render settings
3. ✅ Create custom scenes (code)
4. ✅ Add new tabs (see gui/README.md)
5. ✅ Experiment with integrators

## 🔧 Customization

Want to add your own scenes? See:
- `gui/README.md` - Architecture guide
- `gui_examples/` - Scene generator examples
- `gui/tabs/` - Tab implementation examples

## 📞 Support

Having trouble? Check:
1. This guide
2. Main README.md
3. gui/README.md
4. Log console (shows errors)
5. Log files in `logs/`

## 🎉 Have Fun!

The best way to learn is to experiment:
- Try extreme values
- Break things (it's OK!)
- Compare renders
- Learn from the logs

Happy rendering! 🎨✨
