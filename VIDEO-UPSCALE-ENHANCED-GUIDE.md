# 🎬 Video-Upscale-Enhanced Quick Start Guide

## 📋 Overview

This workflow is designed to work as **Stage 2** in the two-stage pipeline, providing professional video upscaling and frame interpolation with efficient VRAM management.

```
Input: Video from Stage 1 (640×1136 @ 24fps)
   ↓
Process: FlashVSR Upscale + RIFE Interpolation
   ↓
Output: HD video (1280×2272 @ 48fps)
```

---

## 🎯 Features

- ✅ **3 Upscale Modes**: None / 2x / 1080P Fixed
- ✅ **RIFE Frame Interpolation**: 24fps → 48fps (or any multiplier)
- ✅ **Manual FPS Control**: No auto-calculation errors
- ✅ **Strategic VRAM Management**: Purge VRAM between heavy operations
- ✅ **Preview Nodes**: See input vs output comparison

---

## 🚀 Quick Start (5 Steps)

### Step 1: Load Workflow
```bash
Open ComfyUI → Load → Video-Upscale-Enhanced.json
```

### Step 2: Upload Video
- Click **Node 1 (Load Video)**
- Choose your video file (preferably output from Stage 1)
- Supported formats: MP4, MOV, AVI, WebM

### Step 3: Select Upscale Mode
- Click **Node 5 (Upscale Mode)**
- Choose option:
  - `0` = No upscale (original size)
  - `1` = 2x upscale ← **Recommended!**
  - `2` = Fixed 1080P

### Step 4: Configure RIFE (Optional but Recommended)
- **Node 10 (Enable RIFE)**: Set to `true`
- **Node 12 (RIFE Multiplier)**: Set to `2` (double FPS)
- **Node 13 (Output FPS)**: Calculate as `Source FPS × Multiplier`
  - Example: 24 × 2 = `48` fps

### Step 5: Run!
- Click **Queue Prompt**
- Wait for processing (~3-4 minutes for 10 seconds)
- Download from `ComfyUI/output/upscaled_enhanced_XXXXX.mp4`

---

## ⚙️ Upscale Mode Details

### Mode 0: NO UPSCALE
```
Input:  640×1136
Output: 640×1136 (unchanged)
VRAM:   ~3-5GB
Speed:  ⭐⭐⭐⭐⭐
Use When: Source already good resolution, only need RIFE
```

### Mode 1: 2X UPSCALE (FlashVSR) ← Recommended!
```
Input:  640×1136
Output: 1280×2272 (exactly 2× each dimension)
VRAM:   ~8-13GB
Speed:  ⭐⭐⭐⭐
Use When: Want highest quality upgrade
Model:  FlashVSR v1.1 (tiny-long)
```

### Mode 2: FIXED 1080P
```
Input:  640×1136 (portrait)
Output: 1101×1920 (longest side = 1920, maintains aspect ratio)
VRAM:   ~10-16GB
Speed:  ⭐⭐⭐⭐
Use When: Need specific ~1080P size for platforms (YouTube, TikTok)
Method: Lanczos interpolation with aspect ratio preservation
```

---

## 🎬 RIFE Interpolation Guide

### What is RIFE?
AI-powered frame interpolation that creates smooth in-between frames for fluid motion.

### Settings Explained

#### Enable RIFE (Node 10)
```
true  = Apply interpolation ← Recommended for smooth output
false = Skip interpolation (original FPS)
```

#### RIFE Multiplier (Node 12)
```
2 = Double FPS (24→48, 30→60) ← Most common
3 = Triple FPS (24→72, 30→90)
4 = Quadruple FPS (24→96, 30→120) ⚠️ Heavy!
```

#### Output FPS (Node 13) ⚠️ IMPORTANT!
**You MUST set this manually!**

Formula: `Source FPS × RIFE Multiplier`

Examples:
- Source 24fps + Multiplier 2 → Set **48**
- Source 30fps + Multiplier 2 → Set **60**
- Source 24fps + Multiplier 3 → Set **72**
- **If RIFE disabled** → Set to **source FPS** (24 or 30)

### Why Manual FPS Control?
Prevents auto-calculation errors that cause:
- ❌ Wrong playback speed (too fast/too slow)
- ❌ Audio desync
- ❌ Incorrect frame timing

---

## 💾 VRAM Usage Guide (24GB System)

### Scenario 1: No Upscale + No RIFE
```
VRAM: ~3-5GB ⚡
Speed: Super fast
Use: Quick FPS check, no quality upgrade needed
```

### Scenario 2: 2x Upscale + No RIFE
```
VRAM: ~8-10GB ✅
Speed: Fast
Use: Resolution upgrade only
```

