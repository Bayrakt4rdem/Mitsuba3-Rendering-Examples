"""
Inverse Rendering Examples - Demonstrate 2D→3D capabilities

This script shows how to use Mitsuba 3's differentiable rendering
for inverse problems like material estimation and shape optimization.

IMPORTANT: These examples require the 'llvm_ad_rgb' or 'cuda_ad_rgb' variant!
"""

import sys
from pathlib import Path

def check_variant():
    """Check if differentiable variant is available"""
    try:
        import mitsuba as mi
        variants = mi.variants()
        
        has_ad = any('_ad_' in v for v in variants)
        
        if not has_ad:
            print("=" * 70)
            print("⚠️  WARNING: No differentiable variants found!")
            print("=" * 70)
            print("\nYou need to install Mitsuba 3 with AD support:")
            print("  pip uninstall mitsuba")
            print("  pip install mitsuba[ad]")
            print("\nOr build from source with AD variants enabled.")
            print("=" * 70)
            return False
        
        print("✓ Differentiable variants available:")
        for v in variants:
            if '_ad_' in v:
                print(f"  - {v}")
        return True
        
    except ImportError:
        print("✗ Mitsuba 3 not installed!")
        return False


def example_1_optimize_albedo():
    """
    Example 1: Texture/Albedo Optimization
    
    Task: Given a photo of an object with known lighting,
          recover the albedo (base color) texture.
    """
    import mitsuba as mi
    import drjit as dr
    import numpy as np
    from PIL import Image
    
    print("\n" + "="*70)
    print("Example 1: Albedo Recovery from Image")
    print("="*70)
    
    # Use AD variant
    mi.set_variant('llvm_ad_rgb')
    
    # Step 1: Create "ground truth" scene (what we're trying to recover)
    print("\n1. Creating ground truth scene...")
    target_albedo = [0.8, 0.3, 0.1]  # Orange color - this is what we want to find
    
    target_scene = mi.load_dict({
        'type': 'scene',
        'integrator': {'type': 'path'},
        'sensor': {
            'type': 'perspective',
            'fov': 45,
            'to_world': mi.ScalarTransform4f.look_at(
                origin=[0, 0, 4],
                target=[0, 0, 0],
                up=[0, 1, 0]
            ),
            'film': {
                'type': 'hdrfilm',
                'width': 128,
                'height': 128,
            }
        },
        'sphere': {
            'type': 'sphere',
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': target_albedo  # Ground truth albedo
                }
            }
        },
        'light': {
            'type': 'point',
            'position': [3, 3, 3],
            'intensity': {'type': 'spectrum', 'value': 50.0}
        }
    })
    
    # Render target image
    print("2. Rendering target image...")
    target_image = mi.render(target_scene, spp=64)
    
    # Step 2: Create optimization scene (start with wrong albedo)
    print("3. Creating optimization scene with initial guess...")
    initial_albedo = [0.5, 0.5, 0.5]  # Gray - wrong initial guess
    
    opt_scene = mi.load_dict({
        'type': 'scene',
        'integrator': {'type': 'path'},
        'sensor': {
            'type': 'perspective',
            'fov': 45,
            'to_world': mi.ScalarTransform4f.look_at(
                origin=[0, 0, 4],
                target=[0, 0, 0],
                up=[0, 1, 0]
            ),
            'film': {
                'type': 'hdrfilm',
                'width': 128,
                'height': 128,
            }
        },
        'sphere': {
            'type': 'sphere',
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': initial_albedo
                }
            }
        },
        'light': {
            'type': 'point',
            'position': [3, 3, 3],
            'intensity': {'type': 'spectrum', 'value': 50.0}
        }
    })
    
    # Step 3: Set up optimization
    print("4. Setting up optimization...")
    params = mi.traverse(opt_scene)
    
    # Make albedo differentiable
    key = 'sphere.bsdf.reflectance.value'
    params.keep([key])
    
    # Optimizer
    opt = mi.ad.Adam(lr=0.05)
    
    # Step 4: Optimization loop
    print("5. Optimizing albedo...")
    print(f"\n{'Iter':<8} {'Loss':<12} {'Albedo R':<10} {'Albedo G':<10} {'Albedo B':<10}")
    print("-" * 60)
    
    for i in range(50):
        # Render with current albedo
        current_image = mi.render(opt_scene, params, spp=4)
        
        # Compute loss (MSE)
        loss = dr.mean(dr.sqr(current_image - target_image))
        
        # Backpropagation
        dr.backward(loss)
        
        # Optimizer step
        opt.step(params)
        
        # Get current albedo value
        current_albedo = params[key]
        
        # Print progress
        if i % 10 == 0:
            print(f"{i:<8} {loss[0]:<12.6f} {current_albedo[0]:<10.4f} {current_albedo[1]:<10.4f} {current_albedo[2]:<10.4f}")
        
        # Update scene
        params.update()
    
    # Final result
    final_albedo = params[key]
    print("\n" + "="*60)
    print(f"Target albedo:  [{target_albedo[0]:.4f}, {target_albedo[1]:.4f}, {target_albedo[2]:.4f}]")
    print(f"Recovered:      [{final_albedo[0]:.4f}, {final_albedo[1]:.4f}, {final_albedo[2]:.4f}]")
    print(f"Error:          {abs(final_albedo[0] - target_albedo[0]):.4f}, {abs(final_albedo[1] - target_albedo[1]):.4f}, {abs(final_albedo[2] - target_albedo[2]):.4f}")
    print("="*60)
    
    print("\n✓ Albedo recovery complete!")


