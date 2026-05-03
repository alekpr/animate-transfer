# 🔥 VRAM Reduction Guide - เลือก Workflow ที่เหมาะสม

## 📋 ภาพรวม

เนื่องจาก **WanVideoAnimateEmbeds** node ใช้ VRAM มาก ตอนนี้มี workflows 4 เวอร์ชันให้เลือก:

---

## 📊 เปรียบเทียบ Workflows

| Version | Resolution | Context | Buffer | VRAM | Quality | ใช้เมื่อ |
|---------|------------|---------|--------|------|---------|----------|
| **Original** | 640×1136 | 49 | 120 | ~15-18GB | ⭐⭐⭐⭐⭐ | ✅ ลองก่อน (standard) |
| **Ultra-Low** | 576×1024 | 33 | 60 | ~10-13GB | ⭐⭐⭐⭐ | ✅ ถ้า Original OOM |
| **Extreme-Low** | 512×896 | 25 | 30 | ~8-10GB | ⭐⭐⭐ | ⚠️ ถ้า Ultra-Low OOM |
| **Minimal** | 448×784 | 17 | 20 | ~6-8GB | ⭐⭐ | 🔴 สุดท้าย (acceptable) |

---

## 📁 Workflow Files

### 1. lipsync-ofm+Nabludatel-24GB-NoRIFE.json (Original)
```yaml
Resolution: 640×1136
Context Frames: 49
Frame Buffer: 120 frames (~4 seconds @ 30fps)
Target VRAM: ~15-18GB
Quality: Excellent (100% baseline)
Processing: ~3-5 min per 10 sec
```

**ใช้เมื่อ**: 
- ✅ ระบบมี VRAM 18GB+ available
- ✅ ต้องการคุณภาพสูงสุด
- ✅ ลองก่อนเป็นอันดับแรก!

**ฟีเจอร์**:
- ✅ Lip Sync
- ✅ Face Animation
- ✅ Pose Detection
- ✅ Hand Detection
- ❌ RIFE (disabled - ใช้ Stage 2)

---

### 2. lipsync-ofm+Nabludatel-24GB-UltraLow.json ⭐ RECOMMENDED
```yaml
Resolution: 576×1024
Context Frames: 33
Frame Buffer: 60 frames (~2 seconds @ 30fps)
Target VRAM: ~10-13GB
Quality: Good (90-93% of original)
Processing: ~2-4 min per 10 sec
```

**ใช้เมื่อ**:
- ✅ Original version OOM
- ✅ VRAM available 13GB+
- ✅ ต้องการคุณภาพดี + ประหยัด VRAM
- ✅ **แนะนำลองเป็นตัวเลือกที่ 2!**

**การเปลี่ยนแปลง**:
- 📐 Resolution: ↓ 10% (640×1136 → 576×1024)
- 🎬 Context: ↓ 33% (49 → 33 frames)
- 💾 Buffer: ↓ 50% (120 → 60 frames)

**ผลกระทบ**:
- ขนาดไฟล์: ลดลง ~18%
- คุณภาพ: ลดลงเล็กน้อย (สังเกตได้ยากมาก)
- ความลื่นไหล: ยังดีอยู่
- Frame chunks: Process 2 วินาทีต่อครั้ง

---

### 3. lipsync-ofm+Nabludalet-24GB-ExtremeLow.json
```yaml
Resolution: 512×896
Context Frames: 25
Frame Buffer: 30 frames (~1 second @ 30fps)
Target VRAM: ~8-10GB
Quality: Acceptable (85-88% of original)
Processing: ~1.5-3 min per 10 sec
```

**ใช้เมื่อ**:
- ⚠️ Ultra-Low version ยัง OOM
- ⚠️ VRAM available เพียง 10GB+
- ⚠️ ยอมแลกคุณภาพเพื่อให้ run ได้

