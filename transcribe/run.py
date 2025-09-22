#!/usr/bin/env python3
"""
Video Transcriber with Whisper Large v3 and Ollama Integration

This script transcribes MP4 videos using Hugging Face's Whisper large v3 model
with GPU acceleration, then formats the output using a local Ollama model.

Requirements:
- CUDA-capable GPU for acceleration
- Local Ollama server running with local model (optional)
- Video file in MP4 format

Usage:
    # Transcribe video with Ollama formatting
    python video_transcriber.py <path_to_video.mp4>
   
    # Transcribe video without Ollama formatting
    python video_transcriber.py <path_to_video.mp4> --no-ollama
   
    # Process existing transcript with Ollama formatting only
    python video_transcriber.py --ollama-only <path_to_transcript.md>
   
    # Process existing transcript with custom output
    python video_transcriber.py --ollama-only <path_to_transcript.md> -o formatted_output.md
"""

import argparse
import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

import torch
from transformers import pipeline, AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa
import numpy as np
import imageio_ffmpeg as ffmpeg


class VideoTranscriber:
    """Transcribes video files using Whisper large v3 and formats with Ollama."""
   
    def __init__(self):
        """Initialize the transcriber with GPU acceleration if available."""
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.whisper_pipeline = None
        self.ollama_url = "http://localhost:11434/api/generate"
       
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
           
            # Create pipeline
            self.whisper_pipeline = pipeline(
                "automatic-speech-recognition",
                model=model,
                tokenizer=processor.tokenizer,
                feature_extractor=processor.feature_extractor,
                max_new_tokens=128,
                chunk_length_s=30,
                batch_size=16,
                return_timestamps=True,
                torch_dtype=self.torch_dtype,
                device=self.device,
            )
           
            print("Whisper model loaded successfully!")
           
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            sys.exit(1)
   
    def extract_audio_from_video(self, video_path: str) -> np.ndarray:
        """Extract audio from video file and convert to format expected by Whisper."""
        print(f"Extracting audio from {video_path}...")
       
        try:
            # Check if video file exists
            if not os.path.exists(video_path):
                raise Exception(f"Video file not found: {video_path}")
           
            # Use imageio_ffmpeg which bundles its own FFmpeg
            temp_audio_path = "temp_audio.wav"
           
            # Get the bundled FFmpeg executable
            ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
           
            # FFmpeg command to extract audio
            ffmpeg_cmd = [
                ffmpeg_exe, "-i", video_path,
                "-vn",  # No video
                "-acodec", "pcm_s16le",  # PCM 16-bit little-endian
                "-ar", "16000",  # Sample rate 16kHz (required by Whisper)
                "-ac", "1",  # Mono channel
                "-y",  # Overwrite output file
                temp_audio_path
            ]
           
            print(f"Using bundled FFmpeg: {ffmpeg_exe}")
            print("This may take a few minutes for large video files...")
           
            # Run FFmpeg with timeout
            import subprocess
            try:
                result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=300)  # 5 minute timeout
            except subprocess.TimeoutExpired:
                print("FFmpeg process timed out after 5 minutes")
                raise Exception("FFmpeg extraction timed out")
           
            if result.returncode != 0:
                print(f"FFmpeg error (return code {result.returncode}):")
                print(f"STDERR: {result.stderr}")
                print(f"STDOUT: {result.stdout}")
                raise Exception("FFmpeg failed to extract audio")
           
            print("FFmpeg extraction completed successfully!")
           
            # Check if output file was created
            if not os.path.exists(temp_audio_path):
                raise Exception(f"Audio file was not created: {temp_audio_path}")
           
            print(f"Loading audio file with librosa...")
            # Load audio with librosa in chunks to handle large files
            try:
                # First, get file info to check size
                file_size = os.path.getsize(temp_audio_path)
                print(f"Audio file size: {file_size / (1024*1024):.1f} MB")
               
                # Always use soundfile for better memory efficiency with large files
                print("Using memory-efficient audio loading...")
                import soundfile as sf
               
                # Read audio file info first
                info = sf.info(temp_audio_path)
                print(f"Audio duration: {info.duration:.1f} seconds")
                print(f"Sample rate: {info.samplerate} Hz")
                print(f"Channels: {info.channels}")
               
                # Read the entire file at once (soundfile is more efficient than librosa for this)
                audio_array, sample_rate = sf.read(temp_audio_path)
               
                # Convert to mono if stereo
                if len(audio_array.shape) > 1:
                    print("Converting stereo to mono...")
                    audio_array = np.mean(audio_array, axis=1)
               
                # Resample to 16kHz if needed using librosa (which is optimized for this)
                if sample_rate != 16000:
                    print(f"Resampling from {sample_rate}Hz to 16kHz...")
                    audio_array = librosa.resample(audio_array, orig_sr=sample_rate, target_sr=16000)
                   
            except Exception as e:
                print(f"Error loading with soundfile: {e}")
                print("Falling back to librosa loading...")
                audio_array, sample_rate = librosa.load(temp_audio_path, sr=16000)
           
            # Clean up
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                print("Temporary audio file cleaned up")
           
            print(f"Audio extracted successfully! Duration: {len(audio_array)/16000:.2f} seconds")
            return audio_array
           
        except Exception as e:
            print(f"Error extracting audio: {e}")
            # Clean up temp file if it exists
            temp_audio_path = "temp_audio.wav"
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            sys.exit(1)
   
    def transcribe_audio(self, audio_array: np.ndarray) -> Dict[str, Any]:
        """Transcribe audio using Whisper large v3."""
        print("Transcribing audio...")
       
        if self.whisper_pipeline is None:
            self.load_whisper_model()
       
        try:
            # Transcribe with timestamps
            result = self.whisper_pipeline(audio_array)
            print("Transcription completed successfully!")
            return result
           
        except Exception as e:
            print(f"Error during transcription: {e}")
            sys.exit(1)
   
    def format_with_ollama(self, transcription_result: Dict[str, Any]) -> str:
        """Format transcription using local Ollama model."""
        print("Formatting transcription with Ollama...")
       
        # Extract text and timestamps
        text = transcription_result.get("text", "")
        chunks = transcription_result.get("chunks", [])
       
        # Create a structured representation
        structured_text = "Raw Transcription:\n" + text + "\n\n"
       
        if chunks:
            structured_text += "Timestamped Segments:\n"
            for i, chunk in enumerate(chunks):
                timestamp = chunk.get("timestamp", [0, 0])
                chunk_text = chunk.get("text", "")
                start_time = self._format_timestamp(timestamp[0])
                end_time = self._format_timestamp(timestamp[1]) if len(timestamp) > 1 else "end"
                structured_text += f"[{start_time} - {end_time}]: {chunk_text.strip()}\n"
       
        # Prepare prompt for Ollama
        prompt = f"""Please format the following video transcription into a well-structured markdown document that is easy to read and follow.

Include:
1. A brief summary at the top
2. Main topics/sections with headers
3. Key points organized logically
4. Timestamps where relevant
5. Clean formatting with proper markdown syntax

Here is the transcription to format:

{structured_text}

Please provide a clean, well-organized markdown version:"""

        try:
            # Send request to Ollama
            payload = {
                "model": "gemma3:4b-it-q8_0",
                "prompt": prompt,
                "stream": False
            }
           
            response = requests.post(self.ollama_url, json=payload, timeout=300)
           
            if response.status_code == 200:
                result = response.json()
                formatted_text = result.get("response", "")
                print("Ollama formatting completed successfully!")
                return formatted_text
            else:
                print(f"Error from Ollama API: {response.status_code}")
                print("Falling back to basic formatting...")
                return self._basic_markdown_format(structured_text)
               
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            print("Falling back to basic formatting...")
            return self._basic_markdown_format(structured_text)
   
    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        if seconds is None:
            return "00:00"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
   
    def _basic_markdown_format(self, text: str) -> str:
        """Basic markdown formatting as fallback."""
        return f"""# Video Transcription

## Summary
This document contains the transcription of the provided video file.

## Content

{text}

---
*Generated using Whisper large v3 and processed automatically*
"""
   
    def process_existing_transcript(self, transcript_path: str, output_path: Optional[str] = None) -> str:
        """Process an existing transcript file with Ollama formatting."""
        print(f"Processing existing transcript: {transcript_path}")
       
        # Check if transcript file exists
        if not os.path.exists(transcript_path):
            print(f"Error: Transcript file '{transcript_path}' not found!")
            sys.exit(1)
       
        # Read the existing transcript
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        except Exception as e:
            print(f"Error reading transcript file: {e}")
            sys.exit(1)
       
        # Extract the structured text from the existing markdown
        # Look for the content section
        if "## Content" in existing_content:
            # Extract content after "## Content" header
            content_start = existing_content.find("## Content") + len("## Content")
            structured_text = existing_content[content_start:].strip()
            # Remove the footer if present
            if "---" in structured_text:
                structured_text = structured_text[:structured_text.rfind("---")].strip()
        else:
            # Use the entire content if no content section found
            structured_text = existing_content
       
        # Create a mock transcription result to use existing format_with_ollama method
        mock_result = {
            "text": structured_text,
            "chunks": []  # We don't have chunks info from the markdown
        }
       
        # Format with Ollama
        formatted_text = self.format_with_ollama(mock_result)
       
        # Save output
        if output_path is None:
            # Create new filename based on original
            transcript_path_obj = Path(transcript_path)
            output_path = transcript_path_obj.parent / f"{transcript_path_obj.stem}_ollama.md"
       
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
       
        print(f"Ollama-formatted transcript saved to: {output_path}")
        return formatted_text

    def transcribe_video(self, video_path: str, output_path: Optional[str] = None, use_ollama: bool = True) -> str:
        """Main function to transcribe video and format output."""
        # Validate input
        if not os.path.exists(video_path):
            print(f"Error: Video file '{video_path}' not found!")
            sys.exit(1)
       
        if not video_path.lower().endswith('.mp4'):
            print("Warning: File does not have .mp4 extension, attempting to process anyway...")
       
        # Extract audio
        audio_array = self.extract_audio_from_video(video_path)
       
        # Transcribe
        transcription_result = self.transcribe_audio(audio_array)
       
        # Format output based on user preference
        if use_ollama:
            formatted_text = self.format_with_ollama(transcription_result)
        else:
            print("Skipping Ollama formatting, using basic format...")
            # Create basic formatted output with timestamps
            text = transcription_result.get("text", "")
            chunks = transcription_result.get("chunks", [])
           
            structured_text = "Raw Transcription:\n" + text + "\n\n"
           
            if chunks:
                structured_text += "Timestamped Segments:\n"
                for i, chunk in enumerate(chunks):
                    timestamp = chunk.get("timestamp", [0, 0])
                    chunk_text = chunk.get("text", "")
                    start_time = self._format_timestamp(timestamp[0])
                    end_time = self._format_timestamp(timestamp[1]) if len(timestamp) > 1 else "end"
                    structured_text += f"[{start_time} - {end_time}]: {chunk_text.strip()}\n"
           
            formatted_text = self._basic_markdown_format(structured_text)
       
        # Save output
        if output_path is None:
            video_name = Path(video_path).stem
            output_path = f"{video_name}_transcription.md"
       
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
       
        print(f"Transcription saved to: {output_path}")
        return formatted_text


