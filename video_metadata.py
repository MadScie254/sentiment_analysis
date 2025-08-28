"""
Enhanced Video Metadata Extractor
Supports both URL (YouTube, TikTok, etc.) and local file metadata extraction
"""

import yt_dlp
import json
import os
import subprocess
from typing import Dict, Any, Optional
from datetime import timedelta
import hashlib
from functools import lru_cache

class VideoMetadataExtractor:
    """
    Enhanced video metadata extractor with caching and multiple backend support
    """
    
    def __init__(self):
        self.cache = {}
        
    def _get_cache_key(self, input_data: str) -> str:
        """Generate cache key for input"""
        return hashlib.md5(input_data.encode()).hexdigest()
        
    @lru_cache(maxsize=128)
    def extract_from_url(self, url: str) -> Dict[str, Any]:
        """
        Extracts video metadata from a URL using yt-dlp
        No downloading, just metadata extraction
        """
        cache_key = self._get_cache_key(url)
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,  # Need full info
            'writeinfojson': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'skip_download': True,
            'ignoreerrors': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                if info_dict:
                    result = self.normalize_metadata(info_dict, 'url')
                    self.cache[cache_key] = result
                    return result
                else:
                    return {"error": "No video information found"}
        except Exception as e:
            return {"error": f"URL extraction failed: {str(e)}"}

    def extract_from_file(self, filepath: str) -> Dict[str, Any]:
        """
        Extracts video metadata from a local file using multiple methods
        Tries pymediainfo first, falls back to ffprobe
        """
        if not os.path.exists(filepath):
            return {"error": "File not found"}
            
        cache_key = self._get_cache_key(f"file:{filepath}:{os.path.getmtime(filepath)}")
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        # Try pymediainfo first
        try:
            result = self._extract_with_pymediainfo(filepath)
            if result and "error" not in result:
                self.cache[cache_key] = result
                return result
        except ImportError:
            pass
        except Exception as e:
            print(f"PyMediaInfo failed: {e}")
            
        # Fallback to ffprobe
        try:
            result = self._extract_with_ffprobe(filepath)
            if result and "error" not in result:
                self.cache[cache_key] = result
                return result
        except Exception as e:
            return {"error": f"File extraction failed: {str(e)}"}
            
        return {"error": "No suitable metadata extractor available"}
        
    def _extract_with_pymediainfo(self, filepath: str) -> Dict[str, Any]:
        """Extract using pymediainfo"""
        try:
            from pymediainfo import MediaInfo
            media_info = MediaInfo.parse(filepath)
            return self.normalize_metadata(media_info.to_data(), 'file_pymediainfo')
        except ImportError:
            raise ImportError("pymediainfo not available")
            
    def _extract_with_ffprobe(self, filepath: str) -> Dict[str, Any]:
        """Extract using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', filepath
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return self.normalize_metadata(data, 'file_ffprobe')
            else:
                return {"error": f"ffprobe failed: {result.stderr}"}
        except subprocess.TimeoutExpired:
            return {"error": "ffprobe timeout"}
        except FileNotFoundError:
            return {"error": "ffprobe not found - install FFmpeg"}
        except json.JSONDecodeError:
            return {"error": "Invalid ffprobe output"}

    def normalize_metadata(self, data: Dict[str, Any], source_type: str) -> Dict[str, Any]:
        """Normalizes metadata from different sources into a consistent format"""
        
        if source_type == 'url':
            return self._normalize_url_metadata(data)
        elif source_type == 'file_pymediainfo':
            return self._normalize_pymediainfo_metadata(data)
        elif source_type == 'file_ffprobe':
            return self._normalize_ffprobe_metadata(data)
        
        return {"error": "Unknown source type"}
        
    def _normalize_url_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize yt-dlp metadata"""
        duration_seconds = data.get("duration")
        duration_formatted = None
        if duration_seconds:
            duration_formatted = str(timedelta(seconds=int(duration_seconds)))
            
        # Get best thumbnail
        thumbnails = data.get("thumbnails", [])
        best_thumbnail = None
        if thumbnails:
            # Prefer larger thumbnails
            best_thumbnail = max(thumbnails, key=lambda x: (x.get('width', 0) * x.get('height', 0)))
            best_thumbnail = best_thumbnail.get('url')
            
        return {
            "source_type": "url",
            "title": data.get("title", "Unknown Title"),
            "duration_seconds": duration_seconds,
            "duration_formatted": duration_formatted,
            "uploader": data.get("uploader") or data.get("channel"),
            "upload_date": data.get("upload_date"),
            "view_count": data.get("view_count"),
            "like_count": data.get("like_count"),
            "resolution": f"{data.get('width', 'Unknown')}x{data.get('height', 'Unknown')}" if data.get('width') and data.get('height') else "Unknown",
            "fps": data.get("fps"),
            "vcodec": data.get("vcodec"),
            "acodec": data.get("acodec"),
            "filesize": data.get("filesize") or data.get("filesize_approx"),
            "thumbnail": best_thumbnail,
            "has_subtitles": bool(data.get("subtitles") or data.get("automatic_captions")),
            "webpage_url": data.get("webpage_url"),
            "extractor": data.get("extractor"),
            "platform": self._detect_platform(data.get("webpage_url", "")),
            "tags": data.get("tags", []),
            "description": data.get("description", "")[:500] + "..." if data.get("description", "") and len(data.get("description", "")) > 500 else data.get("description", ""),
            "raw_available": True
        }
        
    def _normalize_pymediainfo_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize pymediainfo metadata"""
        tracks = data.get('tracks', [])
        video_track = next((track for track in tracks if track.get('track_type') == 'Video'), {})
        audio_track = next((track for track in tracks if track.get('track_type') == 'Audio'), {})
        text_track = next((track for track in tracks if track.get('track_type') == 'Text'), {})
        general_track = next((track for track in tracks if track.get('track_type') == 'General'), {})
        
        duration_ms = general_track.get('duration') or video_track.get('duration')
        duration_seconds = None
        duration_formatted = None
        if duration_ms:
            try:
                duration_seconds = float(duration_ms) / 1000
                duration_formatted = str(timedelta(seconds=int(duration_seconds)))
            except (ValueError, TypeError):
                pass
                
        filesize = general_track.get('file_size')
        if filesize:
            try:
                filesize = int(filesize)
            except (ValueError, TypeError):
                filesize = None
        
        return {
            "source_type": "file",
            "title": general_track.get('file_name', 'Unknown File'),
            "duration_seconds": duration_seconds,
            "duration_formatted": duration_formatted,
            "resolution": f"{video_track.get('width', 'Unknown')}x{video_track.get('height', 'Unknown')}" if video_track.get('width') and video_track.get('height') else "Unknown",
            "fps": float(video_track.get('frame_rate')) if video_track.get('frame_rate') else None,
            "vcodec": video_track.get('format'),
            "acodec": audio_track.get('format'),
            "bitrate": general_track.get('overall_bit_rate'),
            "filesize": filesize,
            "has_subtitles": bool(text_track),
            "container": general_track.get('format'),
            "raw_available": True
        }
        
    def _normalize_ffprobe_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize ffprobe metadata"""
        format_info = data.get('format', {})
        streams = data.get('streams', [])
        
        video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
        audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), {})
        subtitle_streams = [s for s in streams if s.get('codec_type') == 'subtitle']
        
        duration_seconds = None
        duration_formatted = None
        duration_str = format_info.get('duration') or video_stream.get('duration')
        if duration_str:
            try:
                duration_seconds = float(duration_str)
                duration_formatted = str(timedelta(seconds=int(duration_seconds)))
            except (ValueError, TypeError):
                pass
                
        filesize = format_info.get('size')
        if filesize:
            try:
                filesize = int(filesize)
            except (ValueError, TypeError):
                filesize = None
        
        return {
            "source_type": "file",
            "title": os.path.basename(format_info.get('filename', 'Unknown File')),
            "duration_seconds": duration_seconds,
            "duration_formatted": duration_formatted,
            "resolution": f"{video_stream.get('width', 'Unknown')}x{video_stream.get('height', 'Unknown')}" if video_stream.get('width') and video_stream.get('height') else "Unknown",
            "fps": self._parse_fps(video_stream.get('r_frame_rate')),
            "vcodec": video_stream.get('codec_name'),
            "acodec": audio_stream.get('codec_name'),
            "bitrate": format_info.get('bit_rate'),
            "filesize": filesize,
            "has_subtitles": len(subtitle_streams) > 0,
            "container": format_info.get('format_name'),
            "raw_available": True
        }
        
    def _parse_fps(self, fps_str: Optional[str]) -> Optional[float]:
        """Parse FPS from fraction string like '30/1'"""
        if not fps_str:
            return None
        try:
            if '/' in fps_str:
                num, den = fps_str.split('/')
                return float(num) / float(den)
            return float(fps_str)
        except (ValueError, ZeroDivisionError):
            return None
            
    def _detect_platform(self, url: str) -> str:
        """Detect video platform from URL"""
        url_lower = url.lower()
        if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'YouTube'
        elif 'tiktok.com' in url_lower:
            return 'TikTok'
        elif 'vimeo.com' in url_lower:
            return 'Vimeo'
        elif 'twitch.tv' in url_lower:
            return 'Twitch'
        elif 'instagram.com' in url_lower:
            return 'Instagram'
        elif 'twitter.com' in url_lower or 'x.com' in url_lower:
            return 'Twitter/X'
        else:
            return 'Unknown'
            
    def format_duration(self, seconds: Optional[float]) -> str:
        """Format duration in human readable format"""
        if not seconds:
            return "Unknown"
        return str(timedelta(seconds=int(seconds)))
        
    def format_filesize(self, size_bytes: Optional[int]) -> str:
        """Format file size in human readable format"""
        if not size_bytes:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
