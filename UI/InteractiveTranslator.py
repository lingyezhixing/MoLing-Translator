import streamlit as st
import json
import re
from openai import OpenAI
import copy
import Config
import time
import pickle
import logging

# 设置Logging等级和格式
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w')

def InteractiveTranslator():
    InteractiveTranslator_page = st.empty()
    with InteractiveTranslator_page.container():
        st.sidebar.warning("**流式输出**，边看边译")

        with open("Cache\\Translating_info.pkl", "wb") as f:
            pickle.dump(None, f)
        with open("Cache\\translating_file_sh256.pkl", "wb") as f:
            pickle.dump(None, f)

        # 获取配置信息
        config_dict = Config.Management.read_config()
        config_list = list(config_dict.keys())
        config = st.sidebar.selectbox(
            '选择配置:',
            config_list,
            index=0
        )
        config = config_dict[config]
        system_prompt = config["system_prompt"]
        preset_prompt = config["preset_prompt"]
        split_length = config["split_length"]
        model = config["model"]
        temperature = config["temperature"]
        top_p = config["top_p"]
        frequency_penalty = config["frequency_penalty"]

        # 输入框
        text = st.text_area("请输入要翻译的内容", height=200, key="text")
        glossary_text = st.text_area("请输入术语表（可以留空，建议至少为人名建立术语表，有助于提高翻译质量）", height=200, key="glossary_text")

        # 按钮和状态
        if 'Interactive_translatend_buttons' not in st.session_state:
            st.session_state.Interactive_translatend_buttons = {}
        
        st.session_state.Interactive_translatend_buttons["Interactive_translatend_start"] = st.sidebar.button("开始翻译", key="Interactive_translatend_start")
        st.session_state.Interactive_translatend_buttons["Interactive_translatend_stop"] = st.sidebar.button("停止翻译", key="Interactive_translatend_stop")

        if st.session_state.Interactive_translatend_buttons["Interactive_translatend_start"]:
            if text != '':
                with open("Cache\\Translating_info.pkl", "wb") as f:
                    pickle.dump({"config": config}, f)
                with open("Cache\\translating_file_sh256.pkl", "wb") as f:
                    pickle.dump("model_only", f)
                time.sleep(10)
                client = OpenAI(api_key="llama-cpp", base_url=f"http://127.0.0.1:8080/v1/")
                try:
                    glossary = []
                    if glossary_text != '':
                        # 解析为json
                        glossary = json.loads(glossary_text)
                    data = text.strip()
                    data_raw = re.sub('\n+', '\n', data)
                    data_lines = data_raw.strip().split("\n")

                    data_list = []
                    i = 0
                    while i < len(data_lines):
                        text = ""
                        while len(text) < split_length:
                            if i >= len(data_lines):
                                break
                            if len(text) > max(-len(data_lines[i]) + split_length, 0):
                                break
                            text += data_lines[i] + "\n"
                            i += 1
                        text = text.strip()
                        data_list.append(text)
                    
                    if 'Interactive_translatend' not in st.session_state:
                        st.session_state.Interactive_translatend = {i: False for i in range(len(data_list))}
                    n = 0
                    for org_text in data_list:
                        st.session_state.Interactive_translatend[n] = st.markdown("", unsafe_allow_html=True)
                        gpt_dict_raw_text = ""
                        dict_info_use = []
                        gpt_dict_text_list = []
                        preset_prompt_temp = copy.deepcopy(preset_prompt)
                        if len(glossary) > 0:
                            for dict_info in glossary:
                                if dict_info["src"] in org_text:
                                    dict_info_use.append(dict_info)
                            if len(dict_info_use) > 0:
                                for dict_info in dict_info_use:
                                    src = dict_info['src']
                                    dst = dict_info['dst']
                                    if "info" in dict_info.keys():
                                        if dict_info["info"] != "":
                                            info = dict_info['info']
                                            single = f"{src}->{dst} #{info}"
                                        else:
                                            single = f"{src}->{dst}"
                                    else:
                                        single = f"{src}->{dst}"
                                    gpt_dict_text_list.append(single)

                                gpt_dict_raw_text = "\n".join(gpt_dict_text_list)
                        # 将preset_prompt中的{DICT}替换为gpt_dict_raw_text
                        if gpt_dict_raw_text == "":
                            preset_prompt_temp = "将下面的日文文本翻译成中文："
                        else:
                            preset_prompt_temp = preset_prompt_temp.replace("{DICT}", gpt_dict_raw_text)
                        
                        logging.debug(f"交互式翻译提示词：{preset_prompt_temp}")

                        trans_text = ""
                        for output in client.chat.completions.create(
                            model=model,
                            messages=[
                                {
                                    "role": "system",
                                    "content": system_prompt
                                },
                                {
                                    "role": "user",
                                    "content": preset_prompt_temp + org_text
                                }
                            ],
                            temperature=temperature,
                            top_p=top_p,
                            frequency_penalty=frequency_penalty,
                            stream=True
                        ):
                            # stream=True key response
                            if output.choices[0].delta.content:
                                trans_text += output.choices[0].delta.content
                                st.session_state.Interactive_translatend[n].markdown(trans_text.replace("\n", "<br><br>"), unsafe_allow_html=True)
                            if st.session_state.Interactive_translatend_buttons["Interactive_translatend_stop"]:
                                break
                        n += 1
                    st.toast("翻译结束")
                    with open("Cache\\Translating_info.pkl", "wb") as f:
                        pickle.dump(None, f)
                    with open("Cache\\translating_file_sh256.pkl", "wb") as f:
                        pickle.dump(None, f)
                except Exception as e:
                    st.error(f"翻译失败: {e}")
                    st.session_state.Interactive_translatend[n].markdown("翻译失败")