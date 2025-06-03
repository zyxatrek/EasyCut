from add_sounds import AudioConfig, AudioProcessor
from video_concatenate import VideoConCatProcessor
from background_music import BackgroundMusicProcessor
from config import AudioConfig, SubtitleConfig, BackgroundMusicConfig
import os
import time

def main():
    # 添加开始时间计数
    start_time = time.time()
    
    # 初始化处理器和配置
    audio_processor = AudioProcessor()
    video_processor = VideoConCatProcessor()
    bgm_processor = BackgroundMusicProcessor()
    
    # 准备输入视频和字幕列表
    input_videos = [
        {
            "video": "resource/videos/test1.mp4",
            "subtitle": "What a beautiful day, I want to dance! Come on, Come to dance with me"
        },
        {
            "video": "resource/videos/test2.mp4",
            "subtitle": "The music is so wonderful! Let's enjoy this moment together"
        },
        {
            "video": "resource/videos/test3.mp4",
            "subtitle": "Dancing makes me feel alive! I love dancing so much! Let's dance together"
        },
        {
            "video": "resource/videos/test4.mp4",
            "subtitle": "Dancing is the best way to express myself! I love the rhythm and the beat"
        },
        {
            "video": "resource/videos/test5.mp4",
            "subtitle": "Let's create some wonderful memories through dance! Life is a dance, let's enjoy it"
        }
    ]
    
    # 处理后的视频列表
    processed_videos = []
    
    try:
        # 处理每个视频
        for i, video_data in enumerate(input_videos, 1):
            output_video = f"output{i}.mp4"
            print(f"🤺正在处理视频 {i}/5: {video_data['video']}")
            
            try:
                # 为每个视频添加字幕和配音
                result = audio_processor.process_video_with_subtitle(
                    video_path=video_data['video'],
                    text=video_data['subtitle'],
                    output_path=output_video
                )
                processed_videos.append(result)
                elapsed_time = time.time() - start_time
                print(f"⛳️视频 {i} 处理成功! 此时已耗时{elapsed_time:.2f}秒")
                
            except Exception as e:
                elapsed_time = time.time() - start_time
                print(f"🎱处理视频 {i} 失败: {str(e)} 此时已耗时{elapsed_time:.2f}秒")
                continue
        
        # 拼接所有处理好的视频
        if processed_videos:
            final_output = "final_output.mp4"
            result = video_processor.concat_videos(processed_videos, final_output)
            elapsed_time = time.time() - start_time
            print(f"🏅视频拼接成功! 最终文件: {result} 此时已耗时{elapsed_time:.2f}秒")
            
            # 添加背景音乐
            final_output_with_bgm = "final_output_with_bgm.mp4"
            result = bgm_processor.add_background_music(
                video_path=final_output,
                output_path=final_output_with_bgm
            )
            elapsed_time = time.time() - start_time
            print(f"🎖背景音乐添加成功! 最终文件: {result} 此时已耗时{elapsed_time:.2f}秒")
            
            # 清理中间文件
            for video in processed_videos + [final_output]:
                if os.path.exists(video):
                    os.remove(video)
            elapsed_time = time.time() - start_time
            print(f"🎯清理完成! 总耗时{elapsed_time:.2f}秒")
        else:
            elapsed_time = time.time() - start_time
            print(f"🎲没有成功处理的视频可供拼接 总耗时{elapsed_time:.2f}秒")
            
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"🥁处理失败: {str(e)} 总耗时{elapsed_time:.2f}秒")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()