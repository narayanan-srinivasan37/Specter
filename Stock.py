import requests
import xml.etree.ElementTree as Et
import csv
url = 'http://localhost:9000'
url = 'http://localhost:9000'
data = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>StockItems</ID></HEADER>"
data += "<BODY><DESC><STATICVARIABLES><SVCURRENTCOMPANY>Apple Inc.</SVCURRENTCOMPANY><EXPLODEALLLEVELS>Yes</EXPLODEALLLEVELS><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION Name='StockItems'>"
data += "<TYPE>StockItem</TYPE><FETCH>PARENT,CLOSINGRATE,CLOSINGBALANCE,CLOSINGVALUE,BASEUNITS,GSTDETAILS</FETCH></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>"
req = requests.post(url=url, data=data)
res = req.text.strip()
responseXML = Et.fromstring(res)
print(res)
stock_items = []
for item in responseXML.findall('./BODY/DATA/COLLECTION/STOCKITEM'):
    stock_item = []
    stock_item.append(item.get('NAME'))
    stock_item.append( item.find('PARENT').text)
    stock_closing_balance = (item.find('CLOSINGBALANCE').text)
    stock_closing_price = (item.find('CLOSINGRATE').text)
    #print(item.find('GSTDETAILS'))
    if(stock_closing_balance!=None):
        temp= stock_closing_balance.split(" ")
        tempprice = stock_closing_price.split('/')
        stock_closing_balance= temp[1]
        stock_closing_price= float(tempprice[0])
    else:
        stock_closing_balance= 0
        stock_closing_price= 0
    stock_item.append(stock_closing_balance)
    stock_item.append(stock_closing_price)
    stock_item.append( item.find('BASEUNITS').text)
    stock_items.append(stock_item)
#print(stock_items)
fields=["NAME","PARENT", "CLOSING BALANCE", "CLOSING RATE","BASE UNITS"]
with open('stockitems.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(stock_items)