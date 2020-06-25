import openpyxl 
import csv
from imports import methods
import sqlite3
import strategies
import argparse
import sys

args = sys.argv

#symbole_list= ['AAPL','SPY','MSFT','NIO','AAL','AMZN']
symbole_list=['SPY']

nbr_shares =float(args[2])
interval=args[1] 

def sql_get_data(symbole):
    db = 'data2.db'
    methods.sqlite_connect(db)
    sql_conn = sqlite3.connect(db)
    c = sql_conn.cursor()
    c.execute("SELECT * FROM stock_data where symbole like '"+symbole+"' and interval like '"+interval+"' order by date_time asc")
    rows = c.fetchall()
    x = len(rows)
    for row in rows:
     print(row)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


connection = sqlite3.connect("data2.db")
connection.row_factory = dict_factory
cursor = connection.cursor()

###For a range of dates add "and date_time between '2020-06-18' and '2020-06-19' " to the SQL query ##########
###For specific date add "and date_time like '2020-06-24%' " to the SQL query ##########
for symbole in symbole_list:
 #cursor.execute("SELECT * FROM stock_data where symbole like '"+str(symbole)+"' and interval like '"+interval+"' and date_time between '2020-06-24' and '2020-06-24' order by date_time asc")
 cursor.execute("SELECT * FROM stock_data where symbole like '"+str(symbole)+"' and interval like '"+interval+"' and date_time like '2020-06-24%' order by date_time asc")
 #cursor.execute("SELECT * FROM stock_data where symbole like '"+str(symbole)+"' and interval like '"+interval+"'  order by date_time asc")
 results = cursor.fetchall()
 print('Results for : '+symbole,' Timeframe: ',interval)
 
 rsi_1= sma5_1 = sma8_1 = sma13_1 = 0
 position = position_rsi= position_mix = False     
 pl= pl_all = pl_all_sma = pl_all_rsi = pl_sma = pl_rsi= pl_rsi = pl_all_rsi = 0
 for i in range(len(results)):
  date_time= results[i]['date_time']
  open = results[i]['open']
  high = results[i]['high']
  low = results[i]['low']
  close = results[i]['close']
  volume = results[i]['volume']
  rsi14 = results[i]['rsi14']
  sma5 = results[i]['sma5']
  sma8 = results[i]['sma8']
  sma13 = results[i]['sma13']
  price_level = (float(high)+float(low))/2
  #price_level=close
  sma_result = strategies.SMA5_8_13(price_level,close,nbr_shares,date_time,sma5,sma8,sma13,sma5_1,sma8_1)
  rsi_result = strategies.RSI(price_level,close,nbr_shares,date_time,rsi14,rsi_1)
  
  if 'long' in sma_result:
   if position is False:
      print('[SMA] BUY: ',str(date_time), str(price_level))
      position = True
      avg_price = (float(price_level)* nbr_shares)
  elif 'short' in sma_result:
   if position is True:
      position = False
      sell_price = (float(price_level)* nbr_shares)
      pl_sma = (sell_price - avg_price)-(0.01*float(nbr_shares))
      print('[SMA] SELL: ',str(date_time), str(price_level),'P/L: ',((pl*nbr_shares-(0.01*float(nbr_shares)))))
      print(pl_all_sma)
  
  if 'long' in rsi_result:
   if position_rsi is False:
      position_rsi = True
      avg_price = (float(price_level)* nbr_shares)
  elif 'short' in rsi_result:
   if position_rsi is True:
      position_rsi = False
      sell_price = (float(price_level)* nbr_shares)
      pl_rsi = (float(sell_price) - float(avg_price))

  pl_all_sma+= pl_sma
  pl_all_rsi += pl_rsi
  sma5_1 = sma5
  sma8_1 = sma8
  rsi_1 = rsi14
 print('SMA Strategy P/L: ',pl_all_sma)


connection.close()
