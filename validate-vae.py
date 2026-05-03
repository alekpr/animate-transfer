#!/usr/bin/env python3
"""Validate optimized workflow"""

import json

workflow_path = 'modify-files/lipsync-ofm+Nabludatel-24GB.json'

print("🔍 Validating workflow...\n")

with open(workflow_path, 'r') as f:
    workflow = json.load(f)

print(f"✅ JSON is valid")
print(f"✅ Total nodes: {len(workflow['nodes'])}\n")

# Check VAE nodes
for node in workflow['nodes']:
    if node['id'] == 28:
        print("Node 28 (WanVideoDecode):")
        vals = node['widgets_values']
        print(f"  [0] enable_vae_tiling: {vals[0]} (should be True)")
        print(f"  [1] tile_x: {vals[1]} (should be 256)")
        print(f"  [2] tile_y: {vals[2]} (should be 256)")
        print(f"  [3] tile_stride_x: {vals[3]} (should be 128)")
        print(f"  [4] tile_stride_y: {vals[4]} (should be 128)")
        print(f"  [5] normalization: {vals[5]} (should be 'default')")
        
        valid = (vals[0] == True and vals[1] == 256 and vals[2] == 256 and 
                 vals[3] == 128 and vals[4] == 128 and vals[5] == 'default')
        print(f"  Status: {'✅ VALID' if valid else '❌ INVALID'}\n")
        
    elif node['id'] == 497:
        print("Node 497 (WanVideoEncode):")
        vals = node['widgets_values']
        print(f"  [0] enable_vae_tiling: {vals[0]} (should be True)")
        print(f"  [1] tile_x: {vals[1]} (should be 256)")
        print(f"  [2] tile_y: {vals[2]} (should be 256)")
        print(f"  [3] tile_stride_x: {vals[3]} (should be 128)")
        print(f"  [4] tile_stride_y: {vals[4]} (should be 128)")
        print(f"  [5] noise_aug_strength: {vals[5]} (should be 0)")
        print(f"  [6] latent_strength: {vals[6]} (should be 1)")
        
        valid = (vals[0] == True and vals[1] == 256 and vals[2] == 256 and 
                 vals[3] == 128 and vals[4] == 128 and vals[5] == 0 and vals[6] == 1)
        print(f"  Status: {'✅ VALID' if valid else '❌ INVALID'}\n")

print("=" * 60)
print("✅ Validation complete!")
print("=" * 60)
