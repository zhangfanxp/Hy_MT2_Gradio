# Hy-MT2 本地翻译软件

这是一个适用于 Apple Silicon Mac 的本地翻译页面。应用使用 Gradio 提供网页界面，使用 MLX 和本地缓存的 `mlx-community/Hy-MT2-1.8B` 模型完成推理。

页面包含：

- 输入语言下拉选框，默认 `中文`
- 输出语言下拉选框，默认 `英语`
- 多行翻译文字输入框
- 翻译按钮
- 支持复制的翻译结果框

## 环境准备

当前项目使用 uv 管理虚拟环境,至少需要Python 3.10的版本。首次使用时，在项目目录执行：

```bash
uv venv --python 3.10
source .venv/bin/activate
uv pip install -r requirements.txt
```

模型需要预先下载到 Hugging Face 缓存：

配置镜像站：

export HF_ENDPOINT=https://hf-mirror.com

```bash
hf download mlx-community/Hy-MT2-1.8B
```

## 启动

在项目目录执行：

```bash
source .venv/bin/activate
python app.py
```

本机访问地址：

```text
http://127.0.0.1:7860
```

应用默认监听 `0.0.0.0:7860`，因此同一局域网内的其他电脑也可以访问。先在 Mac 上获取局域网 IP：

```bash
ipconfig getifaddr en0
```

如果 Mac 使用有线网络，可以执行：

```bash
ipconfig getifaddr en1
```

假设命令输出 `192.168.1.10`，局域网中的其他电脑访问：

```text
http://192.168.1.10:7860
```

如果页面无法打开，请检查两台电脑是否连接到同一局域网，以及 macOS 防火墙是否允许 Python 接收入站连接。

## 可选配置

可以通过环境变量修改模型、监听地址、端口和最大输出 token 数：

```bash
MODEL_PATH="mlx-community/Hy-MT2-1.8B" \
SERVER_NAME="0.0.0.0" \
SERVER_PORT="7860" \
MAX_TOKENS="4096" \
python app.py
```

模型会在第一次翻译时加载。第一次请求会比后续请求稍慢。