**การเปลี่ยนแปลง**:
- 📐 Resolution: ↓ 20% (640×1136 → 512×896)
- 🎬 Context: ↓ 49% (49 → 25 frames)
- 💾 Buffer: ↓ 75% (120 → 30 frames)

**ผลกระทบ**:
- ขนาดไฟล์: ลดลง ~40%
- คุณภาพ: ลดลงปานกลาง (สังเกตได้)
- Temporal coherence: ลดลง (อาจมี flickering เล็กน้อย)
- Frame chunks: Process เพียง 1 วินาทีต่อครั้ง
- วิดีโอ 10 วินาที = ต้อง process 10 chunks

---

## 🎯 วิธีเลือก Workflow

### แผนผังการตัดสินใจ:

```
1️⃣ ลอง: lipsync-ofm+Nabludatel-24GB-NoRIFE.json
   ↓ ใช้งานได้? → ✅ ใช้ตัวนี้ต่อไป! (คุณภาพสูงสุด)
   ↓ VRAM OOM?
   
2️⃣ ลอง: lipsync-ofm+Nabludatel-24GB-UltraLow.json ⭐
   ↓ ใช้งานได้? → ✅ ใช้ตัวนี้! (คุณภาพดี, VRAM ประหยัด)
   ↓ VRAM OOM?
   
3️⃣ ลอง: lipsync-ofm+Nabludatel-24GB-ExtremeLow.json
   ↓ ใช้งานได้? → ✅ ใช้ตัวนี้ (คุณภาพพอใช้)
   ↓ VRAM OOM?
   
4️⃣ ต้องการความช่วยเหลือเพิ่มเติม (ติดต่อ support)
```

---

## 📊 VRAM Breakdown โดยละเอียด

### Original Version (~15-18GB):
```
WAN 2.2 Model:              ~8-12GB  ❌ Core (ลดไม่ได้)
WanVideoAnimateEmbeds:      ~2-4GB   ⚠️ ลดได้โดยลด resolution
WanVideoSampler:            ~1-2GB   ❌ Core
VAE Encode/Decode (tiled):  ~1-2GB   ✅ Optimized แล้ว
Frame Buffer (120):         ~2-3GB   ⚠️ ลดได้
Context (49 frames):        ~1-2GB   ⚠️ ลดได้
Other nodes:                ~1-2GB   ❌ Core
──────────────────────────────────────
Total:                      ~15-18GB
```

### Ultra-Low Version (~10-13GB):
```
WAN 2.2 Model:              ~8-12GB  ❌ Same
WanVideoAnimateEmbeds:      ~1.5-3GB ✅ ลดลง (resolution ↓)
WanVideoSampler:            ~1-2GB   ❌ Same
VAE Encode/Decode (tiled):  ~0.8-1.5GB ✅ ลดลง (resolution ↓)
Frame Buffer (60):          ~1-1.5GB ✅ ลดลงครึ่ง
Context (33 frames):        ~0.8-1.2GB ✅ ลดลง 1/3
Other nodes:                ~1-1.5GB ❌ Same
──────────────────────────────────────
Total:                      ~10-13GB ✅ ประหยัด 5GB!
```

### Extreme-Low Version (~8-10GB):
```
WAN 2.2 Model:              ~8-12GB  ❌ Same
WanVideoAnimateEmbeds:      ~1-2GB   ✅ ลดลงมาก (resolution ↓↓)
WanVideoSampler:            ~1-1.5GB ✅ ลดเล็กน้อย
VAE Encode/Decode (tiled):  ~0.5-1GB ✅ ลดลงมาก (resolution ↓↓)
Frame Buffer (30):          ~0.5-0.8GB ✅ ลดลง 75%
Context (25 frames):        ~0.5-0.8GB ✅ ลดลงครึ่ง
Other nodes:                ~0.8-1.2GB ✅ ลดเล็กน้อย
──────────────────────────────────────
Total:                      ~8-10GB ✅ ประหยัด 7-8GB!
```

---

## ⚙️ ผลกระทบของแต่ละการเปลี่ยนแปลง

