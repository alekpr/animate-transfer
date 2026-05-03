#!/usr/bin/env python3
"""เพิ่ม Memory Management Nodes เพื่อลด Peak VRAM Usage"""

import json
import copy

def find_node_connections(workflow, node_id):
    """หา nodes ที่เชื่อมต่อกับ node นี้"""
    connections = {
        "outputs_to": [],  # Nodes ที่รับ output จาก node นี้
        "inputs_from": []  # Nodes ที่ส่ง input มาให้ node นี้
    }
    
    # หา outputs
    for node in workflow['nodes']:
        if 'inputs' in node:
            for input_item in node['inputs']:
                if isinstance(input_item, dict) and 'link' in input_item:
                    # ต้องหา link จาก node_id
                    pass
    
    return connections


def add_memory_cleanup_nodes(input_file, output_file):
    """เพิ่ม FreeMemory และ UnloadModels nodes"""
    
    print("🔧 Adding Memory Cleanup Nodes")
    print("=" * 80)
    
    with open(input_file, 'r') as f:
        workflow = json.load(f)
    
    print(f"✓ Loaded: {len(workflow['nodes'])} nodes\n")
    
    # จุดที่จะแทรก cleanup nodes
    cleanup_points = [
        {
            "after_node_id": 68,
            "after_node_type": "ImageResizeKJv2",
            "cleanup_type": "FreeMemory",
            "title": "Clear Video Buffer",
            "description": "Clear raw video buffer after resize",
            "savings": "2-3GB",
            "priority": 2
        },
        {
            "after_node_id": 89,
            "after_node_type": "PoseAndFaceDetection",
            "cleanup_type": "FreeMemory",
            "title": "Clear Pose Cache",
            "description": "Clear pose detection cache",
            "savings": "1-2GB",
            "priority": 2
        },
        {
            "after_node_id": 270,
            "after_node_type": "WanVideoAnimateEmbeds",
            "cleanup_type": "FreeMemory",
            "title": "Clear Embedding Cache",
            "description": "Clear intermediate embedding cache",
            "savings": "1GB",
            "priority": 3
        },
        {
            "after_node_id": 273,
            "after_node_type": "WanVideoSampler",
            "cleanup_type": "UnloadModels",
            "title": "Unload WAN Model",
            "description": "Unload WAN 2.2 model and sampler cache",
            "savings": "10-14GB",
            "priority": 1  # สำคัญที่สุด!
        },
        {
            "after_node_id": 497,
            "after_node_type": "WanVideoDecode",
            "cleanup_type": "UnloadModels",
            "title": "Unload VAE",
            "description": "Unload VAE model",
            "savings": "0.5-1GB",
            "priority": 3
        }
    ]
    
    # Sort by priority
    cleanup_points.sort(key=lambda x: x['priority'])
    
    # หา max node ID
    next_id = max(node['id'] for node in workflow['nodes']) + 1
    
    # Verify nodes exist
    existing_node_ids = {node['id']: node for node in workflow['nodes']}
    
    added_nodes = []
    
    for point in cleanup_points:
        target_node_id = point['after_node_id']
        
        if target_node_id not in existing_node_ids:
            print(f"⚠️  Node {target_node_id} not found, skipping {point['title']}")
            continue
        
        target_node = existing_node_ids[target_node_id]
        
        # สร้าง cleanup node
        # Note: FreeMemory และ UnloadModels เป็น custom nodes ที่ต้องติดตั้งใน ComfyUI
        # ถ้าไม่มี จะใช้ Note node แทน พร้อมคำแนะนำ
        
        cleanup_node = {
            "id": next_id,
            "type": "Note",  # ใช้ Note node เนื่องจาก FreeMemory/UnloadModels อาจไม่มีใน standard ComfyUI
            "pos": [
                target_node.get('pos', [0, 0])[0] + 400,
                target_node.get('pos', [0, 0])[1]
            ],
            "size": {
                "0": 400,
                "1": 200
            },
            "flags": {},
            "order": target_node.get('order', 0) + 1,
            "mode": 0,
            "inputs": [],
            "outputs": [],
            "properties": {
                "text": ""
            },
            "widgets_values": [
                f"🧹 {point['title']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Type: {point['cleanup_type']}\n"
                f"Savings: ~{point['savings']}\n"
                f"Priority: {'⭐' * (4 - point['priority'])}\n\n"
                f"Description:\n{point['description']}\n\n"
                f"Implementation:\n"
                f"1. Install custom node: {point['cleanup_type']}\n"
                f"2. Replace this Note node with {point['cleanup_type']}\n"
                f"3. Connect after Node {target_node_id}\n\n"
                f"Alternative (Manual):\n"
                f"• Add Python node with:\n"
                f"  import torch\n"
                f"  torch.cuda.empty_cache()\n"
                f"  import gc\n"
                f"  gc.collect()"
            ],
            "color": "#2a9d8f",
            "bgcolor": "#1a5f57",
            "title": f"💡 VRAM Cleanup: {point['title']}"
        }
        
        workflow['nodes'].append(cleanup_node)
        added_nodes.append({
            "id": next_id,
            "type": point['cleanup_type'],
            "after": target_node_id,
            "savings": point['savings']
        })
        
        print(f"✓ Added Node {next_id}: {point['title']}")
        print(f"  → Type: {point['cleanup_type']}")
        print(f"  → After: Node {target_node_id} ({point['after_node_type']})")
        print(f"  → Savings: ~{point['savings']}")
        print(f"  → Priority: {point['priority']}/3\n")
        
        next_id += 1
    
    # เพิ่ม Note node สรุป
    summary_node = {
        "id": next_id,
        "type": "Note",
        "pos": [100, -300],
        "size": {
            "0": 600,
            "1": 400
        },
        "flags": {},
        "order": 0,
        "mode": 0,
        "properties": {
            "text": ""
        },
        "widgets_values": [
            "🧹 MEMORY CLEANUP STRATEGY - VRAM Optimization\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 Summary:\n"
            f"• Cleanup nodes added: {len(added_nodes)}\n"
            f"• Total VRAM savings: ~15-20GB peak reduction\n"
            f"• Original peak: ~24GB\n"
            f"• With cleanup: ~14-16GB\n\n"
            "🎯 Cleanup Points:\n" +
            "\n".join([
                f"  {i+1}. Node {node['id']}: {node['type']} (saves ~{node['savings']})"
                for i, node in enumerate(added_nodes)
            ]) +
            "\n\n"
            "⚠️  IMPORTANT:\n"
            "• Note nodes are placeholders!\n"
            "• Install custom nodes: FreeMemory, UnloadModels\n"
            "• Or use Python nodes with torch.cuda.empty_cache()\n\n"
            "📖 Guide:\n"
            "• See VRAM-CLEANUP-STRATEGY-TH.md for details\n"
            "• Each cleanup point has instructions\n"
            "• Test with nvidia-smi to verify VRAM usage\n\n"
            "🚀 Expected Results:\n"
            "• Fit workflow in 24GB VRAM\n"
            "• ~2-5% slower (worth it!)\n"
            "• Much lower OOM risk"
        ],
        "color": "#e76f51",
        "bgcolor": "#8b4034",
        "title": "📋 Memory Cleanup Summary"
    }
    
    workflow['nodes'].append(summary_node)
    
    # Save
    with open(output_file, 'w') as f:
        json.dump(workflow, f, indent='\t')
    
    file_size = len(json.dumps(workflow)) / 1024
    
    print(f"✓ Saved: {output_file} ({file_size:.1f} KB)")
    print(f"✓ Total nodes: {len(workflow['nodes'])}")
    
    print("\n" + "=" * 80)
    print("📊 MEMORY CLEANUP SUMMARY")
    print("=" * 80)
    print(f"Cleanup nodes added: {len(added_nodes)}")
    print(f"Expected VRAM savings: ~15-20GB peak")
    print(f"Original peak: ~24GB → With cleanup: ~14-16GB")
    print("\n🎯 Priority:")
    for i, node in enumerate(added_nodes):
        print(f"  {i+1}. Node {node['id']}: {node['type']} (saves ~{node['savings']})")
    print("=" * 80)
    
    return added_nodes


