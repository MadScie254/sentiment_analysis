"""
Video Metadata Extractor
"""

import yt_dlp
from pymediainfo import MediaInfo
import json

class VideoMetadataExtractor:
    def extract_from_url(self, url):
        """Extracts video metadata from a URL using yt-dlp."""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'force_generic_extractor': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=False)
                return self.normalize_metadata(info_dict, 'url')
            except Exception as e:
                return {"error": str(e)}

    def extract_from_file(self, filepath):
        """Extracts video metadata from a local file using pymediainfo."""
        try:
            media_info = MediaInfo.parse(filepath)
            return self.normalize_metadata(media_info.to_data(), 'file')
        except Exception as e:
            return {"error": str(e)}

    def normalize_metadata(self, data, source_type):
        """Normalizes metadata from different sources."""
        if source_type == 'url':
            return {
                "title": data.get("title"),
                "duration": data.get("duration"),
                "uploader": data.get("uploader"),
                "resolution": f"{data.get('width')}x{data.get('height')}" if data.get('width') and data.get('height') else None,
                "fps": data.get("fps"),
                "codec": data.get("vcodec"),
                "thumbnail": data.get("thumbnail"),
                "has_subtitles": bool(data.get("subtitles")),
                "raw": data,
            }
        elif source_type == 'file':
            video_track = next((track for track in data['tracks'] if track['track_type'] == 'Video'), None)
            audio_track = next((track for track in data['tracks'] if track['track_type'] == 'Audio'), None)
            text_track = next((track for track in data['tracks'] if track['track_type'] == 'Text'), None)

            return {
                "title": data['tracks'][0].get('file_name'),
                "duration": float(video_track.get('duration')) if video_track and video_track.get('duration') else None,
                "resolution": f"{video_track.get('width')}x{video_track.get('height')}" if video_track and video_track.get('width') and video_track.get('height') else None,
                "fps": float(video_track.get('frame_rate')) if video_track and video_track.get('frame_rate') else None,
                "codec": video_track.get('format') if video_track else None,
                "audio_codec": audio_track.get('format') if audio_track else None,
                "has_subtitles": bool(text_track),
                "raw": data,
            }
        return {}
