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
import tempfile
import shutil

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
            
            # We no longer need to adjust word-level timestamps since we're not using them
            
            return result
            
        except Exception as e:
            print(f"Error transcribing chunk {start_time:.1f}s-{end_time:.1f}s: {e}")
            import traceback
            traceback.print_exc()
            # Return empty result for failed chunks
            return {"text": "", "chunks": []}
    
    def transcribe_audio(self, audio_array: np.ndarray, progress_file: str = None, raw_output_path: str = None) -> Dict[str, Any]:
        """Transcribe audio using Whisper large v3 with chunked processing and incremental saving."""
        total_duration = len(audio_array) / 16000
        print(f"Transcribing audio (duration: {total_duration:.1f}s)...")
        
        if self.whisper_pipeline is None:
            self.load_whisper_model()
        
        try:
            # Split audio into chunks
            chunks = self.split_audio_into_chunks(audio_array, chunk_duration=15)
            print(f"Processing {len(chunks)} chunks of ~15 seconds each...")
            
            # Load existing progress if available
            progress_data = self._load_existing_progress(progress_file) if progress_file else {
                'completed_chunks': [],
                'all_text': [],
                'total_chunks': len(chunks),
                'audio_duration': total_duration
            }
            
            # Update progress data
            progress_data['total_chunks'] = len(chunks)
            progress_data['audio_duration'] = total_duration
            
            # Determine starting point
            completed_chunk_indices = set(progress_data.get('completed_chunks', []))
            start_index = len(completed_chunk_indices)
            
            if start_index > 0:
                print(f"Resuming from chunk {start_index + 1} (already completed: {start_index}/{len(chunks)})")
            
            # Initialize results from existing progress
            all_text = progress_data.get('all_text', [])
            
            # Process chunks with progress bar
            start_time = time.time()
            
            with tqdm(total=len(chunks), initial=start_index, desc="Transcribing", unit="chunk") as pbar:
                for i, (chunk_audio, chunk_start, chunk_end) in enumerate(chunks):
                    # Skip already completed chunks
                    if i in completed_chunk_indices:
                        continue
                        
                    # Update progress bar description with current time range
                    pbar.set_description(f"Transcribing [{self._format_timestamp(chunk_start)}-{self._format_timestamp(chunk_end)}]")
                    
                    try:
                        # Transcribe chunk
                        chunk_result = self.transcribe_audio_chunk(chunk_audio, chunk_start, chunk_end)
                        
                        # Debug: Log chunk results
                        chunk_text = chunk_result.get("text", "")
                        if chunk_text.strip():
                            print(f"  Chunk {i+1}: '{chunk_text[:50]}...' ({len(chunk_text)} chars)")
                        else:
                            print(f"  Chunk {i+1}: NO TEXT DETECTED")
                        
                        # Collect results with segment timestamp
                        if chunk_result.get("text"):
                            # Add segment timestamp at the beginning of the text
                            segment_timestamp = f"[{self._format_timestamp(chunk_start)} - {self._format_timestamp(chunk_end)}] "
                            timestamped_text = segment_timestamp + chunk_result["text"].strip()
                            all_text.append(timestamped_text)
                        
                        # We no longer collect detailed chunks for word-level timestamps
                        # if chunk_result.get("chunks"):
                        #     all_chunks.extend(chunk_result["chunks"])
                        
                        # Mark chunk as completed
                        progress_data['completed_chunks'].append(i)
                        progress_data['all_text'] = all_text
                        
                        # Save progress after each chunk
                        if progress_file:
                            self._save_progress(progress_file, progress_data)
                        
                        # Save current transcript state
                        if raw_output_path:
                            self._save_current_transcript(progress_data, raw_output_path)
                        
                    except Exception as chunk_error:
                        print(f"Error processing chunk {i+1}: {chunk_error}")
                        print("Continuing with next chunk...")
                        # Still mark as "completed" to avoid infinite retry
                        progress_data['completed_chunks'].append(i)
                        if progress_file:
                            self._save_progress(progress_file, progress_data)
                    
                    # Update progress
                    pbar.update(1)
                    
                    # Show elapsed time and ETA
                    elapsed = time.time() - start_time
                    completed_now = len(progress_data['completed_chunks'])
                    if completed_now > start_index:
                        avg_time_per_chunk = elapsed / (completed_now - start_index)
                        remaining_chunks = len(chunks) - completed_now
                        eta = avg_time_per_chunk * remaining_chunks
                        pbar.set_postfix({
                            'elapsed': f"{elapsed:.0f}s",
                            'eta': f"{eta:.0f}s",
                            'avg': f"{avg_time_per_chunk:.1f}s/chunk"
                        })
            
            # Combine all results - now each text segment already has timestamps
            combined_text = "\n\n".join(all_text).strip()
            combined_result = {
                "text": combined_text,
                "chunks": []  # No longer using detailed word-level chunks
            }
            
            total_elapsed = time.time() - start_time
            completed_chunks = len(progress_data['completed_chunks'])
            print(f"Transcription completed successfully in {total_elapsed:.1f}s!")
            print(f"Processing speed: {total_duration/total_elapsed:.2f}x real-time")
            print(f"Total transcribed text length: {len(combined_text)} characters")
            print(f"Completed chunks: {completed_chunks}/{len(chunks)}")
            print(f"Number of chunks with text: {len([t for t in all_text if t.strip()])}")
            
            # Clean up progress file if transcription is complete
            if progress_file and completed_chunks == len(chunks):
                try:
                    os.remove(progress_file)
                    print(f"Cleaned up progress file: {progress_file}")
                except:
                    pass
            
            if not combined_text:
                print("WARNING: No text was transcribed! This might indicate:")
                print("  - Audio file has no speech")
                print("  - Audio quality is too poor")
                print("  - Model loading failed")
                print("  - Wrong audio format/sample rate")
            
            return combined_result
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            print(f"Progress has been saved. You can resume by running the script again.")
            sys.exit(1)
   
    def format_with_ollama(self, transcription_result: Dict[str, Any]) -> str:
        """Format transcription using local Ollama model."""
        print("Formatting transcription with Ollama...")
       
        # Extract text (already includes segment timestamps)
        text = transcription_result.get("text", "")
       
        # Create a structured representation - text already contains timestamps
        structured_text = "Transcription with Segment Timestamps:\n" + text + "\n\n"
       
        # Prepare prompt for Ollama
        prompt = f"""Please create a comprehensive, fact-based educational document from the following video transcription. Transform this raw transcript into a well-structured knowledge resource.

Requirements:
1. Write a concise, factual document covering all content discussed in the recording
2. Enrich the knowledge with your own expertise - add context, explanations, and related information that would help readers understand the topics better
3. Make it simple to understand and illustrative using:
   - Tables for comparisons or data
   - Diagrams (in mermaid digram language)
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
    
    def _create_incremental_save_file(self, video_path: str) -> str:
        """Create a temporary file for incremental saving of transcription progress."""
        video_name = Path(video_path).stem
        temp_file = f"{video_name}_transcription_progress.json"
        return temp_file
    
    def _load_existing_progress(self, progress_file: str) -> Dict[str, Any]:
        """Load existing transcription progress from file."""
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                print(f"Found existing progress file with {len(progress.get('completed_chunks', []))} completed chunks")
                return progress
            except Exception as e:
                print(f"Error loading progress file: {e}")
                print("Starting fresh transcription...")
        return {
            'completed_chunks': [],
            'all_text': [],
            'total_chunks': 0,
            'video_path': '',
            'audio_duration': 0
        }
    
    def _save_progress(self, progress_file: str, progress_data: Dict[str, Any]):
        """Save current transcription progress to file."""
        try:
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Could not save progress: {e}")
    
    def _save_current_transcript(self, progress_data: Dict[str, Any], output_path: str):
        """Save current transcript state to output file."""
        try:
            # Combine all text (already includes segment timestamps)
            combined_text = "\n\n".join(progress_data.get('all_text', [])).strip()
            
            # Create structured text - no need for separate timestamped segments
            structured_text = "Transcription with Segment Timestamps:\n" + combined_text + "\n\n"
            
            # Add progress info
            completed_chunks = len(progress_data.get('completed_chunks', []))
            total_chunks = progress_data.get('total_chunks', 0)
            if total_chunks > 0:
                structured_text += f"\n--- Progress: {completed_chunks}/{total_chunks} chunks completed ({completed_chunks/total_chunks*100:.1f}%) ---\n"
            
            # Format and save
            formatted_text = self._basic_markdown_format(structured_text)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_text)
                
        except Exception as e:
            print(f"Warning: Could not save current transcript: {e}")
   
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
       
        # Set up incremental saving
        progress_file = self._create_incremental_save_file(video_path)
        
        # Determine raw output path early
        if output_path is None:
            video_name = Path(video_path).stem
            raw_output_path = f"{video_name}_raw_transcription.md"
        else:
            output_path_obj = Path(output_path)
            raw_output_path = output_path_obj.parent / f"{output_path_obj.stem}_raw{output_path_obj.suffix}"
        
        # Transcribe
        print("Step 2/3: Audio Transcription")
        step_start = time.time()
        transcription_result = self.transcribe_audio(audio_array, progress_file, str(raw_output_path))
        step_duration = time.time() - step_start
        print(f"Audio transcription completed in {step_duration:.1f}s\n")
       
        # Format output based on user preference
        print("Step 3/3: Text Formatting")
        step_start = time.time()
        
        # Raw transcription was already saved incrementally during processing
        # Create final version without progress indicators
        text = transcription_result.get("text", "")
        
        raw_structured_text = "Transcription with Segment Timestamps:\n" + text + "\n\n"
        
        raw_formatted_text = self._basic_markdown_format(raw_structured_text)
        
        # Save final clean raw transcription (without progress indicators)
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write(raw_formatted_text)
        print(f"Final raw transcription saved to: {raw_output_path}")
        
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
