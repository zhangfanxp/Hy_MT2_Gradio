# test.py
import requests

url = "http://localhost:8000/v1/chat/completions"

data = {
    "model": "mlx-community/Hy-MT2-1.8B",
    "messages": [
        {"role": "user", "content": "你好"}
    ]
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 打印返回的 JSON
print(response.json())
