#!/bin/python3

'''Script de Atualizações de Ordem de Serviço!

Python Version >= 3.7.3
Modules Used = os, cx_Oracle, time

'''
import os
from time import sleep

try:
    import cx_Oracle as cxo
except:
    os.system('pip3 install cx_Oracle')
    import cx_Oracle as cxo

with open('/opt/Projeto_OS/software/ora.conf', 'r') as data:
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
                    status, codusur, dtvencorig, numtransvenda, dtsaida, codsupervisor, numos, dtfecha):
    sql3 = f"""
    INSERT INTO PCPREST (CODCLI, PREST, DUPLIC, VALOR, DTVENC, CODCOB, DTEMISSAO, CODFILIAL,
	                STATUS, CODUSUR, DTVENCORIG, NUMTRANSVENDA, DTSAIDA, CODSUPERVISOR, NUMOS, DTFECHA)
    VALUES ({codcli}, {prest}, {duplic}, {valor}, to_date('{dtvenc}', 'DD/MM/YYYY'), '{codcob}', 
            to_date('{dtemissao}', 'DD/MM/YYYY'), {codfilial}, '{status}', {codusur}, 
            to_date('{dtvencorig}', 'DD/MM/YYYY'), {numtransvenda}, to_date('{dtsaida}', 'DD/MM/YYYY'), 
            {codsupervisor}, {numos}, to_date('{dtfecha}', 'DD/MM/YYYY'))
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
    sql5 = f"delete from pcprest where numos = {numos}"
    sqlr5 = cursor.execute(sql5)

def modify_situation(numos):
    sql6 = f"""SELECT COUNT(*) 
                FROM PCPREST 
                    WHERE NUMOS = {numos}
                    AND DTPAG IS NOT NULL"""
    sqlr6 = cursor.execute(sql6).fetchone()
    if sqlr6[0] > 0:
        cursor.execute(f"UPDATE PCORDEMSERVICO SET SITUACAO = 2 WHERE NUMOS = {numos}")
        #print(f"OS {numos} foi colocada em execução") #DEBUG

def update_pcprest(numos, valor):
    sql8 = f"UPDATE PCPREST SET VALOR = {valor} where numos = {numos}"
    sqlr8 = cursor.execute(sql8).fetchall()

# Start Program
    # --Consulting open OS
        # Looping iniciado com a função sleep com 15 segundos ao final do Looping

while 0 == 0:
    
    # Primeira consulta para buscar os dados para inserção na PCPREST.

    sql1 =  """ SELECT  O.CODCLI, 
                        '1' PREST, 
                        (SELECT PROXNUMTRANSVENDA FROM PCCONSUM) DUPLIC, 
                        (SELECT SUM(QTDE*PUNIT) FROM PCORDEMSERVICOI WHERE NUMOS = O.NUMOS) VALOR, 
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
                        O.NUMOS,
                        TO_CHAR(SYSDATE, 'DD/MM/YYYY') DTFECHA
                FROM PCORDEMSERVICO O
                WHERE O.SITUACAO = 1
                AND (SELECT SUM(QTDE*PUNIT) 
                        FROM PCORDEMSERVICOI 
                        WHERE NUMOS = O.NUMOS) > 0
            """
    result = cursor.execute(sql1).fetchall()

    # Segunda consulta para buscar OS cancelada.

    sql7 = """ SELECT O.NUMOS
                FROM PCORDEMSERVICO O
                WHERE O.SITUACAO = 3
                AND (SELECT SUM(QTDE*PUNIT) 
                        FROM PCORDEMSERVICOI 
                        WHERE NUMOS = O.NUMOS) > 0
                AND (SELECT COUNT(*) FROM PCPREST WHERE NUMOS = O.NUMOS) <> 0
            """
    sqlr7 = cursor.execute(sql7).fetchall()

    # Terceira consulta para buscar OS com valor diferente da PCPREST

    sql8 =  """SELECT P.NUMOS, 
                     (SELECT SUM(QTDE*PUNIT) FROM PCORDEMSERVICOI WHERE NUMOS = P.NUMOS) VALOR
                     FROM PCPREST P
                        WHERE P.VALOR <> (SELECT SUM(I.QTDE*I.PUNIT) 
                                            FROM PCORDEMSERVICO O, 
                                                PCORDEMSERVICOI I 
                                            WHERE I.NUMOS = P.NUMOS
                                            AND O.SITUACAO = 1)
            """    
    sqlr8 = cursor.execute(sql8).fetchall()
    
    # Laço for para desempacotar as variáveis

    for os in result:
        codcli, prest, duplic, valor = os[0], os[1], os[2], os[3]
        dtvenc, codcob, dtemissao, codfilial = os[4], os[5], os[6], os[7]   
        status, codusur, dtvencorig = os[8], os[9], os[10],
        dtsaida, codsupervisor, numos, dtfecha = os[12], os[13], os[14], os[15]

        #Verificando se o titulo já existe:    
        
        value = verify_pcprest(numos)
        
        #Caso o titulo não exista irá executar a inserção: 
        
        if value == 0:
            #Função para armazenar o NUMTRANSVENDA da PCCONSUM e somar +1
            numtransvenda = stores_transvenda()
            
            #Inserindo titulo

            insert_pcprest(codcli, prest, duplic, valor, dtvenc, codcob, dtemissao, 
            codfilial, status, codusur, dtvencorig, numtransvenda, dtsaida, codsupervisor, numos, dtfecha) 

        #Modificando a situação dos titulos pagos     
        modify_situation(numos)       
        
    #Deletando titulos onde a Situação da OS esteja como cancelada        
    for _os in sqlr7:
        os = _os[0]
        os_del = verify_pcprest(os)
        if os_del >0:
            del_pcprest(os)

    #Atualizando valores dos titulos que estejam diferente entre PCPREST e PCORDEMSERVICOI    
    for _os in sqlr8:
        os = _os[0]
        valor = _os[1]
        update_pcprest(os, valor)    

    #con_orcl.close()
    #print('Aguardando 15 segundos para iniciar novamente.')
    sleep(15)

