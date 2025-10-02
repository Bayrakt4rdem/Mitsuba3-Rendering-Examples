"""
Mitsuba 3 Demo 05: Cornell Box
===============================

The Cornell Box is the "Hello World" of physically-based rendering!

Originally created at Cornell University in 1984, this simple scene
is perfect for understanding:
- Global illumination (indirect lighting)
- Color bleeding (light bouncing between colored surfaces)
- Soft shadows
- Light transport simulation

Learning Goals:
- Understand global illumination
- See color bleeding in action
- Learn about indirect lighting
- Benchmark rendering quality
- Classic computer graphics reference scene
"""

import mitsuba as mi
import matplotlib.pyplot as plt
import os

mi.set_variant('scalar_rgb')

print("Cornell Box Demo")
print("=" * 50)
print("Rendering the famous Cornell Box...")
print("This scene demonstrates global illumination!\n")

# The Cornell Box dimensions (standard)
# All coordinates are relative to a unit box
scene_dict = {
    'type': 'scene',
    
    # Path tracer is essential for global illumination
    'integrator': {
        'type': 'path',
        'max_depth': 8,  # Need several bounces to see color bleeding
    },
    
    'sensor': {
        'type': 'perspective',
        'fov': 39.3,  # Matches original Cornell Box camera
        'film': {
            'type': 'hdrfilm',
            'width': 512,
            'height': 512,
            'rfilter': {'type': 'gaussian'},
        },
        'sampler': {
            'type': 'independent',
            'sample_count': 256,  # High quality for clean indirect lighting
        },
        # Camera looking into the box
        'to_world': mi.ScalarTransform4f.look_at(
            origin=[0, 1, 6.8],   # Looking into the box
            target=[0, 1, 0],
            up=[0, 1, 0]
        ),
    },
    
    # Back wall - white
    'back_wall': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.73, 0.73, 0.73]},
        },
        'to_world': mi.ScalarTransform4f.translate([0, 1, -1.99])
                                         .scale(2)
    },
    
    # Floor - white
    'floor': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.73, 0.73, 0.73]},
        },
        'to_world': mi.ScalarTransform4f.translate([0, -1, 0])
                                         .rotate([1, 0, 0], -90)
                                         .scale(2)
    },
    
    # Ceiling - white
    'ceiling': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.73, 0.73, 0.73]},
        },
        'to_world': mi.ScalarTransform4f.translate([0, 3, 0])
                                         .rotate([1, 0, 0], -90)
                                         .scale(2)
    },
    
    # Left wall - RED (this is key for color bleeding!)
    'left_wall': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.63, 0.065, 0.05]},  # Red
        },
        'to_world': mi.ScalarTransform4f.translate([2, 1, 0])
                                         .rotate([0, 1, 0], -90)
                                         .scale(2)
    },
    
    # Right wall - GREEN (opposite colored wall)
    'right_wall': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.14, 0.45, 0.091]},  # Green
        },
        'to_world': mi.ScalarTransform4f.translate([-2, 1, 0])
                                         .rotate([0, 1, 0], 90)
                                         .scale(2)
    },
    
    # Tall box - white
    'tall_box': {
        'type': 'cube',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.73, 0.73, 0.73]},
        },
        'to_world': mi.ScalarTransform4f.translate([-0.7, -0.15, -0.5])
                                         .rotate([0, 1, 0], -18)
                                         .scale([0.6, 1.65, 0.6])
    },
    
    # Short box - white
    'short_box': {
        'type': 'cube',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.73, 0.73, 0.73]},
        },
        'to_world': mi.ScalarTransform4f.translate([0.7, -0.6, 0.5])
                                         .rotate([0, 1, 0], 16)
                                         .scale([0.6, 0.8, 0.6])
    },
    
    # Area light on ceiling - this is crucial!
    # The area light creates soft shadows and enables global illumination
    'area_light': {
        'type': 'rectangle',
        'emitter': {
            'type': 'area',
            'radiance': {'type': 'rgb', 'value': [18.4, 15.6, 8.0]},  # Slightly warm white
        },
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0, 0, 0]},  # Black (doesn't reflect)
        },
        # Small light in center of ceiling
        'to_world': mi.ScalarTransform4f.translate([0, 2.99, 0])
                                         .rotate([1, 0, 0], -90)
                                         .scale(0.5)
    },
}

print("📦 Cornell Box components:")
print("   • 5 walls (back, floor, ceiling, left red, right green)")
print("   • 2 white boxes (tall and short)")
print("   • 1 area light (ceiling)")
print("\n🎨 The magic:")
print("   • Red wall bounces red light onto nearby objects")
print("   • Green wall bounces green light onto nearby objects")
print("   • Area light creates soft, realistic shadows")
print("   • Multiple light bounces = global illumination")

