import time

import streamlit as st
from calculateMerge import process,get_current_datetime

st.title("合并计算资产小程序v0.1")

# "请上传要「合并计算资产」的表格"
uploaded_file = st.file_uploader(label="请上传要「合并计算资产」的表格")

# region 初始化持久变量
if "isuploaded" not in st.session_state:
    st.session_state["isuploaded"]=False
# endregion

if uploaded_file is not None:
    with open('upload/' + uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    st.session_state["isuploaded"]=True

    # 使用之前的程序
    with st.status("收到表格，处理数据中...."):
        pass
        time.sleep(1)
        exportFilePath="export/" + get_current_datetime()+ uploaded_file.name
        process('upload/' + uploaded_file.name, exportFilePath)

    with open(exportFilePath, "rb") as file:
        btn = st.download_button(
            label="点击下载处理后的表格",
            data=file,
            file_name=uploaded_file.name
        )

st.divider()
if st.button("重新开始"):
    st.session_state["isuploaded"]=False



######处理阶段#####