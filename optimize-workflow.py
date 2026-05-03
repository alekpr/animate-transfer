#!/usr/bin/env python3
"""
Optimize ComfyUI Lip Sync Workflow for 24GB VRAM
Reduces from 26-32GB to ~22-24GB peak usage
"""

import json
import copy

def optimize_workflow(input_path, output_path):
    """Apply all optimization phases to workflow"""
    
    # Read original workflow
    print("📖 Reading workflow...")
    with open(input_path, 'r') as f:
        workflow = json.load(f)
    
    print(f"Total nodes: {len(workflow['nodes'])}")
    
    # Create a deep copy for modifications
    optimized = copy.deepcopy(workflow)
    
    # Track changes
    changes_log = []
    
    # ============================================================
    # Phase 1: Resolution & VAE Optimization (~4-6GB savings)
    # ============================================================
    print("\n🔧 Phase 1: Resolution & VAE Optimization")
    
    for node in optimized['nodes']:
        node_id = node['id']
        node_type = node['type']
        
        # Change ImageResizeKJv2 nodes (68, 158) - Resolution to 640×1136
        if node_type == 'ImageResizeKJv2' and node_id in [68, 158]:
            old_width = node['widgets_values'][0]
            old_height = node['widgets_values'][1]
            node['widgets_values'][0] = 640
            node['widgets_values'][1] = 1136
            changes_log.append(f"Node {node_id} (ImageResizeKJv2): {old_width}×{old_height} → 640×1136")
            print(f"  ✓ Node {node_id} (ImageResizeKJv2): Resolution changed to 640×1136")
        
        # Change WanVideoAnimateEmbeds (270) - Resolution
        elif node_type == 'WanVideoAnimateEmbeds' and node_id == 270:
            old_width = node['widgets_values'][0]
            old_height = node['widgets_values'][1]
            node['widgets_values'][0] = 640
            node['widgets_values'][1] = 1136
            changes_log.append(f"Node {node_id} (WanVideoAnimateEmbeds): resolution {old_width}×{old_height} → 640×1136")
            print(f"  ✓ Node {node_id} (WanVideoAnimateEmbeds): Resolution changed to 640×1136")
        
        # Change DWPreprocessor (159) - Resolution
        elif node_type == 'DWPreprocessor' and node_id == 159:
            old_res = node['widgets_values'][3]
            node['widgets_values'][3] = 640
            changes_log.append(f"Node {node_id} (DWPreprocessor): resolution {old_res} → 640")
            print(f"  ✓ Node {node_id} (DWPreprocessor): Resolution changed to 640")
        
        # Change PoseAndFaceDetection (89) - Resolution
        elif node_type == 'PoseAndFaceDetection' and node_id == 89:
            old_width = node['widgets_values'][0]
            old_height = node['widgets_values'][1]
            node['widgets_values'][0] = 640
            node['widgets_values'][1] = 1136
            changes_log.append(f"Node {node_id} (PoseAndFaceDetection): {old_width}×{old_height} → 640×1136")
            print(f"  ✓ Node {node_id} (PoseAndFaceDetection): Resolution changed to 640×1136")
        
        # Enable VAE Tiling - WanVideoEncode (497)
        # Structure: [enable_tiling, tile_x, tile_y, stride_x, stride_y, noise_aug_strength, latent_strength]
        elif node_type == 'WanVideoEncode' and node_id == 497:
            old_tiling = node['widgets_values'][0]
            node['widgets_values'][0] = True  # enable_vae_tiling
            node['widgets_values'][1] = 256   # tile_x
            node['widgets_values'][2] = 256   # tile_y
            node['widgets_values'][3] = 128   # tile_stride_x
            node['widgets_values'][4] = 128   # tile_stride_y
            # Keep original noise_aug_strength and latent_strength
            if len(node['widgets_values']) < 7:
                node['widgets_values'].extend([0, 1])  # defaults
            changes_log.append(f"Node {node_id} (WanVideoEncode): VAE tiling {old_tiling} → True, tiles 256×256, stride 128×128")
            print(f"  ✓ Node {node_id} (WanVideoEncode): VAE tiling enabled (256×256, stride 128)")
        
        # Enable VAE Tiling - WanVideoDecode (28)
        # Structure: [enable_tiling, tile_x, tile_y, stride_x, stride_y, normalization]
        elif node_type == 'WanVideoDecode' and node_id == 28:
            old_tiling = node['widgets_values'][0]
            node['widgets_values'][0] = True      # enable_vae_tiling
            node['widgets_values'][1] = 256       # tile_x
            node['widgets_values'][2] = 256       # tile_y
            node['widgets_values'][3] = 128       # tile_stride_x
            node['widgets_values'][4] = 128       # tile_stride_y
            # Keep original normalization setting
            if len(node['widgets_values']) < 6:
                node['widgets_values'].append('default')
            changes_log.append(f"Node {node_id} (WanVideoDecode): VAE tiling {old_tiling} → True, tiles 256×256, stride 128×128")
            print(f"  ✓ Node {node_id} (WanVideoDecode): VAE tiling enabled (256×256, stride 128)")
    
    print(f"✅ Phase 1 Complete")
    
    # ============================================================
    # Phase 2: Context Window Optimization (~1-2GB savings)
    # ============================================================
    print("\n🔧 Phase 2: Context Window Optimization")
    
    for node in optimized['nodes']:
        node_id = node['id']
        node_type = node['type']
        
        # Change WanVideoContextOptions (87) - Reduce context frames
        if node_type == 'WanVideoContextOptions' and node_id == 87:
            old_context = node['widgets_values'][1]
            node['widgets_values'][1] = 49  # context_frames: 81 → 49
            changes_log.append(f"Node {node_id} (WanVideoContextOptions): context_frames {old_context} → 49")
            print(f"  ✓ Node {node_id} (WanVideoContextOptions): Context frames reduced to 49")
    
    print(f"✅ Phase 2 Complete")
    
    # ============================================================
    # Phase 3: Model Memory Management (~2-4GB savings)
    # ============================================================
    print("\n🔧 Phase 3: Model Memory Management")
    
    for node in optimized['nodes']:
        node_id = node['id']
        node_type = node['type']
        
        # Enable force_offload - WanVideoAnimateEmbeds (270)
        if node_type == 'WanVideoAnimateEmbeds' and node_id == 270:
            old_offload = node['widgets_values'][3]
            node['widgets_values'][3] = True  # force_offload
            changes_log.append(f"Node {node_id} (WanVideoAnimateEmbeds): force_offload {old_offload} → True")
            print(f"  ✓ Node {node_id} (WanVideoAnimateEmbeds): force_offload enabled")
        
        # Enable low_mem_load - WanVideoLoraSelectMulti (354)
        elif node_type == 'WanVideoLoraSelectMulti' and node_id == 354:
            old_low_mem = node['widgets_values'][9]
            node['widgets_values'][9] = True  # low_mem_load
            changes_log.append(f"Node {node_id} (WanVideoLoraSelectMulti): low_mem_load {old_low_mem} → True")
            print(f"  ✓ Node {node_id} (WanVideoLoraSelectMulti): low_mem_load enabled")
    
    print(f"✅ Phase 3 Complete")
    
    # ============================================================
    # Phase 4: Frame Buffer Optimization (~2-3GB savings)
    # ============================================================
    print("\n🔧 Phase 4: Frame Buffer Optimization")
    
    for node in optimized['nodes']:
        node_id = node['id']
        node_type = node['type']
        
        # Reduce frame buffer - VHS_LoadVideo (75)
        if node_type == 'VHS_LoadVideo' and node_id == 75:
            # widgets_values is a dictionary, not a list
            if isinstance(node['widgets_values'], dict) and 'frame_load_cap' in node['widgets_values']:
                old_cap = node['widgets_values']['frame_load_cap']
                node['widgets_values']['frame_load_cap'] = 120  # 241 → 120
                # Also update videopreview params if present
                if 'videopreview' in node['widgets_values'] and 'params' in node['widgets_values']['videopreview']:
                    node['widgets_values']['videopreview']['params']['frame_load_cap'] = 120
                changes_log.append(f"Node {node_id} (VHS_LoadVideo): frame_load_cap {old_cap} → 120")
                print(f"  ✓ Node {node_id} (VHS_LoadVideo): Frame buffer reduced to 120 frames")
                print(f"     NOTE: For 30s videos (900 frames), process in ~8 chunks with overlap")
    
    print(f"✅ Phase 4 Complete")
    
    # ============================================================
    # Save optimized workflow
    # ============================================================
    print(f"\n💾 Saving optimized workflow...")
    with open(output_path, 'w') as f:
        json.dump(optimized, f, indent='\t')
    
    print(f"✅ Saved to {output_path}")
    
    # ============================================================
    # Summary
    # ============================================================
    print(f"\n" + "="*60)
    print("📊 OPTIMIZATION SUMMARY")
    print("="*60)
    print(f"Total changes applied: {len(changes_log)}")
    print("\nChanges by phase:")
    print("\n🔹 Phase 1: Resolution & VAE Optimization")
    for log in changes_log:
        if 'ImageResize' in log or 'Animate' in log or 'Preprocessor' in log or 'Pose' in log or 'VAE tiling' in log:
            print(f"  • {log}")
    
    print("\n🔹 Phase 2: Context Window Optimization")
    for log in changes_log:
        if 'Context' in log:
            print(f"  • {log}")
    
    print("\n🔹 Phase 3: Model Memory Management")
    for log in changes_log:
        if 'offload' in log or 'low_mem' in log:
            print(f"  • {log}")
    
    print("\n🔹 Phase 4: Frame Buffer Optimization")
    for log in changes_log:
        if 'frame_load_cap' in log:
            print(f"  • {log}")
    
    print("\n" + "="*60)
    print("💡 MEMORY SAVINGS ESTIMATE")
    print("="*60)
    print("Resolution reduction (720×1280 → 640×1136):  ~1.5-2GB")
    print("VAE Tiling enabled:                          ~2-3GB")
    print("Context frames reduced (81 → 49):            ~1-2GB")
    print("Model offloading enabled:                    ~1-2GB")
    print("LoRA low memory mode:                        ~0.5-1GB")
    print("Frame buffer reduced (241 → 120):            ~2-3GB")
    print("-" * 60)
    print("Total estimated savings:                     ~9-13GB")
    print("Expected peak VRAM: 26-32GB → 19-23GB ✅")
    print("="*60)
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("1. For 30s videos (900 frames), process in chunks:")
    print("   - 8 chunks × 112 frames each")
    print("   - Use 8-frame overlap between chunks")
    print("   - Apply linear blending at boundaries")
    print("2. Monitor VRAM with nvidia-smi during processing")
    print("3. If still exceeding 24GB:")
    print("   - Reduce context_frames to 33 (fallback)")
    print("   - Or disable secondary LoRA (Wan21_PusaV1)")
    print("4. All features preserved:")
    print("   ✓ Lip sync")
    print("   ✓ Face animation")
    print("   ✓ Pose detection")
    print("   ✓ Hand detection")
    print("   ✓ Frame interpolation")
    
    return optimized, changes_log

if __name__ == "__main__":
    input_file = "original-files/lipsync-ofm+_+Nabludatel.json"
    output_file = "modify-files/lipsync-ofm+Nabludatel-24GB.json"
    
    print("="*60)
    print("🚀 COMFYUI WORKFLOW OPTIMIZER FOR 24GB VRAM")
    print("="*60)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print("="*60)
    
    optimized_workflow, changes = optimize_workflow(input_file, output_file)
    
    print("\n✅ Optimization complete!")
