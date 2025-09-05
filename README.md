# MoLing-Translator

一个日文轻小说翻译系统，支持TXT和EPUB格式的批量翻译，配备术语表管理和交互式翻译功能。

## 🌟 主要特性

### 核心功能
- **多格式支持**: 完整支持TXT和EPUB文件格式的翻译
- **批量处理**: 高效的批量翻译能力，支持并发处理
- **智能断句**: 智能分段处理，保持原文格式和结构
- **术语表管理**: 自动检测和翻译日文片假名，支持自定义术语表
- **交互式翻译**: 实时流式翻译界面，支持即时翻译
- **断点续传**: 基于SHA256的智能缓存系统，支持翻译中断后恢复

### 专业特性
- **轻小说优化**: 专门针对日文轻小说翻译场景优化
- **行数匹配**: 确保译文与原文行数一致，保持格式完整
- **多模型支持**: 基于LLaMA-CPP的本地模型部署
- **配置管理**: 灵活的配置系统，支持多种翻译参数
- **质量控制**: 内置重试机制和错误处理，确保翻译质量

### 用户界面
- **现代化UI**: 基于Streamlit的响应式Web界面
- **实时进度**: 翻译进度实时监控和时间预估
- **队列管理**: 多任务队列管理系统
- **文件管理**: 直观的文件上传和管理界面

## 🚀 快速开始

### 系统要求
- **操作系统**: Windows 10/11
- **Python**: 3.8 或更高版本
- **Conda**: 用于环境管理
- **内存**: 推荐8GB以上RAM
- **存储**: 建议SSD存储以提高性能

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
```

#### 3. 模型配置
- 下载支持的LLaMA模型文件
- 配置`llama-cpp`目录下的模型启动脚本
- 确保模型服务正常运行

#### 4. 启动应用
```bash
# 使用批处理文件启动（推荐）
MoLing-Translator.bat

# 或手动启动
conda activate MoLing-Translator
streamlit run MoLing-Translator.py
```

## 📚 使用指南

### 1. 配置管理
首次使用需要配置翻译参数：
1. 进入"配置管理"页面
2. 添加新的翻译配置
3. 设置服务器地址、模型参数等
4. 设置默认配置

### 2. 文件翻译
1. 在"文件翻译"页面选择配置
2. 上传TXT或EPUB文件
3. 系统自动预处理文件
4. 启动翻译任务
5. 监控翻译进度

### 3. 术语表制作
- **自动检测**: 自动检测日文片假名词汇
- **批量翻译**: 一键翻译检测到的词汇
- **格式转换**: 支持外部术语表格式转换
- **术语管理**: 可视化术语表编辑和管理

### ⚠️ 重要说明：术语表匹配规则
**术语表文件名必须与小说文件名一致**，否则系统无法自动匹配并使用术语表。

例如：
- 小说文件：`小説1.txt` 或 `小説1.epub`
- 对应术语表：`小説1.json`

系统会根据小说文件名自动查找同名的术语表文件，并在翻译过程中自动应用。如果术语表文件名与小说文件名不匹配，术语表将不会被使用。

### 4. 交互式翻译
- **实时翻译**: 输入文本即时翻译
- **流式输出**: 翻译结果实时显示
- **术语集成**: 自动应用自定义术语表

## 🏗️ 项目架构

### 项目结构
```
MoLing-Translator/
├── MoLing-Translator.py      # 主程序入口
├── Controller.py             # 后台翻译控制器
├── Translator.py             # 翻译执行器
├── count_lines.py           # 代码行数统计
├── src/                      # 静态资源
│   └── Logo.png             # 应用Logo
├── Cache/                    # 缓存目录
│   ├── TXT/                 # TXT文件缓存
│   ├── EPUB/                # EPUB文件缓存
│   └── Time/                # 时间指示器
├── Clients/                  # 客户端模块
│   ├── UnifiedRequest.py   # 统一请求接口
│   ├── llama_cpp.py        # LLaMA-CPP实现
│   └── Timeout.py          # 超时配置
├── Config/                   # 配置管理
│   └── Management.py        # 配置管理系统
├── Glossary/                 # 术语表管理
│   ├── GetKatakana.py      # 片假名检测
│   └── Translator.py       # 术语翻译
├── Translators/             # 翻译引擎
│   ├── Controller.py       # 翻译控制器
│   ├── TxtTranslate.py     # TXT翻译器
│   ├── EpubTranslate.py    # EPUB翻译器
│   └── FilePretreatment.py # 文件预处理
├── UI/                      # 用户界面
│   ├── WebUI.py            # 主界面
│   ├── ConfigManagement.py # 配置管理界面
│   ├── FileManagement.py   # 文件管理界面
│   ├── GlossaryUI.py       # 术语表界面
│   ├── InteractiveTranslator.py # 交互翻译界面
│   └── TranslatorManagement.py # 翻译管理界面
└── Result/                  # 翻译结果输出
```

### 核心模块说明

#### 翻译引擎 (Translators/)
- `TxtTranslate.py`: TXT文件翻译核心，支持并发处理和行数匹配
- `EpubTranslate.py`: EPUB文件翻译，保持文档结构完整性
- `FilePretreatment.py`: 文件预处理，智能分段和格式处理

#### 服务接口 (Clients/)
- `UnifiedRequest.py`: 统一的翻译服务抽象层
- `llama_cpp.py`: LLaMA-CPP模型服务实现
- `Timeout.py`: 全局超时配置管理

#### 配置管理 (Config/)
- `Management.py`: 配置文件的CRUD操作和默认配置管理

#### 术语表系统 (Glossary/)
- `GetKatakana.py`: 日文片假名自动检测和提取
- `Translator.py`: 术语表条目的高精度翻译

#### 用户界面 (UI/)
- 完整的Web界面，涵盖所有功能模块
- 响应式设计，支持实时状态更新

## ⚙️ 配置说明

### 翻译配置参数
```json
{
  "server": "http://localhost:8080",
  "model": "japanese-novel-model",
  "temperature": 0.7,
  "top_p": 0.9,
  "frequency_penalty": 0.1,
  "max_retry_count": 3,
  "Concurrent_quantity": 5,
  "system_prompt": "你是一个专业的日文轻小说翻译家...",
  "preset_prompt": "将下面的日文文本翻译成中文：{DICT}",
  "bat_name": "start_model.bat"
}
```

### 参数说明
- **server**: LLaMA-CPP服务器地址
- **model**: 使用的模型名称
- **temperature**: 温度参数，控制翻译创造性
- **top_p**: Top-p采样参数
- **frequency_penalty**: 频率惩罚参数
- **max_retry_count**: 最大重试次数
- **Concurrent_quantity**: 并发翻译数量
- **system_prompt**: 系统提示词，定义翻译风格
- **preset_prompt**: 预设提示词，支持术语表插入
- **bat_name**: 模型启动批处理文件名

## 🛠️ 开发指南

### 开发环境设置
```bash
# 激活虚拟环境
conda activate MoLing-Translator

