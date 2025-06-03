from dataclasses import dataclass
import asyncio
import os
import subprocess
from typing import Optional
import edge_tts
from pydub import AudioSegment

@dataclass
class AudioConfig:
    """音频处理配置类"""
    voice_name: str = "en-US-JennyNeural"
    voice_rate: str = "+0%"
    volume: float = 1.0
    output_format: str = "mp3"

class AudioProcessor:
    """音频处理器类"""
    def __init__(self, config: Optional[AudioConfig] = None):
        self.config = config or AudioConfig()
        
    async def generate_voice(self, text: str, output_path: str) -> str:
        """生成语音文件
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径
            
        Returns:
            str: 生成的语音文件路径
        """
        try:
            communicate = edge_tts.Communicate(
                text,
                self.config.voice_name,
                rate=self.config.voice_rate
            )
            await communicate.save(output_path)
            
            if self.config.volume != 1.0:
                self._adjust_volume(output_path)
                
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"生成语音失败: {str(e)}")

    def _adjust_volume(self, audio_path: str) -> None:
        """调整音频文件音量
        
        Args:
            audio_path: 音频文件路径
        """
        audio = AudioSegment.from_file(audio_path)
        audio = audio + (20 * self.config.volume)
        audio.export(audio_path, format=self.config.output_format)

    def merge_audio_video(self, video_path: str, audio_path: str, output_path: str) -> str:
        """合并音频和视频
        
        Args:
            video_path: 视频文件路径
            audio_path: 音频文件路径
            output_path: 输出文件路径
            
        Returns:
            str: 输出视频文件路径
        """
        try:
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-shortest",
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"合并音视频失败: {e.stderr.decode()}")

    def process_video(self, video_path: str, text: str, output_path: str) -> str:
        """处理视频：生成配音并合并
        
        Args:
            video_path: 输入视频路径
            text: 配音文本
            output_path: 输出视频路径
            
        Returns:
            str: 处理后的视频路径
        """
        temp_audio = "temp_voice.mp3"
        try:
            asyncio.run(self.generate_voice(text, temp_audio))
            result = self.merge_audio_video(video_path, temp_audio, output_path)
            return result
        finally:
            if os.path.exists(temp_audio):
                os.remove(temp_audio)