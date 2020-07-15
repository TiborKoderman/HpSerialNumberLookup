import pyodbc

conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\kodermant\Documents\Python serial lookup\Inventar-automated.accdb;')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Computers WHERE [PurchaseDate] IS NULL OR [WarrantyExpiration] IS NULL OR [ProductNumber] IS NULL;")


#
for row in cursor.fetchall():
    print(row)
#    SerialNumber = row.__getattribute__('Serial number')
    
    #...Put code here...#

#    cursor.execute('UPDATE Computers
#                    SET row.__getattribute__('PurchaseDate') = PurchaseDate,
#                        row.__getattribute__('WarrantyExpiration') = WarrantyExpiration)
#                        row.__getattribute__('ProductNumber') = ProductNumber
#                        row.__getattribute__('Serial number') = SerialNumber;')