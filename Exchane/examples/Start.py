import datetime
import json
import math
import time
from binance.client import Client
from binance.enums import *
from datetime import datetime
from BinanceKeys import BinanceKey1
api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
#load twitter instantiating code
client = Client(api_key, api_secret)
ETHBTC =0.0
BNBBTC = 0.0
BTCUSDT = 0.0

def run():
    print((0.001345542 % 0.02))
    return
    welcome_message = "\n\n---------------------------------------------------------\n\n"
    welcome_message += "Hello and Welcome to the Binance Arbitrage Crypto Trader Bot Python"
    welcome_message += "A quick 'run-through' will be performed to introduce you to the functionality of this bot\n"
    bot_start_time = str(datetime.now())
    welcome_message += "\nBot Start Time: {}\n\n\n".format(bot_start_time)
    print(welcome_message)
    info = client.get_account()
    exchange_data = Exchange_info()
    all_tickers = AllTickers()
    balance = client.get_asset_balance(asset='BTC')
    btc_balance = balance['free']
    trade_amt = btc_balance;
    symbols,ETHBTC,BNBBTC,BTCUSDT = (BuildSymbol(all_tickers))
    max, out_curr,out_curr_BTC_price,out_curr_rate_price,curr_rate_btc_price, out_rate_curr, trade_amt = run_alg(symbols,ETHBTC,BNBBTC,BTCUSDT,trade_amt)
    percentage = ((float(max)-float(trade_amt))/float(trade_amt))*100;
    print(max, out_curr,out_rate_curr,percentage,)
    CreateOrders(max, out_curr,out_curr_BTC_price,out_curr_rate_price,curr_rate_btc_price, out_rate_curr, trade_amt,percentage,exchange_data)
    print(max, out_curr,out_curr_BTC_price,out_curr_rate_price,curr_rate_btc_price, out_rate_curr, trade_amt,percentage)

    symbol_1 = out_curr+'BTC'
    symbol_2 = out_curr+out_rate_curr
    symbol_3 = out_rate_curr+'BTC'
#    fees_1 = client.get_trade_fee(symbol=symbol_1)
#    fees_2 = client.get_trade_fee(symbol=symbol_2)
#    fees_3 = client.get_trade_fee(symbol=symbol_3)




def CreateOrders(max, out_curr,out_curr_BTC_price,out_curr_rate_price,curr_rate_btc_price, out_rate_curr, trade_amt,percentage,exchange_data):


    if float(trade_amt) >= float(max) :
        print("No Arbitrage !")
        return
    else:
        symbol_1 = out_curr + "BTC"
        symbol_2 = out_curr + out_rate_curr
        symbol_3 = out_rate_curr + "BTC"
        trade_amt = float(trade_amt)-((float(trade_amt)*10)/100)
#     calculate order_1 amt
        print("Order 1")
        order_1_amt = float(trade_amt) / float(out_curr_BTC_price)
#        order_1_new_amt = (float(order_1_amt) - (float(order_1_amt) % float(exchange_data[symbol_1]["minQty"])))
        order_1_new_amt = 0.0
        while True:
            if float(order_1_amt)>float(order_1_new_amt+float(exchange_data[symbol_1]["minQty"])):
                order_1_new_amt = order_1_new_amt +float(exchange_data[symbol_1]["minQty"])
            else:
                break
        print("Buying ",symbol_1,order_1_new_amt)
        order = client.order_market_buy(symbol=symbol_1,quantity=order_1_new_amt)
#        data_log_to_file(order)
        time.sleep(3)
        balance = client.get_asset_balance(asset=out_curr)
        trade_amt = balance['free']
        print(trade_amt)
#     calculate order_2 amt
        print("Order 2")
        order_2_amt = float(trade_amt)*float(out_curr_rate_price)
        print(order_2_amt)
#        order_2_new_amt = (float(order_2_amt) - (float(order_2_amt) % float(exchange_data[symbol_2]["minQty"])))
        order_2_new_amt = 0.0
        while True:
            if float(order_2_amt) > float(order_2_new_amt + float(exchange_data[symbol_2]["minQty"])):
                order_2_new_amt = order_2_new_amt + float(exchange_data[symbol_2]["minQty"])
            else:
                break
        print("Selling ", symbol_2, order_2_new_amt)
        order = client.order_market_sell(symbol=symbol_2,quantity=order_2_amt)
        print(order)
#       data_log_to_file(order)
        time.sleep(3)
        balance = client.get_asset_balance(asset=out_rate_curr)
        trade_amt = balance['free']
        print(trade_amt)
