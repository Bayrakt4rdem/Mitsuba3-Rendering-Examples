"""
Mitsuba 3 Demo 03: Lighting Techniques
=======================================

Explore different lighting setups:
- Point lights (omni-directional)
- Directional lights (sun-like)
- Area lights (soft shadows)
- Environment lighting (HDRI-style)
- Multiple light combinations

Learning Goals:
- Understand different light types
- See how lighting affects mood and appearance
- Learn about hard vs soft shadows
- Master lighting intensity and color
"""

import mitsuba as mi
import matplotlib.pyplot as plt
import os

mi.set_variant('scalar_rgb')

print("Lighting Techniques Demo")
print("=" * 50)

def create_scene_with_lighting(light_config, title):
    """Helper function to create a scene with specific lighting"""
    
    base_scene = {
        'type': 'scene',
        'integrator': {
            'type': 'path',
            'max_depth': 6,
        },
        'sensor': {
            'type': 'perspective',
            'fov': 45,
            'film': {
                'type': 'hdrfilm',
                'width': 600,
                'height': 600,
                'rfilter': {'type': 'gaussian'},
            },
            'sampler': {
                'type': 'independent',
                'sample_count': 64,
            },
            'to_world': mi.ScalarTransform4f.look_at(
                origin=[4, 3, 8],
                target=[0, 0, 0],
                up=[0, 1, 0]
            ),
        },
        
        # Main sphere
        'sphere': {
            'type': 'sphere',
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {'type': 'rgb', 'value': [0.8, 0.3, 0.3]},
            },
            'to_world': mi.ScalarTransform4f.translate([0, 0, 0]).scale(1.0)
        },
        
        # Ground
        'ground': {
            'type': 'rectangle',
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {'type': 'rgb', 'value': [0.6, 0.6, 0.6]},
            },
            'to_world': mi.ScalarTransform4f.translate([0, -1.5, 0])
                                             .rotate([1, 0, 0], -90)
                                             .scale(8)
        },
        
        # Back wall
        'wall': {
            'type': 'rectangle',
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {'type': 'rgb', 'value': [0.7, 0.7, 0.8]},
            },
            'to_world': mi.ScalarTransform4f.translate([0, 0, -3])
                                             .scale(8)
        },
    }
    
    # Add the specific light configuration
    base_scene.update(light_config)
    
    return base_scene, title


# Define different lighting setups
lighting_configs = [
    # 1. Single point light
    (
        {
            'light1': {
                'type': 'point',
                'intensity': {'type': 'spectrum', 'value': 80.0},
                'position': [3, 4, 4],
            }
        },
        "Point Light (Hard Shadows)"
    ),
    
    # 2. Area light (soft shadows)
    (
        {
            'area_light': {
                'type': 'rectangle',
                'emitter': {
                    'type': 'area',
                    'radiance': {'type': 'rgb', 'value': [15, 15, 15]},
                },
                'to_world': mi.ScalarTransform4f.translate([2, 4, 3])
                                                 .rotate([1, 0, 0], -45)
                                                 .scale(2)
            }
        },
        "Area Light (Soft Shadows)"
    ),
    
    # 3. Directional light (sun)
    (
        {
            'sun': {
                'type': 'directional',
                'direction': [-1, -1, -1],
                'irradiance': {'type': 'rgb', 'value': [3, 3, 3]},
            }
        },
        "Directional Light (Sun)"
    ),
    
    # 4. Three-point lighting (professional)
    (
        {
            'key_light': {  # Main light
                'type': 'point',
                'intensity': {'type': 'spectrum', 'value': 60.0},
                'position': [4, 4, 4],
            },
            'fill_light': {  # Fill shadows
                'type': 'point',
                'intensity': {'type': 'spectrum', 'value': 20.0},
                'position': [-3, 2, 3],
            },
            'back_light': {  # Rim lighting
                'type': 'point',
                'intensity': {'type': 'spectrum', 'value': 30.0},
                'position': [0, 3, -3],
            }
        },
        "Three-Point Lighting"
    ),
    
    # 5. Environment lighting
    (
        {
            'env': {
                'type': 'envmap',
                'filename': None,  # We'll use constant
                'emitter': {
                    'type': 'constant',
                    'radiance': {'type': 'rgb', 'value': [1.5, 1.5, 1.5]},
                }
            }
        },
        "Environment Lighting"
    ),
    
    # 6. Colored lights
    (
        {
            'light_red': {
                'type': 'point',
                'intensity': {'type': 'rgb', 'value': [100, 20, 20]},  # Red
                'position': [3, 3, 3],
            },
            'light_blue': {
                'type': 'point',
                'intensity': {'type': 'rgb', 'value': [20, 20, 100]},  # Blue
                'position': [-3, 3, 3],
            }
        },
        "Colored Lights (Red + Blue)"
    ),
]

