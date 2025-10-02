"""
Subprocess script for rendering - runs in separate process
This avoids Qt/Mitsuba threading conflicts
"""

import sys
import pickle
import numpy as np
from pathlib import Path
import os

# Disable ANSI color codes in logs
os.environ['LOGURU_COLORIZE'] = 'false'
os.environ['LOGURU_AUTOINIT'] = 'false'

def log(message):
    """Log message to stdout for parent process"""
    from datetime import datetime
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"LOG:[{timestamp}] {message}", flush=True)

def progress(value):
    """Send progress to parent process"""
    print(f"PROGRESS:{value}", flush=True)

def main():
    if len(sys.argv) != 3:
        print("ERROR:Invalid arguments", file=sys.stderr)
        sys.exit(1)
    
    scene_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Import Mitsuba
        log("Importing Mitsuba...")
        import mitsuba as mi
        
        # Load scene data
        log("Loading scene data...")
        with open(scene_file, 'rb') as f:
            data = pickle.load(f)
        
        scene_dict = data['scene_dict']
        params = data['params']
        
        # Set variant
        variant = params.get('variant', 'scalar_rgb')
        log(f"Setting variant: {variant}")
        mi.set_variant(variant)
        progress(5)
        
        # Preprocess transforms
        log("Preprocessing scene...")
        scene_dict = preprocess_transforms(scene_dict)
        progress(10)
        
        # Load scene
        log("Loading scene...")
        scene = mi.load_dict(scene_dict)
        progress(20)
        
        # Render
        spp = params.get('spp', 256)
        log(f"Rendering ({spp} spp)...")
        progress(30)
        
        image = mi.render(scene, spp=spp)
        progress(80)
        
        # Save
        log("Saving image...")
        bitmap = mi.Bitmap(image)
        
        # Convert to numpy and save as PNG
        img_array = np.array(bitmap)
        from PIL import Image
        
        # Convert to 8-bit
        img_8bit = np.clip(img_array ** (1.0/2.2) * 255, 0, 255).astype(np.uint8)
        
        if len(img_8bit.shape) == 3 and img_8bit.shape[2] == 4:
            img = Image.fromarray(img_8bit)  # RGBA auto-detected
        elif len(img_8bit.shape) == 3 and img_8bit.shape[2] == 3:
            img = Image.fromarray(img_8bit)  # RGB auto-detected
        else:
            img = Image.fromarray(img_8bit)  # Grayscale auto-detected
        
        img.save(output_file)
        progress(100)
        
        log(f"Render complete: {output_file}")
        
        # Cleanup
        Path(scene_file).unlink(missing_ok=True)
        
        sys.exit(0)
        
    except Exception as e:
        print(f"ERROR:{str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def preprocess_transforms(scene_dict):
    """Convert transform dictionaries to Mitsuba objects"""
    import mitsuba as mi
    import copy
    
    processed = copy.deepcopy(scene_dict)
    _process_recursive(processed, mi)
    return processed


def _process_recursive(obj, mi):
    """Recursively process transforms"""
    if isinstance(obj, dict):
        if 'to_world' in obj:
            to_world = obj['to_world']
            
            if isinstance(to_world, list):
                # Matrix
                import numpy as np
                if isinstance(to_world[0], list):
                    matrix_np = np.array(to_world, dtype=np.float32)
                else:
                    matrix_np = np.array(to_world, dtype=np.float32).reshape(4, 4)
                obj['to_world'] = mi.ScalarTransform4f(matrix_np)
            
            elif isinstance(to_world, dict):
                # Transform operations
                obj['to_world'] = _build_transform(to_world, mi)
        
        # Recurse
        for key, value in obj.items():
            if key != 'to_world':
                _process_recursive(value, mi)
    
    elif isinstance(obj, list):
        for item in obj:
            _process_recursive(item, mi)


def _build_transform(transform_dict, mi):
    """Build transform from dictionary"""
    transform_type = transform_dict.get('type', 'identity')
    
    if transform_type == 'look_at':
        origin = transform_dict.get('origin', [0, 0, 0])
        target = transform_dict.get('target', [0, 0, 0])
        up = transform_dict.get('up', [0, 1, 0])
        transform = mi.ScalarTransform4f.look_at(origin=origin, target=target, up=up)
    elif transform_type == 'translate':
        value = transform_dict.get('value', [0, 0, 0])
        transform = mi.ScalarTransform4f.translate(value)
    elif transform_type == 'scale':
        value = transform_dict.get('value', 1.0)
        if isinstance(value, (int, float)):
            transform = mi.ScalarTransform4f.scale([value, value, value])
        else:
            transform = mi.ScalarTransform4f.scale(value)
    elif transform_type == 'rotate':
        axis = transform_dict.get('axis', [0, 0, 1])
        angle = transform_dict.get('angle', 0.0)
        transform = mi.ScalarTransform4f.rotate(axis, angle)
    else:
        transform = mi.ScalarTransform4f()
    
    # Handle child transforms
    if 'child' in transform_dict:
        child_transform = _build_transform(transform_dict['child'], mi)
        transform = transform @ child_transform
    
    return transform


if __name__ == '__main__':
    main()