print("\n🎬 Rendering Cornell Box...")
print("   Resolution: 512x512")
print("   Samples per pixel: 256")
print("   Max bounces: 8")
print("   ⏱️  This will take 1-2 minutes...")

scene = mi.load_dict(scene_dict)
image = mi.render(scene, spp=256)

print("✅ Rendering complete!")

# Save output
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, '05_cornell_box.png')
mi.util.write_bitmap(output_path, image)
print(f"\n💾 Image saved to: {output_path}")

# Create detailed visualization
fig = plt.figure(figsize=(16, 12))

# Main render
ax1 = plt.subplot(2, 2, (1, 2))
ax1.imshow(mi.util.convert_to_bitmap(image))
ax1.axis('off')
ax1.set_title('Cornell Box - Global Illumination Demo', fontsize=18, fontweight='bold', pad=20)

# Add annotations for color bleeding
from matplotlib.patches import Circle, FancyBboxPatch
# Highlight red color bleeding on tall box (left side)
circle1 = Circle((128, 300), 30, fill=False, edgecolor='red', linewidth=3)
ax1.add_patch(circle1)
ax1.text(128, 360, 'Red color\nbleeding', ha='center', color='red', 
         fontweight='bold', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Highlight green color bleeding on short box (right side)
circle2 = Circle((384, 380), 30, fill=False, edgecolor='green', linewidth=3)
ax1.add_patch(circle2)
ax1.text(384, 440, 'Green color\nbleeding', ha='center', color='green', 
         fontweight='bold', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Explanation panel
ax2 = plt.subplot(2, 2, 3)
ax2.axis('off')

explanation = """
🎓 WHAT IS THE CORNELL BOX?

Created in 1984 at Cornell University to test
physically-based rendering algorithms.

🌟 KEY CONCEPTS DEMONSTRATED:

1. GLOBAL ILLUMINATION
   Light bounces multiple times before
   reaching the camera. Not just direct
   light from the source!

2. COLOR BLEEDING
   Red wall reflects red light onto nearby
   white boxes → boxes look reddish
   Green wall reflects green light → boxes
   look greenish on that side

3. INDIRECT LIGHTING
   Most of the light you see is reflected
   from walls and objects, not directly
   from the light source

4. SOFT SHADOWS
   Area light creates gradual shadow edges
   (unlike point lights with hard shadows)
"""

ax2.text(0.05, 0.95, explanation, transform=ax2.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))

# Technical details panel
ax3 = plt.subplot(2, 2, 4)
ax3.axis('off')

technical = """
⚙️ TECHNICAL DETAILS:

LIGHT TRANSPORT:
• Light starts from area light
• Bounces off ceiling (diffuse)
• Hits walls (red/green/white)
• Bounces again to other surfaces
• Eventually reaches camera

Each bounce carries color information!

RENDER SETTINGS:
• Path tracer integrator
• 8 maximum bounces
• 256 samples per pixel
• Diffuse (Lambertian) materials
• Area light for soft illumination

WHY IT'S IMPORTANT:
✓ Validates rendering accuracy
✓ Tests global illumination
✓ Benchmarks performance
✓ Standard reference scene
✓ Used in research papers

WHAT TO LOOK FOR:
👁️ Soft shadow under boxes
👁️ Red tint on left box sides
👁️ Green tint on right box sides
👁️ Bright ceiling near light
👁️ Gradual light falloff
"""

ax3.text(0.05, 0.95, technical, transform=ax3.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

plt.tight_layout()

annotated_path = os.path.join(output_dir, '05_cornell_box_annotated.png')
plt.savefig(annotated_path, dpi=150, bbox_inches='tight')
print(f"💾 Annotated version saved to: {annotated_path}")

plt.show()

print("\n" + "=" * 50)
print("🎓 Understanding Global Illumination:")
print("\n   Without global illumination (direct lighting only):")
print("   • Boxes would be pure white")
print("   • Hard black shadows")
print("   • Unrealistic appearance")
print("\n   With global illumination (what you see here):")
print("   • Color bleeding from walls")
print("   • Soft, realistic shadows")
print("   • Ambient lighting in shadowed areas")
print("   • Natural, photorealistic look")
print("\n💡 Experiment:")
print("   • Try max_depth=1 (direct lighting only) - see the difference!")
print("   • Change wall colors")
print("   • Move or resize the boxes")
print("   • Adjust light intensity")
print("   • Try different sample counts (16, 64, 512)")
print("\n📚 Historical Note:")
print("   The Cornell Box is to rendering what 'Hello World' is to")
print("   programming - a standard test that everyone uses!")
print("=" * 50)
