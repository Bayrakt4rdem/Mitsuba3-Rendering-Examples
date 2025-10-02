# Mitsuba 3 Learning Roadmap

## Your Journey to Master Mitsuba 3

This guide will help you progress from complete beginner to advanced user.

---

## Phase 1: Setup & Basics (Day 1)

### Goals
- Get Mitsuba running
- Understand basic scene structure
- Render your first image

### Steps
1. **Verify Installation**
   ```powershell
   .\mitsuba_venv\Scripts\Activate.ps1
   python 00_quick_start.py
   ```
   ✓ Should see a red sphere rendered

2. **Run Basic Scene**
   ```powershell
   python 01_basic_scene.py
   ```
   ✓ Understand: scene dict, integrator, sensor, shapes, materials, lights

3. **Experiment**
   - Change sphere color to blue: `[0.1, 0.1, 0.8]`
   - Move camera: change `origin` in look_at()
   - Adjust FOV: try `fov=30` or `fov=70`
   - Change light position

### Key Concepts
- Scene dictionary structure
- Basic shapes (sphere, rectangle)
- Camera setup with look_at()
- Simple lighting

---

## Phase 2: Materials (Days 2-3)

### Goals
- Understand different material types
- Learn when to use each BSDF
- Master material properties

### Steps
1. **Materials Showcase**
   ```powershell
   python 02_materials_showcase.py
   ```
   ✓ See 5 different material types side-by-side

2. **Study Each Material**
   - **Diffuse**: Matte surfaces (walls, paper, cloth)
   - **Conductor**: Metals (gold, copper, aluminum)
   - **RoughConductor**: Brushed metals
   - **Dielectric**: Transparent (glass, water, diamond)
   - **Plastic**: Glossy coating over matte base

3. **Experiments**
   - Create a scene with only metal objects
   - Try different roughness values: 0.0 (mirror) to 1.0 (very rough)
   - Make a glass of water (dielectric sphere)
   - Combine materials in one scene

### Key Concepts
- BSDF (Bidirectional Scattering Distribution Function)
- Reflectance vs transmission
- Roughness and microfacet models
- Index of refraction (IOR)
- Fresnel effects

---

## Phase 3: Lighting (Days 4-5)

### Goals
- Master different light types
- Understand hard vs soft shadows
- Learn professional lighting setups

### Steps
1. **Lighting Techniques**
   ```powershell
   python 03_lighting_techniques.py
   ```
   ✓ Compare 6 different lighting setups

2. **Study Lighting Types**
   - **Point Light**: Fast, hard shadows (light bulb)
   - **Area Light**: Realistic, soft shadows (softbox)
   - **Directional**: Parallel rays (sun)
   - **Environment**: Sky dome (outdoor lighting)

3. **Professional Setups**
   - Three-point lighting (key + fill + back)
   - Color temperature (warm vs cool)
   - Light intensity and falloff
   - Multiple light interactions

4. **Experiments**
   - Create dramatic lighting (single side light)
   - Make sunset lighting (warm directional + orange tint)
   - Studio portrait lighting (three-point setup)
   - Moody scene (low-key lighting)

### Key Concepts
- Direct vs indirect lighting
- Shadow quality (hard/soft)
- Light intensity and units
- Color temperature
- Three-point lighting technique

---

## Phase 4: Global Illumination (Day 6)

### Goals
- Understand light transport
- See color bleeding in action
- Learn about indirect lighting

### Steps
1. **Cornell Box**
   ```powershell
   python 05_cornell_box.py
   ```
   ✓ The classic global illumination demo

2. **Observe Carefully**
   - Red tint on left side of boxes (from red wall)
   - Green tint on right side (from green wall)
   - Soft shadows under boxes
   - Bright ceiling near light
   - Ambient light in shadowed areas

3. **Experiments**
   - Set `max_depth=1`: See direct lighting only (no color bleeding!)
   - Set `max_depth=2`: One bounce (some color)
   - Set `max_depth=8`: Full global illumination
   - Change wall colors to blue and yellow
   - Add a glass sphere (see caustics!)

### Key Concepts
- Global illumination vs local illumination
- Light bouncing
- Color bleeding
- Indirect lighting
- Ray depth and convergence

---

## Phase 5: Advanced Scenes (Days 7-10)

### Goals
- Combine all techniques
- Build complex scenes
- Optimize render quality

### Steps
1. **Advanced Scene**
   ```powershell
   python 04_advanced_scene.py
   ```
   ✓ Multiple materials + complex lighting

2. **Analyze the Scene**
   - How are objects positioned?
   - Why does the lighting work?
   - What makes it look professional?
   - How do materials interact?

3. **Create Your Own Scene**
   Start simple, add complexity:
   - Plan: Sketch your scene on paper
   - Build: Start with basic shapes
   - Light: Add one light at a time
   - Refine: Adjust materials and positions
   - Polish: Increase quality settings

