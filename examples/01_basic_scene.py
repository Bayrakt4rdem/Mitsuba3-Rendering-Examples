"""
Mitsuba 3 Demo 01: Basic Scene
================================

This is your first Mitsuba 3 program! We'll create a simple scene with:
- A red sphere in the center
- A white ground plane
- A point light source
- A perspective camera

Learning Goals:
- Understand basic scene structure
- Learn how to create shapes
- Set up a camera
- Add lighting
- Render and save an image
"""

import mitsuba as mi
import matplotlib.pyplot as plt
import os

# Set the variant - this determines the rendering mode
# 'scalar_rgb' is good for learning - it's simple and works on all systems
mi.set_variant('scalar_rgb')

print("Creating a basic scene...")
print("=" * 50)

# Define the scene as a dictionary
# This is how Mitsuba describes scenes - like XML but in Python
scene_dict = {
    # The integrator determines HOW we render
    # 'path' = path tracing, physically accurate, handles indirect lighting
    'type': 'scene',
    
    # Integrator: The rendering algorithm
    'integrator': {
        'type': 'path',          # Path tracer - realistic rendering
        'max_depth': 6,          # Maximum number of light bounces
    },
    
    # Sensor: The camera
    'sensor': {
        'type': 'perspective',   # Standard perspective camera
        'fov': 45,               # Field of view in degrees
        
        # Film: The "sensor" that captures the image
        'film': {
            'type': 'hdrfilm',   # High dynamic range film
            'width': 512,        # Image width in pixels
            'height': 512,       # Image height in pixels
            'rfilter': {         # Reconstruction filter for anti-aliasing
                'type': 'gaussian'
            },
        },
        
        # Sampler: Determines how many rays per pixel
        'sampler': {
            'type': 'independent',
            'sample_count': 64,  # More samples = better quality but slower
        },
        
        # Camera position and orientation
        'to_world': mi.ScalarTransform4f.look_at(
            origin=[0, 0, 5],    # Camera position: 5 units back
            target=[0, 0, 0],    # Look at: center of scene
            up=[0, 1, 0]         # Up direction: Y axis
        ),
    },
    
    # The main sphere - our star object!
    'sphere': {
        'type': 'sphere',        # Shape type
        
        # BSDF: Bidirectional Scattering Distribution Function
        # This determines how light interacts with the surface
        'bsdf': {
            'type': 'diffuse',   # Matte/Lambertian surface
            'reflectance': {     # Surface color
                'type': 'rgb',
                'value': [0.8, 0.1, 0.1],  # RGB: Red sphere
            }
        },
        
        # Transform: Position, rotation, scale
        'to_world': mi.ScalarTransform4f.translate([0, 0, 0]).scale(1.0)
    },
    
    # Ground plane - so the sphere has something to sit on
    'ground': {
        'type': 'rectangle',     # Flat rectangular shape
        
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {
                'type': 'rgb',
                'value': [0.8, 0.8, 0.8],  # Light gray
            }
        },
        
        # Rotate and position the plane
        'to_world': mi.ScalarTransform4f.translate([0, -1, 0])
                                         .rotate([1, 0, 0], -90)  # Rotate to horizontal
                                         .scale(5)  # Make it bigger
    },
    
    # Light source - let there be light!
    'light': {
        'type': 'point',         # Point light (like a light bulb)
        'intensity': {
            'type': 'spectrum',
            'value': 100.0,      # Brightness
        },
        'position': [5, 5, 5],   # Upper right
    }
}

print("\n📦 Scene Components:")
print("   - Red sphere (center)")
print("   - Gray ground plane")
print("   - Point light (upper right)")
print("   - Perspective camera (looking at center)")

# Load the scene from our dictionary
scene = mi.load_dict(scene_dict)

print("\n🎬 Rendering...")
print("   Resolution: 512x512")
print("   Samples per pixel: 64")
print("   Max ray bounces: 6")

# Render the scene!
# This is where the magic happens
image = mi.render(scene, spp=64)  # spp = samples per pixel

print("✅ Rendering complete!")

# Create output directory if it doesn't exist
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Save the image
output_path = os.path.join(output_dir, '01_basic_scene.png')
mi.util.write_bitmap(output_path, image)

print(f"\n💾 Image saved to: {output_path}")

# Display the image using matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(mi.util.convert_to_bitmap(image))
plt.axis('off')
plt.title('Basic Scene: Red Sphere with Point Light', fontsize=16)
plt.tight_layout()

# Save matplotlib figure too
plt_output = os.path.join(output_dir, '01_basic_scene_preview.png')
plt.savefig(plt_output, dpi=150, bbox_inches='tight')
print(f"💾 Preview saved to: {plt_output}")

plt.show()

print("\n" + "=" * 50)
print("🎓 What You Learned:")
print("   ✓ Scene structure (integrator, sensor, shapes, lights)")
print("   ✓ Creating basic shapes (sphere, rectangle)")
print("   ✓ Setting up a camera with look_at()")
print("   ✓ Adding a point light")
print("   ✓ Rendering and saving images")
print("\n💡 Try This:")
print("   - Change the sphere color in 'reflectance'")
print("   - Move the light to a different position")
print("   - Adjust the camera 'fov' (try 30 or 70)")
print("   - Change 'sample_count' (try 16 or 256)")
print("=" * 50)
