'''Script de Atualizações de Ordem de Serviço!

Python Version >= 3.7.3
Modeules Used = os, cx_Oracle

Funções Básicas:
1 - Consultar Ordens de Serviço OK
2 - Inserir contas a receber das ordens de serviço 
3 - Colocar as ordens de serviço em execução
4 - criar tabela de log
5 - Caso a ordem de serviço seja cancelada ou reaberta, excluir o contas a receber.

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
    sqlr2 = cursor.execute(sql2).rowcount
    return sqlr2
    
def insert_pcprest(codcli, prest, duplic, valor, dtvenc, codcob, dtemissao, codfilial,
                    status, codusur, dtvencorig, numtransvenda, dtsaida, codsupervisor, numos):
    sql3 = f"""
    INSERT INTO (CODCLI, PREST, DUPLIC, VALOR, DTVENC, CODCOB, DTEMISSAO, CODFILIAL,
	                STATUS, CODUSUR, DTVENCORIG, NUMTRANSVENDA, DTSAIDA, CODSUPERVISOR, NUMOS)
    VALUES ({codcli}, {prest}, {duplic}, {valor}, {dtvenc}, {codcob}, {dtemissao}, {codfilial},
            {status}, {codusur}, {dtvencorig}, {numtransvenda}, {dtsaida}, {codsupervisor}, {numos})
    """
    sqlr3 = cursor.execute(sql3)

def stores_transvenda():
    sql4 = "SELECT PROXNUMTRANSVENDA FROM PCCONSUM"
    sqlr4 = cursor.execute(sql4).fetchone() 
    for _ in sqlr4:
        numtrans = _
    return numtrans

def del_pcprest(numos):
    sql5 = f"delete from pcprest where nums = {numos}"

def modify_situation():
    pass

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
    status, codusur, dtvencorig, numtransvenda = os[8], os[9], os[10], os[11]
    dtsaida, codsupervisor, numos = os[12], os[13], os[14]
        
    value = verify_pcprest(numos)
    if value == 0:
        numtransvenda = stores_transvenda()        
        
        #DEBUG
        #print(codcli, prest, duplic, valor, dtvenc, codcob, dtemissao, codfilial,
        #            status, codusur, dtvencorig, numtransvenda, dtsaida, codsupervisor, numos)
    else:
        del_pcprest(numos)

con_orcl.close()


