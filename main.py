import random
import datetime
import sqlite3
import initdb
import numpy as np
import prova

print("inizio")
initdb.setup()
conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row
def table(name:str, params:tuple, names:tuple):
    
    
    mark = ""
    if type(params) != str:
        for i in params:
            mark += "?,"
        mark = mark[:-1]
        conn.execute(f"INSERT INTO {name} {names} VALUES ({mark})",(*params,))
    else:
        mark = "?"
        conn.execute(f"INSERT INTO {name} ({names}) VALUES ({mark})",(params,))
    conn.commit()
    
    
def Meteo(x):#TAB_DATOMETEREOLOGICO_PREV[i, j]  = [[u, 3], [v, 5], [p, 2], [t, 8], [u, 5], [v,6 ], [p, 9], [t, 0]]
    u = []
    p = []
    v = []
    t = []
    for i in x:
        if i[0] == "umidità":
            u.append(i[1])
        elif i[0] == "precipitazioni":
            p.append(i[1])
        elif i[0] == "vento":
            v.append(i[1])
        else:
            t.append(i[1])

    u = np.sum(u)/len(u)
    p = np.sum(p)/len(p)
    v = np.sum(v)/len(v)
    t = np.sum(t)/len(t)

    y = [u, p, v, t]

    if y[0] > 50:
        return 3
    elif y[1] > 50:
        return 1
    elif y[2] > 50:
        return 2
    else:
        return 0

def Generate_ids(x, y=1000):
    return [i+y for i in range(x)]

RAW = 10
FAT = 0.5

base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(30)]
prec = []
for i in date_list:
    if not i in prec:
        prec.append(i.strptime(i.strftime("%d-%m-%Y"), "%d-%m-%Y"))
date_list = prec
date_list.reverse()

#ATTRIBUTI#
pivas = [i for i in range(10000, 20000)]
numeri_ditte_manutenzione = [i+3300000000 for i in range(100)] #(3300000000, 3399999999)
tipo = ["umidità", "precipitazioni", "vento", "temperatura"]
marca = ["Toyota, AGL, Barrow", "Vagen", "Dickies", "EAN"]
previsione = ["soleggiato", "precipitazioni", "temporale", "ventoso", "nuvoloso"]
categoria = ["giornaliero", "settimanale", "mensile"]
orbita = ["LEO", "MEO", "GEO", "NULL"]
nomi_agenzia_metereologiche = ["Monsters & CO", "Panini Corporation", "Sonyc"]

#LIV 0#
località = ["Salerno", "Riccione", "Padova", "Bassano", "Novara"]
TAB_DITTAMANUTENZIONE = {}

TAB_STAZIONE = {}
TAB_AGENZIE_METEO = {}

#LIV 1#
TAB_TERRESTRE_MERITTIMO = {}
FOR_TAB_TERRESTRE_MERITTIMO = {}

TAB_STORICO = {}

TAB_SENSORE = {}
FOR_TAB_SENSORE = {}

#LIV 2#
TAB_APPARTENENZA = {}
FOR1_TAB_APPARTENENZA = {}
FOR2_TAB_APPARTENENZA = {}

TAB_STIMA = {}
FOR1_TAB_STIMA = {}
FOR2_TAB_STIMA = {}

TAB_COLLEZIONE = {}
FOR1_TAB_COLLEZIONE = {}
FOR2_TAB_COLLEZIONE = {}

TAB_INTERVENTO = {}
FOR1_TAB_INTERVENTO = {}
FOR2_TAB_INTERVENTO = {}

TAB_DATOMETEREOLOGICO = {}
FOR_TAB_DATOMETEREOLOGICO = {}
TAB_DATOMETEREOLOGICO_UNIQUE = {}
TAB_DATOMETEREOLOGICO_PREV = {}

TAB_PREVISIONE = {}
FOR1_TAB_PREVISIONE = {}
FOR2_TAB_PREVISIONE = {}

#LIV 3#
TAB_CONFRONTO = {}

#################################LOCAZIONE############################################
for i in località:
    table("Locazione", (i), ("nome"))

###########################################DITTA DI MANUTENZIONE###########################################
giro = 0
for i in numeri_ditte_manutenzione:
    piva = pivas[giro%len(pivas)]
    TAB_DITTAMANUTENZIONE[piva] = [piva, i]
    table("DittaManutenzione", (piva, i), ("piva", "telefono"))
    giro += 1
    
###################################STAZIONI##########################################
id_stazioni = Generate_ids(RAW)
giro = 0
for i in id_stazioni:
    orb = orbita[giro%len(orbita)]
    print(giro%len(orbita), orb)
    TAB_STAZIONE[i] = [i, orb]
    table("Stazione", (i, orb), ("id","orbita"))
    giro += 1

