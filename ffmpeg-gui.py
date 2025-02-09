import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def find_ffmpeg():
    paths = [
        "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
        "C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe",
        "C:\\Program Files\\ffmpeg\\ffmpeg.exe",
        "C:\\Program Files (x86)\\ffmpeg\\ffmpeg.exe",
        "C:\\ffmpeg\\ffmpeg.exe",
        "C:\\ffmpeg\\bin\\ffmpeg.exe",
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return filedialog.askopenfilename(title="Select FFmpeg Binary", filetypes=[("Executable", "*.exe")])

def browse_input():
    filename = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, filename)

def browse_output():
    filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filename)

def set_preset(preset):
    presets = {
        "Default": ("2500000", "192000", "1280x720", "30"),
        "LQ": ("50000", "25000", "640x480", "10"),
        "MQ": ("75000", "50000", "640x480", "20")
    }
    if preset in presets:
        video_bitrate_entry.delete(0, tk.END)
        video_bitrate_entry.insert(0, presets[preset][0])
        audio_bitrate_entry.delete(0, tk.END)
        audio_bitrate_entry.insert(0, presets[preset][1])
        resolution_entry.delete(0, tk.END)
        resolution_entry.insert(0, presets[preset][2])
        fps_entry.delete(0, tk.END)
        fps_entry.insert(0, presets[preset][3])

def run_ffmpeg():
    input_file = input_entry.get()
    output_file = output_entry.get()
    video_bitrate = video_bitrate_entry.get()
    audio_bitrate = audio_bitrate_entry.get()
    resolution = resolution_entry.get()
    fps = fps_entry.get()
    ffmpeg_path = find_ffmpeg()
    
    if not ffmpeg_path:
        messagebox.showerror("Error", "FFmpeg binary not found.")
        return
    
    command = [
        ffmpeg_path, "-i", input_file,
        "-b:v", f"{video_bitrate}",
        "-b:a", f"{audio_bitrate}",
        "-s", resolution,
        "-r", fps,
        output_file
    ]
    
    subprocess.run(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

root = tk.Tk()
root.title("FFmpeg GUI")

# Preset Selection
preset_label = tk.Label(root, text="Preset:")
preset_label.grid(row=0, column=0)
preset_var = tk.StringVar(root)
preset_var.set("Default")
preset_menu = tk.OptionMenu(root, preset_var, "Default", "LQ", "MQ", command=set_preset)
preset_menu.grid(row=0, column=1)

# Input file
input_label = tk.Label(root, text="Input File:")
input_label.grid(row=1, column=0)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=1, column=1)
browse_input_btn = tk.Button(root, text="Browse", command=browse_input)
browse_input_btn.grid(row=1, column=2)

# Output file
output_label = tk.Label(root, text="Output File:")
output_label.grid(row=2, column=0)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1)
browse_output_btn = tk.Button(root, text="Browse", command=browse_output)
browse_output_btn.grid(row=2, column=2)

# Video Bitrate
video_bitrate_label = tk.Label(root, text="Video Bitrate (bps):")
video_bitrate_label.grid(row=3, column=0)
video_bitrate_entry = tk.Entry(root)
video_bitrate_entry.grid(row=3, column=1)
video_bitrate_entry.insert(0, "2500000")

# Audio Bitrate
audio_bitrate_label = tk.Label(root, text="Audio Bitrate (bps):")
audio_bitrate_label.grid(row=4, column=0)
audio_bitrate_entry = tk.Entry(root)
audio_bitrate_entry.grid(row=4, column=1)
audio_bitrate_entry.insert(0, "192000")

# Resolution
resolution_label = tk.Label(root, text="Resolution (e.g., 1920x1080):")
resolution_label.grid(row=5, column=0)
resolution_entry = tk.Entry(root)
resolution_entry.grid(row=5, column=1)
resolution_entry.insert(0, "1280x720")

# FPS
fps_label = tk.Label(root, text="FPS:")
fps_label.grid(row=6, column=0)
fps_entry = tk.Entry(root)
fps_entry.grid(row=6, column=1)
fps_entry.insert(0, "30")

# Run FFmpeg Button
run_btn = tk.Button(root, text="Convert", command=run_ffmpeg)
run_btn.grid(row=7, column=1)

root.mainloop()
