# 🎬 คู่มือการใช้ Two-Stage Workflow (แบบแยก 2 ขั้นตอน)

## 📋 ภาพรวม

เนื่องจาก workflow เดิมใช้ VRAM มากเกินไป (เกิน 24GB), เราจะแยกกระบวนการออกเป็น 2 ขั้นตอน:

```
┌──────────────────────────────────────────────────────────────────┐
│ STAGE 1: Animation Generation (Core Features)                   │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ Workflow: lipsync-ofm+Nabludatel-24GB-NoRIFE.json               │
│ VRAM: ~15-18GB (พอดีกับ 24GB!)                                   │
│ Output: 640×1136 @ 24fps (ไม่มี interpolation)                  │
└──────────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│ STAGE 2: Upscale + Interpolation (Quality Enhancement)          │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ Workflow: Video-Upscale-Enhanced.json                            │
│ VRAM: ~10-13GB (ใช้น้อยกว่าเพราะ input พร้อมแล้ว)                │
│ Output: 1280×2272 @ 48fps (HD + smooth!)                         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 STAGE 1: Animation Generation

### ไฟล์ที่ใช้
`lipsync-ofm+Nabludatel-24GB-NoRIFE.json`

### ฟีเจอร์ที่มี
- ✅ **Lip Sync** (ปากสอดคล้องกับเสียง)
- ✅ **Face Animation** (ใบหน้าเคลื่อนไหว)
- ✅ **Pose Detection** (ตรวจจับท่าทาง)
- ✅ **Hand Detection** (ตรวจจับมือ)
- ❌ **Frame Interpolation** (ปิดเพื่อประหยัด VRAM)

### ฟีเจอร์ที่ปิดไว้
- ❌ **RIFE Interpolation** (Node 360 ถูก bypass)
  - **เหตุผล**: ประหยัด VRAM ~3-5GB
  - **ผลกระทบ**: Output จะเป็น 24fps ตามต้นฉบับ (ไม่ได้เพิ่มความลื่นไหล)
  - **แก้ไข**: ใช้ Stage 2 เพิ่ม interpolation ภายหลัง

### ขั้นตอนการใช้งาน

#### 1. เปิด Workflow ใน ComfyUI
```bash
# โหลดไฟล์นี้ใน ComfyUI
lipsync-ofm+Nabludatel-24GB-NoRIFE.json
```

#### 2. อัปโหลดวิดีโอต้นฉบับ
- คลิก Node: **VHS_LoadVideo** (Node 75)
- เลือกวิดีโอที่ต้องการประมวลผล
- **แนะนำ**: วิดีโอสั้น 10-15 วินาที สำหรับทดสอบก่อน

#### 3. ตรวจสอบการตั้งค่า

| Node ID | Node Type | Parameter | Value | หมายเหตุ |
|---------|-----------|-----------|-------|----------|
| 75 | VHS_LoadVideo | frame_load_cap | 120 | ประมวลผลสูงสุด 120 frames (~4 วินาที @ 30fps) |
| 68, 158 | ImageResizeKJ | Resolution | 640×1136 | ความละเอียดที่ลดแล้ว |
| 87 | WanVideoContextOptions | context_frames | 49 | หน้าต่าง context ที่ปรับแล้ว |
| 270 | WanVideoAnimateEmbeds | force_offload | True | Offload model เมื่อไม่ใช้งาน |
| 360 | RIFEInterpolation | mode | 4 | **Bypass (ปิดไว้!)** |

#### 4. กด Queue Prompt
- VRAM ที่ใช้: **~15-18GB**
- เวลาประมวลผล: **~3-5 นาที สำหรับ 10 วินาที**
- Output: **ไฟล์วิดีโอใน ComfyUI/output/**

#### 5. ดาวน์โหลด Output
```
ComfyUI/output/lipsync_output_XXXXX.mp4
→ นำไฟล์นี้ไปใช้ใน Stage 2
```

---

## ✨ STAGE 2: Upscale + Interpolation

### ไฟล์ที่ใช้
`Video-Upscale-Enhanced.json`

### ฟีเจอร์
- ✅ **FlashVSR Upscale** (ขยายความละเอียด 2 เท่า หรือ fix 1080P)
- ✅ **RIFE Interpolation** (เพิ่มความลื่นไหล 2x: 24fps → 48fps)
- ✅ **VRAM Management** (จัดการ VRAM อย่างมีประสิทธิภาพ)
- ✅ **Manual FPS Control** (ควบคุม FPS output ด้วยตัวเอง)

### ขั้นตอนการใช้งาน

#### 1. เปิด Workflow ใน ComfyUI
```bash
# โหลดไฟล์นี้
Video-Upscale-Enhanced.json
```

#### 2. อัปโหลด Output จาก Stage 1
- คลิก Node: **VHS_LoadVideo** (Node 1)
- เลือกไฟล์ที่ได้จาก Stage 1
  ```
  lipsync_output_XXXXX.mp4 (640×1136 @ 24fps)
  ```

#### 3. เลือก Upscale Mode

| Mode | Output Resolution | VRAM | เหมาะสำหรับ |
|------|-------------------|------|-------------|
| **0: No upscale** | 640×1136 (เดิม) | ~3-5GB | ไม่ต้องการเพิ่มความละเอียด |
| **1: 2x upscale** | 1280×2272 | ~8-10GB | ✅ แนะนำ - คุณภาพสูงสุด |
| **2: 1080P fixed** | ~1101×1920 | ~10-13GB | ใช้เมื่อต้องการขนาด 1080P แน่นอน |

**วิธีตั้งค่า**:
- คลิก Node: **Upscale Mode** (Node 5)
- เลือก: `1` (2x upscale) ← **แนะนำ**

#### 4. ตั้งค่า RIFE Interpolation

**4.1 เปิด/ปิด RIFE**
- Node: **Enable RIFE** (Node 10)
- เลือก: `true` (เปิด) ← **แนะนำเพื่อความลื่นไหล**

**4.2 ตั้งค่า Multiplier**
- Node: **RIFE Multiplier** (Node 12)
- เลือก: `2` (เพิ่ม FPS เป็น 2 เท่า)

**4.3 ตั้งค่า Output FPS**  
⚠️ **สำคัญมาก!** ต้องคำนวณด้วยตัวเอง:
- Node: **Output FPS** (Node 13)
- สูตร: `Source FPS × RIFE Multiplier`
- ตัวอย่าง:
  - Source = 24fps, Multiplier = 2 → **ตั้ง 48**
  - Source = 30fps, Multiplier = 2 → **ตั้ง 60**

#### 5. กด Queue Prompt
- VRAM ที่ใช้: **~10-13GB**
- เวลาประมวลผล: **~3-4 นาที สำหรับ 10 วินาที**
- Output: **ไฟล์วิดีโอคุณภาพสูง + ลื่นไหล**

#### 6. ดาวน์โหลด Final Output
```
ComfyUI/output/upscaled_enhanced_XXXXX.mp4
→ วิดีโอสำเร็จรูป 1280×2272 @ 48fps 🎉
```

---

## 📊 VRAM Usage Comparison

### แบบเดิม (Single-Stage with RIFE)
```
┌─────────────────────────────────────────────┐
│ ⚠️ SINGLE WORKFLOW WITH EVERYTHING          │
│ VRAM: ~19-23GB (เสี่ยงเกิน 24GB!)           │
│ Status: ❌ OOM Error                        │
└─────────────────────────────────────────────┘
```

### แบบใหม่ (Two-Stage)
```
┌─────────────────────────────────────────────┐
│ ✅ STAGE 1: Animation Only                  │
│ VRAM: ~15-18GB                              │
│ Status: ✅ Safe                             │
└─────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│ ✅ STAGE 2: Upscale + RIFE                  │
│ VRAM: ~10-13GB                              │
│ Status: ✅ Safe                             │
└─────────────────────────────────────────────┘

