# MoLing-Translator

一个专业的日文轻小说翻译系统，基于本地大语言模型，支持TXT和EPUB格式的批量翻译，配备智能术语表管理和交互式翻译功能。

## 🌟 主要特性

### 核心功能
- **多格式支持**: 完整支持TXT和EPUB文件格式的翻译，保持原文结构
- **批量处理**: 高效的批量翻译能力，支持多文件并发处理
- **智能分段**: 基于长度和语义的智能分段处理，保持上下文连贯性
- **术语表管理**: 自动检测日文片假名词汇，支持批量翻译和自定义术语表
- **交互式翻译**: 实时翻译界面，支持即时文本翻译和术语应用
- **断点续传**: 基于SHA256哈希的智能缓存系统，支持翻译中断后精确恢复

### 专业特性
- **轻小说优化**: 专门针对日文轻小说翻译场景优化，保持文学风格
- **行数匹配**: 智能行数对齐算法，确保译文与原文行数一致
- **本地模型**: 基于LLaMA-CPP的本地模型部署，保护隐私和数据安全
- **配置管理**: 灵活的配置系统，支持多配置文件和默认配置管理
- **质量控制**: 内置重试机制和错误处理，支持最大重试次数配置

### 用户界面
- **现代化UI**: 基于Streamlit的响应式Web界面，支持实时状态更新
- **实时进度**: 翻译进度实时监控、时间预估和完成率显示
- **任务管理**: 支持多任务队列管理和优先级控制
- **文件管理**: 直观的文件上传、预览和管理界面

## 🚀 快速开始

### 系统要求
- **操作系统**: Windows 10/11 (64位)
- **Python**: 3.8 或更高版本
- **Conda**: 用于环境管理
- **内存**: 推荐16GB以上RAM (大型模型需要更多内存)
- **存储**: 建议SSD存储以提高模型加载性能
- **GPU**: 支持CUDA的NVIDIA显卡 (推荐，用于模型加速)

### 安装步骤

#### 1. 环境准备
```bash
# 创建并激活虚拟环境
conda create -n MoLing-Translator python=3.8
conda activate MoLing-Translator
```

#### 2. 安装依赖
```bash
# 安装基础依赖
pip install streamlit aiohttp pillow pyperclip

# 安装LLaMA-CPP (根据你的CUDA版本选择)
# CUDA 11.x
pip install llama-cpp-python --prefer-binary --extra-index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118
# 或 CPU版本
pip install llama-cpp-python
```

#### 3. 模型配置
- 下载支持的日文翻译模型 (如Sakura-14B)
- 在`llama-cpp`目录下配置模型启动脚本
- 确保模型路径正确且可访问

#### 4. 启动应用
```bash
# 使用批处理文件启动（推荐）
MoLing-Translator.bat

# 或手动启动
conda activate MoLing-Translator
streamlit run MoLing-Translator.py
```

应用将在浏览器中自动打开，通常访问地址为 `http://localhost:8501`

## 📚 使用指南

### 1. 配置管理
首次使用需要配置翻译参数：
1. 进入"配置管理"页面
2. 添加新的翻译配置（系统会自动创建默认配置模板）
3. 设置分段长度、模型参数、并发数量等
4. 设置默认配置以简化后续操作

### 2. 文件翻译
1. 在"文件翻译"页面选择配置
2. 上传TXT或EPUB文件（支持批量上传）
3. 系统自动预处理文件并生成哈希缓存
4. 启动翻译任务（后台控制器会自动启动模型服务）
5. 实时监控翻译进度和预估时间

### 3. 术语表制作
- **自动检测**: 基于正则表达式自动检测日文片假名词汇
- **频率统计**: 按出现频率排序，支持阈值过滤
- **批量翻译**: 一键翻译检测到的词汇并生成术语表
- **术语管理**: 可视化术语表编辑和管理，支持导入导出

