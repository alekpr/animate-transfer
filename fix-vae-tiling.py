#!/usr/bin/env python3
"""Fix VAE tiling parameter errors in workflow"""

import json

def fix_vae_nodes():
    """Fix Node 28 and 497 VAE tiling parameters"""
    
    print("🔧 Fixing VAE tiling parameters...\n")
    
    # Read workflow
    with open('modify-files/lipsync-ofm+Nabludatel-24GB.json', 'r') as f:
        workflow = json.load(f)
    
    fixed = []
    
    for node in workflow['nodes']:
        if node['id'] == 28:  # WanVideoDecode
            print("Node 28 (WanVideoDecode):")
            print(f"  Before: {node['widgets_values']}")
            
            # Correct order: [enable_tiling, tile_x, tile_y, stride_x, stride_y, normalization]
            node['widgets_values'] = [
                True,       # enable_vae_tiling
                256,        # tile_x
                256,        # tile_y
                128,        # tile_stride_x
                128,        # tile_stride_y
                'default'   # normalization
            ]
            
            print(f"  After:  {node['widgets_values']}")
            fixed.append(28)
            
        elif node['id'] == 497:  # WanVideoEncode
            print("\nNode 497 (WanVideoEncode):")
            print(f"  Before: {node['widgets_values']}")
            
            # Correct order: [enable_tiling, tile_x, tile_y, stride_x, stride_y, noise_aug, latent]
            node['widgets_values'] = [
                True,   # enable_vae_tiling
                256,    # tile_x
                256,    # tile_y
                128,    # tile_stride_x
                128,    # tile_stride_y
                0,      # noise_aug_strength
                1       # latent_strength
            ]
            
            print(f"  After:  {node['widgets_values']}")
            fixed.append(497)
    
    # Save
    print(f"\n💾 Saving fixed workflow...")
    with open('modify-files/lipsync-ofm+Nabludatel-24GB.json', 'w') as f:
        json.dump(workflow, f, indent='\t')
    
    print(f"✅ Fixed {len(fixed)} nodes: {fixed}")
    
    # Verify
    print("\n🔍 Verification:")
    with open('modify-files/lipsync-ofm+Nabludatel-24GB.json', 'r') as f:
        verify = json.load(f)
    
    for node in verify['nodes']:
        if node['id'] in [28, 497]:
            print(f"\nNode {node['id']}:")
            for i, v in enumerate(node['widgets_values']):
                print(f"  [{i}] = {v} ({type(v).__name__})")
    
    return True

if __name__ == "__main__":
    try:
        fix_vae_nodes()
        print("\n" + "="*60)
        print("✅ VAE tiling parameters fixed successfully!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
