import sqlite3

connection = sqlite3.connect("instance/site.db")
cursor = connection.cursor()

cursor.execute("ALTER TABLE product ADD COLUMN specification TEXT")

connection.commit()
connection.close()

print("Specification Column Added Successfully")