####################################AGENZIE METEREOLOGICHE'#########################################
for i in nomi_agenzia_metereologiche:
    TAB_AGENZIE_METEO[i] = [i, f"https://{i.replace(' ', '_')}.it", f"{i}.exe"]
    table("Agenzia_meteorologica", (i, f"https://{i.replace(' ', '_')}.it", f"{i}.exe"), ("nome", "sitoWeb", "app"))

##################################TERRESTRE MARITTIMO###########################################
for i in TAB_STAZIONE.keys():
    if TAB_STAZIONE[i][1] == "NULL":
        state = random.choice([False, True])
        TAB_TERRESTRE_MERITTIMO[i] = [i, state]
        FOR_TAB_TERRESTRE_MERITTIMO[i] = TAB_STAZIONE[i]
        table("Terrestre_Marittimo", (i, state), ("id", "tipo"))

########################################STORICO##############################################
giro = 0
id_Storico = Generate_ids(len(località)*len(date_list))
for i in località:
    for j in date_list:
        meteo_effettivo = random.choice(previsione)
        TAB_STORICO[i,j] = [i, j, meteo_effettivo, id_Storico[giro]]
        table("Storico", (id_Storico[giro], i, j, meteo_effettivo), ("id" ,"locazione", "data", "meteo_effettivo"))
        print(giro)
        giro += 1

########################################SENSORI##############################################
giro = 0
k = len(tipo)
id_sensori = Generate_ids(RAW*k)
offest = 0
for i in id_stazioni:
    for j in id_sensori[offest:offest+k]:
        t, m, mod = tipo[giro%k], random.choice(marca), random.randint(0, 999)
        TAB_SENSORE[j] = [i, t, m, mod, i]
        FOR_TAB_SENSORE[i] = TAB_STAZIONE[i]                                                #DA RIVEDERE
        table("Sensore", (j, t, m, mod, i), ("id", "tipo", "marca", "modello", "id_stazione"))
        giro += 1 
    offest += k
    print(giro)

######################################APPARTENENZA################################################
giro = 0
for i in id_stazioni:
    locazione = località[giro%len(località)]
    TAB_APPARTENENZA[i] = [i, locazione]
    FOR1_TAB_APPARTENENZA[i] = TAB_STAZIONE[i]
    if locazione in FOR2_TAB_APPARTENENZA:
        FOR2_TAB_APPARTENENZA[locazione].append(i)
    else:
        FOR2_TAB_APPARTENENZA[locazione] = [i]
    table("Appartenenza", (i, locazione), ("id_stazione", "locazione"))
    giro += 1