### Scenario 3: 2x Upscale + RIFE 2x ← Recommended!
```
VRAM: ~10-13GB ✅
Speed: Moderate
Use: Best quality (HD + smooth)
Output: 1280×2272 @ 48fps
```

### Scenario 4: 1080P + RIFE 2x
```
VRAM: ~12-16GB ⚠️
Speed: Slower
Use: Platform requirements (YouTube)
Output: ~1101×1920 @ 48fps
```

---

## ⏱️ Processing Time Estimates

For 10-second video (300 frames @ 30fps):

| Configuration | Time | VRAM | Quality |
|--------------|------|------|---------|
| No upscale + No RIFE | ~30 sec | ~3-5GB | ⭐⭐⭐ |
| No upscale + RIFE 2x | ~1-2 min | ~5-7GB | ⭐⭐⭐⭐ |
| 2x upscale + No RIFE | ~2-3 min | ~8-10GB | ⭐⭐⭐⭐ |
| 2x upscale + RIFE 2x | ~3-4 min | ~10-13GB | ⭐⭐⭐⭐⭐ |
| 1080P + RIFE 2x | ~4-5 min | ~12-16GB | ⭐⭐⭐⭐⭐ |

*Times vary based on GPU (RTX 4090 / A100)*

---

## 🔄 Two-Stage Workflow Integration

### Complete Pipeline

```
┌──────────────────────────────────────────────────────────┐
│ STAGE 1: lipsync-ofm+Nabludatel-24GB-NoRIFE.json        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ Features: Lip sync, Face animation, Pose/Hand detect    │
│ VRAM: ~15-18GB                                           │
│ Output: 640×1136 @ 24fps                                 │
└──────────────────────────────────────────────────────────┘
                         ↓
          Save to: lipsync_output_00001.mp4
                         ↓
┌──────────────────────────────────────────────────────────┐
│ STAGE 2: Video-Upscale-Enhanced.json ← YOU ARE HERE     │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ Input: lipsync_output_00001.mp4                          │
│ Process: 2x upscale + RIFE 2x                            │
│ VRAM: ~10-13GB                                           │
│ Output: 1280×2272 @ 48fps                                │
└──────────────────────────────────────────────────────────┘
                         ↓
      Final: upscaled_enhanced_00001.mp4 🎉
```

### Why Two Stages?

**Problem**: Running everything in one workflow:
- VRAM: ~26-32GB (exceeds 24GB limit) ❌

**Solution**: Split into two stages:
- Stage 1: ~15-18GB ✅
- Stage 2: ~10-13GB ✅
- **Never exceeds 24GB!**

**Benefits**:
- ✅ Fits in 24GB VRAM systems
- ✅ Can retry each stage independently
- ✅ Easier to troubleshoot
- ✅ Can skip Stage 2 if satisfied with Stage 1 output

---

## 🎯 Use Case Examples

### Case 1: Social Media (TikTok, Instagram Reels)
```yaml
Upscale Mode: 1 (2x upscale)
Enable RIFE: true
RIFE Multiplier: 2
Output FPS: 48
Reason: Smooth motion catches attention, HD looks professional
```

### Case 2: YouTube Upload
```yaml
Upscale Mode: 2 (1080P)
Enable RIFE: true
RIFE Multiplier: 2
Output FPS: 48
Reason: Platform-friendly 1080P, smooth 48fps for quality tier
```

### Case 3: Quick Preview Check
```yaml
Upscale Mode: 0 (no upscale)
Enable RIFE: false
Output FPS: 24 (source)
Reason: Fast processing, check animation quality before full upscale
```

### Case 4: Maximum Quality Archive
```yaml
Upscale Mode: 1 (2x upscale)
Enable RIFE: true
RIFE Multiplier: 3
Output FPS: 72
CRF: 15 (lower = better)
Reason: Best possible quality for archival or client delivery
```

---

## 🎨 Workflow Node Map

### Input Section (Green)
- **Node 1**: Load Video
- **Node 2**: Video Info (shows FPS, resolution, duration)

### Upscaling Section (Purple)
- **Node 5**: Upscale Mode selector
- **Node 6**: FlashVSR 2x Upscale
- **Node 7**: Resize to 1080P
- **Node 8**: Upscale Switch (routes based on mode)
- **Node 9**: Purge VRAM (clears GPU memory)

### RIFE Section (Cyan)
- **Node 10**: Enable RIFE toggle
- **Node 11**: RIFE VFI (frame interpolation engine)
- **Node 12**: RIFE Multiplier
- **Node 13**: Output FPS (manual control)
- **Node 14**: RIFE Switch (routes based on enable setting)

### Output Section (Magenta)
- **Node 16**: Video Combine & Save
- **Node 19**: Input Preview
- **Node 20**: Output Preview

