#!/usr/bin/env python3
"""
用 OpenCV inpainting 自然去除视频右上角 PlayRobot Logo，
再叠加 WW-Robot Logo，通过 ffmpeg pipe 编码为 webm。
"""

import cv2
import numpy as np
import subprocess
import sys

# ── 路径 ──────────────────────────────────────────────────────────────
SRC   = "C:/Users/49563/Documents/LinkerHand L20 - Teaching Experiments.mkv"
OUT   = "C:/Users/49563/WorkBuddy/2026-06-23-18-06-23/UnitClaw.cn/assets/videos/hand-experiments.webm"
LOGO  = "C:/Users/49563/WorkBuddy/2026-06-23-18-06-23/UnitClaw.cn/assets/videos/wwrobot-logo.png"
FFMPEG = "C:/Users/49563/AppData/Roaming/Python/Python314/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

# ── 视频信息 ────────────────────────────────────────────────────────
cap = cv2.VideoCapture(SRC)
fps   = cap.get(cv2.CAP_PROP_FPS)
w     = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total / fps
print(f"[信息] 视频 {w}x{h}  {fps}fps  {total}帧  {duration:.1f}s")

# ── 裁剪时长（去掉最后4秒）─────────────────────────────────────────
cut_duration = max(0, duration - 4.0)
cut_frames   = int(cut_duration * fps)
print(f"[信息] 裁剪后 {cut_duration:.1f}s  ({cut_frames}帧)")

# ── 创建 inpaint mask（Logo 区域）──────────────────────────────────
# Logo 范围：x=1290-1920, y=0-210 (精确像素检测结果)
mask = np.zeros((h, w), dtype=np.uint8)
mask[0:210, 1290:1920] = 255
# 轻微扩张让融合更自然
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
mask = cv2.dilate(mask, kernel, iterations=1)
print(f"[信息] Mask 白色像素数: {np.sum(mask == 255)}")

# ── 读取 WW-Robot Logo（带 alpha）──────────────────────────────────
logo_bgra = cv2.imread(LOGO, cv2.IMREAD_UNCHANGED)
if logo_bgra is None:
    print("[错误] 无法读取 WW-Robot Logo"); sys.exit(1)
# 如果没有 alpha 通道，加一个全不透明的
if logo_bgra.shape[2] == 3:
    alpha = np.full((logo_bgra.shape[0], logo_bgra.shape[1], 1), 255, dtype=np.uint8)
    logo_bgra = np.concatenate([logo_bgra, alpha], axis=2)
print(f"[信息] Logo 尺寸: {logo_bgra.shape}")

# 缩放 Logo 到合适大小（高度 100px，放在右上角）
logo_h = 100
scale  = logo_h / logo_bgra.shape[0]
logo_w = int(logo_bgra.shape[1] * scale)
logo_resized = cv2.resize(logo_bgra, (logo_w, logo_h), interpolation=cv2.INTER_AREA)
# Logo 位置：右上角，距右边缘 20px，距顶 15px
logo_x = w - logo_w - 20
logo_y = 15
print(f"[信息] Logo 放置位置: ({logo_x}, {logo_y})  size={logo_w}x{logo_h}")

# ── 启动 ffmpeg 进程（从 stdin 读取原始帧）────────────────────────
# 先只处理视频帧，音频后面单独混流
ffmpeg_proc = subprocess.Popen(
    [
        FFMPEG, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{w}x{h}", "-pix_fmt", "bgr24",
        "-r", str(int(fps)),
        "-i", "pipe:0",
        "-c:v", "libvpx-vp9", "-crf", "28", "-b:v", "2M",
        "-maxrate", "4M", "-bufsize", "8M",
        "-threads", "4", "-cpu-used", "4", "-deadline", "good", "-row-mt", "1",
        "-pix_fmt", "yuv420p",
        "-an",   # 先不要音频
        OUT,
    ],
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# ── 逐帧处理 ────────────────────────────────────────────────────────
print("[开始] 逐帧 inpainting ...")
import time
t0 = time.time()
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret or frame_idx >= cut_frames:
        break

    # 每 100 帧打印一次进度
    if frame_idx % 100 == 0:
        pct = frame_idx / cut_frames * 100
        print(f"  帧 {frame_idx}/{cut_frames}  ({pct:.0f}%)")

    # 1) inpainting 去除 Logo
    inpainted = cv2.inpaint(frame, mask, 5, cv2.INPAINT_TELEA)

    # 2) 叠加 WW-Robot Logo（alpha 混合）
    alpha_logo = logo_resized[:, :, 3:4].astype(np.float32) / 255.0
    rgb_logo  = logo_resized[:, :, :3].astype(np.float32)
    bg_region  = inpainted[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w].astype(np.float32)
    blended = bg_region * (1 - alpha_logo) + rgb_logo * alpha_logo
    inpainted[logo_y:logo_y+logo_h, logo_x:logo_x+logo_w] = blended.astype(np.uint8)

    # 3) 写入 ffmpeg stdin
    try:
        ffmpeg_proc.stdin.write(inpainted.tobytes())
    except BrokenPipeError:
        print("[错误] ffmpeg pipe 已关闭")
        break

    frame_idx += 1

cap.release()

# ── 关闭 stdin，等待 ffmpeg 完成 ──────────────────────────────────
ffmpeg_proc.stdin.close()
print("[等待] ffmpeg 编码完成 ...")
stderr = ffmpeg_proc.communicate()[1]
if ffmpeg_proc.returncode != 0:
    print(f"[错误] ffmpeg 退出码 {ffmpeg_proc.returncode}")
    print(stderr.decode(errors="ignore")[-2000:])
    sys.exit(1)

elapsed = time.time() - t0
print(f"[完成] 视频帧处理完毕，耗时 {elapsed:.1f}s")

# ── 混流音频 ─────────────────────────────────────────────────────────
# 用 ffmpeg 从源视频提取对应时长的音频，混入 webm
print("[等待] 混流音频 ...")
temp_out = OUT + ".tmp.webm"
import os
os.replace(OUT, temp_out)
subprocess.run(
    [
        FFMPEG, "-y",
        "-i", temp_out,
        "-ss", "0", "-t", str(cut_duration),
        "-i", SRC,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "libopus", "-b:a", "96k",
        OUT,
    ],
    check=True,
)
os.remove(temp_out)

# ── 输出文件信息 ────────────────────────────────────────────────────
size_mb = os.path.getsize(OUT) / 1024 / 1024
print(f"[完成] 输出: {OUT}")
print(f"[完成] 文件大小: {size_mb:.1f} MB")
print(f"[完成] 总耗时: {time.time() - t0:.1f}s")
