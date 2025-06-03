# 视频字幕配音合成工具

这是一个视频字幕配音合成工具，可以为无声视频添加字幕、配音和背景音乐，并将多个视频拼接成一个完整的作品。

## 项目结构

```
project/
├── config.py               # 配置文件，包含字幕、配音和背景音乐的配置
├── add_sounds.py          # 音频处理模块，负责配音生成和添加
├── video_concatenate.py   # 视频拼接模块，负责多个视频的拼接
├── background_music.py    # 背景音乐处理模块，负责添加背景音乐
├── main.py               # 主程序，协调各个模块的工作
├── resource/             # 资源文件夹
│   ├── fonts/           # 字体文件
│   │   └── Charm-Regular.ttf
│   ├── videos/          # 输入视频
│   │   ├── test1.mp4
│   │   ├── test2.mp4
│   │   └── ...
│   └── sounds/          # 背景音乐
│       └── output001.mp3
```

### 工作流程

1. 读取配置文件(`config.py`)
2. 为每个视频生成配音和字幕(`add_sounds.py`)
3. 拼接处理后的视频(`video_concatenate.py`)
4. 添加背景音乐(`background_music.py`)
5. 清理临时文件，输出最终视频

## 使用说明

### 环境要求

```bash
# 安装必要的Python包
pip install edge-tts pydub

# 安装ffmpeg (Mac环境)
brew install ffmpeg
```

### 准备工作

1. **替换视频文件**：
   - 将您的5个无声视频放入 `resource/videos/` 目录
   - 修改 `main.py` 中的视频路径和对应字幕：
   ```python
   input_videos = [
       {
           "video": "resource/videos/your_video1.mp4",
           "subtitle": "你的第一段字幕"
       },
       # ... 其他视频和字幕
   ]
   ```

2. **配置设置**：
   在 `config.py` 中可以调整以下配置：

   ```python
   # 字幕配置
   SubtitleConfig:
       font_path = "resource/fonts/你的字体.ttf"  # 字体文件
       font_size = 50                           # 字体大小
       font_color = "yellow"                    # 字体颜色
       position = (0, 1050)                     # 字幕位置

   # 配音配置
   AudioConfig:
       voice_name = "zh-CN-XiaoxiaoNeural"     # 中文配音
       voice_rate = "+0%"                       # 语速
       volume = 1.0                             # 音量

   # 背景音乐配置
   BackgroundMusicConfig:
       music_path = "resource/sounds/你的音乐.mp3" # 背景音乐
       volume = 0.3                             # 背景音乐音量
   ```

### 运行程序

```bash
python main.py
```

### 输出结果

1. 程序会生成两个文件：
   - `final_output.mp4`: 拼接后的视频(无背景音乐)
   - `final_output_with_bgm.mp4`: 最终视频(含背景音乐)

2. 处理过程中会显示进度信息：
   ```
   🤺正在处理视频 1/5: resource/videos/test1.mp4
   ⛳️视频 1 处理成功! 此时已耗时12.34秒
   ...
   🏅视频拼接成功! 最终文件: final_output.mp4
   🎖背景音乐添加成功! 最终文件: final_output_with_bgm.mp4
   ```

## 预期效果

- 每个视频都会添加对应的字幕和配音
- 字幕会根据配音自动对齐
- 所有视频会按顺序无缝拼接
- 背景音乐会自动循环或裁剪以匹配视频长度
- 最终输出一个完整的、带字幕、配音和背景音乐的视频文件

## 注意事项

1. 确保所有输入视频格式一致(建议使用MP4)
2. 字体文件必须是.ttf格式
3. 背景音乐建议使用mp3格式
4. 视频分辨率建议保持一致
5. 确保磁盘有足够的存储空间

## 常见问题

Q: 如何更换配音语音？
A: 在 `config.py` 中修改 `voice_name`，支持多种语音，如：
- 中文女声：zh-CN-XiaoxiaoNeural
- 英文女声：en-US-JennyNeural
- 更多语音可参考 edge-tts 文档

Q: 字幕位置不合适怎么调整？
A: 字幕位置底部居中对齐，暂不可调整，方法调试中
A: 字幕位置可以通过修改 `config.py` 中的 `SubtitleConfig` 配置来调整：

1. 位置调整：
   ```python
   SubtitleConfig:
       position = (x, y)  # x是水平位置，y是垂直位置
   ```
   - x值：从左到右，0是最左边，越大越靠右
   - y值：从上到下，0是最上边，越大越下
   - 例如：
     - `position = (0, 0)` 左上角
     - `position = (0, 1050)` 左下方
     - `position = (960, 1050)` 底部居中（假设视频宽度为1920px）

2. 字体大小调整：
   ```python
   SubtitleConfig:
       font_size = 50  # 数值越大字体越大
   ```

3. 描边调整：
   ```python
   SubtitleConfig:
       outline_width = 2  # 描边粗细
       outline_color = "black"  # 描边颜色
   ```

实用建议：
- 1080P视频推荐y值设置在900-1050之间
- 如需居中显示，x值设为视频宽度的一半
- 如果字幕看不清楚，可以适当增加outline_width值
- 建议先用小视频测试调整效果

## 如何贡献

1. Fork 该仓库
2. 创建新的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m '添加新功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## License

MIT License - 详见 [LICENSE](LICENSE) 文件