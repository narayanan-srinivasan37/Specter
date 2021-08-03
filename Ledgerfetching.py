import requests
import lxml.etree as etree
import xml.etree.ElementTree as Et
import csv
import json
from Call_Functions import get_function, refresh_token_function,post_ledger

url = "http://localhost:9000"
data="<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE>"
data+="<ID>Ledger</ID></HEADER><BODY><DESC><STATICVARIABLES><SVCURRENTCOMPANY>Apple Inc.</SVCURRENTCOMPANY><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>"
data+="</STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION NAME=""\"Ledger\"""ISINITIALIZE=""\"Yes\"""><TYPE>Ledger</TYPE>"
data+="<NATIVEMETHOD>PARENT</NATIVEMETHOD><NATIVEMETHOD>LEDGERMOBILE</NATIVEMETHOD><NATIVEMETHOD>ADDRESS</NATIVEMETHOD><NATIVEMETHOD>LEDSTATENAME</NATIVEMETHOD>"
data+="<NATIVEMETHOD>PINCODE</NATIVEMETHOD><NATIVEMETHOD>CREDITPERIOD</NATIVEMETHOD><NATIVEMETHOD>COUNTRYOFRESIDENCE</NATIVEMETHOD>"
data+="<NATIVEMETHOD>PARTYGSTIN</NATIVEMETHOD><NATIVEMETHOD>GRANDPARENT</NATIVEMETHOD></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>"
try:
    request = requests.post(url = url,data=data)
    response = request.text.strip().replace("&amp;","and") #replace special char &
    response = response.strip().replace("&#4; ","")
    response = response.strip().replace("�"," ")
    response = response.strip().replace("&#10;"," ")
    #print(response)
    responseXML = Et.fromstring(response)
    #print(response)
    #loop through xmlnodes and get ledger names using Xpath
    ledgerdetails=[]
   
    for data in responseXML.findall('./BODY/DATA/COLLECTION/LEDGER'):
        ledger=[]
    
        ledger.append(data.get('NAME'))
        ledger.append(data.find('PARENT').text)
        ledger.append(None if data.find('LEDGERMOBILE')==None else data.find('LEDGERMOBILE').text)
        ledger.append(None if data.find('LEDSTATENAME')==None else data.find('LEDSTATENAME').text)
        ledger.append(None if data.find('COUNTRYOFRESIDENCE')==None else data.find('COUNTRYOFRESIDENCE').text)
        address=None if data.findall('./ADDRESS.LIST/ADDRESS')==None else data.findall('./ADDRESS.LIST/ADDRESS')
        ledgeraddress=""
        if(address!=None):
            for add in address:
                ledgeraddress+=add.text
                ledgeraddress+="\t\n"
            ledger.append(ledgeraddress)
        else:
            ledgeraddress="None"
            ledger.append(ledgeraddress)
        ledger.append(None if data.find('PINCODE')==None else data.find('PINCODE').text)
        ledger.append(None if data.find('PARTYGSTIN')==None else data.find('PARTYGSTIN').text)
        ledger.append(None if data.find('CREDITPERIOD')==None else data.find('CREDITPERIOD').text)
        ledger.append(None if data.find('GRANDPARENT')==None else data.find('GRANDPARENT').text)
        print(None if data.find('GRANDPARENT')==None else data.find('GRANDPARENT').text)
        ledgerdetails.append(ledger)
    print(ledgerdetails)
    fields=["NAME","PARENT", "Mobile no", "State ", "Country","Address","Pincode","GSTIN","Credit Period","Grand Parent"]
    with open('LedgerDetails.csv', 'w') as f:
        
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(ledgerdetails)

    
    with open("Secret_key.json",) as json_file:
        keys = json.load(json_file)
        json_file.close()
    access_token = keys["access_token"]
    refresh_token = keys["refresh_token"]
    client_id = keys["client_id"]
    client_secret = keys["client_secret"]
    print("Entering while loop")


    while(1):
        my_headers = {
            "Authorization": 'Zoho-oauthtoken ' + access_token
        }
        jsondict={}
        count=0
        for datas in ledgerdetails:
            count=count+1
            jsondict['NAME']=datas[0]
            jsondict['PARENT']=datas[1]
            jsondict['Phone_Number']=datas[2]
            jsondict['State']=datas[3]
            jsondict['Country_Of_Residence']=datas[4]
            jsondict['Address']=datas[5]
            jsondict['Pincode']=datas[6]
            jsondict['GSTIN']=datas[7]
            jsondict['Credit_Period']=datas[8]
            jsondict["Grand_Parent"]= datas[9]
            data={"data":jsondict}
            data=json.dumps(data)
            print(count, len(ledgerdetails))
            response = post_ledger(data,my_headers)
            textresp=json.loads(response.text)
            print(response.text)
            if(textresp["code"]==2945):
                status_code = refresh_token_function(
                refresh_token, client_id, client_secret, keys)
                print(status_code)
                if(status_code == 200):
                    access_token = keys["access_token"]
                    break
                break
        if(count==(len(ledgerdetails)-1)):
            break
        break
    
        
except:
    print("Not able to communicate with tally.")

