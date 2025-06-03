import subprocess
from typing import Optional
from pydub import AudioSegment
import os
from config import BackgroundMusicConfig

class BackgroundMusicProcessor:
    """背景音乐处理器类"""
    
    def __init__(self):
        self.config = BackgroundMusicConfig()
    
    def add_background_music(self, video_path: str, output_path: str) -> str:
        """为视频添加背景音乐
        
        Args:
            video_path: 输入视频路径
            output_path: 输出视频路径
            
        Returns:
            str: 输出视频路径
        """
        try:
            # 获取视频时长
            video_duration = float(subprocess.check_output([
                'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', video_path
            ]).decode().strip())
            
            # 处理背景音乐
            self._process_background_music(
                self.config.music_path, 
                self.config.temp_filename, 
                video_duration, 
                self.config.volume
            )
            
            # 合并视频和背景音乐
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', self.config.temp_filename,
                '-filter_complex', '[1:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[music];[0:a][music]amix=inputs=2:duration=first:dropout_transition=0',
                '-c:v', 'copy',
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # 清理临时文件
            if os.path.exists(self.config.temp_filename):
                os.remove(self.config.temp_filename)
                
            return output_path
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"添加背景音乐失败: {e.stderr.decode()}")
            
    def _process_background_music(self, music_path: str, output_path: str, 
                                target_duration: float, volume: float) -> None:
        """处理背景音乐：调整时长和音量"""
        audio = AudioSegment.from_file(music_path)
        
        # 调整音量
        audio = audio - (20 * (1 - volume))  # 将音量范围0-1映射到dB
        
        # 调整时长
        target_duration_ms = int(target_duration * 1000)
        audio_duration_ms = len(audio)
        
        if audio_duration_ms < target_duration_ms:
            # 如果音乐太短，循环播放
            repeat_times = int(target_duration_ms / audio_duration_ms) + 1
            audio = audio * repeat_times
            
        # 裁剪到目标时长
        audio = audio[:target_duration_ms]
        
        # 导出处理后的音频
        audio.export(output_path, format="mp3")

def test_background_music_processor():
    """测试背景音乐处理功能"""
    processor = BackgroundMusicProcessor()
    
    # 测试视频路径
    test_video = "final_output.mp4"
    test_music = "resource/songs/output001.mp3"
    test_output = "test_output_with_bgm.mp4"
    
    try:
        result = processor.add_background_music(
            video_path=test_video,
            output_path=test_output,
        )
        print(f"测试成功! 输出文件: {result}")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_background_music_processor()