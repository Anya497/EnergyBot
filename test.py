import sqlite3


con = sqlite3.connect("energy_bot.db")
cur = con.cursor()
cur.execute(f'''SELECT COUNT(*) FROM users''')
num = cur.fetchall()
print(num[0][0])
con.close()