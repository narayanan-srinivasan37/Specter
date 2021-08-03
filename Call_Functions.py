import requests
import json
import xml.etree.ElementTree as Et


def get_function(my_headers):
    resp = requests.get(
        'https://creatorapp.zoho.in/api/v2/narayanansrinivasan37/narayanan-app/report/Dummy_OrderDetails_Report', headers=my_headers)
    return resp


def post_ledger(data, my_headers):
    resp = requests.post(
        'https://creatorapp.zoho.in/api/v2/narayanansrinivasan37/narayanan-app/form/Ledger_Details',data=data, headers=my_headers)
    return resp
def refresh_token_function(ref_token, client_id, client_secret, keys):
    resp = requests.post('https://accounts.zoho.in/oauth/v2/token?refresh_token='+ref_token +
                         '&client_id='+client_id+'&client_secret='+client_secret+'&grant_type=refresh_token')
    refreshed_token = json.loads(resp.text)
    
    keys["access_token"] = refreshed_token["access_token"]

    with open("Secret_key.json", "w") as jsonFile:
        json.dump(keys, jsonFile)
        jsonFile.close()
    return resp.status_code


def All_ledgers(url):
    data = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>List of Ledgers</ID>"
    data += "</HEADER><BODY><DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES></DESC></BODY></ENVELOPE>"
    request = requests.post(url=url, data=data)
    response = request.text
    responseXML = Et.fromstring(response)
    ledgers = []
    for data in responseXML.findall('./BODY/DATA/COLLECTION/LEDGER'):
        ledgers.append[data.get('NAME')]
    return ledgers


def get_stockitems(url):
    data = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>StockItems</ID></HEADER>"
    data += "<BODY><DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION Name='StockItems'>"
    data += "<TYPE>StockItem</TYPE><FETCH>Name,ClosingBalance,BaseUnits</FETCH></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>"
    req = requests.post(url=url, data=data)
    res = req.text.strip()
    responseXML = Et.fromstring(res)
    stock_items = []
    for item in responseXML.findall('./BODY/DATA/COLLECTION/STOCKITEM'):
        stock_item = []
        stock_item.append(item.get('NAME'))
        stock_item.append(item.find('CLOSINGBALANCE').text)
        stock_item.append(0, item.find('BASEUNITS').text)
        stock_items.append(stock_item)
    return stock_items
