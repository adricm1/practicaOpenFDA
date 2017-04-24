#Copyright [yyyy] [Adrian Calvo MOntes]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import http.server
import socketserver
import json
import http.client


class OpenFDAClient():
    OPENFDA_API_URL= "api.fda.gov"
    OPENFDA_API_EVENT= "/drug/event.json"

    def get_med(self,drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?search=patient.drug.medicinalproduct:"+drug+"&limit=10")
        r1 = conn.getresponse()
        data1 = r1.read()
        data=data1.decode("utf8")

        return data

    def get_comp(self,company):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?search="+company+"&limit=10")
        r1 = conn.getresponse()
        data1 = r1.read()
        data=data1.decode("utf8")

        return data


    def get_event(self,limit): #ESTA DEFINIENDO LA CLASE QUE ACOGE TO LO QUE VA DENTRO DEL GET EVENT
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL) #clase dentro de la biblioteca http.client que gestiona la conexion con la pagina
        #de la biblioteca coge httpsconection que permite establecer conexcionex con https con una url. crea un cliente
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit="+limit)
        r1 = conn.getresponse()
        data1 = r1.read()
        data=data1.decode("utf8")
        return data

class OpenFDAParser():
    def get_drugs(self,data):
        events=json.loads(data)
        medicamentos=[]
        for event in events["results"]:
            medicamentos+=[event["patient"]["drug"][0]["medicinalproduct"]]
        return medicamentos

    def get_company_numb(self,data):
        events=json.loads(data)
        com_numb=[]
        for event in events["results"]:
            com_numb+= [event["companynumb"]]
        return com_numb

    def get_Gender(self,data):
        events=json.loads(data)
        gender= []
        for event in events["results"]:
            gender+=event["patient"]["patientsex"]
        return gender

class OpenFDAHTML():

    def get_main_page(self):

        html = """
        <html>

            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1>Open FDA Client </h1>
                <form method="get" action="listDrugs">
                    <input type= "submit" value= "List  Drugs"></input>
                    Limit:<input type= "text" name = "limit"> </input>
                </form>


                <form method="get"action="searchDrug">
                    <input type= "text" name = "drug"> </input>
                    <input type= "submit" value= "Search drugs"></input>
                </form>
                <form method="get" action="listCompanies">
                    <input type= "submit" value= "List companies"></input>
                    Limit:<input type= "text" name = "limit"> </input>
                </form>
                <form method="get"action="searchCompany">
                    <input type= "text" name = "company"> </input>
                    <input type= "submit" value= "Search companies"></input>
                </form>

                <form method="get"action="listGender">
                    <input type= "submit" value= "List Gender"></input>
                    Limit:<input type= "text" name = "limit"> </input>
                </form>

            </body>
        </html>
        """
        return html


    def gender_page(self,gender):
        s=""
        for gender in gender:
            s += "<li>" +gender+ "</li>"
        html="""
        <html>
            <head></head>
                <body>
                    <ol>
                        %s
                    </ol>
                </body>
        <html>""" %(s)
        return html


    def drug_page(self,medicamentos):
        s=""
        for med in medicamentos:
            s += "<li>" +med+ "</li>"
        html="""
        <html>
            <head></head>
                <body>
                    <ul>
                        %s
                    </ul>
                </body>
        <html>""" %(s)
        return html

    def errorHTML(self):
        html= """
        <html>
            <head></head>
                <body> EROR 404 FILE NOT FOUND </body>

        </html>"""
        return html
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):


    def do_GET(self):

        #h1 es el tamañconn = http.client.HTTPSConnection("api.fda.gov") #clase dentro de la biblioteca http.client que gestiona la conexion con la pagina

        # Send message back to cli1/receivedrugent

        # Write content as utf-8 data

        client=OpenFDAClient()
        parser= OpenFDAParser()
        openhtml=OpenFDAHTML()
        response=200
        cabecera1='Content-type'
        cabecera2='text/html'
        if self.path =="/":
            html= openhtml.get_main_page()

        elif "/listDrugs" in self.path: #DE ESTA MANERA, LA PAGINA SE ABRE CUANDO SE EJECUTA EL BOTON
            limit= self.path.split("=")[1]
            events= client.get_event(limit)
            medicamentos= parser.get_drugs(events)
            html= openhtml.drug_page(medicamentos)

        elif "/searchDrug" in self.path:
            drug= self.path.split("=")[1]
            events = client.get_med(drug)
            com_num= parser.get_company_numb(events)
            html= openhtml.drug_page(com_num)

        elif "/listCompanies" in self.path:
            limit= self.path.split("=")[1]
            events = client.get_event(limit)
            com_num=parser.get_company_numb(events)
            html= openhtml.drug_page(com_num)

        elif "/searchCompany"in self.path:
            company= self.path.split("=")[1]
            events=client.get_comp(company)
            medicamentos= parser.get_drugs(events)
            html= openhtml.drug_page(medicamentos)

        elif "/listGender"in self.path:
            limit= self.path.split("=")[1]
            data=client.get_event(limit)
            gend= parser.get_Gender(data)
            html= openhtml.gender_page(gend)

        elif "/redirect" in self.path:
            response=302
            cabecera1= "Location"
            cabecera2= "http://Localhost:8000"

        elif "/secret" in self.path:
            response=401
            cabecera1= "WWW-Authenticate"
            cabecera2= 'Basic realm="My Realm"'

        else:
            response=404
            html= openhtml.errorHTML()

        self.send_response(response)
        self.send_header(cabecera1,cabecera2)
        self.end_headers()
        if response==200 or response==404:
            self.wfile.write(bytes(html,"utf8"))
