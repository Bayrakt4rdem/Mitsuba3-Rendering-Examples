"""
Mitsuba 3 Demo 04: Advanced Scene
==================================

A more complex scene combining everything:
- Multiple objects with different materials
- Complex lighting setup
- Camera composition
- Realistic rendering settings

This demonstrates what you can create after learning the basics!

Learning Goals:
- Combine multiple techniques
- Build a complete scene
- Understand scene composition
- See professional rendering settings
"""

import mitsuba as mi
import matplotlib.pyplot as plt
import os

mi.set_variant('scalar_rgb')

print("Advanced Scene Demo")
print("=" * 50)
print("Creating a complex scene with multiple objects and materials...")

# Build a more interesting scene
scene_dict = {
    'type': 'scene',
    
    # Use path tracer with more bounces for better realism
    'integrator': {
        'type': 'path',
        'max_depth': 12,  # More bounces for glass/reflections
        'rr_depth': 5,    # Russian roulette depth
    },
    
    'sensor': {
        'type': 'perspective',
        'fov': 40,  # Slightly narrow for a more "professional" look
        'film': {
            'type': 'hdrfilm',
            'width': 1024,
            'height': 768,
            'rfilter': {'type': 'gaussian'},
        },
        'sampler': {
            'type': 'independent',
            'sample_count': 256,  # High quality
        },
        # Camera at an interesting angle
        'to_world': mi.ScalarTransform4f.look_at(
            origin=[5, 4, 10],
            target=[0, 0, 0],
            up=[0, 1, 0]
        ),
    },
    
    # Floor - checkerboard pattern using a texture
    'floor': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.8, 0.8, 0.8]},
        },
        'to_world': mi.ScalarTransform4f.translate([0, -2, 0])
                                         .rotate([1, 0, 0], -90)
                                         .scale(15)
    },
    
    # Back wall
    'back_wall': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.9, 0.85, 0.8]},  # Warm tone
        },
        'to_world': mi.ScalarTransform4f.translate([0, 0, -5])
                                         .scale(15)
    },
    
    # Left wall
    'left_wall': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.8, 0.3, 0.3]},  # Red wall
        },
        'to_world': mi.ScalarTransform4f.translate([-7, 0, 0])
                                         .rotate([0, 1, 0], 90)
                                         .scale(15)
    },
    
    # Central glass sphere
    'glass_sphere': {
        'type': 'sphere',
        'bsdf': {
            'type': 'dielectric',
            'int_ior': 1.5,  # Glass
        },
        'to_world': mi.ScalarTransform4f.translate([0, 0, 0]).scale(1.5)
    },
    
    # Gold sphere (left)
    'gold_sphere': {
        'type': 'sphere',
        'bsdf': {
            'type': 'conductor',
            'material': 'Au',
        },
        'to_world': mi.ScalarTransform4f.translate([-3, -0.5, 1]).scale(1.0)
    },
    
    # Rough copper sphere (right)
    'copper_sphere': {
        'type': 'sphere',
        'bsdf': {
            'type': 'roughconductor',
            'material': 'Cu',
            'alpha': 0.2,
        },
        'to_world': mi.ScalarTransform4f.translate([3, -0.5, 1]).scale(1.0)
    },
    
    # Plastic sphere (front left)
    'plastic_sphere': {
        'type': 'sphere',
        'bsdf': {
            'type': 'plastic',
            'diffuse_reflectance': {'type': 'rgb', 'value': [0.2, 0.6, 0.9]},
            'nonlinear': True,
        },
        'to_world': mi.ScalarTransform4f.translate([-1.5, -1, 3]).scale(0.7)
    },
    
    # Diffuse red sphere (front right)
    'diffuse_sphere': {
        'type': 'sphere',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.8, 0.2, 0.9]},  # Purple
        },
        'to_world': mi.ScalarTransform4f.translate([1.5, -1, 3]).scale(0.7)
    },
    
    # Key light - main illumination from upper right
    'key_light': {
        'type': 'rectangle',
        'emitter': {
            'type': 'area',
            'radiance': {'type': 'rgb', 'value': [30, 30, 28]},  # Slightly warm
        },
        'to_world': mi.ScalarTransform4f.translate([4, 6, 3])
                                         .rotate([1, 0, 0], -45)
                                         .rotate([0, 1, 0], -30)
                                         .scale(2)
    },
    
    # Fill light - softer, from left
    'fill_light': {
        'type': 'rectangle',
        'emitter': {
            'type': 'area',
            'radiance': {'type': 'rgb', 'value': [8, 8, 10]},  # Slightly cool
        },
        'to_world': mi.ScalarTransform4f.translate([-4, 4, 2])
                                         .rotate([1, 0, 0], -30)
                                         .rotate([0, 1, 0], 30)
                                         .scale(1.5)
    },
    
    # Back light - rim lighting
    'back_light': {
        'type': 'point',
        'intensity': {'type': 'spectrum', 'value': 60.0},
        'position': [0, 3, -4],
    },
    
    # Ambient environment light
    'env': {
        'type': 'constant',
        'radiance': {'type': 'rgb', 'value': [0.3, 0.3, 0.4]},  # Subtle blue ambient
    },
}

