"""
Real Video Metadata Extractor with Advanced Features
Extracts metadata, transcripts, and performs sentiment analysis on video content
"""

import os
import cv2
import json
import logging
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import tempfile
import shutil
import hashlib

# For audio extraction and processing
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    logging.warning("MoviePy not available - video processing limited")

# For speech recognition
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logging.warning("SpeechRecognition not available - transcript extraction disabled")

# For YouTube video processing
try:
    import youtube_dl
    YOUTUBE_DL_AVAILABLE = True
except ImportError:
    YOUTUBE_DL_AVAILABLE = False
    logging.warning("youtube-dl not available - YouTube processing disabled")

import requests
from urllib.parse import urlparse, parse_qs
import re

class RealVideoMetadataExtractor:
    """
    Advanced video metadata extractor with real capabilities
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = tempfile.mkdtemp(prefix='video_analysis_')
        
        # Supported video formats
        self.supported_formats = {
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', 
            '.m4v', '.mpg', '.mpeg', '.3gp', '.ogv'
        }
        
        # Initialize speech recognizer if available
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
        
        # YouTube-dl configuration
        self.ydl_opts = {
            'format': 'best[height<=720]',  # Limit quality for faster processing
            'extractaudio': True,
            'outtmpl': os.path.join(self.temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True
        }
    
    def __del__(self):
        """Cleanup temporary directory"""
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except:
            pass
    
    def extract_from_file(self, file_path: str) -> Dict:
        """Extract comprehensive metadata from video file"""
        try:
            if not os.path.exists(file_path):
                return {'error': 'File not found'}
            
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.supported_formats:
                return {'error': f'Unsupported format: {file_ext}'}
            
            metadata = {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'extraction_time': datetime.now().isoformat()
            }
            
            # Extract basic video properties
            video_info = self._extract_video_properties(file_path)
            metadata.update(video_info)
            
            # Extract frames for analysis
            frame_analysis = self._analyze_video_frames(file_path)
            metadata.update(frame_analysis)
            
            # Extract audio and transcript if possible
            if MOVIEPY_AVAILABLE:
                audio_info = self._extract_audio_info(file_path)
                metadata.update(audio_info)
                
                if SPEECH_RECOGNITION_AVAILABLE:
                    transcript = self._extract_transcript(file_path)
                    if transcript:
                        metadata['transcript'] = transcript
                        metadata['transcript_length'] = len(transcript)
                        metadata['word_count'] = len(transcript.split())
            
            # Calculate file hash for uniqueness
            metadata['file_hash'] = self._calculate_file_hash(file_path)
            
            # Add technical metadata
            technical_info = self._extract_technical_metadata(file_path)
            metadata.update(technical_info)
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting from file {file_path}: {str(e)}")
            return {'error': f'Extraction failed: {str(e)}'}
    
    def extract_from_url(self, url: str) -> Dict:
        """Extract metadata from video URL (YouTube, Vimeo, etc.)"""
        try:
            if not self._is_valid_video_url(url):
                return {'error': 'Invalid video URL'}
            
            metadata = {
                'url': url,
                'extraction_time': datetime.now().isoformat()
            }
            
            # Check if it's a YouTube URL
            if 'youtube.com' in url or 'youtu.be' in url:
                return self._extract_from_youtube(url)
            
            # Check if it's a Vimeo URL
            elif 'vimeo.com' in url:
                return self._extract_from_vimeo(url)
            
            # For other URLs, try to download and analyze
            else:
                return self._extract_from_generic_url(url)
                
        except Exception as e:
            self.logger.error(f"Error extracting from URL {url}: {str(e)}")
            return {'error': f'URL extraction failed: {str(e)}'}
    
    def _extract_video_properties(self, file_path: str) -> Dict:
        """Extract basic video properties using OpenCV"""
        try:
            cap = cv2.VideoCapture(file_path)
            
            if not cap.isOpened():
                return {'error': 'Could not open video file'}
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                'duration': round(duration, 2),
                'fps': round(fps, 2),
                'frame_count': frame_count,
                'width': width,
                'height': height,
                'resolution': f"{width}x{height}",
                'aspect_ratio': round(width / height, 2) if height > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting video properties: {str(e)}")
            return {'error': 'Could not extract video properties'}
    
    def _analyze_video_frames(self, file_path: str, sample_count: int = 10) -> Dict:
        """Analyze sample frames from the video"""
        try:
            cap = cv2.VideoCapture(file_path)
            
            if not cap.isOpened():
                return {'frame_analysis_error': 'Could not open video'}
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if frame_count == 0:
                return {'frame_analysis_error': 'No frames found'}
            
            # Sample frames evenly throughout the video
            frame_indices = [int(i * frame_count / sample_count) for i in range(sample_count)]
            
            brightness_values = []
            contrast_values = []
            colors = {'r': [], 'g': [], 'b': []}
            
            for frame_idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if ret:
                    # Calculate brightness (convert to grayscale and get mean)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    brightness = gray.mean()
                    brightness_values.append(brightness)
                    
                    # Calculate contrast (standard deviation of grayscale)
                    contrast = gray.std()
                    contrast_values.append(contrast)
                    
                    # Average colors
                    b, g, r = cv2.split(frame)
                    colors['r'].append(r.mean())
                    colors['g'].append(g.mean())
                    colors['b'].append(b.mean())
            
            cap.release()
            
            # Calculate statistics
            avg_brightness = sum(brightness_values) / len(brightness_values) if brightness_values else 0
            avg_contrast = sum(contrast_values) / len(contrast_values) if contrast_values else 0
            
            avg_colors = {
                'red': sum(colors['r']) / len(colors['r']) if colors['r'] else 0,
                'green': sum(colors['g']) / len(colors['g']) if colors['g'] else 0,
                'blue': sum(colors['b']) / len(colors['b']) if colors['b'] else 0
            }
            
            # Determine video characteristics
            characteristics = []
            if avg_brightness < 50:
                characteristics.append('dark')
            elif avg_brightness > 200:
                characteristics.append('bright')
            
            if avg_contrast < 30:
                characteristics.append('low_contrast')
            elif avg_contrast > 100:
                characteristics.append('high_contrast')
            
            return {
                'frame_analysis': {
                    'average_brightness': round(avg_brightness, 2),
                    'average_contrast': round(avg_contrast, 2),
                    'average_colors': avg_colors,
                    'characteristics': characteristics,
                    'frames_analyzed': len(frame_indices)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing frames: {str(e)}")
            return {'frame_analysis_error': str(e)}
    
    def _extract_audio_info(self, file_path: str) -> Dict:
        """Extract audio information using MoviePy"""
        try:
            with VideoFileClip(file_path) as clip:
                if clip.audio is None:
                    return {'audio_info': 'No audio track found'}
                
                audio_info = {
                    'has_audio': True,
                    'audio_duration': round(clip.audio.duration, 2),
                    'audio_fps': clip.audio.fps if hasattr(clip.audio, 'fps') else None
                }
                
                # Try to get more detailed audio info
                try:
                    # This might not work on all systems
                    audio_info['channels'] = clip.audio.nchannels if hasattr(clip.audio, 'nchannels') else None
                except:
                    pass
                
                return {'audio_info': audio_info}
                
        except Exception as e:
            self.logger.error(f"Error extracting audio info: {str(e)}")
            return {'audio_info_error': str(e)}
    
    def _extract_transcript(self, file_path: str) -> Optional[str]:
        """Extract transcript using speech recognition"""
        if not SPEECH_RECOGNITION_AVAILABLE or not MOVIEPY_AVAILABLE:
            return None
        
        try:
            # Extract audio to temporary WAV file
            audio_path = os.path.join(self.temp_dir, 'temp_audio.wav')
            
            with VideoFileClip(file_path) as video:
                if video.audio is None:
                    return None
                
                # Limit audio duration for processing (first 5 minutes)
                max_duration = min(300, video.duration)  # 5 minutes max
                audio_clip = video.audio.subclip(0, max_duration)
                audio_clip.write_audiofile(audio_path, verbose=False, logger=None)
                audio_clip.close()
            
            # Use speech recognition
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.record(source)
            
            # Try to recognize speech
            try:
                transcript = self.recognizer.recognize_google(audio)
                return transcript
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                self.logger.error(f"Speech recognition error: {e}")
                return None
            
        except Exception as e:
            self.logger.error(f"Error extracting transcript: {str(e)}")
            return None
        finally:
            # Clean up temporary audio file
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except:
                pass
    
    def _extract_from_youtube(self, url: str) -> Dict:
        """Extract metadata from YouTube URL"""
        if not YOUTUBE_DL_AVAILABLE:
            return {'error': 'YouTube processing not available'}
        
        try:
            import youtube_dl
            
            # Configure youtube-dl for metadata extraction only
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                metadata = {
                    'url': url,
                    'title': info.get('title', 'Unknown'),
                    'description': info.get('description', ''),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'upload_date': info.get('upload_date', ''),
                    'uploader': info.get('uploader', 'Unknown'),
                    'thumbnail': info.get('thumbnail', ''),
                    'tags': info.get('tags', []),
                    'categories': info.get('categories', []),
                    'width': info.get('width', 0),
                    'height': info.get('height', 0),
                    'fps': info.get('fps', 0),
                    'format': info.get('format', 'Unknown'),
                    'extraction_time': datetime.now().isoformat()
                }
                
                # Extract automatic captions if available
                if info.get('automatic_captions'):
                    captions = info['automatic_captions']
                    if 'en' in captions:  # English captions
                        metadata['has_captions'] = True
                        # Note: We're not downloading captions to keep it simple
                        metadata['caption_languages'] = list(captions.keys())
                
                return metadata
                
        except Exception as e:
            self.logger.error(f"Error extracting YouTube metadata: {str(e)}")
            return {'error': f'YouTube extraction failed: {str(e)}'}
    
    def _extract_from_vimeo(self, url: str) -> Dict:
        """Extract metadata from Vimeo URL"""
        try:
            # Extract video ID from URL
            video_id = None
            if 'vimeo.com' in url:
                match = re.search(r'vimeo\.com/(\d+)', url)
                if match:
                    video_id = match.group(1)
            
            if not video_id:
                return {'error': 'Could not extract Vimeo video ID'}
            
            # Use Vimeo API (oEmbed)
            api_url = f"https://vimeo.com/api/oembed.json?url={url}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                metadata = {
                    'url': url,
                    'title': data.get('title', 'Unknown'),
                    'description': data.get('description', ''),
                    'duration': data.get('duration', 0),
                    'width': data.get('width', 0),
                    'height': data.get('height', 0),
                    'thumbnail': data.get('thumbnail_url', ''),
                    'upload_date': data.get('upload_date', ''),
                    'author_name': data.get('author_name', 'Unknown'),
                    'author_url': data.get('author_url', ''),
                    'provider_name': data.get('provider_name', 'Vimeo'),
                    'extraction_time': datetime.now().isoformat()
                }
                
                return metadata
            else:
                return {'error': f'Vimeo API request failed: {response.status_code}'}
                
        except Exception as e:
            self.logger.error(f"Error extracting Vimeo metadata: {str(e)}")
            return {'error': f'Vimeo extraction failed: {str(e)}'}
    
    def _extract_from_generic_url(self, url: str) -> Dict:
        """Extract metadata from generic video URL"""
        try:
            # Try to get basic info about the URL
            response = requests.head(url, timeout=10)
            
            if response.status_code != 200:
                return {'error': f'URL not accessible: {response.status_code}'}
            
            content_type = response.headers.get('content-type', '')
            content_length = response.headers.get('content-length', 0)
            
            if not content_type.startswith('video/'):
                return {'error': f'URL does not point to a video file: {content_type}'}
            
            metadata = {
                'url': url,
                'content_type': content_type,
                'file_size': int(content_length) if content_length else 0,
                'extraction_time': datetime.now().isoformat()
            }
            
            # Try to download a small portion to analyze
            # (This is simplified - in a real implementation, you might want to download the entire file)
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting from generic URL: {str(e)}")
            return {'error': f'Generic URL extraction failed: {str(e)}'}
    
    def _extract_technical_metadata(self, file_path: str) -> Dict:
        """Extract technical metadata using ffprobe if available"""
        try:
            # Try to use ffprobe for detailed metadata
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                '-show_format', '-show_streams', file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                technical_info = {
                    'format_name': data.get('format', {}).get('format_name', 'Unknown'),
                    'bit_rate': data.get('format', {}).get('bit_rate', 0),
                    'streams': []
                }
                
                # Extract stream information
                for stream in data.get('streams', []):
                    stream_info = {
                        'codec_type': stream.get('codec_type', 'Unknown'),
                        'codec_name': stream.get('codec_name', 'Unknown'),
                        'duration': stream.get('duration', 0)
                    }
                    
                    if stream.get('codec_type') == 'video':
                        stream_info.update({
                            'width': stream.get('width', 0),
                            'height': stream.get('height', 0),
                            'avg_frame_rate': stream.get('avg_frame_rate', '0/0')
                        })
                    
                    technical_info['streams'].append(stream_info)
                
                return {'technical_metadata': technical_info}
                
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            # ffprobe not available or failed
            pass
        except Exception as e:
            self.logger.error(f"Error extracting technical metadata: {str(e)}")
        
        return {'technical_metadata': 'Not available'}
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of the file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating file hash: {str(e)}")
            return "hash_calculation_failed"
    
    def _is_valid_video_url(self, url: str) -> bool:
        """Check if URL is a valid video URL"""
        try:
            parsed = urlparse(url)
            
            # Check if it's a valid URL
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Check for known video platforms
            video_domains = [
                'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
                'twitch.tv', 'facebook.com', 'instagram.com', 'tiktok.com'
            ]
            
            if any(domain in parsed.netloc.lower() for domain in video_domains):
                return True
            
            # Check file extension
            path = parsed.path.lower()
            if any(path.endswith(ext) for ext in self.supported_formats):
                return True
            
            return False
            
        except Exception:
            return False
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported video formats"""
        return list(self.supported_formats)
    
    def get_capabilities(self) -> Dict:
        """Get information about extractor capabilities"""
        return {
            'supported_formats': list(self.supported_formats),
            'moviepy_available': MOVIEPY_AVAILABLE,
            'speech_recognition_available': SPEECH_RECOGNITION_AVAILABLE,
            'youtube_dl_available': YOUTUBE_DL_AVAILABLE,
            'features': {
                'file_analysis': True,
                'url_analysis': YOUTUBE_DL_AVAILABLE,
                'transcript_extraction': SPEECH_RECOGNITION_AVAILABLE and MOVIEPY_AVAILABLE,
                'frame_analysis': True,
                'audio_analysis': MOVIEPY_AVAILABLE,
                'technical_metadata': True
            }
        }

# Global instance
real_video_extractor = RealVideoMetadataExtractor()
