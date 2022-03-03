import mysql.connector
import time
import socket

#Eintrag in welche Tabelle die Daten geschrieben werden. Muss bei jedem PI angepasst werden
table = "entries"

#Wenn das Produkt sich in Produktion befindet werde keine unnötigen Konsolenausgaben gemacht
production = True

#Diese Funktion wird zum Start ausgeführt
def main():
    if not production:
        if isConnectionOk():
            datenbankAnfrage()
            
    while True:
        if isConnectionOk():
            insertData(str(get_cpu_temp()), str(get_cpu_speed()))
        
        waitFor(5)

#Fragt alle Einträge der Datenbank ab (In Produktion nicht mehr notwendig). Für Monitoring und Kontrolle in developement
def datenbankAnfrage():
    try:
        mydb = mysql.connector.connect(
            host="34.159.157.247",
            user="root",
            passwd="OA6I2K76r7BzEIGC",
            database="monitoringDatenbank"
            )

        print(mydb)

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM " + table)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)   
    except:
        #Falls es einen Fehler gibt, wird dieser dokumentiert
        print("Datenbank Anfrage Error")
        
#Liest die CPU Temperatur des PIs aus
def get_cpu_temp():
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        tempFile.close()
        return round(float(cpu_temp)/1000, 1)

#Liest die CPU Geschwindigkeit des PIs aus
def get_cpu_speed():
        tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
        cpu_speed = tempFile.read()
        tempFile.close()
        return float(cpu_speed)/1000000
    
#Fügt die aktuellen Temperatur- und Geschwindigkeitswerte in die Datenbank ein
def insertData(temp, speed):
    try:
        mydb = mysql.connector.connect(
        host="34.159.157.247",
        user="root",
        passwd="OA6I2K76r7BzEIGC",
        database="monitoringDatenbank"
        )
        if not production:
            print(mydb)

        mycursor = mydb.cursor()
        if not production:
            print("Try insert: " + temp + " " + speed)
        mycursor.execute("INSERT INTO " + table + "(cpuTemp, cpuSpeed) VALUES (" + temp + ", " + speed + ");")
        if not production:
            print("insert complete")
            
        #Bestätigt/Sichert den Eintrag in der Datenbank
        mydb.commit()
        if not production:
            datenbankAnfrage()
    except:
        if not production:
            print("Daten insert Error")
    
#Überprüft die Verbindung zum Internet
def isConnectionOk():
    try:
        socket.create_connection(("www.google.com", 80))
        if not production:
            print('Gute Internetverbindung')
        return True
    except:
        if not production:
            print('Keine Internetverbindung')
        return False
    
#Sorgt für eine Wartezeit zwischen den einzelnen Einträgen in die Datenbank
def waitFor(timer):
    for x in range(timer):
        time.sleep(1)
        if not production:
            print(x)
        
main()
