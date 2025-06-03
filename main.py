from add_sounds import AudioConfig, AudioProcessor

def main():
    # 创建配置
    config = AudioConfig(
        voice_name="en-US-JennyNeural", # 使用中文语音
        voice_rate="+0%",
        volume=1.0,
        output_format="mp3"
    )
    
    # 初始化音频处理器
    processor = AudioProcessor(config)
    
    # 测试文本和文件路径
    test_text = "What a beautiful day, I want to dance! Come on, Come to dance with me"  # 测试文本
    input_video = "test.mp4"  # 请确保此视频文件存在
    output_video = "test_output.mp4"
    
    try:
        # 处理视频
        result = processor.process_video(
            video_path=input_video,
            text=test_text,
            output_path=output_video
        )
        print(f"视频处理成功! 输出文件: {result}")
        
    except Exception as e:
        print(f"处理失败: {str(e)}")

if __name__ == "__main__":
    main()