print("\n📦 Scene contents:")
print("   Objects:")
print("   • Glass sphere (center) - refractive dielectric")
print("   • Gold sphere (left) - conductor material")
print("   • Copper sphere (right) - rough conductor")
print("   • Blue plastic sphere (front left)")
print("   • Purple diffuse sphere (front right)")
print("\n   Lighting:")
print("   • Key light (main, warm)")
print("   • Fill light (soft, cool)")
print("   • Back light (rim lighting)")
print("   • Ambient environment (blue)")

print("\n🎬 Rendering high-quality scene...")
print("   Resolution: 1024x768")
print("   Samples per pixel: 256")
print("   Max bounces: 12")
print("   ⏱️  This will take 2-5 minutes (worth the wait!)")

scene = mi.load_dict(scene_dict)
image = mi.render(scene, spp=256)

print("✅ Rendering complete!")

# Save output
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, '04_advanced_scene.png')
mi.util.write_bitmap(output_path, image)
print(f"\n💾 High-res image saved to: {output_path}")

# Create figure with annotations
fig = plt.figure(figsize=(16, 12))

# Main image
ax1 = plt.subplot(2, 1, 1)
ax1.imshow(mi.util.convert_to_bitmap(image))
ax1.axis('off')
ax1.set_title('Advanced Scene: Multiple Materials & Professional Lighting', 
              fontsize=18, fontweight='bold', pad=20)

# Annotations
ax2 = plt.subplot(2, 1, 2)
ax2.axis('off')

scene_info = """
SCENE BREAKDOWN:

🎯 COMPOSITION TECHNIQUES:
• Rule of thirds: Main sphere at center
• Depth layers: Objects at different distances
• Color harmony: Warm/cool color balance
• Leading lines: Sphere arrangement guides the eye

🎨 MATERIALS USED:
• Dielectric (Glass): Transparent, refractive, realistic caustics
• Conductor (Gold): Mirror-like metallic reflections, complex Fresnel
• RoughConductor (Copper): Brushed metal look, controlled roughness
• Plastic (Blue): Glossy coating over diffuse base
• Diffuse (Purple): Matte, non-reflective surface

💡 LIGHTING SETUP (Three-Point + Ambient):
• Key Light: Primary illumination, warm tone (30,30,28), area light for soft shadows
• Fill Light: Reduces harsh shadows, cool tone (8,8,10), from opposite side
• Back Light: Rim lighting for depth, point light for highlight
• Ambient: Subtle blue environment light (0.3,0.3,0.4) for realism

⚙️ RENDER SETTINGS:
• Integrator: Path tracer with 12 bounces (handles complex light paths)
• Samples: 256 per pixel (high quality, low noise)
• Resolution: 1024x768 (HD quality)
• Russian Roulette: Depth 5 (optimization for efficiency)

🎓 ADVANCED CONCEPTS:
• Global Illumination: Light bounces between surfaces (see color bleeding on floor)
• Caustics: Light focused by glass sphere creates patterns
• Fresnel Effect: Reflections vary with viewing angle (especially on metals)
• Soft Shadows: Area lights create realistic, graduated shadows
• Color Temperature: Warm key + cool fill = dimensional lighting

💡 WHY THIS LOOKS GOOD:
✓ Variety: Different materials show different light interactions
✓ Depth: Multiple distance layers create 3D feel
✓ Contrast: Dark and light areas balance
✓ Color: Complementary colors (red/blue/purple) are visually pleasing
✓ Lighting: Professional three-point setup with ambient
✓ Quality: High sample count eliminates noise
"""

ax2.text(0.05, 0.95, scene_info, transform=ax2.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.2))

plt.tight_layout()

annotated_path = os.path.join(output_dir, '04_advanced_scene_annotated.png')
plt.savefig(annotated_path, dpi=150, bbox_inches='tight')
print(f"💾 Annotated version saved to: {annotated_path}")

plt.show()

print("\n" + "=" * 50)
print("🎓 What Makes This Scene Advanced:")
print("\n   1. MULTIPLE MATERIALS")
print("      Different BSDFs interact with light uniquely")
print("\n   2. COMPLEX LIGHTING")
print("      Three-point lighting + ambient for depth")
print("\n   3. HIGH QUALITY")
print("      256 samples per pixel for clean result")
print("\n   4. DEEP RECURSION")
print("      12 bounces capture glass and metal reflections")
print("\n   5. COMPOSITION")
print("      Thoughtful object placement and camera angle")
print("\n💡 Next Steps:")
print("   • Try moving the camera position")
print("   • Add more objects or change positions")
print("   • Experiment with different material combinations")
print("   • Adjust lighting colors and intensities")
print("   • Change the field of view (fov)")
print("   • Try different render qualities (spp: 64, 128, 512)")
print("\n🚀 You're now ready to create your own scenes!")
print("=" * 50)
