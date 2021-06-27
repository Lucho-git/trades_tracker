import websocket, json
from trade_classes import Trade, FTrade, MFTrade 

bnbtrade = FTrade('bnbusdt', 390, 400, 410, 'ongoing', 'Midnight', '10', 'short', 10, 'isolation')
bnbtrade.trade_status()

ethtrade = FTrade('ethusdt', 2000, 1500, 2500, 'ongoing', 'Midnight', '10', 'short', 10, 'isolation')
ethtrade.trade_status()

btctrade = MFTrade('btcusdt', 30000, 25000,35000, 'ongoing', 'Yesterday', 20, 'long', 10, 'cross', [1,2,3,4,5], [10,20,30,20,20], 1, -1)
btctrade.trade_status()


active_trades = []
completed_trades = []
active_trades.extend((ethtrade, bnbtrade, btctrade))
glob = []
num_trades = len(active_trades)
glob.append(num_trades)
first_time = False
glob.append(first_time)

print('Trading:', glob[0], "Values")
print("First time:", glob[1])

def on_message(ws, message):
    #Get Message and chosen values from message
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    high = candle['h']
    low = candle['l']
    vol = candle['v']
    symbol = candle['s']

    #Forcing global variable due to google colab scoping issues
    #print(glob[0])
    if glob[1] == False:
      if glob[0] > 0:
        #print("reducing...from", glob[0], 'to', str(glob[0]-1))
        glob[0] -= 1
        glob[1] = True
    elif glob[1] == True:
        pass
    
    #Get trade data, related to current stream
    for t in active_trades:
      if t.pair.upper() == symbol:
        trade = t
      
    #Every 1 Minute, or first runthrough
    #print(glob[1])
    if is_candle_closed or glob[1]: 
      glob[1] = False
      print('\n______________________________')
      print(symbol,'Status:', trade.status)
      if trade.status is "ongoing":
        #trade_actions(json_message, trade)
        if (float(high) > float(trade.exitprice)):
          trade.status = "tookprofit"
        if (float(low) < float(trade.stoploss)):
          trade.status = "stoploss"
        if (float(high) > float(trade.highest)):
          trade.highest = float(high)
        if (float(low) < float(trade.lowest)):
          trade.lowest = float(low)

        if trade is '!Multiple Entry / Exits':
            print("Add Multi functionality here")

      if trade.status == "tookprofit":
        #trade_tookprofit(json_message, trade)
        print("Trade Complete")
        print("Entry Price :", trade.entryprice)
        print('Reached Take profit, Took profit at:', trade.exitprice)
        print("Lowest reached: ",trade.lowest,"/",trade.stoploss)

        up_percent = ((trade.exitprice - trade.entryprice)/trade.entryprice)*100
        #up_percent = up_percent * leverage
        print('Up ',up_percent,'%')
        ws.close()
      elif trade.status == "stoploss":
        #trade_stoploss(json_message, trade)
        print("Trade Complete")
        print("Entry Price :", trade.entryprice)
        print('Reached Stoploss, Exited at:', trade.stoploss)
        print("Highest reached: ",trade.highest,"/",trade.exitprice )
        down_percent = ((trade.entryprice - trade.stoploss)/trade.stoploss)*100
        #down_percent = down_percent * leverage
        print('- ',down_percent,'%')
        ws.close()
      else:
        #trade_ongoing(json_message, trade)
        print("Current price is: ", close)
        print("Highest: ", trade.highest)
        print("Entry: ", trade.entryprice)
        print("Lowest: ", trade.lowest)

        close = float(close)
        percentage = abs(close - trade.entryprice)  / trade.entryprice*100  
        #percentage = percentage * trade.leverage

        if close < float(trade.entryprice):
          #print('\033[91m' + "- ", percentage,"%" + '\033[0m')
          print("- ", percentage,"%")

        else:
          print("+ ", percentage,"%")

def on_close(ws):
    print("### closed ###")

def futures_market_order():
  print("Starting Trade Order...")
  interval = '1m'

  tradestring = ''
  tradelist = ''
  for t in active_trades:
    tradestring += '/' + t.pair + '@kline_' + interval
    tradelist += t.pair.upper() + ' | '
  print(tradestring)

  #cointradingpair, time interval and socket stream initialized here
  socket = f'wss://stream.binance.com:9443/ws{tradestring}'
  print(socket) #output socket just to be sure

  print("Tracking Trades...", tradelist)

  ws = websocket.WebSocketApp(socket, on_message = on_message, on_close = on_close)

  while active_trades:
    for t in active_trades:
      print(t.pair.upper(),'|', end='')
    print("Entering stream", glob[1], glob[0])
    ws.run_forever()
    removals = True
    while removals:
      removals = False
      for t in active_trades:
        if not t.status == 'ongoing':
          print('--------------------------')
          print(t.pair.upper(),'Status: ',t.status)
          print('[Removing] ', t.pair.upper())
          print('--------------------------')
          completed_trades.append(t)
          active_trades.remove(t)
          removals = True
   
  print("closed")
futures_market_order()
