import pdfkit
import requests
import json
import re

urlCorsi = "https://ludotosk.it/corsi"
urlMaster = "https://json-server-corsi.herokuapp.com/master"
theadCorsi = "<thead><tr><th scope='col'>#</th><th scope='col'>Nome corso</th><th scope='col'>Unviersit&agrave;</th><th scope='col'>Test</th><th scope='col'>Citt&agrave;</th></tr></thead>"
theadMaster =  "<thead><tr><th scope='col'>#</th><th scope='col'>Nome corso</th><th scope='col'>Unviersit&agrave;</th><th scope='col'>Durata</th><th scope='col'>Lingua</th><th scope='col'>Citt&agrave;</th></tr></thead>"
tipoMaster = 'tipo'
tipoCorsi = 't'

def pdf(name, db, tipo):
    global theadCorsi
    global urlCorsi
    global tipoCorsi
    global tipoMaster
    global urlMaster
    global theadMaster
    tbody = '<tbody>'

    i = 1
    if db == 1:
        thead = theadCorsi
        url = urlCorsi
        varTipo = tipoCorsi
    elif db == 2:
        url = urlMaster
        thead = theadMaster
        varTipo = tipoMaster

    ploads = {varTipo: tipo}
    r = requests.get(url, params=ploads)
    corsi = json.loads(r.text)
    if db == 1:
        for corso in corsi:
            if re.search(name, corso["n"], re.IGNORECASE):
                tbody += '<tr><th scope="row">' + str(i) + '</th><td><a href="' + corso["h"] + '">' + corso["n"].replace('à', '&agrave;') + '</a></td><td>' + corso["u"].replace(
                    'à', '&agrave;') + '</td><td>' + corso["a"].replace('ì', '&igrave;') + '</td><td>' + corso["s"] + '</td><tr>'
                i += 1
        tbody += '</tbody>'
    elif db == 2:
        for corso in corsi:
            if re.search(name, corso["corso"], re.IGNORECASE):
                tbody += '<tr><th scope="row">' + str(i) + '</th><td><a href="' + corso["link"] + '">' + corso["corso"] + '</a></td><td>' + corso["uni"].replace('à', '&agrave;') + '</td><td>' +  corso["durata"] + '</td><td>' + corso["lingua"].upper() + '</td><td>' + corso["citta"] + '</td><tr>'
                i += 1
        tbody += '</tbody>'    

    if i == 1:
        return 0

    f = open("prova.html", "r")
    html = f.read()
    f.close()
    html = html.replace("<h1 class='display-6'></h1>", "<h1 class='display-6'>Report " + tipo + " in " + name + ".</h1>")
    html = html.replace("<thead></thead>", thead)
    html = html.replace("<tbody></tbody>", tbody)

    return pdfkit.from_string(html, False)