print(f"\n🎬 Rendering {len(lighting_configs)} lighting setups...")
print("   This will take 2-3 minutes total...")

output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

images = []
titles = []

for i, (light_config, title) in enumerate(lighting_configs, 1):
    print(f"\n   [{i}/{len(lighting_configs)}] {title}...")
    
    # Handle environment map specially
    if 'env' in light_config and light_config['env']['filename'] is None:
        # For constant environment, simplify
        scene_dict, scene_title = create_scene_with_lighting({}, title)
        scene_dict['constant_emitter'] = {
            'type': 'constant',
            'radiance': {'type': 'rgb', 'value': [1.5, 1.5, 1.5]},
        }
    else:
        scene_dict, scene_title = create_scene_with_lighting(light_config, title)
    
    scene = mi.load_dict(scene_dict)
    image = mi.render(scene, spp=64)
    
    images.append(mi.util.convert_to_bitmap(image))
    titles.append(scene_title)
    
    # Save individual image
    filename = f"03_lighting_{i:02d}_{title.lower().replace(' ', '_').replace('(', '').replace(')', '')}.png"
    mi.util.write_bitmap(os.path.join(output_dir, filename), image)

print("\n✅ All renders complete!")

# Create comparison grid
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for idx, (img, title) in enumerate(zip(images, titles)):
    axes[idx].imshow(img)
    axes[idx].axis('off')
    axes[idx].set_title(title, fontsize=14, fontweight='bold')

plt.suptitle('Lighting Techniques Comparison', fontsize=20, fontweight='bold')
plt.tight_layout()

comparison_path = os.path.join(output_dir, '03_lighting_comparison.png')
plt.savefig(comparison_path, dpi=150, bbox_inches='tight')
print(f"\n💾 Comparison grid saved to: {comparison_path}")

plt.show()

# Print explanations
print("\n" + "=" * 50)
print("🎓 Lighting Types Explained:")
print("\n1. POINT LIGHT")
print("   • Emits light in all directions from a single point")
print("   • Creates hard, sharp shadows")
print("   • Like: bare light bulb, candle")
print("   • Properties: intensity, position")
print("\n2. AREA LIGHT")
print("   • Light emitted from a surface area")
print("   • Creates soft, realistic shadows")
print("   • Like: softbox, window, LED panel")
print("   • Properties: radiance, shape, size")
print("\n3. DIRECTIONAL LIGHT")
print("   • Parallel rays from infinity (sun-like)")
print("   • Consistent shadow direction")
print("   • Like: sunlight, moonlight")
print("   • Properties: direction, irradiance")
print("\n4. THREE-POINT LIGHTING")
print("   • Key light: main illumination (brightest)")
print("   • Fill light: softens shadows (dimmer)")
print("   • Back light: rim lighting, separation from background")
print("   • Professional photography/cinematography standard")
print("\n5. ENVIRONMENT LIGHTING")
print("   • Light coming from all directions (sky dome)")
print("   • Can use HDRI images for realistic outdoor lighting")
print("   • Soft, ambient illumination")
print("   • Properties: radiance map or constant value")
print("\n6. COLORED LIGHTS")
print("   • Lights can have any RGB color")
print("   • Creates dramatic color mixing")
print("   • Used for artistic effects, mood lighting")
print("   • Properties: RGB intensity values")
print("\n💡 Lighting Tips:")
print("   • More light sources = softer overall lighting")
print("   • Area lights = realistic soft shadows (but slower to render)")
print("   • Point lights = fast rendering, hard shadows")
print("   • Three-point lighting = professional look")
print("   • Color temperature: warm (orange) vs cool (blue)")
print("\n🔧 Try Experimenting:")
print("   • Change light positions")
print("   • Adjust intensity values")
print("   • Mix different light types")
print("   • Add more lights to a scene")
print("   • Change light colors for mood")
print("=" * 50)
