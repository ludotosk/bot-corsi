import datetime

def nuovoUtente():
    f = open("utenti.txt", "a")
    x = datetime.datetime.now()
    f.write(x.strftime("%d/%m/%Y-%X\n"))
    f.close()

def ricerche(tipo, corso):
    f = open("ricerche.csv", "a")
    x = datetime.datetime.now()
    s = x.strftime("%d/%m/%Y-%X")
    f.write('"' + tipo + '","' + corso + '","' + s + '"\n')
    f.close()