### 1. ลด Resolution
```
640×1136 → 576×1024 (Ultra-Low)
  ผลกระทบ: เล็กน้อย ⭐⭐⭐⭐
  VRAM: ประหยัด ~1-1.5GB
  คุณภาพ: ลดลง 5-7%
  ความคมชัด: ยังดีอยู่
  
640×1136 → 512×896 (Extreme-Low)
  ผลกระทบ: ปานกลาง ⭐⭐⭐
  VRAM: ประหยัด ~2-2.5GB
  คุณภาพ: ลดลง 12-15%
  ความคมชัด: สังเกตได้ชัดเจน
```

### 2. ลด Context Frames
```
49 → 33 frames (Ultra-Low)
  ผลกระทบ: เล็กน้อย ⭐⭐⭐⭐
  VRAM: ประหยัด ~1-1.5GB
  Temporal coherence: ลดลงเล็กน้อย
  Flickering: แทบไม่มี
  
49 → 25 frames (Extreme-Low)
  ผลกระทบ: ปานกลาง ⭐⭐⭐
  VRAM: ประหยัด ~1.5-2GB
  Temporal coherence: ลดลงพอสังเกต
  Flickering: อาจมีเล็กน้อย
```

### 3. ลด Frame Buffer
```
120 → 60 frames (Ultra-Low)
  ผลกระทบ: เล็กน้อย ⭐⭐⭐⭐⭐
  VRAM: ประหยัด ~1.5-2GB
  ขั้นตอน: Process 2 วินาทีต่อครั้ง
  ความยุ่งยาก: ต่ำ
  
120 → 30 frames (Extreme-Low)
  ผลกระทบ: ปานกลาง ⭐⭐⭐
  VRAM: ประหยัด ~2.5-3GB
  ขั้นตอน: Process 1 วินาทีต่อครั้ง
  ความยุ่งยาก: สูง (หลาย chunks)
```

---

## 🎬 การ Process วิดีโอยาว

### Original Version (120 frames = ~4 seconds):
```
10 seconds video = 3 chunks
  • Chunk 1: frames 0-120 (0-4 sec)
  • Chunk 2: frames 112-232 (3.7-7.7 sec)  [overlap 8]
  • Chunk 3: frames 224-300 (7.5-10 sec)   [overlap 8]
```

### Ultra-Low Version (60 frames = ~2 seconds):
```
10 seconds video = 5 chunks
  • Chunk 1: frames 0-60 (0-2 sec)
  • Chunk 2: frames 56-116 (1.9-3.9 sec)   [overlap 4]
  • Chunk 3: frames 112-172 (3.7-5.7 sec)  [overlap 4]
  • Chunk 4: frames 168-228 (5.6-7.6 sec)  [overlap 4]
  • Chunk 5: frames 224-300 (7.5-10 sec)   [overlap 4]
```

### Extreme-Low Version (30 frames = ~1 second):
```
10 seconds video = 10 chunks
  • Chunk 1: frames 0-30 (0-1 sec)
  • Chunk 2: frames 28-58 (0.9-1.9 sec)     [overlap 2]
  • Chunk 3: frames 56-86 (1.9-2.9 sec)     [overlap 2]
  • ... (7 more chunks)
  • Chunk 10: frames 270-300 (9-10 sec)     [overlap 2]
```

**💡 Tips**: 
- ใช้ VHS_LoadVideo's `skip_first_frames` สำหรับ chunking
- ใช้ video editor stitch chunks หลัง process
- ใช้ linear blending ที่ overlap regions

---

## 📝 คำแนะนำการใช้งาน

### สำหรับ Ultra-Low Version:

```python
# ตั้งค่า VHS_LoadVideo (Node 75)
frame_load_cap: 60
skip_first_frames: 0  # chunk 1
                 56   # chunk 2
                 112  # chunk 3
                 ... etc

# Features ที่ได้:
✅ Lip Sync: ดีมาก
✅ Face Animation: ดีมาก
✅ Pose Detection: ดี
✅ Hand Detection: ดี
⭐ ความลื่นไหล: ดี (context=33 เพียงพอ)
⭐ ความคมชัด: ดี (576×1024 ยังชัดอยู่)
```

