'''Script de Atualizações de Ordem de Serviço!

Python Version >= 3.7.3
Modeules Used = os, cx_Oracle

Funções Básicas:

1 - Consultar OS's com Situaão 1 (Abertas) STATUS = OK 
2 - Inserir contas a receber de OS abertas. STATUS = OK 
3 - Colocar as ordens de serviço em execução após pagamento. STATUS =
4 - Caso a ordem de serviço seja cancelada ou reaberta, excluir o contas a receber. STATUS =
5 - criar tabela de log STATUS =

'''
import os
import time

try:
    import cx_Oracle as cxo
except:
    os.system('pip3 install cx_Oracle')

with open('ora.conf', 'r') as data:
    read = data.read().split('\n')
    list_data = []
    for x in read:
        list_data.append(x.split('='))

data = dict(list_data)  
host, db =  data['host'], data['string']
user, _pass = data['user'], data['pass'] 

con_orcl = cxo.connect(f"{user}/{_pass}@{host}/{db}")
con_orcl.autocommit = True
cursor = con_orcl.cursor()


def verify_pcprest(numos):
    sql2 =  f""" SELECT COUNT(*) 
                     FROM PCPREST 
                        WHERE NUMOS = {numos}
            """
    
    sqlr2 = cursor.execute(sql2).fetchone()
    return sqlr2[0]
    
def insert_pcprest(codcli, prest, duplic, valor, dtvenc, codcob, dtemissao, codfilial,
                    status, codusur, dtvencorig, numtransvenda, dtsaida, codsupervisor, numos):
    sql3 = f"""
    INSERT INTO PCPREST (CODCLI, PREST, DUPLIC, VALOR, DTVENC, CODCOB, DTEMISSAO, CODFILIAL,
	                STATUS, CODUSUR, DTVENCORIG, NUMTRANSVENDA, DTSAIDA, CODSUPERVISOR, NUMOS)
    VALUES ({codcli}, {prest}, {duplic}, {valor}, to_date('{dtvenc}', 'DD/MM/YYYY'), '{codcob}', 
            to_date('{dtemissao}', 'DD/MM/YYYY'), {codfilial}, '{status}', {codusur}, 
            to_date('{dtvencorig}', 'DD/MM/YYYY'), {numtransvenda}, to_date('{dtsaida}', 'DD/MM/YYYY'), 
            {codsupervisor}, {numos})
    """
    print(sql3)
    sqlr3 = cursor.execute(sql3)

def stores_transvenda():
    sql4 = "SELECT PROXNUMTRANSVENDA FROM PCCONSUM"
    sqlr4 = cursor.execute(sql4).fetchone()
    cursor.execute("UPDATE PCCONSUM SET PROXNUMTRANSVENDA = PROXNUMTRANSVENDA+1") 
    for _ in sqlr4:
        print(_)
        numtrans = _
    return numtrans

def del_pcprest(numos):
    sql5 = f"delete from pcprest where nums = {numos}"

def modify_situation(numos):
    sql6 = f"""SELECT COUNT(*) 
                FROM PCPREST 
                    WHERE NUMOS = {numos}
                    AND DTPAG IS NOT NULL"""
    sqlr6 = cursor.execute(sql6).fetchone()
    if sqlr6[0] > 0:
        cursor.execute(f"UPDATE PCORDEMSERVICO SET SITUACAO = 1 WHERE NUMOS = {numos}")

# Start Program
    # --Consulting open OS

sql1 =  """ SELECT  O.CODCLI, 
                    '1' PREST, 
                    (SELECT PROXNUMTRANSVENDA FROM PCCONSUM) DUPLIC, 
                    (SELECT SUM(PUNIT) FROM PCORDEMSERVICOI WHERE NUMOS = O.NUMOS) VALOR, 
                    TO_CHAR(SYSDATE, 'DD/MM/YYYY') DTVENC, 
                    'ORDS' CODCOB, 
                    TO_CHAR(SYSDATE, 'DD/MM/YYYY') DTEMISSAO, 
                    O.CODFILIAL,
                    'A' STATUS, 
                    O.CODRCA, 
                    TO_CHAR(SYSDATE, 'DD/MM/YYYY') DTVENCORIG, 
                    (SELECT PROXNUMTRANSVENDA FROM PCCONSUM) NUMTRANSVENDA, 
                    TO_CHAR(SYSDATE, 'DD/MM/YYYY') DTSAIDA, 
                    (SELECT CODSUPERVISOR FROM PCUSUARI WHERE CODUSUR = O.CODRCA) CODSUPERVISOR, 
                    O.NUMOS
            FROM PCORDEMSERVICO O
            WHERE O.SITUACAO = 1
            AND (SELECT SUM(PUNIT) 
		            FROM PCORDEMSERVICOI 
		            WHERE NUMOS = O.NUMOS) > 0
        """
result = cursor.execute(sql1).fetchall()

for os in result:
    codcli, prest, duplic, valor = os[0], os[1], os[2], os[3]
    dtvenc, codcob, dtemissao, codfilial = os[4], os[5], os[6], os[7]   
    status, codusur, dtvencorig = os[8], os[9], os[10],
    dtsaida, codsupervisor, numos = os[11], os[12], os[13]
        
    value = verify_pcprest(numos)
    if value == 0:
        numtransvenda = stores_transvenda()
        insert_pcprest(codcli, prest, duplic, valor, dtvenc, codcob, dtemissao, 
        codfilial, status, codusur, dtvencorig, numtransvenda, dtsaida, codsupervisor, numos)        
        
        #DEBUG
        #print(codcli, prest, duplic, valor, dtvenc, codcob, dtemissao, codfilial,
        #            status, codusur, dtvencorig, numtransvenda, dtsaida, codsupervisor, numos)
    else:
        del_pcprest(numos)


con_orcl.close()


