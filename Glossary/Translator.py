import requests
import logging

# 设置Logging等级和格式
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w')

def translator(text):
    try:
        # 构建请求体
        prompt = "将下面的日文文本翻译成中文：" + text
        data = {
            "messages": [
            {"role": "system", "content": "你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。"},
            {"role": "user", "content": prompt}
        ],
            "stream": False,
            "temperature": 0.2,
            "top_p": 0.8,
            "frequency_penalty": 0.1
        }
        # 发送请求到http://127.0.0.1:8080/v1/chat/completions
        response = requests.post("http://127.0.0.1:8080/v1/chat/completions", json=data, timeout=600)
        # 解析响应
        if response.status_code == 200:
            result = response.json()
            translated_text = result['choices'][0]['message']['content']
            return translated_text
    except Exception as e:
        logging.error(f"术语表词汇翻译失败: {e}")
        return None