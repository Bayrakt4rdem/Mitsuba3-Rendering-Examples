# GUI Examples - Detailed Educational Scenes

This folder contains parametric scene generators with comprehensive educational content. Each example teaches specific rendering concepts through well-commented code and interactive parameters.

## 📚 Available Examples

### 1. Basic Scene (`basic_scene.py`)
**Difficulty:** Beginner  
**Render Time:** ~30 seconds  
**Key Concepts:**
- Scene structure (camera, objects, lights)
- Basic materials (diffuse, plastic, conductor, dielectric)
- Camera positioning
- Simple lighting

**What You'll Learn:**
- How to position objects in 3D space
- Difference between material types
- Effect of camera distance on composition
- Basic light-material interaction

**Parameters:**
- Sphere radius and position (X, Y, Z)
- Material type selection
- Color controls (RGB)
- Roughness adjustment
- Camera distance

---

### 2. Materials Showcase (`materials_showcase.py`)
**Difficulty:** Beginner-Intermediate  
**Render Time:** ~45 seconds  
**Key Concepts:**
- Material comparison (5 types side-by-side)
- Diffuse vs. specular reflection
- Conductor materials (metals)
- Dielectric materials (glass)
- Surface roughness

**What You'll Learn:**
- How different materials respond to light
- Difference between diffuse and glossy surfaces
- Why metals look metallic (conductor physics)
- How roughness affects appearance
- Material property tradeoffs

**Scene Setup:**
Five spheres demonstrating:
1. **Diffuse** (Red) - Matte, non-reflective
2. **Plastic** (Blue) - Glossy coat over diffuse base
3. **Conductor** (Gold) - Metallic reflection
4. **Dielectric** (Clear) - Transparent glass
5. **Rough Conductor** (Aluminum) - Brushed metal

**Parameters:**
- Light intensity and position
- Conductor roughness (smooth→rough)
- Plastic roughness (glossy→matte)
- Glass IOR (refractive index)
- Sphere spacing and size

---

### 3. Lighting Techniques (`lighting_techniques.py`)
**Difficulty:** Intermediate  
**Render Time:** ~45 seconds  
**Key Concepts:**
- Three-point lighting (key + fill + rim)
- Dramatic lighting (high contrast)
- Soft lighting (even illumination)
- Rim lighting (silhouettes)
- Top lighting (mysterious mood)

**What You'll Learn:**
- Professional photography/film lighting
- How light position affects mood
- Key light vs. fill light ratios
- Creating depth with rim lights
- Controlling contrast with multiple lights

**Lighting Setups:**

#### Three-Point Lighting
Classic studio setup used in photography and film:
- **Key Light** (45° side, above) - Main light, creates primary shadows
- **Fill Light** (opposite side, lower) - Softens shadows from key
- **Rim Light** (behind, above) - Separates subject from background

**When to use:** Product photography, portraits, balanced scenes

#### Dramatic Lighting
Single strong light for high contrast:
- One powerful side light
- Deep shadows
- High contrast mood

**When to use:** Film noir, horror, dramatic portraits, mystery

#### Soft Lighting
Large area lights for even illumination:
- Multiple soft light sources
- Minimal shadows
- Flattering, even light

**When to use:** Beauty photography, product shots, clean aesthetic

#### Rim Lighting
Strong backlight emphasis:
- Powerful light from behind subject
- Creates glowing edge
- Dramatic silhouette

**When to use:** Product reveals, dramatic effect, separating from background

#### Top Lighting
Overhead dramatic lighting:
- Light directly above
- Strong shadows below
- Mysterious, ominous mood

**When to use:** Horror scenes, mystery, interrogation scenes

**Parameters:**
- Lighting technique selection
- Key/fill/rim light intensities
- Light height and distance
- Object type (sphere, cube, both)
- Object material (diffuse, plastic, metal)
- Background brightness

---

### 4. Glass & Transparency (`glass_demo.py`)
**Difficulty:** Advanced  
**Render Time:** 1-2 minutes (needs high SPP)  
**Key Concepts:**
- Index of Refraction (IOR)
- Light refraction and bending
- Caustics (focused light patterns)
- Transparent materials
- Total internal reflection