### Example Project Ideas
- **Still Life**: Fruits on a table
- **Product Visualization**: Phone, watch, or gadget
- **Jewelry**: Gems with glass and metal
- **Architectural**: Room interior
- **Abstract**: Geometric composition

---

## Phase 6: Optimization & Quality (Days 11-14)

### Goals
- Balance quality vs speed
- Understand render settings
- Debug common issues

### Key Settings to Master

#### Samples Per Pixel (spp)
- **16-32**: Fast preview (noisy)
- **64-128**: Good quality
- **256-512**: High quality
- **1024+**: Production quality

#### Max Depth (light bounces)
- **2-4**: Fast, direct lighting
- **6-8**: Standard quality
- **12-16**: Complex materials (glass, metals)
- **32+**: Very complex scenes (usually not needed)

#### Resolution
- **256x256**: Quick tests
- **512x512**: Standard preview
- **1024x768**: Good quality
- **1920x1080**: HD output
- **4K+**: Final production

### Optimization Tips
1. **Preview First**: Use low spp/resolution for composition
2. **Progressive**: Start with max_depth=4, increase if needed
3. **Target Problem Areas**: Only high quality where visible
4. **Use Denoising**: For faster high-quality results
5. **Profile**: Identify slow parts of scene

---

## Phase 7: Advanced Topics (Days 15+)

Ready for more? Explore these advanced features:

### 1. Loading 3D Models
- Import OBJ, PLY files
- Apply materials to meshes
- Use multiple objects

### 2. Textures
- Image-based materials
- UV mapping
- Normal maps, bump maps

### 3. Volumetric Rendering
- Fog, smoke, clouds
- Subsurface scattering
- Participating media

### 4. Advanced Materials
- Layered BSDFs
- Anisotropic materials
- Custom shaders

### 5. Animation
- Keyframe animation
- Motion blur
- Time-varying properties

### 6. Differentiable Rendering
- Inverse rendering
- Gradient-based optimization
- Parameter estimation

---

## Resources for Continued Learning

### Official Documentation
- **Main Docs**: https://mitsuba.readthedocs.io/
- **API Reference**: https://mitsuba.readthedocs.io/en/latest/src/api_reference.html
- **Tutorials**: https://mitsuba.readthedocs.io/en/latest/src/getting_started/intro.html

### Example Galleries
- **Official Gallery**: https://www.mitsuba-renderer.org/gallery.html
- **Research Papers**: https://rgl.epfl.ch/publications

### Community
- **GitHub**: https://github.com/mitsuba-renderer/mitsuba3
- **Discord**: Join the Mitsuba community
- **Forum**: Ask questions, share renders

### Related Topics
- **PBR Theory**: Physically Based Rendering book
- **Graphics Gems**: Classic computer graphics algorithms
- **SIGGRAPH**: Research conference proceedings
- **ShaderToy**: Shader programming practice

---

## Progress Checklist

Mark your progress as you learn:

### Beginner Level
- [ ] Installed Mitsuba successfully
- [ ] Rendered first scene
- [ ] Changed basic parameters (color, position)
- [ ] Understand scene structure
- [ ] Created a simple scene from scratch

### Intermediate Level
- [ ] Used all 5 basic material types
- [ ] Set up three-point lighting
- [ ] Rendered Cornell Box
- [ ] Understand global illumination
- [ ] Optimized render settings
- [ ] Created a complex scene

### Advanced Level
- [ ] Loaded external 3D models
- [ ] Used texture maps
- [ ] Implemented volumetric effects
- [ ] Created custom materials
- [ ] Built a complete project
- [ ] Contributed to community

---

## Tips for Success

1. **Be Patient**: Rendering takes time, especially high quality
2. **Experiment**: Change one parameter at a time
3. **Save Often**: Keep versions of your work
4. **Start Simple**: Add complexity gradually
5. **Read Code**: Study the example files carefully
6. **Ask Questions**: Community is helpful
7. **Share Work**: Get feedback on your renders
8. **Have Fun**: Enjoy the creative process!

---

## Common Pitfalls to Avoid

1. **Too High Quality Initially**: Start with low spp for testing
2. **Forgetting Units**: Keep scale consistent
3. **Too Many Lights**: Often 2-3 lights is enough
4. **Extreme Values**: Keep parameters reasonable
5. **Not Saving**: Save work frequently
6. **Skipping Basics**: Master fundamentals first

---

## Next Steps After This Guide

1. **Recreate Famous Renders**: Try to replicate renders you admire
2. **Join Challenges**: Participate in rendering competitions
3. **Build Portfolio**: Create showcase pieces
4. **Learn Related Skills**: 3D modeling, photography, color theory
5. **Teach Others**: Best way to solidify knowledge
6. **Contribute**: Help improve Mitsuba or create tutorials

---

**Remember**: Every expert was once a beginner. Take your time, practice regularly, and enjoy the journey!

Happy Rendering! 🎨✨