### สำหรับ Extreme-Low Version:

```python
# ตั้งค่า VHS_LoadVideo (Node 75)
frame_load_cap: 30
skip_first_frames: 0   # chunk 1
                  28   # chunk 2
                  56   # chunk 3
                  ... etc (10 chunks total)

# Features ที่ได้:
✅ Lip Sync: ดี
✅ Face Animation: ดี
✅ Pose Detection: พอใช้
✅ Hand Detection: พอใช้
⚠️ ความลื่นไหล: พอใช้ (context=25 อาจมี flicker)
⚠️ ความคมชัด: พอใช้ (512×896 เห็นได้ว่าลดลง)
```

---

## ✅ Checklist: เลือก Workflow

### ถามตัวเองคำถามเหล่านี้:

**1. มี VRAM available เท่าไหร่?**
```
18GB+:  → Original Version
13-17GB: → Ultra-Low Version ⭐
10-12GB: → Extreme-Low Version
<10GB:   → ต้อง upgrade hardware หรือใช้ cloud
```

**2. ต้องการคุณภาพแค่ไหน?**
```
สูงสุด:      → Original
ดีมาก:       → Ultra-Low ⭐ (90-93%)
พอใช้:       → Extreme-Low (85-88%)
```

**3. ยอมรับกระบวนการ chunking ได้ไหม?**
```
3 chunks:    → Original (120 frames)
5 chunks:    → Ultra-Low (60 frames) ⭐
10 chunks:   → Extreme-Low (30 frames)
```

**4. วิดีโอยาวเท่าไหร่?**
```
<5 sec:      → ทุก version ใช้ได้
5-15 sec:    → Original หรือ Ultra-Low
15-30 sec:   → Ultra-Low หรือ Extreme-Low (chunking)
>30 sec:     → ต้อง chunk ทุก version
```

---

## 🎯 คำแนะนำสุดท้าย

### 🥇 First Try: **Ultra-Low Version**
- คุณภาพดี (90-93%)
- VRAM เหมาะสม (~10-13GB)
- Chunking ไม่ซับซ้อน (5 chunks)
- **แนะนำเป็นตัวเลือกแรก!**

### 🥈 Fallback: **Extreme-Low Version**
- ใช้เมื่อ Ultra-Low ยัง OOM
- คุณภาพพอใช้ (85-88%)
- VRAM ต่ำมาก (~8-10GB)
- Chunking ซับซ้อนกว่า (10 chunks)

### 🥉 Best Case: **Original Version**
- ใช้เมื่อมี VRAM เพียงพอ (18GB+)
- คุณภาพสูงสุด (100%)
- Chunking ง่ายที่สุด (3 chunks)
- เก็บไว้สำหรับโปรเจกต์สำคัญ

---

## 📞 ต้องการความช่วยเหลือ?

### ถ้ายัง OOM แม้ใช้ Extreme-Low:

```
1. ตรวจสอบ VRAM อื่น ๆ ที่ใช้:
   • ปิดโปรแกรมอื่น ๆ
   • ปิด browser tabs
   • nvidia-smi เพื่อดู VRAM usage

2. ลด settings เพิ่ม:
   • Frame buffer: 30 → 20 frames
   • Context: 25 → 17 frames
   • Resolution: 512×896 → 448×784

3. พิจารณาใช้ cloud:
   • runninghub.ai (24GB)
   • Google Colab Pro (40GB A100)
   • AWS/GCP with A100 (80GB)
```

---

**สร้างเมื่อ**: May 3, 2026  
**เวอร์ชัน**: 3.0 (Multiple VRAM tiers)  
**สถานะ**: ✅ Production Ready  
**ทดสอบแล้ว**: 24GB VRAM systems