### Info Sections (Blue Notes)
- **Node 3**: Main instructions
- **Node 4**: Upscale options explained
- **Node 17**: RIFE settings guide
- **Node 18**: Output settings info

---

## 🛠️ Troubleshooting

### Issue: Output video plays too fast/slow
**Solution**: Check Output FPS (Node 13)
- Must be: `Source FPS × RIFE Multiplier`
- If RIFE disabled: Must be `Source FPS`

### Issue: Audio desync
**Solution**: 
- Ensure Output FPS is correctly calculated
- Check that audio link is connected (Node 1 → Node 16)
- Verify source video has audio track

### Issue: VRAM OOM in Stage 2
**Solution**:
- Use Mode 0 (no upscale) + RIFE only
- Disable RIFE (Node 10 = false)
- Process shorter video chunks

### Issue: Poor upscale quality
**Solution**:
- Use Mode 1 (FlashVSR) instead of Mode 2
- Lower CRF value: 18 → 15 (Node 16)
- Ensure source video is good quality

### Issue: Processing too slow
**Solution**:
- Use Mode 0 (no upscale)
- Disable RIFE (Node 10 = false)
- Lower RIFE multiplier: 3 → 2

---

## 📊 Output File Size Estimates

For 1-minute video:

| Configuration | File Size | Quality | Platform |
|--------------|-----------|---------|----------|
| 640×1136 @ 24fps | ~20-30 MB | Good | Discord, WhatsApp |
| 640×1136 @ 48fps | ~35-50 MB | Good + Smooth | Telegram |
| 1280×2272 @ 24fps | ~50-70 MB | HD | YouTube (min) |
| 1280×2272 @ 48fps | ~90-120 MB | HD + Smooth | YouTube (recommended) |
| 1101×1920 @ 48fps | ~90-150 MB | Full HD | TikTok, Instagram |

**CRF Impact** (Node 16):
- CRF 15: Larger files, best quality
- CRF 18: Balanced (default)
- CRF 21: Smaller files, good quality
- CRF 23: Smallest, acceptable quality

---

## 💡 Pro Tips

### Tip 1: Test with Short Clips First
Always test with 5-10 second clips before processing full videos.

### Tip 2: Monitor VRAM Usage
```bash
# In terminal, watch VRAM usage:
watch -n 1 nvidia-smi

# Look for "GPU-Util" and "Memory-Usage"
```

### Tip 3: Save Intermediate Outputs
Keep Stage 1 output before running Stage 2 (in case Stage 2 fails).

### Tip 4: Batch Processing
Process multiple videos sequentially by queuing multiple prompts.

### Tip 5: Quality Settings
For client delivery: CRF 15, 2x upscale, RIFE 2x
For social media: CRF 18, 1080P, RIFE 2x
For preview: CRF 21, no upscale, no RIFE

### Tip 6: FPS Calculation Cheat Sheet
```
Source FPS | RIFE 2x | RIFE 3x | RIFE 4x
-----------|---------|---------|--------
24 fps     | 48      | 72      | 96
25 fps     | 50      | 75      | 100
30 fps     | 60      | 90      | 120
60 fps     | 120     | 180     | 240
```

---

## 📝 Quick Reference Checklist

### Before Starting:
- [ ] Workflow loaded: `Video-Upscale-Enhanced.json`
- [ ] Have Stage 1 output video ready (or any video to upscale)
- [ ] Know source video FPS (check with MediaInfo/VLC)
- [ ] GPU has at least 10GB free VRAM

### During Setup:
- [ ] Video uploaded to Node 1
- [ ] Upscale Mode selected (Node 5)
- [ ] RIFE enabled/disabled (Node 10)
- [ ] RIFE Multiplier set (Node 12)
- [ ] Output FPS calculated correctly (Node 13)

### After Processing:
- [ ] Check preview (Node 20) before downloading
- [ ] Verify FPS in output file (use MediaInfo)
- [ ] Check audio sync
- [ ] File size reasonable (~100MB per minute for HD)

---

## 🔗 Related Documentation

- **TWO-STAGE-WORKFLOW-GUIDE-TH.md**: Complete two-stage guide (Thai)
- **OPTIMIZATION-REPORT.md**: Stage 1 technical details
- **README-TH.md**: Stage 1 user guide (Thai)
- **QUICK-REFERENCE.md**: Stage 1 optimization summary

---

## 🆘 Support

If you encounter issues:
1. Check **Node 3** (blue note) in workflow for quick instructions
2. Review this guide's Troubleshooting section
3. Monitor VRAM usage with `nvidia-smi`
4. Test with shorter video clips first

---

**Version**: 1.0  
**Date**: May 3, 2026  
**Target**: 24GB VRAM systems  
**Status**: ✅ Production Ready  
**Works Best With**: Output from `lipsync-ofm+Nabludatel-24GB-NoRIFE.json`
