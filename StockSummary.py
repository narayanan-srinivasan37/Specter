import requests
import xml.etree.ElementTree as Et
import csv
url = 'http://localhost:9000'
data = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>StockItems</ID></HEADER>"
data += "<BODY><DESC><STATICVARIABLES><EXPLODEALLLEVELS>Yes</EXPLODEALLLEVELS><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION Name='StockItems'>"
data += "<TYPE>StockItem</TYPE><FETCH>PARENT,CLOSINGRATE,CLOSINGBALANCE,CLOSINGVALUE,BASEUNIT</FETCH></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>"


data1 = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>StockGroups</ID></HEADER>"
data1 += "<BODY><DESC><STATICVARIABLES><EXPLODEALLLEVELS>Yes</EXPLODEALLLEVELS><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION Name='StockGroups'>"
data1 += "<TYPE>StockGroup</TYPE><FETCH>PARENT,HSNCODE,GSTDETAILS</FETCH></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>"
req = requests.post(url=url, data=data1)
res = req.text.strip()
response = res.strip().replace("&#4; ","")
responseXML = Et.fromstring(response)
stockgroupswithgst=[]
print(res)
for data in responseXML.findall('./BODY/DATA/COLLECTION/STOCKGROUP'):
    stockgroup=[]
    stockgroup.append(data.get('NAME'))
    stockgroup.append(data.find('./GSTDETAILS.LIST/HSNCODE').text)
    #stockgroup.append(data.find('./GSTDETAILS.LIST/HSN').text)
    temp=data.findall('./GSTDETAILS.LIST/STATEWISEDETAILS.LIST/RATEDETAILS.LIST/GSTRATEDUTYHEAD')
    #stockgroup.append(temp[0].text)
    temp1=data.findall('./GSTDETAILS.LIST/STATEWISEDETAILS.LIST/RATEDETAILS.LIST/GSTRATE')
    stockgroup.append(temp1[0].text)
    #stockgroup.append(temp[1].text)
    stockgroup.append(temp1[1].text)
    #stockgroup.append(temp[2].text)
    stockgroup.append(temp1[2].text)
    stockgroupswithgst.append(stockgroup)
#print(stockgroupswithgst)

fields=["NAME","HSN CODE", "Central tax percent", "State tax percent", "Integrated tax percent"]
with open('stocksummary.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(stockgroupswithgst)