def main():
    """Main function to run the video transcriber."""
    parser = argparse.ArgumentParser(
        description="Transcribe MP4 videos using Whisper large v3 and optionally format with Ollama"
    )
   
    # Create mutually exclusive group for input type
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "video_path",
        nargs='?',
        help="Path to the MP4 video file to transcribe"
    )
    input_group.add_argument(
        "--ollama-only",
        metavar="TRANSCRIPT_FILE",
        help="Process existing transcript file with Ollama formatting only"
    )
   
    parser.add_argument(
        "-o", "--output",
        help="Output path for the markdown file (optional)"
    )
    parser.add_argument(
        "--no-ollama",
        action="store_true",
        help="Skip Ollama formatting and use basic markdown format instead (ignored when using --ollama-only)"
    )
   
    args = parser.parse_args()
   
    # Create transcriber instance
    transcriber = VideoTranscriber()
   
    try:
        if args.ollama_only:
            # Process existing transcript with Ollama only
            if args.no_ollama:
                print("Warning: --no-ollama is ignored when using --ollama-only")
            result = transcriber.process_existing_transcript(args.ollama_only, args.output)
            print("\nOllama formatting completed successfully!")
        else:
            # Regular video transcription
            if not args.video_path:
                print("Error: Video path is required when not using --ollama-only")
                sys.exit(1)
           
            result = transcriber.transcribe_video(
                args.video_path,
                args.output,
                use_ollama=not args.no_ollama
            )
            print("\nTranscription completed successfully!")
       
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
