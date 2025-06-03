from dataclasses import dataclass
from typing import Tuple

@dataclass
class SubtitleConfig:
    """字幕配置类"""
    font_path: str = "resource/fonts/Charm-Regular.ttf"
    font_size: int = 50
    font_color: str = "yellow"
    position: Tuple[int, int] = (0, 1050)  # (x, y)坐标
    outline_color: str = "black"
    outline_width: int = 2

@dataclass
class AudioConfig:
    """音频处理配置类"""
    voice_name: str = "en-US-JennyNeural"
    voice_rate: str = "+0%"
    volume: float = 1.0
    output_format: str = "mp3"

@dataclass
class BackgroundMusicConfig:
    """背景音乐配置类"""
    music_path: str = "resource/songs/output002.mp3"
    volume: float = 0.7  # 背景音乐音量，范围0-1
    output_format: str = "mp3"
    temp_filename: str = "temp_background.mp3"  # 临时文件名