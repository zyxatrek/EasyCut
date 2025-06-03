from add_sounds import AudioConfig, AudioProcessor
from config import SubtitleConfig

def main():
    # 初始化处理器
    processor = AudioProcessor()
    
    # 测试文本和文件路径
    test_text = "What a beautiful day, I want to dance! Come on, Come to dance with me"
    input_video = "test.mp4"
    output_video = "test_output.mp4"
    
    try:
        # 处理视频
        result = processor.process_video_with_subtitle(
            video_path=input_video,
            text=test_text,
            output_path=output_video
        )
        print(f"视频处理成功! 输出文件: {result}")
        
    except Exception as e:
        print(f"处理失败: {str(e)}")
        import traceback
        print(traceback.format_exc())  # 打印完整错误栈信息

if __name__ == "__main__":
    main()