Total VRAM: แยกกันประมวลผล → ไม่เกิน 24GB!
```

---

## ⏱️ Processing Time Estimate

สำหรับวิดีโอ 10 วินาที (300 frames @ 30fps):

| Stage | Process | Time | VRAM |
|-------|---------|------|------|
| **Stage 1** | Lip sync + Animation | ~3-5 นาที | ~15-18GB |
| **Stage 2** (No upscale + RIFE) | Interpolation only | ~1-2 นาที | ~5-7GB |
| **Stage 2** (2x upscale + RIFE) | Upscale + Interpolation | ~3-4 นาที | ~10-13GB |
| **Stage 2** (1080P + RIFE) | Upscale + Interpolation | ~4-5 นาที | ~12-16GB |

**Total Time**: ~6-10 นาที สำหรับ 10 วินาที (ขึ้นอยู่กับ Stage 2 mode)

---

## 🎯 Use Case Scenarios

### 🟢 Scenario 1: ต้องการคุณภาพสูงสุด (แนะนำ!)
```
Stage 1: Animation @ 640×1136, 24fps
   ↓
Stage 2: 2x upscale + RIFE 2x
   ↓
Final: 1280×2272 @ 48fps
VRAM: Safe ✅ | Quality: ⭐⭐⭐⭐⭐
```

### 🟡 Scenario 2: ต้องการความเร็ว ไม่ต้องการขยายความละเอียด
```
Stage 1: Animation @ 640×1136, 24fps
   ↓
