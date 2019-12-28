

def create_tables(cursor,fileName):

    file = open(fileName)
    sql = file.read()
    cursor.executescript(sql)
    file.close()
