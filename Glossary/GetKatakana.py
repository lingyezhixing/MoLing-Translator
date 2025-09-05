from collections import Counter
import os
import re
import hashlib
import logging
import fnmatch
import zipfile
import shutil

# 设置Logging等级和格式
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w')

# 获取片假名词汇表
def katakana_detection(text, Katakanas_list, threshold=1):
    # 正则表达式匹配片假名字符范围
    pattern = r'[\u30A0-\u30FF]+'

    # 使用 re.findall 查找所有片假名词项
    katakana_words = re.findall(pattern, text)

    # 过滤掉单个字符的词语
    katakana_words = [word for word in katakana_words if len(word) > 1]

    # 统计每个词语出现的次数
    word_counts = Counter(katakana_words)

    # 过滤掉出现次数低于阈值的词语
    filtered_word_counts = {word: count for word, count in word_counts.items() if count >= threshold}

    # 按出现次数从多到少排序
    sorted_word_counts = sorted(filtered_word_counts.items(), key=lambda x: x[1], reverse=True)

    # 将元组转换为列表
    sorted_katakana_counts = [[word, count, ""] for word, count in sorted_word_counts]

    # 如果某个词语在sorted_katakana_counts中不存在但是在Katakanas_list中存在，则从Katakanas_list中删除
    for katakana in Katakanas_list:
        if katakana[0] not in [item[0] for item in sorted_katakana_counts]:
            Katakanas_list.remove(katakana)

    # 如果在Katakanas_list中找到匹配的词语，则优先使用Katakanas_list中的信息
    for i in range(len(sorted_katakana_counts)):
        for katakana in Katakanas_list:
            if katakana[0] == sorted_katakana_counts[i][0]:
                sorted_katakana_counts[i] = katakana

    return sorted_katakana_counts

# 定义一个函数用于获取文件的sha256哈希值
def get_sha256(file_path):
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logging.error(f"TXT错误：获取文件sha256哈希值时发生错误: {e}")
        return None

# 寻找EPUB文件中的所有html文件
def find_all_htmls(root_dir):
    try:
        html_files = []
        for foldername, subfolders, filenames in os.walk(root_dir):
            for extension in ['*.html', '*.xhtml', '*.htm']:
                for filename in fnmatch.filter(filenames, extension):
                    file_path = os.path.join(foldername, filename)
                    html_files.append(file_path)
        return html_files
    except Exception as e:
        logging.error(f"EPUB错误：寻找EPUB文件中的所有html文件时发生异常：{e}")
        return None

# 获取EPUB单文件文本
def get_html_text_list(epub_html_path):
    def clean_text(text):
        text = re.sub(r'<rt[^>]*?>.*?</rt>', '', text)
        text = re.sub(r'<[^>]*>|\n', '', text)
        return text
    try:
        match_text = ""
        with open(epub_html_path, 'r', encoding='utf-8') as f:
            file_text = f.read()
            matches = re.finditer(r'<(h[1-6]|p|a|title).*?>(.+?)</\1>', file_text, flags=re.DOTALL)
            if not matches:
                logging.info("这可能是个结构文件，跳过")
                return match_text, file_text
            
            for match in matches:
                match_text += clean_text(match.group(2))
        return match_text, file_text
    
    except Exception as e:
        logging.error(f"EPUB错误：获取EPUB单文件文本发生异常：{e}")
        return None, None

def Txt_to_text(txt_book_path):
    try:
        # 获取TXT文本
        try:
            with open(txt_book_path, 'r', encoding='utf-8') as f:
                data = f.read().strip()
        except:
            with open(txt_book_path, 'r', encoding='gbk') as f:
                data = f.read().strip()
        txt_texts = re.sub('\n+', '\n', data)
        
        return txt_texts

    except Exception as e:
        logging.error(f"TXT错误：获取分段失败: {e}")
        return None

def Epub_to_text(epub_book_path):
    try:
        sha256 = get_sha256(epub_book_path)
        epub_texts = []
        os.makedirs(os.path.join(".\Cache\\Glossary\\Temp", sha256))
        with zipfile.ZipFile(epub_book_path, "r") as f:
            f.extractall(os.path.join(".\Cache\\Glossary\\Temp", sha256, "temp"))
        all_htmls = find_all_htmls(os.path.join(".\Cache\\Glossary\\Temp", sha256, "temp"))
        for html_path in all_htmls:
            match_text, file_text = get_html_text_list(html_path)
            if len(match_text) == 0:
                logging.info("这可能是个结构文件，跳过")
                continue
            epub_texts.append(match_text)
        
        # 用\n连接所有元素
        epub_texts = '\n'.join(epub_texts)

        # 删除临时文件夹
        shutil.rmtree(os.path.join(".\Cache\\Glossary\\Temp", sha256))
        
        return epub_texts
    
    except Exception as e:
        logging.error(f"EPUB错误：获取分段失败: {e}")
        return None

def get_katakana_list(limit, Katakanas_list):
    try:
        texts = []
        file_list = os.listdir(".\Cache\Glossary")
        for file_name in file_list:
            if file_name.endswith(".txt"):
                txt_text = Txt_to_text(os.path.join(".\Cache\Glossary", file_name))
                if txt_text is not None:
                    texts.append(txt_text)
            elif file_name.endswith(".epub"):
                epub_text = Epub_to_text(os.path.join(".\Cache\Glossary", file_name))
                if epub_text is not None:
                    texts.append(epub_text)
        text = '\n'.join(texts)
        katakana_list = katakana_detection(text, Katakanas_list, limit)
        return katakana_list

    except Exception as e:
        logging.error(f"错误：获取假名列表失败: {e}")
        return None