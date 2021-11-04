# uninow_trace
Kontaktverfolgung für Uninow-Checkin-Logs

Dieses Skript liest die Checkin-Logs von UniNow aus (erwartet werden sie in Form einer CSV-Datei (Excel: Speichern unter.../CSV (Trennzeichen-getrennt)) und findet alle Kontakte (= überlappende Checkin-Zeiträume) zwischen einer anzugebenden Matrikelnummer und allen anderen ab einem bestimmten Datum.

Es ist möglich, weitere Räume/Zeiträume anzugeben, zu denen die Index-Matrikelnummer anwesend war, aber nicht online eingecheckt hat.

Ausgabe ist zunächst eine Liste aller Kontaktereignisse, danach eine Liste der Kontakt-Matrikelnummern.

Die Liste wird anschließend in die Windows-Zwischenablage eingefügt.

Danach wird noch eine Liste ausgegeben, die neben den Matrikelnummern die Anzahl und Gesamtdauer der jeweiligen Kontakte enthält und zum Einfügen in z. B. eine Excel-Tabelle geeignet ist.