def example_2_optimize_position():
    """
    Example 2: Object Position Optimization
    
    Task: Given an image, recover the 3D position of an object.
    """
    import mitsuba as mi
    import drjit as dr
    import numpy as np
    
    print("\n" + "="*70)
    print("Example 2: 3D Position Recovery from Image")
    print("="*70)
    
    mi.set_variant('llvm_ad_rgb')
    
    # Ground truth position
    target_pos = [1.5, 0.5, 1.0]
    
    print(f"\n1. Target position: {target_pos}")
    
    # Create target scene
    target_scene = mi.load_dict({
        'type': 'scene',
        'integrator': {'type': 'path'},
        'sensor': {
            'type': 'perspective',
            'fov': 45,
            'to_world': mi.ScalarTransform4f.look_at(
                origin=[5, 5, 3],
                target=[0, 0, 1],
                up=[0, 1, 0]
            ),
            'film': {'type': 'hdrfilm', 'width': 128, 'height': 128}
        },
        'sphere': {
            'type': 'sphere',
            'center': target_pos,
            'radius': 0.5,
            'bsdf': {'type': 'diffuse', 'reflectance': {'type': 'rgb', 'value': [0.8, 0.2, 0.2]}}
        },
        'ground': {
            'type': 'rectangle',
            'to_world': mi.ScalarTransform4f.scale(10),
            'bsdf': {'type': 'diffuse', 'reflectance': {'type': 'rgb', 'value': [0.5, 0.5, 0.5]}}
        },
        'light': {
            'type': 'point',
            'position': [5, 5, 5],
            'intensity': {'type': 'spectrum', 'value': 100.0}
        }
    })
    
    target_image = mi.render(target_scene, spp=32)
    
    # Optimization scene with wrong initial position
    initial_pos = [0.0, 0.0, 0.5]
    print(f"2. Initial guess: {initial_pos}")
    
    opt_scene = mi.load_dict({
        'type': 'scene',
        'integrator': {'type': 'path'},
        'sensor': {
            'type': 'perspective',
            'fov': 45,
            'to_world': mi.ScalarTransform4f.look_at(
                origin=[5, 5, 3],
                target=[0, 0, 1],
                up=[0, 1, 0]
            ),
            'film': {'type': 'hdrfilm', 'width': 128, 'height': 128}
        },
        'sphere': {
            'type': 'sphere',
            'center': initial_pos,
            'radius': 0.5,
            'bsdf': {'type': 'diffuse', 'reflectance': {'type': 'rgb', 'value': [0.8, 0.2, 0.2]}}
        },
        'ground': {
            'type': 'rectangle',
            'to_world': mi.ScalarTransform4f.scale(10),
            'bsdf': {'type': 'diffuse', 'reflectance': {'type': 'rgb', 'value': [0.5, 0.5, 0.5]}}
        },
        'light': {
            'type': 'point',
            'position': [5, 5, 5],
            'intensity': {'type': 'spectrum', 'value': 100.0}
        }
    })
    
    params = mi.traverse(opt_scene)
    params.keep(['sphere.center'])
    
    opt = mi.ad.Adam(lr=0.1)
    
    print("\n3. Optimizing position...")
    print(f"\n{'Iter':<8} {'Loss':<12} {'Pos X':<10} {'Pos Y':<10} {'Pos Z':<10}")
    print("-" * 60)
    
    for i in range(100):
        current_image = mi.render(opt_scene, params, spp=4)
        loss = dr.mean(dr.sqr(current_image - target_image))
        
        dr.backward(loss)
        opt.step(params)
        params.update()
        
        if i % 20 == 0:
            pos = params['sphere.center']
            print(f"{i:<8} {loss[0]:<12.6f} {pos[0]:<10.4f} {pos[1]:<10.4f} {pos[2]:<10.4f}")
    
    final_pos = params['sphere.center']
    print("\n" + "="*60)
    print(f"Target position: [{target_pos[0]:.4f}, {target_pos[1]:.4f}, {target_pos[2]:.4f}]")
    print(f"Recovered:       [{final_pos[0]:.4f}, {final_pos[1]:.4f}, {final_pos[2]:.4f}]")
    print("="*60)
    
    print("\n✓ Position recovery complete!")