Stage 2: No upscale + RIFE 2x
   ↓
Final: 640×1136 @ 48fps
VRAM: Safe ✅ | Speed: ⚡⚡⚡⚡⚡
```

### 🟠 Scenario 3: ต้องการ 1080P แน่นอน (สำหรับ YouTube/TikTok)
```
Stage 1: Animation @ 640×1136, 24fps
   ↓
Stage 2: 1080P fixed + RIFE 2x
   ↓
Final: ~1101×1920 @ 48fps
VRAM: Moderate ⚠️ | Platform: Perfect for uploads
```

### 🔴 Scenario 4: ต้องการเฉพาะ animation (ไม่ต้องการ upscale/interpolation)
```
Stage 1: Animation @ 640×1136, 24fps
   ↓
Final: 640×1136 @ 24fps (ข้าม Stage 2)
VRAM: Safe ✅ | Speed: ⚡⚡⚡⚡⚡ | File size: Small
```

---

## ❓ FAQ

### Q1: ทำไมต้องแยกเป็น 2 workflows?
**A**: เพราะการทำ animation, upscale, และ interpolation พร้อมกันใช้ VRAM มากเกินไป (>24GB). การแบ่งออกทำให้แต่ละขั้นตอนใช้ VRAM ไม่เกิน ~15-18GB

### Q2: Stage 2 จำเป็นไหม?
**A**: ไม่จำเป็น! ถ้าคุณพอใจกับ 640×1136 @ 24fps จาก Stage 1 ก็ใช้ได้เลย. Stage 2 เป็นการเพิ่มคุณภาพเท่านั้น

### Q3: ถ้ายังเกิน 24GB ใน Stage 1 ต้องทำยังไง?
**A**: ปรับลดเพิ่มเติม:
```python
# Option 1: ลด frame buffer
Node 75 (VHS_LoadVideo): frame_load_cap = 120 → 60

# Option 2: ลด context window
Node 87 (WanVideoContextOptions): context_frames = 49 → 33

# Option 3: ลดความละเอียด
Nodes 68, 158, 270: 640×1136 → 576×1024
```

### Q4: Output FPS ใน Stage 2 ตั้งยังไง?
**A**: ต้องตั้งด้วยตัวเอง! สูตร:
```
Output FPS = Source FPS × RIFE Multiplier

