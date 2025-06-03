from dataclasses import dataclass
import asyncio
import os
import subprocess
from typing import Optional
import edge_tts
from pydub import AudioSegment
import json
from config import AudioConfig, SubtitleConfig

class AudioProcessor:
    """音频处理器类"""
    def __init__(self):
        self.audio_config = AudioConfig()
        self.subtitle_config = SubtitleConfig()
        
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
                self.audio_config.voice_name,
                rate=self.audio_config.voice_rate
            )
            await communicate.save(output_path)
            
            if self.audio_config.volume != 1.0:
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
        audio = audio + (20 * self.audio_config.volume)
        audio.export(audio_path, format=self.audio_config.output_format)

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

    async def generate_voice_with_timing(self, text: str, output_path: str) -> tuple[str, list]:
        """生成语音文件并返回时间轴信息"""
        communicate = edge_tts.Communicate(text, self.audio_config.voice_name, rate=self.audio_config.voice_rate)
        
        # 保存音频
        await communicate.save(output_path)
        
        # 创建新的通信实例来获取时间轴信息
        communicate = edge_tts.Communicate(text, self.audio_config.voice_name, rate=self.audio_config.voice_rate)
        
        # 收集时间轴信息
        word_timings = []
        current_sentence = []
        sentences = self._split_into_sentences(text)
        print(f"🏂处理视频字幕: {sentences}")
        current_sentence_text = ""
        
        async for event in communicate.stream():
            if event["type"] == "WordBoundary":
                word_timings.append({
                    "word": event["text"],
                    "start": event["offset"] / 10000000,
                    "end": (event["offset"] + event["duration"]) / 10000000
                })
                
        # 将单词时间轴信息合并为句子时间轴
        sentence_timings = []
        word_index = 0
        
        for sentence in sentences:
            sentence_words = sentence.split()
            if not sentence_words:
                continue
                
            start_time = word_timings[word_index]["start"]
            while word_index < len(word_timings) and len(sentence_words) > 0:
                word_index += 1
                sentence_words.pop(0)
                
            end_time = word_timings[min(word_index - 1, len(word_timings) - 1)]["end"]
            
            sentence_timings.append({
                "word": sentence,
                "start": start_time,
                "end": end_time
            })
        
        return output_path, sentence_timings

    def generate_subtitle_file(self, timings: list, output_path: str):
        """生成ASS字幕文件"""
        ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{self.subtitle_config.font_path},{self.subtitle_config.font_size},&H0000FFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,{self.subtitle_config.outline_width},0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        # 生成字幕内容
        for timing in timings:
            start_time = self._format_time(timing["start"])
            end_time = self._format_time(timing["end"])
            text = timing["word"]
            ass_content += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ass_content)
        
        return output_path

    def _format_time(self, seconds: float) -> str:
        """将秒数转换为ASS时间格式 (H:MM:SS.cc)"""
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        seconds = seconds % 60
        centiseconds = int((seconds % 1) * 100)
        seconds = int(seconds)
        return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

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

    def process_video_with_subtitle(self, video_path: str, text: str, output_path: str) -> str:
        """处理视频：生成配音、字幕并合并"""
        temp_audio = "temp_voice.mp3"
        temp_subtitle = "temp_subtitle.ass"
        
        try:
            # 生成语音和时间轴信息
            audio_path, timings = asyncio.run(self.generate_voice_with_timing(text, temp_audio))
            
            # 生成字幕文件
            subtitle_path = self.generate_subtitle_file(timings, temp_subtitle)
            
            # 合并视频、音频和字幕
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-vf", f"ass={subtitle_path}",
                "-map", "0:v",
                "-map", "1:a",
                "-c:a", "aac",
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
            
        finally:
            # 清理临时文件
            for temp_file in [temp_audio, temp_subtitle]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

    def _split_into_sentences(self, text: str) -> list[str]:
        """将文本分割为句子
    
        Args:
            text: 输入文本
    
        Returns:
            list[str]: 句子列表
        """
        import re
        # 在标点符号处分割文本
        sentences = re.split(r'([,.!?])', text)
        # 将标点符号附加到前一个句子
        result = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences) and sentences[i+1].strip() in [',', '.', '!', '?']:
                # 如果下一个元素是标点符号，将其与当前句子合并
                result.append(sentences[i].strip() + sentences[i+1])
                i += 2
            else:
                # 处理最后一个没有标点符号的句子
                current = sentences[i].strip()
                if current:
                    result.append(current)
                i += 1
            
        return [s.strip() for s in result if s.strip()]