### ⚠️ 重要说明：术语表匹配规则
**术语表文件名必须与小说文件名一致**，否则系统无法自动匹配并使用术语表。

例如：
- 小说文件：`小説1.txt` 或 `小説1.epub`
- 对应术语表：`小説1.json`

系统会根据小说文件名自动查找同名的术语表文件，并在翻译过程中自动应用。如果术语表文件名与小说文件名不匹配，术语表将不会被使用。

### 4. 交互式翻译
- **实时翻译**: 输入日文文本即时翻译
- **流式输出**: 翻译结果实时显示
- **术语集成**: 自动应用当前配置的术语表
- **模型控制**: 支持启动/停止模型服务

## 🏗️ 项目架构

### 项目结构
```
MoLing-Translator/
├── MoLing-Translator.py      # 主程序入口 (启动WebUI)
├── Controller.py             # 后台翻译控制器 (进程管理)
├── Translator.py             # 翻译执行器 (断点续传)
├── count_lines.py            # 代码统计工具
├── src/                      # 静态资源
│   └── Logo.png             # 应用Logo
├── Cache/                    # 缓存目录
│   ├── TXT/                 # TXT文件处理缓存
│   ├── EPUB/                # EPUB文件处理缓存
│   ├── Temp/                # 临时文件缓存
│   ├── Time/                # 时间指示器
│   └── Source/              # 上传文件源目录
├── Clients/                  # 客户端模块
│   ├── UnifiedRequest.py   # 统一请求接口抽象层
│   ├── llama_cpp.py        # LLaMA-CPP客户端实现
│   └── Timeout.py          # 全局超时配置
├── Config/                   # 配置管理
│   ├── Management.py        # 配置管理系统
│   ├── config.json          # 用户配置文件
│   └── default_config.txt   # 默认配置标识
├── Glossary/                 # 术语表管理
│   ├── GetKatakana.py      # 片假名检测算法
│   └── Translator.py       # 术语翻译功能
├── Translators/             # 翻译引擎
│   ├── Controller.py       # 翻译控制器
│   ├── TxtTranslate.py     # TXT文件翻译核心
│   ├── EpubTranslate.py    # EPUB文件翻译核心
│   └── FilePretreatment.py # 文件预处理工具
├── UI/                      # 用户界面
│   ├── WebUI.py            # 主界面路由
│   ├── ConfigManagement.py # 配置管理界面
│   ├── FileManagement.py   # 文件管理界面
│   ├── GlossaryUI.py       # 术语表界面
│   ├── InteractiveTranslator.py # 交互翻译界面
│   └── TranslatorManagement.py # 翻译管理界面
├── llama-cpp/               # 模型启动脚本目录
└── Result/                  # 翻译结果输出目录
```

### 核心模块说明

#### 翻译引擎 (Translators/)
- `TxtTranslate.py`: TXT文件翻译核心，支持异步并发处理和智能行数匹配
- `EpubTranslate.py`: EPUB文件翻译，保持文档结构完整性和HTML标签处理
- `FilePretreatment.py`: 文件预处理，包含SHA256哈希生成和智能分段算法
- `Controller.py`: 翻译进程控制，支持多任务队列管理

#### 服务接口 (Clients/)
- `UnifiedRequest.py`: 统一的翻译服务抽象层，支持多服务端扩展
- `llama_cpp.py`: LLaMA-CPP模型服务实现，支持OpenAI兼容API
- `Timeout.py`: 全局超时配置管理 (当前设置为600秒)

#### 配置管理 (Config/)
- `Management.py`: 配置文件的CRUD操作和默认配置管理
- `config.json`: 用户配置存储，支持多配置文件管理
- 支持动态配置更新和实时生效

#### 术语表系统 (Glossary/)
- `GetKatakana.py`: 基于正则表达式的日文片假名自动检测和频率统计
- `Translator.py`: 术语表条目的批量翻译和管理

