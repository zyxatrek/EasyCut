import subprocess
import os
from typing import List, Dict

class VideoConCatProcessor:
    """视频处理器类"""
    
    @staticmethod
    def concat_videos(video_list: List[str], output_path: str) -> str:
        """拼接多个视频文件
        
        Args:
            video_list: 视频文件路径列表
            output_path: 输出文件路径
            
        Returns:
            str: 输出视频文件路径
        """
        try:
            # 创建临时文件存储视频文件列表
            temp_list = "temp_videos.txt"
            with open(temp_list, "w", encoding="utf-8") as f:
                for video in video_list:
                    f.write(f"file '{video}'\n")
            
            # 使用 ffmpeg 进行视频拼接
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", temp_list,
                "-c", "copy",
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"视频拼接失败: {e.stderr.decode()}")
        finally:
            if os.path.exists(temp_list):
                os.remove(temp_list)