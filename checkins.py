import csv
import datetime
from collections import defaultdict
import win32clipboard

def get_datum(prompt):
    while True:
        s = input(prompt).strip()
        if not s: return None
        try:
            datum = datetime.datetime.strptime(s, "%d.%m.%Y")
        except ValueError:
            print("Das scheint kein gültiges Datum zu sein... bitte nochmal versuchen!")
            continue
        break    
    return datum

def get_zeit(prompt):
    while True:
        s = input(prompt).strip()
        if not s: return None
        try:
            zeit = datetime.datetime.strptime(s, "%H:%M")
        except ValueError:
            print("Das scheint keine gültige Uhrzeit zu sein... bitte nochmal versuchen!")
            continue
        break    
    return zeit - datetime.datetime.strptime("00:00", "%H:%M")

# checkins-Datei lesen - in Excel als CSV-Datei abgespeichert im gleichen Ordner
# wie dieses Skript

with open("checkins.csv", newline="", encoding="cp1252") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    daten = list(reader)

räume = set(eintrag["room"] for eintrag in daten)

matr_index = input("Welche Matrikelnummer hat der Indexfall? ")

sd_index = get_datum("Wann war der positive Test bzw. Symptombeginn (TT.MM.JJJJ)? ")

suchdatum_index = sd_index - datetime.timedelta(days=2)
sd_text = datetime.datetime.strftime(suchdatum_index, "%d.%m.%Y")

# Alle Check-Ins der Indexperson seit zwei Tagen vor Test/Symptombeginn
checkins = []

print(f"Diese Einträge in der Datei seit dem {sd_text} habe ich gefunden:")
for eintrag in daten:
    if matr_index == eintrag["external_id"]:
        checkin = {}
        checkin["ein"] = datetime.datetime.strptime(eintrag["checked_in_at"], "%d.%m.%Y, %H:%M")
        if checkin["ein"] > suchdatum_index:
            checkin["raum"] = eintrag["room"]
            checkin["aus"] = datetime.datetime.strptime(eintrag["checked_out_at"], "%d.%m.%Y, %H:%M")
            checkins.append(checkin)

checkins.sort(key=lambda l: l["ein"])
print(f"Checkins für Matrikelnummer {matr_index}:")
for checkin in checkins:
    print("Check-in {} in Raum {} bis {} (Dauer: {})".format(checkin["ein"],
                                                             checkin["raum"],
                                                             checkin["aus"],
                                                             checkin["aus"] - checkin["ein"]))
while True:
    datum = get_datum("Gibt es weitere Checkins, die nicht erkannt wurden?\nWenn nein, ENTER drücken.\nWenn ja, wann (TT.MM.JJJJ)? ")
    if datum is None:
        break
    while True:
        raum = input("In welchem Raum? ").strip()
        if raum in räume:
            break
        print("Dieser Raum kommt in der Checkin-Liste nicht vor! Bitte Schreibweise überprüfen.")
    start = get_zeit("Von wann (HH:MM)? ")
    sdatum = datum + start
    ende = get_zeit("Bis wann (HH:MM)? ")
    edatum = datum + ende
    
    checkins.append({"ein": sdatum, "raum": raum, "aus": edatum})
    

# Überlappungen der Check-Ins aller anderen Einträge suchen
kontakte = defaultdict(list)
for checkin in checkins:
    for eintrag in daten:
        if eintrag["room"] == checkin["raum"] and eintrag["external_id"] != matr_index:
            kontakt_ein = datetime.datetime.strptime(eintrag["checked_in_at"], "%d.%m.%Y, %H:%M")
            kontakt_aus = datetime.datetime.strptime(eintrag["checked_out_at"], "%d.%m.%Y, %H:%M")
            if checkin["ein"] <= kontakt_aus and checkin["aus"] >= kontakt_ein:
                start_kontakt = max(checkin["ein"], kontakt_ein)
                end_kontakt = min(checkin["aus"], kontakt_aus)
                kontakte[eintrag["external_id"]].append([eintrag["room"], start_kontakt, end_kontakt])

for kontakt, details in kontakte.items():
    print(f"Kontakte mit {kontakt}:")
    for detail in details:
        print(f"  {detail[0]} von {detail[1]} bis {detail[2]} ({detail[2]-detail[1]})")

print(f"Liste aller Kontaktpersonen seit dem {sd_text}:")
for kontakt in kontakte:
    print(kontakt)

win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardText("\n".join(kontakte))
win32clipboard.CloseClipboard()
input("Fertig! Die Matrikelnummern der Kontaktpersonen befinden sich in der Zwischenablage.\nENTER zum Beenden.")