def example_3_light_estimation():
    """
    Example 3: Lighting Estimation
    
    Task: Given an image of an object with known geometry and material,
          recover the light position and intensity.
    """
    import mitsuba as mi
    import drjit as dr
    
    print("\n" + "="*70)
    print("Example 3: Light Source Recovery from Image")
    print("="*70)
    
    mi.set_variant('llvm_ad_rgb')
    
    # Ground truth light
    target_light_pos = [3.0, -2.0, 4.0]
    target_intensity = 80.0
    
    print(f"\n1. Target light position: {target_light_pos}")
    print(f"   Target intensity: {target_intensity}")
    
    # Create target scene
    target_scene = mi.load_dict({
        'type': 'scene',
        'integrator': {'type': 'path'},
        'sensor': {
            'type': 'perspective',
            'fov': 45,
            'to_world': mi.ScalarTransform4f.look_at(
                origin=[0, -5, 2],
                target=[0, 0, 1],
                up=[0, 0, 1]
            ),
            'film': {'type': 'hdrfilm', 'width': 128, 'height': 128}
        },
        'sphere': {
            'type': 'sphere',
            'center': [0, 0, 1],
            'radius': 1.0,
            'bsdf': {'type': 'diffuse', 'reflectance': {'type': 'rgb', 'value': [0.8, 0.8, 0.8]}}
        },
        'light': {
            'type': 'point',
            'position': target_light_pos,
            'intensity': {'type': 'spectrum', 'value': target_intensity}
        }
    })
    
    target_image = mi.render(target_scene, spp=32)
    
    # Optimization scene
    initial_light_pos = [0.0, 0.0, 3.0]
    initial_intensity = 50.0
    
    print(f"2. Initial guess - position: {initial_light_pos}, intensity: {initial_intensity}")
    
    opt_scene = mi.load_dict({
        'type': 'scene',
        'integrator': {'type': 'path'},
        'sensor': {
            'type': 'perspective',
            'fov': 45,
            'to_world': mi.ScalarTransform4f.look_at(
                origin=[0, -5, 2],
                target=[0, 0, 1],
                up=[0, 0, 1]
            ),
            'film': {'type': 'hdrfilm', 'width': 128, 'height': 128}
        },
        'sphere': {
            'type': 'sphere',
            'center': [0, 0, 1],
            'radius': 1.0,
            'bsdf': {'type': 'diffuse', 'reflectance': {'type': 'rgb', 'value': [0.8, 0.8, 0.8]}}
        },
        'light': {
            'type': 'point',
            'position': initial_light_pos,
            'intensity': {'type': 'spectrum', 'value': initial_intensity}
        }
    })
    
    params = mi.traverse(opt_scene)
    params.keep(['light.position', 'light.intensity.value'])
    
    opt = mi.ad.Adam(lr=0.05)
    
    print("\n3. Optimizing light parameters...")
    print(f"\n{'Iter':<8} {'Loss':<12} {'Light X':<10} {'Light Y':<10} {'Light Z':<10} {'Intensity':<10}")
    print("-" * 70)
    
    for i in range(80):
        current_image = mi.render(opt_scene, params, spp=4)
        loss = dr.mean(dr.sqr(current_image - target_image))
        
        dr.backward(loss)
        opt.step(params)
        params.update()
        
        if i % 20 == 0:
            pos = params['light.position']
            intensity = params['light.intensity.value']
            print(f"{i:<8} {loss[0]:<12.6f} {pos[0]:<10.4f} {pos[1]:<10.4f} {pos[2]:<10.4f} {intensity[0]:<10.2f}")
    
    final_pos = params['light.position']
    final_intensity = params['light.intensity.value']
    
    print("\n" + "="*70)
    print(f"Target:    position=[{target_light_pos[0]:.2f}, {target_light_pos[1]:.2f}, {target_light_pos[2]:.2f}], intensity={target_intensity:.2f}")
    print(f"Recovered: position=[{final_pos[0]:.2f}, {final_pos[1]:.2f}, {final_pos[2]:.2f}], intensity={final_intensity[0]:.2f}")
    print("="*70)
    
    print("\n✓ Light estimation complete!")


def main():
    """Run all inverse rendering examples"""
    print("="*70)
    print("Mitsuba 3 - Inverse Rendering Examples")
    print("Demonstrating 2D→3D Reconstruction Capabilities")
    print("="*70)
    
    # Check if AD variants are available
    if not check_variant():
        print("\nCannot run examples without differentiable variants.")
        print("Install with: pip install mitsuba[ad]")
        return
    
    # Run examples
    try:
        example_1_optimize_albedo()
    except Exception as e:
        print(f"\n✗ Example 1 failed: {e}")
    
    try:
        example_2_optimize_position()
    except Exception as e:
        print(f"\n✗ Example 2 failed: {e}")
    
    try:
        example_3_light_estimation()
    except Exception as e:
        print(f"\n✗ Example 3 failed: {e}")
    
    print("\n" + "="*70)
    print("All examples complete!")
    print("="*70)
    print("\nNext steps:")
    print("  - Explore more complex scenes")
    print("  - Try multi-view reconstruction")
    print("  - Integrate with neural networks (NeRF-style)")
    print("  - Apply to real photographs")
    print("="*70)


if __name__ == '__main__':
    main()
