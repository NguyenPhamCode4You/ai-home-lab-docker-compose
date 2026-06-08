# Transcribe

Transcribes video files and YouTube streams using Whisper large-v3 with GPU acceleration, then formats output using a local Ollama model.

## Requirements

- Python 3.14+
- NVIDIA GPU with CUDA support
- NVIDIA driver (610+) + CUDA Toolkit 13.2+
- Local Ollama server (optional, for output formatting)

## CUDA Setup (Windows)

CUDA Toolkit 13.2 must be installed. Verify with:

```powershell
nvcc --version
```

Install PyTorch with CUDA 13.2 support (replaces the default CPU-only build):

```powershell
python -m pip install --force-reinstall torch==2.12.0+cu132 torchvision==0.27.0+cu132 --index-url https://download.pytorch.org/whl/cu132
```

For Python in System PATH:

```powershell
& "C:\python314\python.exe" -m pip install --force-reinstall torch==2.12.0+cu132 torchvision==0.27.0+cu132 --index-url https://download.pytorch.org/whl/cu132
```

For Python in venvironment:

```powershell
& ".venv\Scripts\python.exe" -m pip install --force-reinstall torch==2.12.0+cu132 torchvision==0.27.0+cu132 --index-url https://download.pytorch.org/whl/cu132
```

Verify CUDA is available:

```powershell
& "C:\python314\python.exe" -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0))"
```

## Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

> Note: The first run downloads Whisper large-v3 (~3 GB) from Hugging Face — cached after the first download.

## Transcribe a Video File

```powershell
python run.py "videos/test-video.mp4"

python run.py "videos/test-video.mp4" --continue
```

## Transcribe a YouTube Video

1. Install the browser extension **"Get cookies.txt LOCALLY"** (works offline, safe)
2. Visit YouTube while logged in
3. Click the extension to export cookies
4. Save as `cookies.txt`
5. Run:

```powershell
python run-youtube-stream.py "https://www.youtube.com/watch?v=sSso2J0lWAk" --cookies cookies.txt
```
