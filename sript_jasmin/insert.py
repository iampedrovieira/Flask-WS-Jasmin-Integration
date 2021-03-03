import pandas as pd
import requests
import json
from unidecode import unidecode

lista_produtos =[]

url_token = "https://identity.primaverabss.com//core/connect/token"

#autenticação
payload_token = "grant_type=client_credentials&client_id=XXXXXXXX&client_secret=xxxxxxx&scope=application"
headers_token = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'postman-token': "XXXXXXXXXXXXXXXXXX"
    }

response_token = requests.request("POST", url_token, data=payload_token, headers=headers_token)

token = response_token.json()["access_token"]

excel_travagem = pd.read_excel('Data.xlsx', sheet_name='Travagem')

for nome in excel_travagem.iloc[:,0]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_7 = pd.read_excel('Data.xlsx', sheet_name='Alternador, motor de arranque')
for nome in excel_7.iloc[:,0]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_8 = pd.read_excel('Data.xlsx', sheet_name='Arranque, Bateria')
for nome in excel_8.iloc[:,1]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_9= pd.read_excel('Data.xlsx', sheet_name='Direção, Suspensão')

for nome in excel_9.iloc[:,0]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_10 = pd.read_excel('Data.xlsx', sheet_name='Velas e peças de ignição')

for nome in excel_10.iloc[:,0]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_1 = pd.read_excel('Data.xlsx', sheet_name='Amortecedores e pratos')
for nome in excel_1.iloc[:,0]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_2 = pd.read_excel('Data.xlsx', sheet_name='Embraiagem')
for nome in excel_2.iloc[:,0]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_3 = pd.read_excel('Data.xlsx', sheet_name='Escape')
for nome in excel_3.iloc[:,0]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_4 = pd.read_excel('Data.xlsx', sheet_name='Motorização e correias')
for nome in excel_4.iloc[:,1]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_5 = pd.read_excel('Data.xlsx', sheet_name='Refrigeração Líquida')
for nome in excel_5.iloc[:,1]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))

excel_6 = pd.read_excel('Data.xlsx', sheet_name='Ópticas')
for nome in excel_6.iloc[:,0]:
    if str(nome) != 'nan':
        lista_produtos.append(str(nome))



lista_Final = []
for x in lista_produtos:
    lista_Final.append(unidecode(x.replace(" ","_").replace("+","p").replace("%","pr").replace("(","").replace(")","").replace(".","-").replace("°","-").replace("/","-").replace('"',"").replace("'","")[-20:]))

lista_prod = []

for j in lista_produtos:
    lista_prod.append(unidecode(j.replace('"',"").replace("'",""))) 

print(lista_Final)
print(len(lista_produtos))


for i in range(228,len(lista_Final)):
    itemKey = str(lista_Final[i])
    desc = str(lista_prod[i])
    print('A adicionar artigo nº '+str(i)+ ' : '+itemKey)
  
    url_add = "https://my.jasminsoftware.com/api/243032/243032-0001/salesCore/salesItems"

    payload_add = '{"unit":"UN","Description":'+'"'+desc+'"'+',"itemTaxSchema":"NORMAL","locked":"false","itemKey":'+'"'+itemKey+'"'+'}'
    print(payload_add)
    a= json.loads(payload_add)
    print(a)
    headers_add = {
        'Content-Type': "application/json",
        'Authorization': "Bearer "+token
        }

    response_add = requests.request("POST", url_add, json=a, headers=headers_add)
    if(response_add.status_code == 201):
        print("Adicionado com sucesso")
    else:
        print('Erro: '+response_add.text)
    print("--------------------------")


