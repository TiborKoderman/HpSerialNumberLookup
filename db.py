import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Inventar-automated.accdb')
cursor = conn.cursor()
cursor.execute('SELECT * FROM Computers')


for row in cursor.fetchall():
    print(row)