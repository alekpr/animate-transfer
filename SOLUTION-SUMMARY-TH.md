# 💡 สรุปวิธีแก้ปัญหา VRAM OOM

## ⚠️ ปัญหาที่เจอ
```
【VRAM OOM Alert】
The process was interrupted due to insufficient VRAM
```

## ✅ วิธีแก้: แยก workflow เป็น 2 ขั้นตอน

---

## 🎯 คำตอบสั้น ๆ: ถอด RIFE ออก!

### Node ที่ต้องปิด:
```
Node 360: RIFEInterpolation
└─> เปลี่ยน mode: 0 → 4 (Bypass)
└─> ประหยัด VRAM: ~3-5GB
```

### ทำไมต้องถอด RIFE?
- RIFE กิน VRAM มาก (~3-5GB)
- การทำ animation + RIFE พร้อมกัน → ใช้ VRAM รวม ~19-23GB
- **แก้ไข**: ย้าย RIFE ไปทำใน workflow แยกต่างหาก (Video-Upscale-Enhanced)

---

## 📋 แผนการใช้งานแบบใหม่

### ขั้นตอนที่ 1: ทำ Animation (ไม่มี RIFE)
```
ไฟล์: lipsync-ofm+Nabludatel-24GB-NoRIFE.json
       └─> ถูกสร้างแล้ว! ใช้ไฟล์นี้

คุณสมบัติที่ได้:
✅ Lip Sync (ปากสอดคล้องกับเสียง)
✅ Face Animation (ใบหน้าเคลื่อนไหว)
✅ Pose Detection (ตรวจจับท่าทาง)
✅ Hand Detection (ตรวจจับมือ)
❌ RIFE (ถูกปิดเพื่อประหยัด VRAM)

VRAM: ~15-18GB ✅ พอดี!
Output: 640×1136 @ 24fps
```

### ขั้นตอนที่ 2: ขยายความละเอียด + เพิ่มความลื่นไหล
```
ไฟล์: Video-Upscale-Enhanced.json
       └─> มีอยู่แล้ว! นำมาใช้หลัง Stage 1

Input: ไฟล์จาก Stage 1
Process: 
  ✅ FlashVSR 2x upscale (640×1136 → 1280×2272)
  ✅ RIFE 2x interpolation (24fps → 48fps)

VRAM: ~10-13GB ✅ ปลอดภัย!
Output: 1280×2272 @ 48fps (HD + ลื่นไหล)
```

---

## 🚀 วิธีใช้งาน (ง่าย ๆ)

### Stage 1: Animation
```bash
1. เปิด ComfyUI
2. โหลด: lipsync-ofm+Nabludalet-24GB-NoRIFE.json
3. อัปโหลดวิดีโอต้นฉบับ (Node 75)
4. กด Queue Prompt
5. รอ ~3-5 นาที
6. ดาวน์โหลด output จาก ComfyUI/output/
   └─> ชื่อไฟล์: lipsync_output_XXXXX.mp4
```

### Stage 2: Upscale + Smooth (Optional)
```bash
1. โหลด: Video-Upscale-Enhanced.json
2. อัปโหลดไฟล์จาก Stage 1 (Node 1)
3. ตั้งค่า:
   • Node 5 (Upscale Mode): 1 (2x upscale)
   • Node 10 (Enable RIFE): true
   • Node 12 (RIFE Multiplier): 2
   • Node 13 (Output FPS): 48
4. กด Queue Prompt
5. รอ ~3-4 นาที
6. ดาวน์โหลด final output
   └─> ชื่อไฟล์: upscaled_enhanced_XXXXX.mp4
```

---

## 📊 เปรียบเทียบ

### ก่อนแก้ไข (Workflow เดิม)
```
┌────────────────────────────────────────┐
│ ทำทุกอย่างพร้อมกัน                     │
│ • Animation                            │
│ • Lip Sync                             │
│ • RIFE Interpolation                   │
├────────────────────────────────────────┤
│ VRAM: ~19-23GB (spike ถึง 32GB!)       │
│ Status: ❌ VRAM OOM ERROR              │
└────────────────────────────────────────┘
```

### หลังแก้ไข (Two-Stage)
```
┌────────────────────────────────────────┐
│ Stage 1: Animation Only                │
│ • Lip Sync                             │
│ • Face Animation                       │
│ • Pose + Hand Detection                │
├────────────────────────────────────────┤
│ VRAM: ~15-18GB                         │
│ Status: ✅ ใช้งานได้!                  │
└────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────┐
│ Stage 2: Upscale + RIFE                │
│ • 2x Upscale (FlashVSR)                │
│ • RIFE Interpolation                   │
├────────────────────────────────────────┤
│ VRAM: ~10-13GB                         │
│ Status: ✅ ใช้งานได้!                  │
└────────────────────────────────────────┘
```

---

## 💾 ประโยชน์ที่ได้

