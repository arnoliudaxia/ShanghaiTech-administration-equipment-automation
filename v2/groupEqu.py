import logging
from datetime import datetime
import pandas as pd
import openpyxl
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def get_current_datetime():
    """
    获取当前的日期和时间。

    返回:
        formatted_datetime (str): 格式化的当前日期和时间，格式为月日-时分秒。
    """
    now = datetime.now()  # 获取当前的日期和时间
    formatted_datetime = now.strftime("%m%d-%H%M%S")  # 将日期和时间格式化为字符串
    return formatted_datetime


def process(filepath: str, outputPath=None) -> str:
    logging.info(f"处理{filepath}, 导出到{outputPath}")
    errorLog = ""

    # 读取Excel文件
    df = pd.read_excel(filepath)

    # 过滤数据，假设 "适用范围" 和 "是否为配件/增值" 是要过滤的列
    filterSet = df[df["是否为配件/增值"] == "否"]["适用范围"].unique()



    # 创建新Excel文件，逐个将过滤后的数据写入
    with pd.ExcelWriter(outputPath) as writer:
        for filter_value in filterSet:
            print(f"筛选{filter_value}")
            # 1. 筛选出 "是否为配件/增值" 为 "否" 且 "适用范围" 满足条件的行
            filtered_data = df[(df["是否为配件/增值"] == "否") & (df["适用范围"] == filter_value)]
            print('筛选出 "是否为配件/增值" 为 "否" 且 "适用范围" 满足条件的行 个数为'+str(len(filtered_data)))

            # 2. 对于 "是否为配件/增值" 为 "是" 的行，找到其 "父资产编号"
            for index, row in df[df["是否为配件/增值"] == "是"].iterrows():
                # 找到当前行的 "父资产编号"
                parent_asset_number = row["父资产编号"]

                # 找到 "资产编号" 是这个 "父资产编号" 的那一行
                parent_row = df[df["资产编号"] == str(int(parent_asset_number))]

                # 如果找到该父资产，且父资产的 "适用范围" == filter_value
                if not parent_row.empty and parent_row["适用范围"].values[0] == filter_value:
                    # 把当前 "是否为配件/增值" 为 "是" 的行也加入过滤结果
                    filtered_data = pd.concat([filtered_data, pd.DataFrame([row])], ignore_index=True)

            print('总数为'+str(len(filtered_data)))

            filtered_data.to_excel(writer, sheet_name=str(filter_value), index=False)

    return errorLog



if __name__ == '__main__':
    process(filepath=r"v2/data/1000元以上历年设备对平.xlsx",outputPath="v2/data/1000元以上历年设备对平_all_11.xlsx")