#### 用户界面 (UI/)
- `WebUI.py`: 主界面路由和导航管理
- 完整的Web界面，涵盖所有功能模块
- 响应式设计，支持实时状态更新和进度监控

#### 系统控制
- `Controller.py`: 后台翻译控制器，负责模型服务进程管理和翻译任务调度
- `Translator.py`: 翻译执行器，支持断点续传和缓存恢复

## ⚙️ 配置说明

### 翻译配置参数
```json
{
  "split_length": 500,
  "server": "llama-cpp",
  "bat_name": "Sakura-14b-Qwen2.5-v1.0-Q6_K-2Kx10.bat",
  "model": "Sakura-14b-Qwen2.5-v1.0-Q6_K",
  "system_prompt": "你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。",
  "preset_prompt": "根据以下术语表（可以为空）：\n{DICT}\n\n将下面的日文文本根据上述术语表的对应关系和备注翻译成中文：",
  "temperature": 0.1,
  "top_p": 0.3,
  "frequency_penalty": 0.25,
  "max_retry_count": 16,
  "Concurrent_quantity": 10
}
```

### 参数说明
- **split_length**: 文本分段长度 (200-1000)，影响翻译上下文
- **server**: 服务器类型 (当前仅支持 "llama-cpp")
- **bat_name**: 模型启动批处理文件名，位于 `llama-cpp/` 目录
- **model**: 使用的模型名称，需要与启动脚本中的模型一致
- **system_prompt**: 系统提示词，定义翻译风格和质量要求
- **preset_prompt**: 预设提示词模板，`{DICT}` 会被术语表内容替换
- **temperature**: 温度参数 (0.0-1.0)，控制翻译创造性，建议0.1-0.3
- **top_p**: Top-p采样参数 (0.0-1.0)，建议0.3-0.5
- **frequency_penalty**: 频率惩罚参数，减少重复内容
- **max_retry_count**: 最大重试次数，建议3-16次
- **Concurrent_quantity**: 并发翻译数量，根据系统内存调整 (建议4-10)

### 模型启动脚本配置
在 `llama-cpp/` 目录下的批处理文件示例：
```batch
@echo off
D:\LLM\llama.cpp\llama-server.exe -m E:\models\LLM\Sakura\Sakura-14B-Qwen2.5-v1.0-Q6_K.gguf -c 20480 -ngl 999 -fa --parallel 10 --defrag-thold 0.05 -a Sakura-14B-Qwen2.5-v1.0-Q6_K --device cuda1
```

参数说明：
- `-m`: 模型文件路径
- `-c`: 上下文长度
- `-ngl`: GPU层数
- `--parallel`: 并行处理数量
- `--device`: 指定GPU设备

## 📊 性能优化

### 性能特性
- **异步并发**: 支持多段落并行翻译，提高处理效率
- **智能缓存**: 基于SHA256文件哈希的缓存机制，避免重复处理
- **断点续传**: 翻译中断后可精确恢复进度，支持热重启
- **内存优化**: 大文件分块处理，避免内存溢出
- **进度监控**: 实时进度跟踪和时间预估

### 性能调优建议
1. **并发数量**: 根据系统内存和GPU性能调整`Concurrent_quantity` (建议4-10)
2. **分段长度**: 平衡上下文理解和处理效率 (建议500-800字符)
3. **缓存管理**: 定期清理`Cache/`目录释放存储空间
4. **模型优化**: 使用量化模型减少内存占用，提高推理速度
5. **GPU配置**: 合理分配GPU资源，避免显存溢出

### 系统要求建议
- **小型文件** (< 1MB): 8GB RAM + 中等GPU
- **中型文件** (1-10MB): 16GB RAM + 高性能GPU
- **大型文件** (> 10MB): 32GB RAM + 多GPU配置

## 🔧 故障排除

### 常见问题

