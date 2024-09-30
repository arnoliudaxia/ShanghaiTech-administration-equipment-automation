import logging
from datetime import datetime

import openpyxl


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


def process(filepath:str,outputPath=None)->str:
    errorLog=""
 
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    # Create a mapping from column headers to their indices
    keywordTable = {} 
    rowNumber = ws.max_row
    keywordRow = ws[1]
    for index in range(len(keywordRow)):
        keywordTable[keywordRow[index].value] = index + 1
    
    # Check if "适用范围" exists in the headers
    if "适用范围" not in keywordTable:
        errorLog = f'Error: "适用范围" column not found in the provided Excel file.'
        return errorLog
    
    def filterOne(filter):
        # 创建一个sheet，名称为filter
        filtered_sheet=wb.create_sheet(title=filter)
        # Copy the header row to the new sheet
        for col in range(1, ws.max_column + 1):
            filtered_sheet.cell(row=1, column=col, value=ws.cell(row=1, column=col).value)
        
        filtered_row_index = 2
        #遍历列 keywordTable["适用范围"]
        for i in range(2, rowNumber+1):
            cellValue = str(ws.cell(row=i, column=keywordTable["适用范围"]).value)
            isPeijian= ws.cell(row=i, column=keywordTable["是否为配件/增值"]).value
            filterOut=False
            if (filter in cellValue and isPeijian=="否"):
                filterOut=True
            if isPeijian=="是":
                # 读取「父资产编号」单元格，从开头一行行遍历「资产编号」，直到找到匹配的行，复制该行到新sheet中
                父资产编号=str(ws.cell(row=i, column=keywordTable["父资产编号"]).value)
                for j in range(2,rowNumber+1):
                    if str(ws.cell(row=j, column=keywordTable["资产编号"]).value)==父资产编号:
                        if filter in str(ws.cell(row=j, column=keywordTable["适用范围"]).value):
                            filterOut=True
                        break
            if filterOut:
                # 复制该行到新sheet中
                for col in range(1, ws.max_column + 1):
                    filtered_sheet.cell(row=filtered_row_index, column=col, value=ws.cell(row=i, column=col).value)
                filtered_row_index += 1
    
    # 遍历「适用范围」，获取一个set集合
    filterSet=set()
    for i in range(2,rowNumber+1):
        cellValue = str(ws.cell(row=i, column=keywordTable["适用范围"]).value)
        isPeijian= ws.cell(row=i, column=keywordTable["是否为配件/增值"]).value
        if isPeijian=="否":
            filterSet.add(cellValue)

    for filter in filterSet:
        filterOne(filter)

    if outputPath:
        wb.save(outputPath)
    else:
        wb.save(filepath)
        
    return errorLog

if __name__ == '__main__':
    process(filepath=r"v2/data/test文档.xlsx",outputPath="v2/data/test文档_All.xlsx")