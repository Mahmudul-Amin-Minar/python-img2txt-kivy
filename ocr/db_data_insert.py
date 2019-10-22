import json
 

# read file

def create_table():
    # create connection to the database file if there is no file then it will create one
    conn = sqlite3.connect("word.db")

    # create cursor for that connection
    curr = conn.cursor()

    # sql query to create a table named store if table is not exist
    curr.execute("CREATE TABLE IF NOT EXISTS wordlist (en_word TEXT, bn_word TEXT, en_syns TEXT, bn_syns TEXT)")

    # commit those changes
    conn.commit()
    conn.close()

create_table()

def insert_data(en, bn, en_syns, bn_syns):
    conn = sqlite3.connect("word.db")
    curr = conn.cursor()

    # using ? mark placeholder to insert data
    curr.execute("INSERT INTO wordlist VALUES (?, ?, ?, ?)", (en, bn, en_syns, bn_syns))
    conn.commit()
    conn.close()

with open('C://Users//username//Desktop//kivy app//ocr//BengaliDictionary.json', 'r', encoding='utf8') as myfile:
    data = myfile.read()

decoded_data = data.encode().decode('utf-8-sig')
# parse file
objs = json.loads(decoded_data)
print(len(objs))

for id_n, obj in enumerate(objs, start=1):
    print(id_n)
    insert_data(str(obj['en']), str(obj['bn']), str(obj['en_syns']), str(obj['bn_syns']))
    