#### 1. 模型服务启动失败
```bash
# 检查模型服务状态
tasklist | findstr "llama"

# 检查端口占用 (默认8080)
netstat -ano | findstr :8080

# 检查模型文件路径
dir E:\models\LLM\Sakura\
```

#### 2. 翻译任务卡住或停滞
- 检查`Cache/`目录写入权限
- 确认磁盘空间充足 (建议至少10GB可用空间)
- 重启后台控制器进程
- 检查模型服务是否正常运行

#### 3. 术语表不生效
- 验证术语表JSON格式正确性
- 检查文件编码是否为UTF-8
- 确认术语表文件名与小说文件名完全一致
- 检查术语表是否在`Cache/Source/`目录中

#### 4. 内存不足错误
- 减少`Concurrent_quantity`值
- 降低`split_length`分段长度
- 使用更小的量化模型
- 增加系统虚拟内存

### 调试和日志
系统会自动生成详细的日志文件：
```bash
# 查看应用日志 (包含详细错误信息)
type app.log

# 检查缓存状态
dir Cache\ /s

# 查看翻译进度文件
dir Cache\Time\
```

### 错误代码说明
- **翻译失败**: 检查模型服务连接和API响应
- **文件处理错误**: 验证文件格式和编码
- **缓存错误**: 检查磁盘空间和写入权限
- **配置错误**: 验证config.json格式和参数

## 🛠️ 开发指南

### 开发环境设置
```bash
# 激活虚拟环境
conda activate MoLing-Translator

# 启动Web界面 (开发模式)
streamlit run MoLing-Translator.py --server.port 8501

# 启动后台控制器 (独立终端)
python Controller.py

# 启动翻译执行器 (用于断点续传)
python Translator.py
```

### 代码规范和架构
- **异步编程**: 使用asyncio和aiohttp实现高性能异步处理
- **模块化设计**: 清晰的模块分离，便于维护和扩展
- **错误处理**: 完整的异常处理和日志记录机制
- **缓存策略**: 基于文件哈希的智能缓存系统
- **进程管理**: 后台控制器负责模型服务和翻译任务管理

### 扩展开发
- **新增翻译服务**: 在`Clients/`目录下添加新的服务实现
- **支持新格式**: 在`Translators/`目录下添加新的文件格式支持
- **UI组件**: 在`UI/`目录下添加新的界面组件
- **配置选项**: 扩展配置参数和验证逻辑

## 📝 更新日志

### v0.1.0 (当前版本)
- ✅ 完整的TXT和EPUB文件翻译支持
- ✅ 智能术语表管理和自动检测
- ✅ 交互式翻译界面和实时预览
- ✅ 批量翻译和队列管理系统
- ✅ 基于SHA256的断点续传功能
- ✅ 基于Streamlit的现代化响应式UI
- ✅ LLaMA-CPP模型集成和进程管理
- ✅ 多配置文件管理和默认配置
- ✅ 完整的错误处理和日志记录
- ✅ 性能优化和并发处理

## 📄 致谢

- **LLaMA-CPP**: 提供强大的本地模型推理能力
- **Streamlit**: 构建现代化Web界面的优秀框架
- **aiohttp**: 高性能异步HTTP客户端库
- **Sakura模型**: 优秀的日文翻译模型

---

# ⚠️ 免责声明

**MoLing-Translator** 是一个个人开发项目，仅供学习和研究使用。

- **不提供技术支持**: 本项目不提供任何形式的技术支持、用户指导或问题解答
- **不保证功能**: 不保证软件功能的完整性、准确性或可靠性
- **使用风险**: 使用本软件所产生的任何风险和损失由使用者自行承担
- **开源协议**: 项目代码开源，但请遵守相关开源协议
- **模型版权**: 使用第三方模型时请遵守相应的使用协议

请确认您理解并同意以上条款后再使用本软件。

---

**MoLing-Translator** - 专业的日文轻小说翻译解决方案 🚀