ตัวอย่าง:
- Source 24fps × RIFE 2x = ตั้ง 48
- Source 30fps × RIFE 2x = ตั้ง 60
- Source 24fps × RIFE 3x = ตั้ง 72
```

### Q5: File size จะใหญ่แค่ไหน?
**A**: ประมาณการ (per minute):
- Stage 1 output (640×1136, 24fps): ~20-30 MB
- Stage 2 output (1280×2272, 48fps): ~90-120 MB

### Q6: ถ้าวิดีโอยาวกว่า 120 frames ทำยังไง?
**A**: ต้องแบ่ง process เป็นส่วน ๆ:
1. ตั้ง `frame_load_cap` และ `skip_first_frames` ใน VHS_LoadVideo
2. Process ทีละ chunk (0-120, 112-232, 224-344, ...)
3. ใช้ 8 frames overlap เพื่อ blend
4. Stitch ด้วย video editor ภายหลัง

---

## 🎓 Best Practices

### ✅ DO
- ✅ ทดสอบด้วยวิดีโอสั้น (5-10 วินาที) ก่อน
- ✅ ตรวจสอบ VRAM usage ด้วย `nvidia-smi`
- ✅ บันทึกการตั้งค่าที่ได้ผลดี
- ✅ เก็บ output จาก Stage 1 ไว้ก่อนทำ Stage 2 (กรณี Stage 2 ล้มเหลว)
- ✅ ตั้ง Output FPS ใน Stage 2 ให้ถูกต้อง

### ❌ DON'T
- ❌ อย่าพยายาม run workflow เดิมที่มี RIFE อยู่ (จะ OOM)
- ❌ อย่าลืม bypass Node 360 ใน Stage 1
- ❌ อย่าลืมตั้ง Output FPS ใน Stage 2
- ❌ อย่า process วิดีโอยาวเกิน 30 วินาทีในครั้งเดียว (แบ่งเป็น chunks)

---

## 📝 Summary Checklist

### Stage 1 Checklist:
- [ ] เปิดไฟล์ `lipsync-ofm+Nabludatel-24GB-NoRIFE.json`
- [ ] อัปโหลดวิดีโอต้นฉบับ (Node 75)
- [ ] ตรวจสอบ Node 360 (RIFE) ถูก bypass (mode = 4)
- [ ] กด Queue Prompt
- [ ] รอจนเสร็จ (~3-5 นาที)
- [ ] ดาวน์โหลด output จาก ComfyUI/output/

### Stage 2 Checklist:
- [ ] เปิดไฟล์ `Video-Upscale-Enhanced.json`
- [ ] อัปโหลด output จาก Stage 1 (Node 1)
- [ ] เลือก Upscale Mode (Node 5): 1 = 2x upscale
- [ ] เปิด RIFE (Node 10): true
- [ ] ตั้ง RIFE Multiplier (Node 12): 2
- [ ] ตั้ง Output FPS (Node 13): Source FPS × 2
- [ ] กด Queue Prompt
- [ ] รอจนเสร็จ (~3-4 นาที)
- [ ] ดาวน์โหลด final output 🎉

---

## 🆘 Troubleshooting

### ปัญหา: Stage 1 ยัง OOM
**แก้ไข**:
1. ลด `frame_load_cap` จาก 120 → 60 (Node 75)
2. ลด `context_frames` จาก 49 → 33 (Node 87)
3. ลดความละเอียดจาก 640×1136 → 576×1024

### ปัญหา: Stage 2 output ความเร็วไม่ถูกต้อง (เร็ว/ช้าเกินไป)
**แก้ไข**:
- ตรวจสอบ Output FPS (Node 13)
- ต้องเป็น: `Source FPS × RIFE Multiplier`
- ตัวอย่าง: 24 × 2 = 48 fps

### ปัญหา: Stage 2 คุณภาพไม่ดี
**แก้ไข**:
- ลด CRF จาก 18 → 15 (Node 16) สำหรับคุณภาพสูงขึ้น
- ตรวจสอบว่า Upscale Mode ตั้งเป็น 1 (2x) แล้ว

### ปัญหา: เสียงไม่ตรงกับภาพใน Stage 2
**แก้ไข**:
- ตรวจสอบว่า Output FPS ถูกต้อง
- เสียงจาก Stage 1 ต้องติดมากับไฟล์วิดีโอ
- ตรวจสอบ audio link ใน Node 16

---

## 📞 Support

หากพบปัญหาหรือมีคำถาม:
1. ตรวจสอบ **OPTIMIZATION-REPORT.md** สำหรับรายละเอียด technical
2. ดู **README-TH.md** สำหรับ Stage 1 guide แบบละเอียด
3. ตรวจสอบ Note nodes ใน workflow (สีเขียว) สำหรับ instructions

---

**เวอร์ชัน**: 2.0 (Two-Stage)  
**วันที่**: May 3, 2026  
**VRAM Target**: 24GB (แบ่งเป็น 2 ขั้นตอน)  
**สถานะ**: ✅ Production Ready