#########################################STIMA#############################################
id_dato_metereologico = Generate_ids(len(id_sensori)*len(date_list))#DA CHIEDERE 3
id_previsioni_giornaliere = Generate_ids(len(date_list)*len(località)*len(nomi_agenzia_metereologiche))
id_previsioni_settimanali = Generate_ids((len(date_list)*len(località)*len(nomi_agenzia_metereologiche))//7, len(id_previsioni_giornaliere))
id_previsioni_mensili = Generate_ids((len(date_list)*len(località)*len(nomi_agenzia_metereologiche))//30, len(id_previsioni_giornaliere)+len(id_previsioni_settimanali))

iters = 0

k = len(id_stazioni)*len(tipo)#8
offest = 0

for i in id_previsioni_giornaliere:
    for j in id_dato_metereologico[offest:offest+k]:
        TAB_STIMA[i,j] = [i,j]
        FOR1_TAB_STIMA[i] = i
        FOR2_TAB_STIMA[j] = j
        table("Stima", (j, i), ("id_dato", "id_previsione"))
        print(iters)
        iters += 1
    offest += k
##########################################COLLEZIONE############################################

giro = 0
giro2 = 0
for i in località:
    for j in date_list:
        for v in FOR2_TAB_APPARTENENZA[i]:
            for k in tipo:
                #TAB_STORICO[i,j] = [i, j, meteo_effettivo, id_Storico[giro]]
                TAB_STORICO[i,j][3]
                table("Collezione", (id_dato_metereologico[giro], TAB_STORICO[i,j][3]), ("id_dato", "id_storico"))
                TAB_COLLEZIONE[i, j, k, v] = [id_dato_metereologico[giro], TAB_STORICO[i,j][3]]
                FOR1_TAB_COLLEZIONE[id_dato_metereologico[giro]] = [id_dato_metereologico[giro], i, j, k, v]
                FOR2_TAB_COLLEZIONE[i, j] = TAB_STORICO[i, j]
                giro += 1
                print(giro)
        giro2 += 1

##########################################INTERVENTO############################################

giro = 0
id_interventi = Generate_ids(RAW)
for i in id_interventi:
    piva_ditta = random.choice([i for i in TAB_DITTAMANUTENZIONE.keys()])
    id = random.choice([i for i in TAB_TERRESTRE_MERITTIMO.keys()])
    d = random.choice(date_list)
    TAB_INTERVENTO[i] = [i, d, piva_ditta, id]
    FOR1_TAB_INTERVENTO[piva_ditta] = TAB_DITTAMANUTENZIONE[piva_ditta]
    FOR2_TAB_INTERVENTO[id] = TAB_TERRESTRE_MERITTIMO[id]
    table("Intervento", (i, d, piva_ditta, id), ("id", "dataOra", "piva_ditta", "id_TR_MR"))
    giro += 1

######################################DATO METEREOLOGICO################################################
giro = 0
for i in id_sensori:
    for j in date_list:
        id = id_dato_metereologico[giro]
        tipo = TAB_SENSORE[i][1]

        if tipo == "umidità":
            misurazione = random.randint(0, 100)
        elif tipo == "precipitazioni":
            misurazione = random.randint(0, 100)
        elif tipo == "vento": 
            misurazione = random.randint(0, 50)
        else:
            misurazione = random.randint(-10, 40)
        
        TAB_DATOMETEREOLOGICO[i, j] = [i, j, id, tipo, misurazione]##DA VEDERE
        FOR_TAB_DATOMETEREOLOGICO[i] = TAB_SENSORE[i]
        TAB_DATOMETEREOLOGICO_UNIQUE[id] = [id, i, j, tipo, misurazione]
        
        if (TAB_APPARTENENZA[TAB_SENSORE[i][4]][1], j) in TAB_DATOMETEREOLOGICO_PREV:
            TAB_DATOMETEREOLOGICO_PREV[TAB_APPARTENENZA[TAB_SENSORE[i][4]][1],j].append([tipo, misurazione])
        else:
            TAB_DATOMETEREOLOGICO_PREV[TAB_APPARTENENZA[TAB_SENSORE[i][4]][1],j] = [[tipo, misurazione]]

        table("DatoMeteorologico", (id, tipo, misurazione, j, i), ("id", "tipo", "misurazione", "dataMisurazione", "id_sensore"))
        giro+=1

##########################################PREVISIONI############################################
giro = 1
index_day = 0
bool_set = False
bool_mes = False
index_set = 0
index_mens = 0
lista_meteo_settimanale = []
lista_meteo_mensile = []
for i in località:
    for j in date_list:
        for k in nomi_agenzia_metereologiche:
            acc = random.uniform(10.0, 99.9)
            if giro%1 == 0:
                meteo = Meteo(TAB_DATOMETEREOLOGICO_PREV[i, j])
                TAB_PREVISIONE[id_previsioni_giornaliere[index_day]] = [j, k, i, meteo, "giornaliero", acc, TAB_STORICO[i,j][3]]
                lista_meteo_settimanale.append(meteo)
                table("Previsione", (id_previsioni_giornaliere[index_day], j, k, i, previsione[meteo], "giornaliero", acc, TAB_STORICO[i,j][3]), ("id", "data", "agenzia", "locazione", "meteo", "categoria", "accuratezza","id_storico"))
                index_day += 1

            if giro%7 == 0:
                bool_set = True
                meteo = int(np.sum(lista_meteo_settimanale)/len(lista_meteo_settimanale))
                TAB_PREVISIONE[id_previsioni_settimanali[index_set]] = [j, k, i, meteo, "settimanale", acc]
                lista_meteo_mensile.append(meteo)
                table("Previsione", (id_previsioni_settimanali[index_set], j, k, i, previsione[meteo], "settimanale", acc, "null"), ("id", "data", "agenzia", "locazione", "meteo", "categoria", "accuratezza", "id_storico"))
                index_set += 1

            if giro%30 == 0:
                bool_mes = True
                meteo = int(np.sum(lista_meteo_mensile)/len(lista_meteo_mensile))
                TAB_PREVISIONE[id_previsioni_mensili[index_mens]] =[j, k, i, meteo, "mensile", acc]       
                table("Previsione", (id_previsioni_mensili[index_mens], j, k, i, previsione[meteo], "mensile", acc, "null"), ("id", "data", "agenzia", "locazione", "meteo", "categoria", "accuratezza", "id_storico"))
                index_mens += 1

            FOR1_TAB_PREVISIONE[k] = TAB_AGENZIE_METEO[k]
            FOR2_TAB_PREVISIONE[i] = i

        giro += 1
        if bool_set:
            lista_meteo_settimanale = []
            bool_set = False
        if bool_mes:
            lista_meteo_mensile = []
            bool_mes = False

conn.close()
prova.do()
print("finito")