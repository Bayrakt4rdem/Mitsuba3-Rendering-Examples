"""
Mitsuba 3 Demo 02: Materials Showcase
======================================

This demo showcases different material types in Mitsuba:
- Diffuse (matte) surfaces
- Conductor (metallic) materials  
- Dielectric (glass/transparent) materials
- Plastic materials
- Different roughness values

Learning Goals:
- Understand BSDF (material) types
- See how roughness affects appearance
- Learn about material properties
- Compare different surface types side-by-side
"""

import mitsuba as mi
import matplotlib.pyplot as plt
import os

mi.set_variant('scalar_rgb')

print("Materials Showcase")
print("=" * 50)

# We'll create 5 spheres with different materials
materials_to_demo = [
    ("Diffuse Red", "diffuse", {'reflectance': {'type': 'rgb', 'value': [0.8, 0.1, 0.1]}}),
    ("Smooth Gold", "conductor", {'material': 'Au'}),  # Gold
    ("Rough Copper", "roughconductor", {'material': 'Cu', 'alpha': 0.3}),  # Copper
    ("Glass", "dielectric", {}),  # Clear glass
    ("Blue Plastic", "plastic", {
        'diffuse_reflectance': {'type': 'rgb', 'value': [0.1, 0.3, 0.8]},
        'nonlinear': True
    })
]

# Scene setup
scene_dict = {
    'type': 'scene',
    
    'integrator': {
        'type': 'path',
        'max_depth': 8,  # Need more bounces for glass/reflections
    },
    
    'sensor': {
        'type': 'perspective',
        'fov': 45,
        'film': {
            'type': 'hdrfilm',
            'width': 800,
            'height': 400,
            'rfilter': {'type': 'gaussian'},
        },
        'sampler': {
            'type': 'independent',
            'sample_count': 128,  # More samples for cleaner glass/metal
        },
        'to_world': mi.ScalarTransform4f.look_at(
            origin=[0, 1, 8],
            target=[0, 0, 0],
            up=[0, 1, 0]
        ),
    },
    
    # Ground plane
    'ground': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.7, 0.7, 0.7]},
        },
        'to_world': mi.ScalarTransform4f.translate([0, -1.5, 0])
                                         .rotate([1, 0, 0], -90)
                                         .scale(10)
    },
    
    # Back wall for reference
    'backwall': {
        'type': 'rectangle',
        'bsdf': {
            'type': 'diffuse',
            'reflectance': {'type': 'rgb', 'value': [0.8, 0.8, 0.9]},
        },
        'to_world': mi.ScalarTransform4f.translate([0, 0, -3])
                                         .scale(10)
    },
    
    # Main area light from above
    'area_light': {
        'type': 'rectangle',
        'emitter': {
            'type': 'area',
            'radiance': {'type': 'rgb', 'value': [20, 20, 20]},
        },
        'to_world': mi.ScalarTransform4f.translate([0, 4, 0])
                                         .rotate([1, 0, 0], -90)
                                         .scale(3)
    },
    
    # Side light for highlights
    'light_side': {
        'type': 'point',
        'intensity': {'type': 'spectrum', 'value': 50.0},
        'position': [-5, 2, 3],
    },
}

# Add spheres with different materials
positions = [-4, -2, 0, 2, 4]  # Spread out horizontally

print("\n📦 Creating materials:")
for i, (name, mat_type, props) in enumerate(materials_to_demo):
    sphere_id = f'sphere_{i}'
    
    # Build BSDF dictionary
    bsdf_dict = {'type': mat_type}
    bsdf_dict.update(props)
    
    scene_dict[sphere_id] = {
        'type': 'sphere',
        'bsdf': bsdf_dict,
        'to_world': mi.ScalarTransform4f.translate([positions[i], 0, 0]).scale(1.0)
    }
    
    print(f"   {i+1}. {name} ({mat_type})")

# Load and render
print("\n🎬 Rendering materials showcase...")
print("   Resolution: 800x400")
print("   Samples per pixel: 128")
print("   This may take 30-60 seconds...")

scene = mi.load_dict(scene_dict)
image = mi.render(scene, spp=128)

print("✅ Rendering complete!")

# Save output
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, '02_materials_showcase.png')
mi.util.write_bitmap(output_path, image)
print(f"\n💾 Image saved to: {output_path}")

# Create annotated visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))

# Show the render
ax1.imshow(mi.util.convert_to_bitmap(image))
ax1.axis('off')
ax1.set_title('Materials Showcase', fontsize=18, fontweight='bold')

# Create material explanation panel
ax2.axis('off')
material_info = """
MATERIAL TYPES EXPLAINED:

1. DIFFUSE (Red Sphere)
   • Matte, non-reflective surface
   • Reflects light equally in all directions (Lambertian)
   • Like: chalk, unpolished wood, paper
   • Properties: reflectance (color)

2. CONDUCTOR (Smooth Gold)
   • Metallic, mirror-like reflections
   • Reflects light based on viewing angle (Fresnel)
   • Like: polished gold, silver, aluminum
   • Properties: material type (Au, Cu, Al, etc.)

3. ROUGHCONDUCTOR (Rough Copper)
   • Metallic with microscopic surface roughness
   • Blurred reflections, brushed metal appearance
   • Like: brushed aluminum, worn copper
   • Properties: material type + alpha (roughness 0-1)

4. DIELECTRIC (Glass)
   • Transparent/translucent materials
   • Both reflects and refracts light
   • Like: glass, water, diamond, plastic
   • Properties: IOR (index of refraction), typically 1.5 for glass

5. PLASTIC (Blue Plastic)
   • Diffuse base with specular coating
   • Combines matte color with glossy highlights
   • Like: plastic toys, painted surfaces
   • Properties: diffuse color + specular properties
"""

ax2.text(0.05, 0.95, material_info, transform=ax2.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()

plt_output = os.path.join(output_dir, '02_materials_showcase_annotated.png')
plt.savefig(plt_output, dpi=150, bbox_inches='tight')
print(f"💾 Annotated version saved to: {plt_output}")

plt.show()

# Print detailed explanations
print("\n" + "=" * 50)
print("🎓 Material Properties Guide:")
print("\nDiffuse:")
print("  - reflectance: [R, G, B] color values (0-1)")
print("\nConductor:")
print("  - material: 'Au' (gold), 'Cu' (copper), 'Al' (aluminum), 'Ag' (silver)")
print("  - eta/k: complex IOR (or use preset materials)")
print("\nRoughConductor:")
print("  - material: same as conductor")
print("  - alpha: roughness (0=mirror, 1=very rough)")
print("  - distribution: 'beckmann' or 'ggx' (microfacet model)")
print("\nDielectric:")
print("  - int_ior: internal index of refraction (1.5 for glass, 1.33 for water)")
print("  - ext_ior: external IOR (usually 1.0 for air)")
print("\nPlastic:")
print("  - diffuse_reflectance: base color")
print("  - specular_reflectance: highlight color")
print("  - nonlinear: True for more realistic plastic")
print("\n💡 Experiment:")
print("   - Change 'alpha' in roughconductor (try 0.1 or 0.8)")
print("   - Try different metals: 'Ag' (silver), 'Al' (aluminum)")
print("   - Adjust 'int_ior' in dielectric (1.33=water, 2.42=diamond)")
print("   - Mix materials on the same sphere (layered BSDF)")
print("=" * 50)
