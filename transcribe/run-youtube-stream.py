#!/usr/bin/env python3
"""
YouTube Stream Transcriber with Whisper Large v3 and Ollama Integration

This script transcribes audio from YouTube videos/streams in real-time using 
Hugging Face's Whisper large v3 model with GPU acceleration, then formats 
the output using a local Ollama model.

Requirements:
- CUDA-capable GPU for acceleration
- Local Ollama server running with local model (optional)
- yt-dlp for YouTube audio extraction
- ffmpeg for audio processing

Usage:
    # Transcribe YouTube video with Ollama formatting
    python run-youtube-stream.py <youtube_url>
   
    # Transcribe YouTube video without Ollama formatting
    python run-youtube-stream.py <youtube_url> --no-ollama
   
    # Specify output file
    python run-youtube-stream.py <youtube_url> -o output.md
"""

import argparse
import os
import sys
import json
import requests
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import tempfile
import subprocess

import torch
from transformers import pipeline, AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa
import numpy as np
import imageio_ffmpeg as ffmpeg
from tqdm import tqdm


class YouTubeStreamTranscriber:
    """Transcribes YouTube videos/streams using Whisper large v3 and formats with Ollama."""
   
    def __init__(self):
        """Initialize the transcriber with GPU acceleration if available."""
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.whisper_pipeline = None
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_chat_url = "http://localhost:11434/api/chat"
       
        print(f"Using device: {self.device}")
        if self.device == "cpu":
            print("Warning: CUDA not available, using CPU (will be slower)")
           
    def load_whisper_model(self):
        """Load the Whisper large v3 model for transcription."""
        print("Loading Whisper large v3 model...")
       
        model_id = "openai/whisper-large-v3"
       
        try:
            # Load model and processor
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                model_id,
                torch_dtype=self.torch_dtype,
                low_cpu_mem_usage=True,
                use_safetensors=True
            )
            model.to(self.device)
           
            processor = AutoProcessor.from_pretrained(model_id)
           
            # Create pipeline with settings optimized for streaming
            self.whisper_pipeline = pipeline(
                "automatic-speech-recognition",
                model=model,
                tokenizer=processor.tokenizer,
                feature_extractor=processor.feature_extractor,
                max_new_tokens=200,
                chunk_length_s=15,
                batch_size=4,
                return_timestamps="word",
                torch_dtype=self.torch_dtype,
                device=self.device,
                generate_kwargs={
                    "language": "en",
                    "task": "transcribe",
                    "forced_decoder_ids": None,
                }
            )
           
            print("Whisper model loaded successfully!")
           
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            sys.exit(1)
   
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        print("Checking dependencies...")
        
        # Check for yt-dlp
        try:
            result = subprocess.run(
                ["yt-dlp", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✓ yt-dlp found: {result.stdout.strip()}")
            else:
                print("✗ yt-dlp not working properly")
                return False
        except FileNotFoundError:
            print("✗ yt-dlp not found. Please install it:")
            print("  pip install yt-dlp")
            return False
        except Exception as e:
            print(f"✗ Error checking yt-dlp: {e}")
            return False
        
        # Check for ffmpeg (bundled with imageio_ffmpeg)
        try:
            ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
            print(f"✓ ffmpeg found (bundled): {ffmpeg_exe}")
        except Exception as e:
            print(f"✗ Error getting bundled ffmpeg: {e}")
            print("  Please install: pip install imageio-ffmpeg")
            return False
        
        print("All dependencies satisfied!\n")
        return True
   
    def extract_audio_from_youtube(self, youtube_url: str, cookies_from_browser: Optional[str] = None, cookies_file: Optional[str] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Extract audio from YouTube video using yt-dlp."""
        print(f"Extracting audio from YouTube: {youtube_url}")
        
        # Create temporary file for audio
        temp_dir = tempfile.gettempdir()
        temp_audio_path = os.path.join(temp_dir, "youtube_audio.wav")
        
        try:
            # Build base command with cookie support
            base_cmd = ["yt-dlp"]
            cookie_source = None
            
            # Add cookie authentication if provided
            if cookies_from_browser:
                base_cmd.extend(["--cookies-from-browser", cookies_from_browser])
                cookie_source = f"browser: {cookies_from_browser}"
                print(f"Using cookies from browser: {cookies_from_browser}")
                print(f"Note: Please close {cookies_from_browser.capitalize()} browser if cookie extraction fails")
            elif cookies_file:
                base_cmd.extend(["--cookies", cookies_file])
                cookie_source = f"file: {cookies_file}"
                print(f"Using cookies from file: {cookies_file}")
            
            # First, get video info
            print("Fetching video information...")
            info_cmd = base_cmd + [
                "--print", "%(title)s|||%(duration)s|||%(uploader)s",
                "--no-warnings",
                youtube_url
            ]
            
            result = subprocess.run(
                info_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse video info - be more lenient with errors
            video_info = {
                'title': 'Unknown',
                'duration': 0,
                'uploader': 'Unknown'
            }
            
            if result.returncode == 0 and result.stdout.strip():
                info_parts = result.stdout.strip().split('|||')
                video_info = {
                    'title': info_parts[0] if len(info_parts) > 0 and info_parts[0] else 'Unknown',
                    'duration': int(info_parts[1]) if len(info_parts) > 1 and info_parts[1].isdigit() else 0,
                    'uploader': info_parts[2] if len(info_parts) > 2 and info_parts[2] else 'Unknown'
                }
            else:
                # If info extraction fails, print warning but continue
                print("Warning: Could not extract full video info, continuing with download...")
                if result.stderr:
                    print(f"Info extraction stderr: {result.stderr[:200]}")
            
            print(f"Video: {video_info['title']}")
            print(f"Uploader: {video_info['uploader']}")
            if video_info['duration'] > 0:
                minutes = video_info['duration'] // 60
                seconds = video_info['duration'] % 60
                print(f"Duration: {minutes}:{seconds:02d}")
            
            # Download audio using yt-dlp and convert to WAV
            print("Downloading and extracting audio...")
            print("This may take a few minutes depending on video length and connection speed...")
            
            # Get bundled ffmpeg path for yt-dlp to use
            ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
            ffmpeg_location = str(Path(ffmpeg_exe).parent)
            
            download_cmd = base_cmd + [
                "-x",  # Extract audio
                "--audio-format", "wav",
                "--audio-quality", "0",  # Best quality
                "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",  # 16kHz mono
                "--ffmpeg-location", ffmpeg_location,  # Use bundled ffmpeg
                "-o", temp_audio_path.replace('.wav', '.%(ext)s'),
                youtube_url,
                "--no-playlist",  # Don't download playlists
                "--quiet",  # Reduce output
                "--progress",  # Show progress
            ]
            
            result = subprocess.run(
                download_cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode != 0:
                stderr_str = result.stderr if result.stderr else ''
                
                # Check for DPAPI decryption error (Windows Chrome encryption issue)
                if "Failed to decrypt with DPAPI" in stderr_str:
                    print(f"\nWarning: Failed to decrypt Chrome cookies (DPAPI error)")
                    print("This is a known issue with Windows Chrome cookie encryption.")
                    print(f"Solutions:")
                    print(f"  1. Try Firefox instead: --cookies-from-browser firefox")
                    print(f"  2. Export cookies manually using a browser extension")
                    print(f"  3. Try without cookies (may work for public videos)")
                    
                    # Attempt without cookies as fallback
                    print(f"\nAttempting download without cookies...")
                    fallback_cmd = ["yt-dlp",
                        "-x",
                        "--audio-format", "wav",
                        "--audio-quality", "0",
                        "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",
                        "--ffmpeg-location", ffmpeg_location,
                        "-o", temp_audio_path.replace('.wav', '.%(ext)s'),
                        youtube_url,
                        "--no-playlist",
                        "--quiet",
                        "--progress",
                    ]
                    
                    fallback_result = subprocess.run(
                        fallback_cmd,
                        capture_output=True,
                        text=True,
                        timeout=600
                    )
                    
                    if fallback_result.returncode != 0:
                        fallback_stderr = fallback_result.stderr if fallback_result.stderr else ''
                        error_msg = "yt-dlp failed to download audio (with and without cookies)"
                        if "Sign in to confirm" in fallback_stderr:
                            error_msg += "\n\nYouTube requires authentication for this video. Try:"
                            error_msg += "\n  1. Use Firefox: --cookies-from-browser firefox"
                            error_msg += "\n  2. Export cookies using browser extension like 'Get cookies.txt LOCALLY'"
                            error_msg += "\n     Then use: --cookies <file>"
                            error_msg += "\n  More info: https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp"
                        raise Exception(error_msg)
                    else:
                        print("✓ Fallback download without cookies succeeded!")
                
                # Check for cookie database locked error
                elif "Could not copy" in stderr_str and "cookie database" in stderr_str and cookie_source:
                    print(f"\nWarning: Failed to extract cookies from {cookie_source}")
                    print("This usually happens when the browser is running.")
                    print(f"Solutions:")
                    print(f"  1. Close {cookies_from_browser.capitalize() if cookies_from_browser else 'your browser'} completely and try again")
                    print(f"  2. Export cookies to a file and use --cookies <file>")
                    print(f"  3. Try running without cookies (may not work for all videos)")
                    
                    # Attempt without cookies as fallback
                    print(f"\nAttempting download without cookies...")
                    fallback_cmd = ["yt-dlp",
                        "-x",
                        "--audio-format", "wav",
                        "--audio-quality", "0",
                        "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",
                        "--ffmpeg-location", ffmpeg_location,
                        "-o", temp_audio_path.replace('.wav', '.%(ext)s'),
                        youtube_url,
                        "--no-playlist",
                        "--quiet",
                        "--progress",
                    ]
                    
                    fallback_result = subprocess.run(
                        fallback_cmd,
                        capture_output=True,
                        text=True,
                        timeout=600
                    )
                    
                    if fallback_result.returncode != 0:
                        fallback_stderr = fallback_result.stderr if fallback_result.stderr else ''
                        error_msg = "yt-dlp failed to download audio (with and without cookies)"
                        if "Sign in to confirm" in fallback_stderr:
                            error_msg += "\n\nYouTube is requesting authentication. Please:"
                            error_msg += f"\n  1. Close {cookies_from_browser.capitalize() if cookies_from_browser else 'all browsers'} completely"
                            error_msg += "\n  2. Run the script again with --cookies-from-browser"
                            error_msg += "\n  OR export cookies to file:"
                            error_msg += "\n     https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp"
                        raise Exception(error_msg)
                    else:
                        print("✓ Fallback download without cookies succeeded!")
                
                elif "Sign in to confirm" in stderr_str:
                    error_msg = "yt-dlp failed to download audio"
                    error_msg += "\n\nYouTube is requesting authentication. Please use one of these options:"
                    error_msg += "\n  --cookies-from-browser chrome    (extract cookies from Chrome - close browser first!)"
                    error_msg += "\n  --cookies-from-browser firefox   (extract cookies from Firefox - close browser first!)"
                    error_msg += "\n  --cookies-from-browser edge      (extract cookies from Edge - close browser first!)"
                    error_msg += "\n  --cookies <file>                 (use cookies from file)"
                    error_msg += "\n\nTo export cookies: https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp"
                    raise Exception(error_msg)
                else:
                    raise Exception(f"yt-dlp failed to download audio: {stderr_str[:200]}")
            
            # Check if file was created
            if not os.path.exists(temp_audio_path):
                raise Exception(f"Audio file was not created: {temp_audio_path}")
            
            print("Loading audio file...")
            # Load audio with soundfile for efficiency
            try:
                import soundfile as sf
                
                info = sf.info(temp_audio_path)
                print(f"Audio duration: {info.duration:.1f} seconds")
                print(f"Sample rate: {info.samplerate} Hz")
                
                # Read audio
                audio_array, sample_rate = sf.read(temp_audio_path)
                
                # Convert to mono if stereo
                if len(audio_array.shape) > 1:
                    audio_array = np.mean(audio_array, axis=1)
                
                # Resample to 16kHz if needed
                if sample_rate != 16000:
                    print(f"Resampling from {sample_rate}Hz to 16kHz...")
                    audio_array = librosa.resample(
                        audio_array,
                        orig_sr=sample_rate,
                        target_sr=16000,
                        res_type='kaiser_best'
                    )
                
            except ImportError:
                print("soundfile not available, falling back to librosa...")
                audio_array, sample_rate = librosa.load(temp_audio_path, sr=16000)
            
            # Clean up temporary file
            try:
                os.remove(temp_audio_path)
                print("Temporary audio file cleaned up")
            except:
                pass
            
            print(f"Audio extracted successfully! Duration: {len(audio_array)/16000:.2f} seconds")
            
            return audio_array, video_info
            
        except subprocess.TimeoutExpired:
            print("Download timed out after 10 minutes")
            raise Exception("YouTube download timed out")
        except Exception as e:
            print(f"Error extracting audio from YouTube: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_audio_path):
                try:
                    os.remove(temp_audio_path)
                except:
                    pass
            raise
   
    def split_audio_into_chunks(self, audio_array: np.ndarray, chunk_duration: int = 15, sample_rate: int = 16000) -> List[Tuple[np.ndarray, float, float]]:
        """Split audio array into chunks of specified duration."""
        chunk_samples = chunk_duration * sample_rate
        total_samples = len(audio_array)
        chunks = []
        
        for i in range(0, total_samples, chunk_samples):
            chunk = audio_array[i:i + chunk_samples]
            start_time = i / sample_rate
            end_time = min((i + chunk_samples) / sample_rate, total_samples / sample_rate)
            chunks.append((chunk, start_time, end_time))
        
        return chunks
    
    def transcribe_audio_chunk(self, audio_chunk: np.ndarray, start_time: float, end_time: float) -> Dict[str, Any]:
        """Transcribe a single audio chunk."""
        try:
            # Skip empty or very short chunks
            if len(audio_chunk) < 1600:  # Less than 0.1 seconds
                return {"text": "", "chunks": []}
            
            # For very long chunks, trim to avoid token limit issues
            max_chunk_length = 15 * 16000  # 15 seconds at 16kHz
            if len(audio_chunk) > max_chunk_length:
                audio_chunk = audio_chunk[:max_chunk_length]
                end_time = start_time + 15
            
            # Transcribe chunk
            result = self.whisper_pipeline(
                audio_chunk,
                generate_kwargs={
                    "language": "en",
                    "task": "transcribe",
                    "max_new_tokens": 200
                }
            )
            
            if not result or not result.get("text"):
                return {"text": "", "chunks": []}
            
            return result
            
        except Exception as e:
            print(f"Error transcribing chunk {start_time:.1f}s-{end_time:.1f}s: {e}")
            return {"text": "", "chunks": []}
    
    def transcribe_audio(self, audio_array: np.ndarray, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """Transcribe audio using Whisper large v3 with chunked processing."""
        total_duration = len(audio_array) / 16000
        print(f"\nTranscribing audio (duration: {total_duration:.1f}s)...")
        
        if self.whisper_pipeline is None:
            self.load_whisper_model()
        
        try:
            # Split audio into chunks
            chunks = self.split_audio_into_chunks(audio_array, chunk_duration=15)
            print(f"Processing {len(chunks)} chunks of ~15 seconds each...")
            
            all_text = []
            start_time = time.time()
            
            # Process chunks with progress bar
            with tqdm(total=len(chunks), desc="Transcribing", unit="chunk") as pbar:
                for i, (chunk_audio, chunk_start, chunk_end) in enumerate(chunks):
                    # Update progress bar description
                    pbar.set_description(f"Transcribing [{self._format_timestamp(chunk_start)}-{self._format_timestamp(chunk_end)}]")
                    
                    # Transcribe chunk
                    chunk_result = self.transcribe_audio_chunk(chunk_audio, chunk_start, chunk_end)
                    
                    # Collect results with segment timestamp
                    if chunk_result.get("text"):
                        segment_timestamp = f"[{self._format_timestamp(chunk_start)} - {self._format_timestamp(chunk_end)}] "
                        timestamped_text = segment_timestamp + chunk_result["text"].strip()
                        all_text.append(timestamped_text)
                    
                    # Update progress
                    pbar.update(1)
                    
                    # Show elapsed time and ETA
                    elapsed = time.time() - start_time
                    completed = i + 1
                    if completed > 0:
                        avg_time_per_chunk = elapsed / completed
                        remaining_chunks = len(chunks) - completed
                        eta = avg_time_per_chunk * remaining_chunks
                        pbar.set_postfix({
                            'elapsed': f"{elapsed:.0f}s",
                            'eta': f"{eta:.0f}s",
                            'avg': f"{avg_time_per_chunk:.1f}s/chunk"
                        })
            
            # Combine all results
            combined_text = "\n\n".join(all_text).strip()
            combined_result = {
                "text": combined_text,
                "chunks": [],
                "video_info": video_info
            }
            
            total_elapsed = time.time() - start_time
            print(f"\nTranscription completed successfully in {total_elapsed:.1f}s!")
            print(f"Processing speed: {total_duration/total_elapsed:.2f}x real-time")
            print(f"Total transcribed text length: {len(combined_text)} characters")
            
            return combined_result
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
   
    def format_with_ollama(self, transcription_result: Dict[str, Any]) -> str:
        """Format transcription using local Ollama model."""
        print("\nFormatting transcription with Ollama...")
       
        # Extract text and video info
        text = transcription_result.get("text", "")
        video_info = transcription_result.get("video_info", {})
       
        # Create header with video info
        header = "Video Information:\n"
        header += f"- Title: {video_info.get('title', 'Unknown')}\n"
        header += f"- Uploader: {video_info.get('uploader', 'Unknown')}\n"
        if video_info.get('duration', 0) > 0:
            minutes = video_info['duration'] // 60
            seconds = video_info['duration'] % 60
            header += f"- Duration: {minutes}:{seconds:02d}\n"
        header += "\n"
        
        # Create structured text
        structured_text = header + "Transcription with Segment Timestamps:\n" + text + "\n\n"
       
        # Prepare prompt for Ollama
        prompt = f"""Please create a comprehensive, fact-based educational document from the following YouTube video transcription. Transform this raw transcript into a well-structured knowledge resource.

Requirements:
1. Write a concise, factual document covering all content discussed in the video
2. Enrich the knowledge with your own expertise - add context, explanations, and related information that would help readers understand the topics better
3. Make it simple to understand and illustrative using:
   - Tables for comparisons or data
   - Diagrams (in mermaid diagram language)
   - Examples to clarify concepts
   - Equations or formulas when relevant (using proper markdown math syntax)
4. Include timestamps on important points so viewers can jump to the video to hear more details (format: **[MM:SS]** for emphasis)
5. Structure with clear headers, subheaders, and logical flow
6. Use proper markdown formatting throughout

Create an educational resource that stands alone as a comprehensive guide while still referencing the source video through timestamps.

Here is the transcription to transform:

{structured_text}

Please provide a well-organized, educational markdown document:"""

        try:
            # Try chat API first
            chat_payload = {
                "model": "gemma2:2b",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            }
           
            print(f"Trying Ollama chat API...")
            response = requests.post(self.ollama_chat_url, json=chat_payload, timeout=300)
           
            if response.status_code == 200:
                result = response.json()
                formatted_text = result.get("message", {}).get("content", "")
                if formatted_text:
                    print("Ollama formatting completed successfully!")
                    return formatted_text
            
            # Fallback to generate API
            print(f"Chat API failed ({response.status_code}), trying generate API...")
            generate_payload = {
                "model": "gemma2:2b",
                "prompt": prompt,
                "stream": False
            }
           
            response = requests.post(self.ollama_url, json=generate_payload, timeout=300)
           
            if response.status_code == 200:
                result = response.json()
                formatted_text = result.get("response", "")
                if formatted_text:
                    print("Ollama formatting completed successfully!")
                    return formatted_text
            
            print(f"Error from Ollama API: {response.status_code}")
            print("Falling back to basic formatting...")
            return self._basic_markdown_format(structured_text, video_info)
               
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            print("Falling back to basic formatting...")
            return self._basic_markdown_format(structured_text, video_info)
   
    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        if seconds is None:
            return "00:00"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
   
    def _basic_markdown_format(self, text: str, video_info: Dict[str, Any]) -> str:
        """Basic markdown formatting as fallback."""
        header = f"""# YouTube Video Transcription

## Video Information
- **Title**: {video_info.get('title', 'Unknown')}
- **Uploader**: {video_info.get('uploader', 'Unknown')}
"""
        if video_info.get('duration', 0) > 0:
            minutes = video_info['duration'] // 60
            seconds = video_info['duration'] % 60
            header += f"- **Duration**: {minutes}:{seconds:02d}\n"
        
        return header + f"""
## Content

{text}

---
*Generated using Whisper large v3 and processed automatically*
"""
   
    def transcribe_youtube(self, youtube_url: str, output_path: Optional[str] = None, use_ollama: bool = True, cookies_from_browser: Optional[str] = None, cookies_file: Optional[str] = None) -> str:
        """Main function to transcribe YouTube video and format output."""
        overall_start_time = time.time()
        
        # Check dependencies
        if not self.check_dependencies():
            print("\nPlease install missing dependencies and try again.")
            sys.exit(1)
        
        print(f"\n=== Starting YouTube Video Transcription ===")
        print(f"URL: {youtube_url}")
        print(f"Device: {self.device}")
        print(f"Ollama formatting: {'Enabled' if use_ollama else 'Disabled'}")
        print("="*50)
        
        # Extract audio from YouTube
        print("\nStep 1/3: Audio Extraction from YouTube")
        step_start = time.time()
        audio_array, video_info = self.extract_audio_from_youtube(youtube_url, cookies_from_browser, cookies_file)
        step_duration = time.time() - step_start
        print(f"Audio extraction completed in {step_duration:.1f}s\n")
        
        # Transcribe
        print("Step 2/3: Audio Transcription")
        step_start = time.time()
        transcription_result = self.transcribe_audio(audio_array, video_info)
        step_duration = time.time() - step_start
        print(f"Audio transcription completed in {step_duration:.1f}s\n")
        
        # Format output
        print("Step 3/3: Text Formatting")
        step_start = time.time()
        
        text = transcription_result.get("text", "")
        raw_structured_text = "Transcription with Segment Timestamps:\n" + text + "\n\n"
        
        # Save raw transcription
        if output_path is None:
            # Create filename from video title
            safe_title = "".join(c for c in video_info.get('title', 'youtube_video') 
                                if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
            raw_output_path = f"{safe_title}_raw_transcription.md"
        else:
            output_path_obj = Path(output_path)
            raw_output_path = output_path_obj.parent / f"{output_path_obj.stem}_raw{output_path_obj.suffix}"
        
        raw_formatted_text = self._basic_markdown_format(raw_structured_text, video_info)
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write(raw_formatted_text)
        print(f"Raw transcription saved to: {raw_output_path}")
        
        # Format with Ollama if requested
        if use_ollama:
            formatted_text = self.format_with_ollama(transcription_result)
        else:
            formatted_text = raw_formatted_text
        
        step_duration = time.time() - step_start
        print(f"Text formatting completed in {step_duration:.1f}s\n")
        
        # Save final output
        if output_path is None:
            safe_title = "".join(c for c in video_info.get('title', 'youtube_video') 
                                if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]
            if use_ollama:
                output_path = f"{safe_title}_transcription_ollama.md"
            else:
                output_path = f"{safe_title}_transcription.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        
        # Final summary
        total_duration = time.time() - overall_start_time
        audio_duration = len(audio_array) / 16000
        
        print("=" * 50)
        print("=== Transcription Complete ===")
        print(f"Raw transcription: {raw_output_path}")
        if use_ollama:
            print(f"Ollama formatted: {output_path}")
        else:
            print(f"Final output: {output_path}")
        print(f"Audio duration: {audio_duration:.1f}s")
        print(f"Total processing time: {total_duration:.1f}s")
        print(f"Overall processing speed: {audio_duration/total_duration:.2f}x real-time")
        print(f"Word count: ~{len(transcription_result.get('text', '').split())} words")
        print("=" * 50)
        
        return formatted_text


def main():
    """Main function to run the YouTube stream transcriber."""
    parser = argparse.ArgumentParser(
        description="Transcribe YouTube videos using Whisper large v3 and optionally format with Ollama"
    )
    
    parser.add_argument(
        "youtube_url",
        help="YouTube URL to transcribe"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output path for the markdown file (optional)"
    )
    parser.add_argument(
        "--no-ollama",
        action="store_true",
        help="Skip Ollama formatting and use basic markdown format instead"
    )
    parser.add_argument(
        "--cookies-from-browser",
        metavar="BROWSER",
        help="Browser to extract cookies from (e.g., chrome, firefox, edge). Helps bypass bot detection."
    )
    parser.add_argument(
        "--cookies",
        metavar="FILE",
        help="Path to cookies file in Netscape format"
    )
    
    args = parser.parse_args()
    
    # Create transcriber instance
    transcriber = YouTubeStreamTranscriber()
    
    try:
        result = transcriber.transcribe_youtube(
            args.youtube_url,
            args.output,
            use_ollama=not args.no_ollama,
            cookies_from_browser=args.cookies_from_browser,
            cookies_file=args.cookies
        )
        print("\nTranscription completed successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
