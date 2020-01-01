

def create_tables(cursor,fileName):
    
    file = open(fileName)
    sql = file.readline()
    while sql:
        cursor.execute(sql)
        sql = file.readline()       
    
    file.close()
