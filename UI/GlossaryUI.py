import streamlit as st
import Glossary
import os
import shutil
import pickle
import json
import time
import pyperclip

def Glossary_UI():
    function_name = st.sidebar.radio(
        label = "选择功能",
        options = ('辅助制作', '格式转换'),
        index = 0,
        format_func = str,
        help = '请选择功能',
        key = 'function_name'
    )

    glossary_page = st.empty()

    if function_name == '辅助制作':
        Katakanas_list = []
        if os.path.exists('Cache\\Glossary\\Temp\\katakana.pkl'):
            with open('Cache\\Glossary\\Temp\\katakana.pkl', 'rb') as f:
                Katakanas_list = pickle.load(f)
        else:
            if os.path.exists('Cache\\Glossary') == False:
                os.makedirs('Cache\\Glossary\\Temp')
            else:
                shutil.rmtree('Cache\\Glossary')
                os.makedirs('Cache\\Glossary\\Temp')
        with glossary_page.container():

            # 侧边栏模型提示
            st.sidebar.error('**请先手动启动最高精度的翻译模型**')

            # 侧边栏上传文件
            uploaded_files = st.sidebar.file_uploader("上传文件", type=["txt", "epub"], accept_multiple_files=True)

            # 侧边栏设置识别次数
            limit1 = st.sidebar.slider(
                '次数下限',
                min_value=1,
                max_value=50,
                step=1,
                value=10,
                help='基础次数下限',
                key='limit'
                )
            limit2 = st.sidebar.slider(
                '放大系数',
                min_value=1,
                max_value=50,
                step=1,
                value=1,
                help='基础次数下限的放大系数',
                key='limit2'
                )
            limit = limit1 * limit2

            
            # 分析按钮
            start_katakanas_analysis_button = st.sidebar.button('获取片假名列表')
            # 翻译按钮
            start_katakanas_translation_button = st.sidebar.button('逐一翻译为中文')
            # 保存按钮
            stop_katakanas_translation_button = st.sidebar.button('结束制作并保存')

            # 判断是否上传了文件
            if uploaded_files is not None and len(uploaded_files) > 0:
                # 删除Cache\\Glossary下的所有文件，但是不删除Cache\\Glossary其中的文件夹
                for file in os.listdir('Cache\\Glossary'):
                    file_path = os.path.join('Cache\\Glossary', file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                
                for uploaded_file in uploaded_files:
                    file_path = os.path.join("Cache\Glossary", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
            else:
                # 删除Cache\\Glossary下的所有文件，但是不删除Cache\\Glossary其中的文件夹
                for file in os.listdir('Cache\\Glossary'):
                    file_path = os.path.join('Cache\\Glossary', file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            
            # 判断是否需要获取假名列表
            if start_katakanas_analysis_button:
                Katakanas_list = Glossary.GetKatakana.get_katakana_list(limit, Katakanas_list)
                with open('Cache\\Glossary\\Temp\\katakana.pkl', 'wb') as f:
                    pickle.dump(Katakanas_list, f)
            
            # 显示假名列表
            if len(Katakanas_list) > 0:
                # 设定可变布局
                if 'katakana' not in st.session_state:
                    st.session_state.katakana = {katakana[0]: False for katakana in Katakanas_list}
                if 'katakana_delete_buttons' not in st.session_state:
                    st.session_state.katakana_delete_buttons = {katakana[0]: False for katakana in Katakanas_list}
                
                max_len = max(len(katakana[0]) for katakana in Katakanas_list)
                
                # 显示列表
                for katakana in Katakanas_list:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        nbsp = "&nbsp;"*(max_len-len(katakana[0]))*5
                        if len(katakana) == 3:
                            st.session_state.katakana[katakana[0]] = st.markdown(f"{katakana[1]}&nbsp;&nbsp;|&nbsp;&nbsp;**{katakana[0]}**{nbsp}——>")
                        elif len(katakana) == 4:
                            st.session_state.katakana[katakana[0]] = st.markdown(f"{katakana[1]}&nbsp;&nbsp;|&nbsp;&nbsp;**{katakana[0]}**{nbsp}——>&nbsp;&nbsp;**{katakana[3]}**")
                    with col2:
                        st.session_state.katakana_delete_buttons[katakana[0]] = st.button('删除', key=f'delete_{katakana[0]}')
                        if st.session_state.katakana_delete_buttons[katakana[0]]:
                            Katakanas_list.remove(katakana)
                            # 删除按钮
                            del st.session_state.katakana[katakana[0]]
                            del st.session_state.katakana_delete_buttons[katakana[0]]
                            with open('Cache\\Glossary\\Temp\\katakana.pkl', 'wb') as f:
                                pickle.dump(Katakanas_list, f)
                            glossary_page.empty()
                            st.session_state['navigation'] = '术语表制作'
                            st.rerun()
                
                # 翻译按钮
                if start_katakanas_translation_button:
                    for i in range(len(Katakanas_list)):
                        katakana = Katakanas_list[i]
                        translated_katakana = Glossary.Translator.translator(katakana[0])
                        Katakanas_list[i] = [katakana[0], katakana[1], katakana[2], translated_katakana]
                        nbsp = "&nbsp;"*(max_len-len(katakana[0]))*5
                        st.session_state.katakana[katakana[0]].markdown(f"{katakana[1]}&nbsp;&nbsp;|&nbsp;&nbsp;**{katakana[0]}**{nbsp}——>&nbsp;&nbsp;**{translated_katakana}**")
                    with open('Cache\\Glossary\\Temp\\katakana.pkl', 'wb') as f:
                        pickle.dump(Katakanas_list, f)
                
                # 完成并保存
                if stop_katakanas_translation_button:
                    pd = 0
                    for katakana in Katakanas_list:
                        if len(katakana) == 3:
                            pd += 1
                    if pd > 0:
                        # 有词语还未翻译
                        st.toast("有词语还未翻译，请先翻译所有词语再保存")
                        time.sleep(1)
                        glossary_page.empty()
                        st.session_state['navigation'] = '术语表制作'
                        st.rerun()
                    else:
                        if os.path.exists('Cache\\Glossary\\Temp\\katakana.pkl'):
                            with open('Cache\\Glossary\\Temp\\katakana.pkl', 'rb') as f:
                                Katakanas_list = pickle.load(f)
                            if os.path.exists('Result') == False:
                                os.makedirs('Result')
                            with open("Result\\Glossary.json", "w", encoding='utf-8') as f:
                                glossary = []
                                for katakana in Katakanas_list:
                                    temp = {
                                        'src': katakana[0],
                                        'dst': katakana[3],
                                        'info': katakana[2]
                                    }
                                    glossary.append(temp)
                                json.dump(glossary, f, ensure_ascii=False, indent=4)
                            st.session_state.katakana = {}
                            st.session_state.katakana_delete_buttons = {}
                            shutil.rmtree('Cache\\Glossary')
                            glossary_page.empty()
                            st.session_state['navigation'] = '术语表制作'
                            st.rerun()
    elif function_name == '格式转换':
        warning = st.warning("**格式转换**用于将从**轻小说机翻机器人**获取的术语表转换为符合本程序要求的格式")
        try:
            glossary_text = st.sidebar.text_area("请将获取的术语表粘贴到此处", height=200, key='glossary_text')
            glossary = []
            if glossary_text != '':
                # 按行分割为列表
                glossary_text = glossary_text.split('\n')
                for glossary_line in glossary_text:
                    glossary_line = glossary_line.strip()
                    glossary_line = glossary_line.split(' => ')
                    if len(glossary_line) == 2:
                        temp = {
                            'src': glossary_line[0],
                            'dst': glossary_line[1],
                            'info': ''
                        }
                        glossary.append(temp)
            if len(glossary) > 0:
                st.write("**解析结果**：")
                st.json(glossary)
                if st.sidebar.button("保存为json文件"):
                    if os.path.exists('Result') == False:
                        os.makedirs('Result')
                    with open("Result\\Glossary.json", "w", encoding='utf-8') as f:
                        json.dump(glossary, f, ensure_ascii=False, indent=4)
                    warning.warning("**保存成功！**")
                if st.sidebar.button("复制到剪贴板"):
                    pyperclip.copy(json.dumps(glossary, ensure_ascii=False, indent=4))
                    warning.warning("**复制成功！**")
        except:
            st.error("解析失败，请检查格式是否正确")