import time

import streamlit as st
from calculateMerge import process,get_current_datetime

st.title("合并计算资产小程序v0.1")
# region 初始化持久变量
if "isuploaded" not in st.session_state:
    st.session_state["isuploaded"]=False
if "isprocessed" not in st.session_state:
    st.session_state["isprocessed"]=False
# endregion

with st.chat_message("ai"):
    # st.write("请上传要「合并计算资产」的表格")
    uploaded_file = st.file_uploader(label="请上传要「合并计算资产」的表格")

if uploaded_file is not None:

    with open('upload/' + uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    st.session_state["isuploaded"]=True

    with st.chat_message("ai"):
        st.write("收到表格，处理数据中....")

        errlog=""
        # 使用之前的程序
        with st.status("收到表格，处理数据中...."):
            if not st.session_state["isprocessed"]:
                exportFilePath="export/" + get_current_datetime()+ uploaded_file.name
                errlog=process('upload/' + uploaded_file.name, exportFilePath)

    with st.chat_message("ai"):
        if not st.session_state["isprocessed"]:
            if errlog != "":
                st.write("处理过程中出现了一些错误，详情如下：")
                for e in errlog.split("\n"):
                    st.error(e)
            st.write("处理完成，点击下载处理后的表格")
            st.session_state["isprocessed"] = True

            with open(exportFilePath, "rb") as file:
                btn = st.download_button(
                    label="点击下载处理后的表格",
                    data=file,
                    file_name=uploaded_file.name
                )
        else:
            st.write("流程结束！")
            st.session_state["isuploaded"]=False
            st.session_state["isprocessed"]=False
            st.write("点击上传文件右侧的叉叉来重新开始！")
# if st.session_state["isprocessed"]:
#     with st.chat_message("user"):
#         if st.button("重新开始(按两次)"):
#             st.session_state["isuploaded"]=False
#             st.session_state["isprocessed"]=False



######处理阶段#####