#     calculate order_3 amt
        print("Order3")
        order_3_amt = float(trade_amt)*float(curr_rate_btc_price)
        print(order_3_amt)
#       order_3_new_amt = (float(order_3_amt) - (float(order_3_amt) % float(exchange_data[symbol_3]["minQty"])))
        order_3_new_amt = 0.0
        while True:
            if float(order_3_amt) > float((order_3_new_amt + float(exchange_data[symbol_3]["minQty"]))):
                order_3_new_amt = order_3_new_amt + float(exchange_data[symbol_3]["minQty"])
            else:
                break
        print("Selling ", symbol_3, order_3_new_amt)
        order = client.order_market_sell(symbol=symbol_3,quantity=order_3_amt)
#        data_log_to_file(order)
        time.sleep(3)
        balance = client.get_asset_balance(asset="BTC") #last balance -- result
        trade_amt = balance['free']
        print(trade_amt)

        print(" Created Orders ammount ")
        print(order_1_amt)
        print(order_2_amt)
        print(order_3_amt)


def Exchange_info():
    result = dict(dict())
    exch_data = client.get_exchange_info()
    data = exch_data["symbols"]
    for item_0 in data:
        symbol = item_0['symbol']
        for item_1 in item_0['filters']:
           for key_1,item_2 in item_1.items():
                if key_1 == "minQty":
                    result[symbol]={"minQty":item_2}
                if key_1 == "stepSize":
                    result[symbol]["stepSize"]=item_2
    return result




def run_alg(symbols,ETHBTC,BNBBTC,BTCUSDT,trade_amt):
    max = -9999999999999999;
    out_curr = ''
    for curr_id,curr_info in symbols.items():
        #print("Curr is :  " + curr_id)
        btcRate = curr_info["BTC"]

        for key in curr_info:
            if key == "BTC":
                continue
            if key==curr_id:
                continue
            if key == "USDT":
                continue

            output = 0

            if key=="BNB":
                curr_rate_btc_price = BNBBTC
            elif key=="ETH":
                curr_rate_btc_price = ETHBTC
            elif key=="USDT":
                curr_rate_btc_price = BTCUSDT

            output = ((float(trade_amt) / float(btcRate)) * float(curr_info[key])) *float(curr_rate_btc_price)
            if output>max:
                max = output;
                out_curr = curr_id
                out_rate_curr = key
                out_curr_price = curr_info[key]
                out_curr_BTC_price = btcRate
                out_curr_rate_price = curr_info[key]
           # print("         Rate Curr is :  " +key+"   Price is "+curr_info[key] )
           # print("         Output is " + str(output) )
    return max,out_curr,out_curr_BTC_price,out_curr_rate_price,curr_rate_btc_price,out_rate_curr,trade_amt

def BuildSymbol(all_tickers):
    output = dict(dict());
    for item in all_tickers:
        curr = item["symbol"].encode('ascii', 'ignore')
        price =item["price"].encode('ascii', 'ignore')
        if curr == "ETHBTC":
            ETHBTC = price
        elif curr == "BNBBTC":
            BNBBTC = price
        elif curr == "BTCUSDT":
            BTCUSDT = price
        currRate = '';
        if "BTC" in curr :
            curr = curr.replace("BTC","")
            currRate = "BTC"
        elif "ETH" in curr:
            curr = curr.replace("ETH","")
            currRate = "ETH"
        elif "USDT" in curr:
            curr = curr.replace("USDT", "")
            currRate = "USDT"
        elif "BNB" in curr:
            curr = curr.replace("BNB", "")
            currRate = "BNB"
        if output.has_key(curr):
            output[curr][currRate]= price
            #output[curr][currRate] =
        else:
            output[curr] = {currRate:price}
            #print(output)
#            output[curr].append(currRate)
 #           output[curr][currRate] = price

    return output,ETHBTC,BNBBTC,BTCUSDT

def AllTickers():
    return client.get_all_tickers()


def CreateSampleOrder():
    order = client.order_market_sell(
        symbol='ddereder',
        quantity=9999999999999999999999999)
    print(order)
def data_log_to_file(message):
    with open('myLog.txt', 'a+') as f:
        f.writelines(message)
if __name__ == "__main__":
         run()
       # CreateSampleOrder()

class OutNode:
  def __init__(self, Symbol, Curr,Output):
      self.Symbol = Symbol
      self.Curr = Curr
      self.Output = Output
  def PrintRow(self):
      print("Selected is " + self.Curr + " Rate Curr is : "+ self.Curr + " Output is : "+self.Output)