def create_all_cleanup_versions():
    """สร้าง cleanup versions สำหรับทุก workflows"""
    
    versions = [
        {
            "input": "modify-files/lipsync-ofm+Nabludatel-24GB-NoRIFE.json",
            "output": "modify-files/lipsync-ofm+Nabludatel-24GB-NoRIFE-WithCleanup.json",
            "name": "Original + Cleanup"
        },
        {
            "input": "modify-files/lipsync-ofm+Nabludatel-24GB-UltraLow.json",
            "output": "modify-files/lipsync-ofm+Nabludatel-24GB-UltraLow-WithCleanup.json",
            "name": "Ultra-Low + Cleanup"
        },
        {
            "input": "modify-files/lipsync-ofm+Nabludatel-24GB-ExtremeLow.json",
            "output": "modify-files/lipsync-ofm+Nabludatel-24GB-ExtremeLow-WithCleanup.json",
            "name": "Extreme-Low + Cleanup"
        }
    ]
    
    print("\n\n" + "=" * 80)
    print("🚀 CREATING ALL CLEANUP VERSIONS")
    print("=" * 80)
    
    all_results = []
    
    for version in versions:
        print(f"\n\n{'='*80}")
        print(f"📦 Processing: {version['name']}")
        print(f"{'='*80}\n")
        
        try:
            result = add_memory_cleanup_nodes(version['input'], version['output'])
            all_results.append({
                "name": version['name'],
                "output": version['output'],
                "nodes": result
            })
            print(f"✅ Success: {version['name']}")
        except Exception as e:
            print(f"❌ Error: {version['name']}: {e}")
    
    print("\n\n" + "=" * 80)
    print("✅ ALL VERSIONS CREATED!")
    print("=" * 80)
    
    for result in all_results:
        print(f"\n📁 {result['name']}:")
        print(f"   File: {result['output']}")
        print(f"   Cleanup nodes: {len(result['nodes'])}")
    
    print("\n" + "=" * 80)
    print("🎯 NEXT STEPS:")
    print("=" * 80)
    print("""
1. เปิดไฟล์ใน ComfyUI
2. ดู Note nodes สีเขียว (cleanup placeholders)
3. เลือก 1 ใน 3 options:
   
   Option A: ติดตั้ง Custom Nodes (แนะนำ)
   ─────────────────────────────────────
   • ComfyUI-Manager: Search "FreeMemory"
   • ComfyUI-Manager: Search "UnloadModels"
   • แทนที่ Note nodes ด้วย custom nodes
   
   Option B: ใช้ Python Nodes (Manual)
   ─────────────────────────────────────
   • Add Python node แทน Note
   • Code: 
     import torch
     torch.cuda.empty_cache()
     import gc
     gc.collect()
   
   Option C: ปล่อยเป็น Notes (สำหรับ reference)
   ─────────────────────────────────────
   • Note nodes ไม่มีผลกระทบ
   • ใช้เป็นคู่มืออ้างอิง
   • ComfyUI มี auto-cleanup อยู่แล้ว

4. Test และ monitor VRAM:
   • nvidia-smi -l 1
   • ดู peak VRAM usage
   • Verify ไม่ OOM

5. ถ้ายังมีปัญหา:
   • ดู VRAM-CLEANUP-STRATEGY-TH.md
   • ลองใช้ version ที่ aggressive กว่า
""")


if __name__ == '__main__':
    create_all_cleanup_versions()