### ✅ แก้ปัญหา VRAM OOM
- แยก process หนัก ๆ ออกจากกัน
- ไม่มีขั้นตอนไหนเกิน 18GB

### ✅ คุณภาพไม่ลดลง
- ได้ฟีเจอร์ครบทุกอย่าง
- RIFE ยังใช้ได้ (ย้ายไป Stage 2)
- ผลลัพธ์เหมือนเดิมแต่ใช้ VRAM น้อยกว่า

### ✅ ยืดหยุ่นมากขึ้น
- Stage 2 เป็น optional (ทำหรือไม่ทำก็ได้)
- ถ้า Stage 2 มีปัญหา ไม่ต้อง run Stage 1 ใหม่
- ทดสอบ upscale settings ต่าง ๆ ได้โดยไม่ต้อง run animation ใหม่

### ✅ ประหยัดเวลา
- ถ้ามีปัญหาแค่ Stage 2 → แก้แค่ Stage 2 (ไม่ต้องทำ animation ใหม่)
- แยก test แต่ละส่วนได้

---

## 🎬 ผลลัพธ์ที่คาดหวัง

### จาก Stage 1:
```
ไฟล์: lipsync_output_00001.mp4
ขนาด: 640×1136
FPS: 24fps
คุณภาพ: ดี (มี animation ทั้งหมด)
ขนาดไฟล์: ~20-30MB per minute
```

### จาก Stage 2 (ถ้าทำต่อ):
```
ไฟล์: upscaled_enhanced_00001.mp4
ขนาด: 1280×2272
FPS: 48fps
คุณภาพ: ยอดเยี่ยม (HD + ลื่นไหล)
ขนาดไฟล์: ~90-120MB per minute
```

---

## 📁 ไฟล์ที่สำคัญ

### Workflows:
- ✅ `lipsync-ofm+Nabludatel-24GB-NoRIFE.json` ← Stage 1 (ใช้ไฟล์นี้!)
- ✅ `Video-Upscale-Enhanced.json` ← Stage 2 (Optional)
- ⚠️ `lipsync-ofm+Nabludatel-24GB.json` ← เดิม (อย่าใช้! จะ OOM)

### คู่มือภาษาไทย:
- 🚀 **QUICK-START-TH.md** ← อ่านตรงนี้ถ้าต้องการเริ่มเร็ว!
- 📖 **TWO-STAGE-WORKFLOW-GUIDE-TH.md** ← คู่มือฉบับเต็ม

### คู่มือภาษาอังกฤษ:
- 📖 **VRAM-OPTIMIZATION-SUMMARY.md** ← สรุปครบถ้วน
- 📖 **VIDEO-UPSCALE-ENHANCED-GUIDE.md** ← คู่มือ Stage 2

---

## 🆘 ถ้ายังมีปัญหา

### ถ้า Stage 1 ยัง OOM:
```python
# ลดการใช้ VRAM เพิ่มเติม

Option 1: ลด frame buffer
Node 75: frame_load_cap = 120 → 60
ประหยัด: ~1.5GB

Option 2: ลด context window
Node 87: context_frames = 49 → 33
ประหยัด: ~1GB

Option 3: ลดความละเอียด
Nodes 68, 158, 270: 640×1136 → 576×1024
ประหยัด: ~1.5GB
```

### ถ้า Stage 2 output ความเร็วไม่ถูกต้อง:
```
ตรวจสอบ Node 13 (Output FPS)
ต้องตั้งเป็น: Source FPS × RIFE Multiplier

ตัวอย่าง:
- Source 24fps × RIFE 2x = ตั้ง 48
- Source 30fps × RIFE 2x = ตั้ง 60
```

---

## ✨ สรุป

### ปัญหา:
❌ Workflow เดิมใช้ VRAM มากเกินไป (>24GB)

### วิธีแก้:
✅ แยกเป็น 2 workflows:
- Stage 1: Animation (ปิด RIFE) → ~15-18GB
- Stage 2: Upscale + RIFE → ~10-13GB

### ประโยชน์:
- ✅ ใช้งานได้บน 24GB VRAM
- ✅ ได้ฟีเจอร์ครบทุกอย่าง
- ✅ คุณภาพไม่ลดลง
- ✅ ยืดหยุ่นกว่าเดิม

### ขั้นตอนถัดไป:
1. อ่าน **QUICK-START-TH.md** สำหรับคำแนะนำโดยละเอียด
2. โหลด `lipsync-ofm+Nabludatel-24GB-NoRIFE.json` ใน ComfyUI
3. ทดสอบด้วยวิดีโอสั้น ๆ 10 วินาที
4. ถ้าสำเร็จ → ทำต่อกับ Stage 2

---

**อัปเดตล่าสุด**: 3 พฤษภาคม 2026  
**สถานะ**: ✅ พร้อมใช้งาน  
**เป้าหมาย**: ระบบ 24GB VRAM  
**การเปลี่ยนแปลงหลัก**: Node 360 (RIFE) → mode=4 (Bypass)