**What You'll Learn:**
- How glass bends light (Snell's law)
- Why different materials bend light differently
- How to create realistic caustics
- Glass rendering techniques
- IOR values for real materials

**Index of Refraction Guide:**
- **Air:** 1.0 (no bending, reference)
- **Water:** 1.33 (slight bending)
- **Acrylic:** 1.49 (plastic glass)
- **Glass (standard):** 1.5-1.52 (window glass)
- **Sapphire:** 1.77 (gemstone)
- **Diamond:** 2.42 (extreme bending, strong caustics)

**Glass Shapes:**
1. **Sphere** - Creates lens effect, beautiful caustics
2. **Cube** - Flat refraction, multiple reflections
3. **Cylinder** - Line caustics, cylindrical lens
4. **Wine Glass** - Complex hollow geometry, intricate caustics

**Caustics Explained:**
When light passes through curved transparent objects, it focuses into patterns called caustics. Think of:
- Sunlight through a water glass on a table
- Pool bottom ripples on sunny days
- Rainbow patterns from crystal

**Rendering Tips:**
- **SPP:** Use 512+ for clean caustics
- **Max Depth:** Use 12+ for multiple glass bounces
- **Background:** White shows caustics best
- **Light:** Point lights create sharper caustics than area lights

**Parameters:**
- Glass shape selection
- Index of Refraction (1.0-2.5)
- Glass tint (RGB color)
- Light intensity and height
- Background type (white/checker/gradient)
- Caustic plane toggle

---

### 5. Cornell Box (`cornell_box.py`)
**Difficulty:** Advanced  
**Render Time:** 1-2 minutes  
**Key Concepts:**
- Global illumination
- Color bleeding
- Indirect lighting
- Light bounces
- Energy conservation

**What You'll Learn:**
- How light bounces between surfaces
- Color bleeding (red wall → white floor)
- Difference between direct and indirect lighting
- Why global illumination looks realistic
- Cornell Box as rendering benchmark

**What is Cornell Box?**
The Cornell Box is a classic computer graphics test scene created at Cornell University in 1984. It's used to:
- Test global illumination algorithms
- Compare rendering accuracy
- Validate physically-based rendering
- Demonstrate color bleeding

**Scene Components:**
- **Left Wall:** Red (reflects red light onto objects)
- **Right Wall:** Green (reflects green light onto objects)
- **Back/Floor/Ceiling:** White (neutral, shows color bleeding)
- **Area Light:** Overhead (soft shadows, indirect lighting)
- **Objects:** Metallic sphere + diffuse cube

**Color Bleeding Effect:**
Notice how:
- Left side of white objects appears reddish (from red wall)
- Right side appears greenish (from green wall)
- This is indirect lighting (global illumination)
- Light bounces off colored walls onto objects

**Parameters:**
- Box dimensions
- Light intensity and size
- Wall colors (left/right RGB)
- Object sizes (sphere and cube)
- Render quality (SPP)

---

## 🎓 Learning Path

### Beginner (2-3 hours)
1. **Basic Scene** - Understand fundamentals
2. **Materials Showcase** - See material differences
3. Try different material types on basic scene
4. Experiment with colors and roughness

### Intermediate (3-4 hours)
1. **Lighting Techniques** - Master professional setups
2. Compare all 5 lighting techniques
3. Try different objects with each lighting
4. Understand key/fill/rim ratios

### Advanced (4+ hours)
1. **Glass Demo** - Master transparency
2. Try different IOR values
3. Understand caustic formation
4. **Cornell Box** - Master global illumination
5. Observe color bleeding effects
6. Experiment with wall colors

## 🔬 Scientific Concepts

### Index of Refraction (IOR)
**Physics:** When light moves between materials with different densities, it bends. The amount of bending depends on the IOR ratio.

**Snell's Law:** n₁ × sin(θ₁) = n₂ × sin(θ₂)
- n₁, n₂ = IOR of materials
- θ₁, θ₂ = angles of incidence and refraction

**Practical:** 
- Higher IOR = more bending
- IOR difference creates refraction
- Same IOR = no bending (invisible)

### Fresnel Effect
At grazing angles, materials become more reflective:
- Look at water straight down: see through
- Look at water at shallow angle: see reflection
- This happens with all materials!

### Global Illumination
Light doesn't just travel from light → object → camera. It bounces:
1. Light → red wall → bounces red light
2. Red light → white floor → floor looks reddish
3. Multiple bounces create realistic lighting
4. Path tracer simulates this

### Caustics
Focused light from curved transparent/reflective surfaces:
- Convex (bulging) surfaces focus light
- Concave (hollow) surfaces scatter light
- Creates concentrated bright patterns
- Requires high SPP to render cleanly

## 💡 Rendering Tips

### For Fast Previews
- SPP: 64-128
- Resolution: 400×300 or smaller
- Simple scenes (Basic, Materials)

### For Quality Renders
- SPP: 512-1024
- Resolution: 800×600 or larger
- Complex scenes (Glass, Cornell Box)

### For Production Quality
- SPP: 2048+
- Resolution: 1920×1080+
- All scenes
- Be patient! Can take 10+ minutes

### SPP Guide
- **64:** Fast preview, very noisy
- **128:** Quick preview, noisy
- **256:** Good quality, acceptable noise
- **512:** High quality, minimal noise
- **1024:** Excellent quality, very clean
- **2048+:** Production quality, nearly perfect

### When to Use High SPP
- Glass scenes (caustics are noisy)
- Cornell Box (global illumination is noisy)
- Final renders
- Detailed inspection

## 🎯 Common Issues

### Issue: Black/Dark Images
**Cause:** Light intensity too low
**Fix:** Increase light intensity parameter

### Issue: Overexposed/White Images
**Cause:** Light intensity too high
**Fix:** Decrease light intensity parameter

### Issue: Noisy/Grainy Results
**Cause:** Not enough samples (SPP too low)
**Fix:** Increase SPP in Home tab (512+)

### Issue: Glass Looks Weird
**Cause:** Not enough bounces or SPP
**Fix:** 
- Increase SPP to 512+
- Check that max_depth is 12+ (automatic in our scenes)

### Issue: No Caustics Visible
**Cause:** Background too dark or SPP too low
**Fix:**
- Use white background
- Increase SPP to 512+
- Increase light intensity

### Issue: Render Takes Forever
**Cause:** Too high SPP or resolution
**Fix:**
- Lower SPP for preview (128)
- Reduce resolution (400×300)
- Use simpler scenes first

## 📖 Further Learning

### Books
- "Physically Based Rendering" (Pharr, Jakob, Humphreys)
- "Advanced Global Illumination" (Dutré, Bekaert, Bekaert)

### Online Resources
- Mitsuba 3 Documentation: https://mitsuba.readthedocs.io
- PBRT Book (free online): https://pbrt.org
- Scratchapixel: https://scratchapixel.com

### Practice Projects
1. Create three-point lighting for a product
2. Render glass with different IOR values
3. Design custom Cornell Box colors
4. Combine multiple lighting techniques
5. Create dramatic mood with top lighting

## 🚀 Next Steps

After mastering these examples:
1. Modify the Python code to add new features
2. Create your own scene generators
3. Combine concepts (glass + dramatic lighting)
4. Try different geometry
5. Experiment with textures
6. Learn about advanced integrators

Happy rendering! 🎨✨
