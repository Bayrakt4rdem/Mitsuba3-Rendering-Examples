"""
Quick Start Guide - Run This First!
====================================

This script helps you verify your Mitsuba installation and
creates a simple test render to make sure everything works.

If this runs successfully, you're ready to explore all the demos!
"""

import sys
import os

print("=" * 60)
print("Mitsuba 3 Quick Start - Installation Verification")
print("=" * 60)

# Check Python version
print(f"\n✓ Python version: {sys.version.split()[0]}")
if sys.version_info < (3, 8):
    print("⚠️  Warning: Python 3.8+ recommended")

# Try importing dependencies
print("\n📦 Checking dependencies...")

try:
    import numpy as np
    print(f"✓ NumPy {np.__version__}")
except ImportError:
    print("✗ NumPy not found - install with: pip install numpy")
    sys.exit(1)

try:
    import matplotlib
    print(f"✓ Matplotlib {matplotlib.__version__}")
except ImportError:
    print("✗ Matplotlib not found - install with: pip install matplotlib")
    sys.exit(1)

try:
    from PIL import Image
    print(f"✓ Pillow (PIL) {Image.__version__ if hasattr(Image, '__version__') else 'installed'}")
except ImportError:
    print("⚠️  Pillow not found (optional) - install with: pip install pillow")

try:
    import mitsuba as mi
    print(f"✓ Mitsuba {mi.__version__}")
except ImportError:
    print("\n✗ Mitsuba not found!")
    print("\nInstallation steps:")
    print("1. Activate virtual environment:")
    print("   .\\mitsuba_venv\\Scripts\\Activate.ps1")
    print("2. Install Mitsuba:")
    print("   pip install mitsuba")
    sys.exit(1)

# Check available variants
print(f"\n🎨 Available render modes (variants):")
variants = mi.variants()
for variant in variants:
    print(f"   • {variant}")

# Set variant
print("\n⚙️  Setting render mode to 'scalar_rgb'...")
try:
    mi.set_variant('scalar_rgb')
    print("✓ Render mode set successfully")
except Exception as e:
    print(f"✗ Error setting variant: {e}")
    sys.exit(1)

# Create a minimal test scene
print("\n🎬 Creating test scene...")

test_scene = {
    'type': 'scene',
    'integrator': {'type': 'path'},
    'sensor': {
        'type': 'perspective',
        'fov': 45,
        'film': {
            'type': 'hdrfilm',
            'width': 256,
            'height': 256,
        },
        'sampler': {'type': 'independent', 'sample_count': 16},
        'to_world': mi.ScalarTransform4f.look_at(
            origin=[0, 0, 3],
            target=[0, 0, 0],
            up=[0, 1, 0]
        ),
    },
    'sphere': {
        'type': 'sphere',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.8, 0.2, 0.2]},
        },
    },
    'light': {
        'type': 'point',
        'intensity': {'type': 'spectrum', 'value': 50.0},
        'position': [2, 2, 2],
    },
}

try:
    scene = mi.load_dict(test_scene)
    print("✓ Scene created successfully")
except Exception as e:
    print(f"✗ Error creating scene: {e}")
    sys.exit(1)

# Render test
print("\n🎨 Rendering test image (this will take a few seconds)...")
try:
    image = mi.render(scene, spp=16)
    print("✓ Rendering successful!")
except Exception as e:
    print(f"✗ Render error: {e}")
    sys.exit(1)

# Save test image
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'test_render.png')

try:
    mi.util.write_bitmap(output_path, image)
    print(f"\n💾 Test image saved to: {output_path}")
except Exception as e:
    print(f"⚠️  Could not save image: {e}")

# Show with matplotlib
try:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 8))
    plt.imshow(mi.util.convert_to_bitmap(image))
    plt.axis('off')
    plt.title('Test Render - Installation Successful!', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    preview_path = os.path.join(output_dir, 'test_render_preview.png')
    plt.savefig(preview_path, dpi=100, bbox_inches='tight')
    print(f"💾 Preview saved to: {preview_path}")
    
    plt.show()
except Exception as e:
    print(f"⚠️  Could not display image: {e}")

# Summary
print("\n" + "=" * 60)
print("🎉 SUCCESS! Mitsuba 3 is installed and working!")
print("=" * 60)
print("\n📚 You're ready to explore the demos:")
print("\n   Beginner:")
print("   1. python 01_basic_scene.py        - Learn the basics")
print("   2. python 02_materials_showcase.py - Explore materials")
print("   3. python 05_cornell_box.py        - Classic demo")
print("\n   Intermediate:")
print("   4. python 03_lighting_techniques.py - Master lighting")
print("\n   Advanced:")
print("   5. python 04_advanced_scene.py      - Complex scene")
print("\n💡 Tip: Start with 01_basic_scene.py if you're new!")
print("\n📖 Don't forget to read README.md for detailed info")
print("=" * 60)
