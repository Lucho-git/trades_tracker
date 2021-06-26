import websocket, json
from trade_classes import Trade, FTrade, MFTrade 

bnbtrade = FTrade('bnbusdt', 390, 400, 410, 'ongoing', 'Midnight', '10', 'short', 10, 'isolation')
bnbtrade.trade_status()

ethtrade = FTrade('ethusdt', 2000, 1500, 2500, 'ongoing', 'Midnight', '10', 'short', 10, 'isolation')
ethtrade.trade_status()

btctrade = MFTrade('btcusdt', 30000, 25000,35000, 'ongoing', 'Yesterday', 20, 'long', 10, 'cross', [1,2,3,4,5], [10,20,30,20,20], 1, -1)
btctrade.trade_status()
