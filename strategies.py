def SMA5_8_13(price_level,close,nbr_shares,date_time,sma5,sma8,sma13,sma5_1,sma8_1):
  
  #print(price_level,nbr_shares,date_time,sma5,sma8,sma13,sma5_1,sma8_1)
  ############ SMA STRATEGY ##################
  if (float(sma5) > float(sma8) and float(sma5_1) < float(sma8_1) and float(sma5) > float(sma13) and float(sma13) < float(close)) :
  #if (float(sma5) > float(sma8) and float(sma5_1) < float(sma8_1) and float(sma5) > float(sma13)):
  #if (float(sma5) > float(sma8) and float(sma5_1) < float(sma8_1)  and float(sma13) < float(price_level)) :
   return 'long'
  elif ((float(sma5) < float(sma8) and float(sma5_1) > float(sma8_1) and float(sma5) > float(sma13))):
   return 'short'
  else:
   return 'none'


def RSI(price_level,close,nbr_shares,date_time,rsi,rsi_1):
   ############## RSI STRATEGY #################

  if float(rsi) <= 35 and float(rsi) > float(rsi_1):
     return 'long'
  elif float(rsi) >= 65 and float(rsi) < float(rsi_1):
     return 'short'
  else:
     return 'none'