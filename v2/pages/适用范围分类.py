import time
import os
import streamlit as st
from groupEqu import process,get_current_datetime

st.title("适用范围分类v0.2")
# region 初始化持久变量
if "isuploaded" not in st.session_state:
    st.session_state["isuploaded"]=False
if "isprocessed" not in st.session_state:
    st.session_state["isprocessed"]=False
# endregion

with st.chat_message("ai"):
    uploaded_file = st.file_uploader(label="请上传表格")

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

            st.write("处理完成，点击下载处理后的表格")
            st.session_state["isprocessed"] = True

            with open(exportFilePath, "rb") as file:
                btn = st.download_button(
                    label="点击下载处理后的表格",
                    data=file,
                    file_name=uploaded_file.name
                )
            if errlog != "":
                st.write("注意处理过程中出现了一些错误，详情如下：")
                for e in errlog.split("\n"):
                    st.error(e)
        else:
            st.write("流程结束！")
            st.session_state["isuploaded"]=False
            st.session_state["isprocessed"]=False
            st.write("点击上传文件右侧的叉叉来重新开始！")

    # 清理本地临时文件
    os.remove('upload/' + uploaded_file.name) 


######处理阶段#####