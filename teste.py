import cx_Oracle

con = cx_Oracle.connect('dts/wdts01@192.168.2.7/WINT')
cursor = con.cursor()

sql2 =  f""" SELECT COUNT(*) 
                     FROM PCPREST 
                        WHERE NUMOS = 847
            """
result = cursor.execute(sql2).fetchone()


print(result[0])