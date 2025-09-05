import os
import re

def count_lines_of_code(file_path):
    """统计单个Python文件的代码行数（忽略空行，但不忽略注释行）"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    code_lines = 0
    in_multiline_comment = False

    for line in lines:
        line = line.strip()

        # 忽略空行
        if not line:
            continue

        # 处理多行注释
        if in_multiline_comment:
            if re.search(r"\"\"\"$|\'\'\'$", line):
                in_multiline_comment = False
            code_lines += 1
            continue
        elif re.match(r"\"\"\"|\'\'\'", line):
            in_multiline_comment = True
            code_lines += 1
            continue

        # 保留注释行
        if re.match(r"#", line):
            code_lines += 1
            continue

        # 有效代码行
        code_lines += 1

    return code_lines

def classify_project_size(total_lines):
    """根据代码行数对项目规模进行分类"""
    if total_lines < 1000:
        return "小型项目"
    elif total_lines < 10000:
        return "中型项目"
    elif total_lines < 100000:
        return "大型项目"
    else:
        return "超大型项目"

def main():
    project_root = os.getcwd()  # 获取当前目录作为项目根目录
    total_lines = 0
    ignored_folders = {"runtime"}  # 需要忽略的文件夹列表

    # 遍历项目目录，统计所有Python文件的代码行数
    for root, dirs, files in os.walk(project_root):
        # 忽略指定的文件夹
        dirs[:] = [d for d in dirs if d not in ignored_folders]

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                lines = count_lines_of_code(file_path)
                total_lines += lines
                print(f"文件: {file_path} 代码行数: {lines}")

    # 分类项目规模
    project_size = classify_project_size(total_lines)

    # 打印结果
    print(f"\n项目总代码行数: {total_lines}")
    print(f"项目规模: {project_size}")
    input("按任意键退出...")

if __name__ == "__main__":
    main()