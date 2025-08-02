# 🔥 Fire Detection from Drone Video Feed

This Python script monitors a folder where drone video files are saved and analyzes them in near real-time to detect fire using color-based image processing.

## ✅ Features
- Detects fire-like colors in video frames using HSV filtering.
- Plays an alarm sound when fire is detected.
- Monitors the most recently updated video file in a folder.
- Works cross-platform (Windows, macOS).
- Supports `.mp4` and `.avi` formats.

## 🛠 Setup Instructions

1. Clone or download this repository.
2. Place your drone video files in the folder:
   - Windows: `C:\Users\<YourUsername>\Videos\DroneFeed`
   - macOS: `/Users/<yourusername>/Videos/DroneFeed`
3. Install required Python packages:

```bash
pip install -r requirements.txt
