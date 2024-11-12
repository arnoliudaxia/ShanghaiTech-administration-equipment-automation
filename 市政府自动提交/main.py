import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# cookie_string = 'Hm_lvt_fa659f678fedf5ea21219e8fb2914831=1718603157; Hm_lpvt_fa659f678fedf5ea21219e8fb2914831=1718603157; sgst-instr=0ED024737D6AF1C34606A6E119EB8D63; Hm_lvt_297c9349622a15b64a77366360801f57=1718603232; Hm_lpvt_297c9349622a15b64a77366360801f57=1718603232'
cookie_string = input("输入Cookie：")

# 将cookie字符串转换为字典
cookies_dict = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_string.split('; ')}


response = requests.post("https://cs1.sgst.cn/recordBase/listPage/list", headers=headers, cookies=cookies_dict,json={"page":1,"limit":500,"serviceRecordCode":"","nameCh":"","appCompany":"","subDwAccount":"","finishDate":"","finishDateStart":"","finishDateEnd":"","appDateStart":"","appDateEnd":"","invcCode":"","invcNum":"","deptName":"","completeFlag":"0","recordType":"仪器"})
# response.json()

deviceInfo=[]

for device in response.json()["data"]["content"]:
    # print(device["recordAppCompany"])
    # print(device["recordId"])

    deviceInfo.append({
        "recordAppCompany":device["recordAppCompany"],
        "recordId":device["recordId"]
    })


for device in tqdm(deviceInfo):
    url = f'https://cs1.sgst.cn/recordIns/updatePage/{device["recordId"]}'  # 替换为目标URL
    response = requests.get(url, headers=headers, cookies=cookies_dict)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 辅助函数：获取输入字段的值，如果不存在则返回空字符串
    def get_input_value(soup, input_id):
        input_element = soup.find('input', {'id': input_id})
        if input_element is None:
            input_element = soup.find('input', {'name': input_id})
            if input_element.attrs["type"]=="radio":
                return [radio['value'] for radio in soup.find_all('input', {'name': input_id, 'type': 'radio'}) if radio.has_attr('checked')][0]

            return input_element.attrs["value"]
        if not input_element.has_attr("value"):
            return soup.find('select', {'id': input_id}).find('option', selected=True)['value'],
        return input_element['value']
        # return input_element['value'] if input_element and input_element.has_attr('value') else ""

    # 提取数据
    data = {
        "serviceRecord": {
            "source": soup.find('input', {'name': "source"}).attrs["value"],
            "getInvoiceFlag": get_input_value(soup, 'getInvoiceFlag'),
            "attachPath": get_input_value(soup, 'invcImageUrl'),
            "imageId": get_input_value(soup, 'invoiceImage'),
            "file": "",  # 没有找到相关信息，保留为空
            "isImg": "false",  # 根据上下文推断此值
            "invcCodeOcr": "",  # 没有找到相关信息，保留为空
            "invcNoOcr": get_input_value(soup, 'invcNoOcr'),
            "amountOcr": get_input_value(soup, 'amountOcr'),
            "invcDateOcr": get_input_value(soup, 'invcDateOcr'),
            "sellerName": get_input_value(soup, 'sellerName'),
            "purchaserName": get_input_value(soup, 'purchaserName'),
            "invcCode": get_input_value(soup, 'invcCode'),
            "invcNo": get_input_value(soup, 'invcNo'),
            "amount": get_input_value(soup, 'amount'),
            "invcDate": get_input_value(soup, 'invcDate'),
            "appCompName": get_input_value(soup, 'appCompName'),
            "delegtId": "",
            "dwType": "研究院所",  # 根据上下文推断此值
            "appAddress": get_input_value(soup, 'appAddress'),
            "appUserName": get_input_value(soup, 'appUserName'),
            "appPhone": get_input_value(soup, 'appPhone'),
            "province": "上海市",
            "city": "浦东新区",
            "appArea": "上海市-浦东新区",  # 根据上下文推断此值
            "trade": soup.find('select', {'id': 'trade'}).find('option', selected=True)['value'],
            "appPostcode": "",  # 没有找到相关信息，保留为空
            "appEmail": "",  # 没有找到相关信息，保留为空
            "appFax": "",  # 没有找到相关信息，保留为空
            "appBankName": "",  # 没有找到相关信息，保留为空
            "appBankAccount": "",  # 没有找到相关信息，保留为空
            "serviceCount": get_input_value(soup, 'serviceCount'),
            "operatorName": soup.find('select', {'id': 'operatorName'}).find('option', selected=True)['value'],
            "appCount": get_input_value(soup, 'appCount'),
            "appHour": get_input_value(soup, 'appHour'),
            "appFee": get_input_value(soup, 'appFee'),
            "proName": "",  # 没有找到相关信息，保留为空
            "proCode": "",  # 没有找到相关信息，保留为空
            "serviceType": soup.find('select', {'id': 'serviceType'}).find('option', selected=True)['value'],
            "select": "电子与通信技术",  # 根据上下文推断此值
            "subjectArea": "电子与通信技术",  # 根据上下文推断此值
            "isAgreement": get_input_value(soup, 'isAgreement'),
            "outUseAddress": "",  # 没有找到相关信息，保留为空
            "customsNum": "",  # 没有找到相关信息，保留为空
            "proFrom": "",  # 没有找到相关信息，保留为空
            "estimate": get_input_value(soup, 'estimate'),
            "appRemk": "",  # 没有找到相关信息，保留为空
            "recordType": get_input_value(soup, 'recordType'),
            "id": get_input_value(soup, 'id'),
            "invcId": get_input_value(soup, 'invcId'),
            "macId": get_input_value(soup, 'macId'),
            "invcDeptName": device["recordAppCompany"]
        }
    }

    data["invoice"]=data["serviceRecord"]

    # print(data)
    # break
    res=requests.post(url="https://cs1.sgst.cn/recordIns/updatePage/submit",cookies=cookies_dict,json=data)

    # 使用 json.loads 将响应文本解析为 Python 字典
    response_json = json.loads(res.text)

    # 将 Unicode 转换为可读的中文字符
    # print(device)
    # print(response_json['message'])

    if response_json['message']!="提交成功":
        print(response_json['message'])
