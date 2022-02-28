import mysql.connector
import time
import socket

table = "entries"

def main():
    if isConnectionOk():
        datenbankAnfrage()
    while True:
        if isConnectionOk():
            insertData(str(get_cpu_temp()), str(get_cpu_speed()))
       
        waitFor(30)

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
        print("Datenbank Anfrage Error")
def get_cpu_temp():
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        tempFile.close()
        return round(float(cpu_temp)/1000, 1)

def get_cpu_speed():
        tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
        cpu_speed = tempFile.read()
        tempFile.close()
        return float(cpu_speed)/1000000
   
def insertData(temp, speed):
    try:
        mydb = mysql.connector.connect(
        host="34.159.157.247",
        user="root",
        passwd="OA6I2K76r7BzEIGC",
        database="monitoringDatenbank"
        )

        print(mydb)

        mycursor = mydb.cursor()
        print("Try insert: " + temp + " " + speed)
        mycursor.execute("INSERT INTO " + table + "(cpuTemp, cpuSpeed) VALUES (" + temp + ", " + speed + ");")
        print("insert complete")
        mydb.commit()
        datenbankAnfrage()
    except:
        print("Daten insert Error")
       
def isConnectionOk():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except:
        print('Keine Internetverbindung')
        return False
   
def waitFor(timer):
    for x in range(timer):
        time.sleep(1)
        print(x)
       
main()

#Sinnvoller Kommentar
