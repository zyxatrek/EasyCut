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