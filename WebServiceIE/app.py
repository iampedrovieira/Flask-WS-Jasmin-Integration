from flask import request,Flask,jsonify, Response
import fitz
import json
import requests

app = Flask(__name__)

@app.route('/criar-orcamento', methods=['POST'])
def criar_orçamento():

    token=get_token()
    return {token:token}

@app.route('/criar-fatura', methods=['POST'])
def criar_fatura():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        print (request.json)

        token = get_token()

        req_data = request.get_json()
        cliente_key=""
        artigos=[]
        #do bizagi vais receber:
        #o id do cliente buyerCustomerParty
        # e vais receber uma lista dos produtos/serviços ,quantidade e o preço
        #So tens de criar um json igual ao que tem embaixo,json, e so tens de mudar
        #o buyerCustomerParty para o id que é envidado do bizagi
        #e tens de criar documentLines com todos os produtos que receberes do request do bizagi


        url = "https://my.jasminsoftware.com/api/243032/243032-0001/billing/invoices"

        artigos_para_json=[]
        for artigo in artigos:
            preco = artigo.preco / artigo.quantidade
            json_artigos={
                {
                    "salesItem":artigo.nome,
                    "quantity":artigo.quantidade,
                    "unitPrice": { "amount": preco }
                },
            }
            artigos_para_json.append(json_artigos)

        json = {
        "documentType": "FA",
        "serie":"2021",
        "company": "IPDVDC",
        "buyerCustomerParty":cliente_key ,
        "accountingParty":cliente_key ,
        "loadingCountry":"PT" ,
        "unloadingCountry":"PT" ,
        "paymentTerm":"01",
        "documentLines":artigos_para_json
        }
        
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer "+token
            }

        response = requests.request("POST", url, json=json, headers=headers)
    fatura_key=response.json()
   
    url2 = "https://my.jasminsoftware.com/api/243032/243032-0001/billing/invoices/"+fatura_key
    headers2 = {
    'Content-Type': "application/json",
    'Authorization': "Bearer "+token
    }

    response2 = requests.request("GET", url2, headers=headers2)
    json_final={
        "faturaid":response2.json()['naturalKey'],
        "total": response2.json()['payableAmount']['amount']
    }

    criar_pdf_fatura(json_final['faturaid'],token)

    return json_final

@app.route('/criar-recibo', methods=['POST'])
def criar_recibo():
    if request.method == 'POST':
        token = get_token()
        return token
        print (request.json)
        print(request.json["valorTotal"])
        valor_pago= request.json["valorTotal"] # valor da fatura
        fatura=request.json["idFatura"] # id da fatura
        party="0002" # id do cliente
        url = "https://my.jasminsoftware.com/api/243032/243032-0001/accountsReceivable/processOpenItems/generateReceipt"
        querystring = {"apiOpenAccountPosting":"{apiOpenAccountPosting}"}
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer "+token
            }
        json = {
                "company": "IPDVDC",
                "documentType": "REC",
                "documentDate": "",
                "serie":"2021",
                "postingDate": "",
                "financialAccount": "CONTA",
                "cashFlowItem": "10",
                "note": "",
                "cash":"",
                "party": party,
                "currency": "",
                "exchangeRate": 1,
                "paymentMethod": "TRA",
                "checkNumber": "",
                    "openAccountPostingLines": 
                    [{
                        "selected":"true",
                    "sourceDoc": fatura,
                    "settled":valor_pago,
                    "discount": 0
                        }]
                }
        response = requests.request("POST", url, json=json, headers=headers, params=querystring)
        url2 = "https://my.jasminsoftware.com/api/243032/243032-0001/accountsReceivable/receipts/71aa9226-fe0c-436d-9cad-dda761d8294c"
        response2 = requests.request("GET", url2, headers=headers)
        criar_pdf_recibo(response2.json()['naturalKey'],token)
        return Response(status=200)

@app.route('/produtos', methods=[ 'GET'])
def getProdutos():
    if request.method == 'GET':  #this block is only entered when the form is submitted
        token = get_token()
        url = "https://my.jasminsoftware.com/api/243032/243032-0001/salesCore/salesItems/"
        payload={}
        headers = {
          'Authorization': 'Bearer '+token,
          }
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        data = {}
        linhas = []
        for product in json_response:
            nome_produto = product["itemKey"]
            json_line = {'nome': nome_produto}
            linhas.append(json_line)
        
        json = {'Artigos': linhas}
        return json

def get_token():

    url_token = "https://identity.primaverabss.com//core/connect/token"
    #autenticação
    payload_token = "grant_type=client_credentials&client_id=XXXXX&client_secret=XXXXXX&scope=application"
    headers_token = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'postman-token': "XXXXXX"
    }

    response_token = requests.request("POST", url_token, data=payload_token, headers=headers_token)
    token = response_token.json()["access_token"]   
    return token

def pdf_to_img(string):
    doc = fitz.open(string+".pdf")
    page = doc.loadPage(0)  # number of page
    pix = page.getPixmap()
    output = string+".jpg"
    pix.writePNG(output)

def enviar_pdf_fatura(token,id_fa):
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer "+token
        }
    url = " https://my.jasminsoftware.com/api/243032/243032-0001/billing/invoices/IPDVDC/FA/2021/"+id_fa+"/printOriginal"
    response = requests.request("GET", url, headers=headers)
    with open('fatura.pdf', 'wb') as f:
        f.write(response.content) 
    pdf_to_img("fatura")  

def criar_pdf_recibo(id_rec,token):
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer "+token
        }
    url = "https://my.jasminsoftware.com/api/243032/243032-0001/accountsReceivable/receipts/IPDVDC/REC/2021/"+id_rec+"/printOriginal"
    response = requests.request("GET", url, headers=headers)
    with open('recibo.pdf', 'wb') as f:
        f.write(response.content)

    pdf_to_img("recibo")
if __name__ == '__main__':
    app.run(debug=True)