# 启动开发服务器
streamlit run MoLing-Translator.py --server.port 8501

# 启动后台控制器
python Controller.py
```

### 代码规范
- 遵循PEP 8 Python编码规范
- 使用异步编程模型提高性能
- 实现完整的错误处理机制
- 编写详细的注释和文档

## 📊 性能优化

### 性能特性
- **并发处理**: 支持多段落并行翻译
- **智能缓存**: 基于文件哈希的缓存机制
- **断点续传**: 翻译中断后可恢复进度
- **内存优化**: 大文件分块处理，避免内存溢出

### 性能调优建议
1. **并发数量**: 根据系统内存调整`Concurrent_quantity`
2. **缓存管理**: 定期清理`Cache/`目录释放空间
3. **模型优化**: 使用量化模型减少内存占用
4. **网络优化**: 确保模型服务器稳定连接

## 🔧 故障排除

### 常见问题

#### 1. 模型服务连接失败
```bash
# 检查模型服务状态
tasklist | findstr "llama"

# 检查端口占用
netstat -ano | findstr :8080
```

#### 2. 翻译进度停滞
- 检查`Cache/`目录权限
- 确认磁盘空间充足
- 重启翻译控制器

#### 3. 术语表不生效
- 验证术语表JSON格式
- 检查文件编码(UTF-8)
- 确认术语表文件路径

### 调试模式
启用详细日志记录：
```bash
# 查看应用日志
type app.log
```

## 📝 更新日志

### v0.1.0 (当前版本)
- ✅ 完整的TXT和EPUB翻译支持
- ✅ 智能术语表管理系统
- ✅ 交互式翻译界面
- ✅ 批量翻译和队列管理
- ✅ 断点续传和进度跟踪
- ✅ 基于Streamlit的现代化UI
- ✅ LLaMA-CPP模型集成

## 📄 致谢

- **LLaMA-CPP**: 提供强大的本地模型推理能力
- **Streamlit**: 构建现代化Web界面的优秀框架
- **aiohttp**: 高性能异步HTTP客户端

---

**MoLing-Translator** - 专业的日文轻小说翻译解决方案 🚀