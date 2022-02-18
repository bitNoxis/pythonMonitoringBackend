import mysql.connector

mydb = mysql.connector.connect(
    host="34.159.157.247",
    user="root",
    passwd="OA6I2K76r7BzEIGC",
    database="datenbank"
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM entries")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)