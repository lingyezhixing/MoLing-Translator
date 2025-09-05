import subprocess
import os
import time
import pickle

# 全局变量来管理当前的子进程
current_translated_process = None
current_llama_process = None

# 停止翻译
def stop_translation():
    global current_translated_process, current_llama_process
    try:
        if current_translated_process is not None and current_translated_process.poll() is None:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(current_translated_process.pid)], check=True)
            current_translated_process = None
        if current_llama_process is not None and current_llama_process.poll() is None:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(current_llama_process.pid)], check=True)
            current_llama_process = None
    except Exception as e:
        print("停止进程时发生错误:", e)

# 翻译控制器
def translation_controller():
    global current_translated_process, current_llama_process
    last_translating_file_sh256 = None
    last_model = None
    print("翻译控制器启动")
    while True:
        if os.path.exists("Cache\\translating_file_sh256.pkl"):
            with open("Cache\\translating_file_sh256.pkl", "rb") as f:
                translating_file_sh256 = pickle.load(f)
            if translating_file_sh256 != last_translating_file_sh256 or last_model != None:
                if os.path.exists("Cache\\Translating_info.pkl"):
                    with open("Cache\\Translating_info.pkl", "rb") as f:
                        translating_file_sh256_info = pickle.load(f)
                    if translating_file_sh256 is not None and translating_file_sh256 != "model_only":
                        last_translating_file_sh256 = translating_file_sh256
                        bat_path = os.path.join("llama-cpp", translating_file_sh256_info['config']['bat_name'])
                        stop_translation()
                        # 启动llama进程
                        current_llama_process = subprocess.Popen([bat_path])
                        # 等待llama进程启动完成
                        time.sleep(10)
                        # 启动翻译进程
                        current_translated_process = subprocess.Popen(['E:\\Programming\\pycodes\\miniconda3\\envs\\MoLing-Translator\\python', 'Translator.py'])
                    elif translating_file_sh256 == "model_only":
                        if last_model is None or last_model != translating_file_sh256_info['config']['bat_name']:
                            last_model = translating_file_sh256_info['config']['bat_name']
                            with open("Cache\\Translating_info.pkl", "rb") as f:
                                translating_file_sh256_info = pickle.load(f)
                            bat_path = os.path.join("llama-cpp", translating_file_sh256_info['config']['bat_name'])
                            stop_translation()
                            # 启动llama进程
                            current_llama_process = subprocess.Popen([bat_path])
                    else:
                        stop_translation()
                        last_translating_file_sh256 = None
                        last_model = None

        time.sleep(1)