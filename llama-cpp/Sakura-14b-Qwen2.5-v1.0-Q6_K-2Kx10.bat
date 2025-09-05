@echo off
cmd /k "D:\LLM\llama.cpp\llama-server.exe -m E:\models\LLM\Sakura\Sakura-14B-Qwen2.5-v1.0-Q6_K.gguf -c 20480 -ngl 999 -fa --parallel 10 --defrag-thold 0.05 -a Sakura-14B-Qwen2.5-v1.0-Q6_K --device cuda1"
pause