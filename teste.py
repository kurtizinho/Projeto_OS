
import cx_Oracle

con = cx_Oracle.connect('dts/wdts01@192.168.2.7/WINT')
cursor = con.cursor()

sql = """SELECT O.NUMOS
                FROM PCORDEMSERVICO O
                WHERE O.SITUACAO = 3
                AND (SELECT SUM(PUNIT) 
                        FROM PCORDEMSERVICOI 
                        WHERE NUMOS = O.NUMOS) > 0
                AND (SELECT COUNT(*) FROM PCPREST WHERE NUMOS = O.NUMOS) <> 0
    """

cursor.execute(sql)

result = cursor.fetchall()

for x in result:
    print(x[0])

