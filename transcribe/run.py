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
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

import torch
from transformers import pipeline, AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa
import numpy as np
import imageio_ffmpeg as ffmpeg
from tqdm import tqdm


class VideoTranscriber:
    """Transcribes video files using Whisper large v3 and formats with Ollama."""
   
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
           
            # Create pipeline with better settings for chunked processing
            self.whisper_pipeline = pipeline(
                "automatic-speech-recognition",
                model=model,
                tokenizer=processor.tokenizer,
                feature_extractor=processor.feature_extractor,
                max_new_tokens=200,  # Reduced to avoid token limit issues
                chunk_length_s=15,   # Reduced to avoid timeout
                batch_size=4,        # Further reduced for stability
                return_timestamps="word",  # Word-level timestamps
                torch_dtype=self.torch_dtype,
                device=self.device,
                # Language and task settings to avoid warnings
                generate_kwargs={
                    "language": "en",  # Force English to avoid auto-detection
                    "task": "transcribe",  # Transcribe instead of translate
                    "forced_decoder_ids": None,  # Let model handle this
                }
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
           
            print(f"Loading audio file...")
            # Load audio with memory-efficient processing
            try:
                # First, get file info to check size
                file_size = os.path.getsize(temp_audio_path)
                print(f"Audio file size: {file_size / (1024*1024):.1f} MB")
               
                # Use soundfile for better memory efficiency with large files
                print("Loading audio with progress monitoring...")
                import soundfile as sf
               
                # Read audio file info first
                info = sf.info(temp_audio_path)
                duration = info.duration
                sample_rate = info.samplerate
                channels = info.channels
                
                print(f"Audio duration: {duration:.1f} seconds")
                print(f"Sample rate: {sample_rate} Hz")
                print(f"Channels: {channels}")
               
                # For very large files (> 100MB), consider chunked loading
                if file_size > 100 * 1024 * 1024:  # 100MB
                    print("Large file detected, using chunked loading...")
                    # Load in chunks to manage memory
                    chunk_size = sample_rate * 60  # 1 minute chunks
                    audio_chunks = []
                    
                    with tqdm(total=int(info.frames), desc="Loading audio", unit="samples") as pbar:
                        with sf.SoundFile(temp_audio_path) as f:
                            while True:
                                chunk = f.read(chunk_size)
                                if chunk.size == 0:
                                    break
                                audio_chunks.append(chunk)
                                pbar.update(len(chunk))
                    
                    # Concatenate chunks
                    print("Combining audio chunks...")
                    audio_array = np.concatenate(audio_chunks, axis=0)
                else:
                    # Load entire file for smaller files
                    print("Loading entire audio file...")
                    audio_array, sample_rate = sf.read(temp_audio_path)
               
                # Convert to mono if stereo
                if len(audio_array.shape) > 1:
                    print("Converting stereo to mono...")
                    audio_array = np.mean(audio_array, axis=1)
               
                # Resample to 16kHz if needed using librosa (with progress)
                if sample_rate != 16000:
                    print(f"Resampling from {sample_rate}Hz to 16kHz...")
                    with tqdm(desc="Resampling", unit="samples") as pbar:
                        audio_array = librosa.resample(
                            audio_array, 
                            orig_sr=sample_rate, 
                            target_sr=16000,
                            res_type='kaiser_best'  # High quality resampling
                        )
                        pbar.update(len(audio_array))
                   
            except Exception as e:
                print(f"Error loading with soundfile: {e}")
                print("Falling back to librosa loading...")
                audio_array, sample_rate = librosa.load(temp_audio_path, sr=16000)
           
            # Clean up
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                print("Temporary audio file cleaned up")
           
            print(f"Audio extracted successfully! Duration: {len(audio_array)/16000:.2f} seconds")
            print(f"Audio array shape: {audio_array.shape}")
            print(f"Audio sample rate: 16000 Hz")
            print(f"Audio min/max values: {audio_array.min():.3f}/{audio_array.max():.3f}")
            
            # Check if audio has actual content (not just silence)
            audio_rms = np.sqrt(np.mean(audio_array**2))
            print(f"Audio RMS level: {audio_rms:.6f}")
            if audio_rms < 0.001:
                print("WARNING: Audio RMS is very low - might be silence!")
            
            return audio_array
           
        except Exception as e:
            print(f"Error extracting audio: {e}")
            # Clean up temp file if it exists
            temp_audio_path = "temp_audio.wav"
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            sys.exit(1)
   
    def split_audio_into_chunks(self, audio_array: np.ndarray, chunk_duration: int = 15, sample_rate: int = 16000) -> List[Tuple[np.ndarray, float, float]]:
        """Split audio array into chunks of specified duration.
        
        Returns:
            List of tuples containing (audio_chunk, start_time, end_time)
        """
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
                print(f"Warning: Trimming chunk from {len(audio_chunk)/16000:.1f}s to 15s")
                audio_chunk = audio_chunk[:max_chunk_length]
                end_time = start_time + 15
            
            # Transcribe chunk with explicit parameters to avoid configuration issues
            result = self.whisper_pipeline(
                audio_chunk,
                generate_kwargs={
                    "language": "en",
                    "task": "transcribe",
                    "max_new_tokens": 200
                }
            )
            
            # Debug: Print result structure
            if not result or not result.get("text"):
                print(f"Warning: Empty result for chunk {start_time:.1f}s-{end_time:.1f}s")
                print(f"Result keys: {list(result.keys()) if result else 'None'}")
                return {"text": "", "chunks": []}
            
            # Adjust timestamps to be relative to the full audio
            if "chunks" in result and result["chunks"]:
                for chunk in result["chunks"]:
                    if "timestamp" in chunk and chunk["timestamp"]:
                        # Convert tuple to list if needed for modification
                        if isinstance(chunk["timestamp"], tuple):
                            chunk["timestamp"] = list(chunk["timestamp"])
                        
                        # Adjust the timestamps
                        if len(chunk["timestamp"]) >= 2:
                            chunk["timestamp"][0] = (chunk["timestamp"][0] or 0) + start_time
                            chunk["timestamp"][1] = (chunk["timestamp"][1] or (end_time - start_time)) + start_time
                        elif len(chunk["timestamp"]) == 1:
                            chunk["timestamp"][0] = (chunk["timestamp"][0] or 0) + start_time
            
            # Create chunks from the text if none exist
            if "chunks" not in result or not result["chunks"]:
                if result.get("text"):
                    result["chunks"] = [{
                        "text": result["text"],
                        "timestamp": [start_time, end_time]
                    }]
            
            return result
            
        except Exception as e:
            print(f"Error transcribing chunk {start_time:.1f}s-{end_time:.1f}s: {e}")
            import traceback
            traceback.print_exc()
            # Return empty result for failed chunks
            return {"text": "", "chunks": []}
    
    def transcribe_audio(self, audio_array: np.ndarray) -> Dict[str, Any]:
        """Transcribe audio using Whisper large v3 with chunked processing."""
        total_duration = len(audio_array) / 16000
        print(f"Transcribing audio (duration: {total_duration:.1f}s)...")
        
        if self.whisper_pipeline is None:
            self.load_whisper_model()
        
        try:
            # Split audio into chunks
            chunks = self.split_audio_into_chunks(audio_array, chunk_duration=15)
            print(f"Processing {len(chunks)} chunks of ~15 seconds each...")
            
            # Initialize results
            all_text = []
            all_chunks = []
            
            # Process chunks with progress bar
            start_time = time.time()
            
            with tqdm(total=len(chunks), desc="Transcribing", unit="chunk") as pbar:
                for i, (chunk_audio, chunk_start, chunk_end) in enumerate(chunks):
                    # Update progress bar description with current time range
                    pbar.set_description(f"Transcribing [{self._format_timestamp(chunk_start)}-{self._format_timestamp(chunk_end)}]")
                    
                    # Transcribe chunk
                    chunk_result = self.transcribe_audio_chunk(chunk_audio, chunk_start, chunk_end)
                    
                    # Debug: Log chunk results
                    chunk_text = chunk_result.get("text", "")
                    if chunk_text.strip():
                        print(f"  Chunk {i+1}: '{chunk_text[:50]}...' ({len(chunk_text)} chars)")
                    else:
                        print(f"  Chunk {i+1}: NO TEXT DETECTED")
                    
                    # Collect results
                    if chunk_result.get("text"):
                        all_text.append(chunk_result["text"])
                    
                    if chunk_result.get("chunks"):
                        all_chunks.extend(chunk_result["chunks"])
                    
                    # Update progress
                    pbar.update(1)
                    
                    # Show elapsed time and ETA
                    elapsed = time.time() - start_time
                    if i > 0:
                        avg_time_per_chunk = elapsed / (i + 1)
                        eta = avg_time_per_chunk * (len(chunks) - i - 1)
                        pbar.set_postfix({
                            'elapsed': f"{elapsed:.0f}s",
                            'eta': f"{eta:.0f}s",
                            'avg': f"{avg_time_per_chunk:.1f}s/chunk"
                        })
            
            # Combine all results
            combined_text = " ".join(all_text).strip()
            combined_result = {
                "text": combined_text,
                "chunks": all_chunks
            }
            
            total_elapsed = time.time() - start_time
            print(f"Transcription completed successfully in {total_elapsed:.1f}s!")
            print(f"Processing speed: {total_duration/total_elapsed:.2f}x real-time")
            print(f"Total transcribed text length: {len(combined_text)} characters")
            print(f"Number of chunks with text: {len([t for t in all_text if t.strip()])}")
            
            if not combined_text:
                print("WARNING: No text was transcribed! This might indicate:")
                print("  - Audio file has no speech")
                print("  - Audio quality is too poor")
                print("  - Model loading failed")
                print("  - Wrong audio format/sample rate")
            
            return combined_result
            
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
            # First try the chat API (newer format)
            chat_payload = {
                "model": "gemma3:12b",
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
            if response.text:
                print(f"Response: {response.text[:200]}...")
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
        overall_start_time = time.time()
        
        # Validate input
        if not os.path.exists(video_path):
            print(f"Error: Video file '{video_path}' not found!")
            sys.exit(1)
       
        if not video_path.lower().endswith('.mp4'):
            print("Warning: File does not have .mp4 extension, attempting to process anyway...")
       
        print(f"\n=== Starting Video Transcription ===")
        print(f"Input file: {video_path}")
        print(f"Device: {self.device}")
        print(f"Ollama formatting: {'Enabled' if use_ollama else 'Disabled'}")
        print("="*50)
        
        # Extract audio
        print("\nStep 1/3: Audio Extraction")
        step_start = time.time()
        audio_array = self.extract_audio_from_video(video_path)
        step_duration = time.time() - step_start
        print(f"Audio extraction completed in {step_duration:.1f}s\n")
       
        # Transcribe
        print("Step 2/3: Audio Transcription")
        step_start = time.time()
        transcription_result = self.transcribe_audio(audio_array)
        step_duration = time.time() - step_start
        print(f"Audio transcription completed in {step_duration:.1f}s\n")
       
        # Format output based on user preference
        print("Step 3/3: Text Formatting")
        step_start = time.time()
        
        # Save raw transcription first (before Ollama formatting)
        raw_output_path = None
        if output_path is None:
            video_name = Path(video_path).stem
            raw_output_path = f"{video_name}_raw_transcription.md"
        else:
            # Insert "_raw" before the file extension
            output_path_obj = Path(output_path)
            raw_output_path = output_path_obj.parent / f"{output_path_obj.stem}_raw{output_path_obj.suffix}"
        
        # Create raw transcription content
        text = transcription_result.get("text", "")
        chunks = transcription_result.get("chunks", [])
        
        raw_structured_text = "Raw Transcription:\n" + text + "\n\n"
        
        if chunks:
            raw_structured_text += "Timestamped Segments:\n"
            for i, chunk in enumerate(chunks):
                timestamp = chunk.get("timestamp", [0, 0])
                chunk_text = chunk.get("text", "")
                start_time = self._format_timestamp(timestamp[0])
                end_time = self._format_timestamp(timestamp[1]) if len(timestamp) > 1 else "end"
                raw_structured_text += f"[{start_time} - {end_time}]: {chunk_text.strip()}\n"
        
        raw_formatted_text = self._basic_markdown_format(raw_structured_text)
        
        # Save raw transcription
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write(raw_formatted_text)
        print(f"Raw transcription saved to: {raw_output_path}")
        
        # Now proceed with Ollama formatting if requested
        if use_ollama:
            print("Processing with Ollama formatting...")
            formatted_text = self.format_with_ollama(transcription_result)
        else:
            print("Skipping Ollama formatting, using raw transcription...")
            formatted_text = raw_formatted_text
        
        step_duration = time.time() - step_start
        print(f"Text formatting completed in {step_duration:.1f}s\n")
       
        # Save final output (Ollama formatted or raw)
        if output_path is None:
            video_name = Path(video_path).stem
            if use_ollama:
                output_path = f"{video_name}_transcription_ollama.md"
            else:
                output_path = f"{video_name}_transcription.md"
       
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
