import datetime
import json
import math
import time
from binance.client import Client
from binance.enums import *
from datetime import datetime
from BinanceKeys import BinanceKey1
from SendEmail import NotifyUsers

api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
#load twitter instantiating code
client = Client(api_key, api_secret, {"timeout": 20})
ETHBTC =0.0
BNBBTC = 0.0
BTCUSDT = 0.0
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True
def run():
    welcome_message = "\n\n---------------------------------------------------------\n\n"
    welcome_message += "Hello and Welcome to the Binance Arbitrage Crypto Trader Bot Python"
    welcome_message += "A quick 'run-through' will be performed to introduce you to the functionality of this bot\n"
    bot_start_time = str(datetime.now())
    welcome_message += "\nBot Start Time: {}\n\n\n".format(bot_start_time)
    print(welcome_message)
#    test = client.get_order_book(symbol="APPCBTC")
#    print(test["asks"][50][0])
#    print(test["asks"][0][0])
#    return
    info = client.get_account()
    count = 0
    while count<1:
        all_tickers = AllTickers()
        balance = client.get_asset_balance(asset='BTC')
        btc_balance = balance['free']
        trade_amt = btc_balance
        symbols,ETHBTC,BNBBTC,BTCUSDT = (BuildSymbol(all_tickers))
        run_alg(symbols,ETHBTC,BNBBTC,trade_amt)
        count = count +1
        time.sleep(10)

#    percentage = ((float(max)-float(trade_amt))/float(trade_amt))*100;
   # print(max, out_curr,out_rate_curr,percentage,)
    #CreateOrders(max, out_curr,out_curr_BTC_price,out_curr_rate_price,curr_rate_btc_price, out_rate_curr, trade_amt,percentage,exchange_data)
   # print(max, out_curr,out_curr_BTC_price,out_curr_rate_price,curr_rate_btc_price, out_rate_curr, trade_amt,percentage)

    ##symbol_1 = out_curr+'BTC'
    #symbol_2 = out_curr+out_rate_curr
   # symbol_3 = out_rate_curr+'BTC'
#    fees_1 = client.get_trade_fee(symbol=symbol_1)
#    fees_2 = client.get_trade_fee(symbol=symbol_2)
#    fees_3 = client.get_trade_fee(symbol=symbol_3)




def CreateOrders(trade_amt, symbol_1, symbol_2, symbol_3,price_1,price_2,price_3,exchange_data):
    #trade_amt = float(float(trade_amt)-(float(trade_amt)*0.05))
    #balance = client.get_asset_balance(asset="BTC")
    #trade_amt = balance['free']
    print trade_amt, symbol_1, symbol_2, symbol_3,price_1,price_2,price_3
    price_2_org =  price_2
    price_3_org = price_3
    start_btc = trade_amt
    #calculate order_1 amt
    print("Order 1")
    #test = client.get_order_book(symbol=symbol_1)
    #price_1 = float(test["bids"][0][0])
   # print(float(test["bids"][0][0]),price_1)
    #price_1 = float(price_1)
    precision = 8
    price_1 = '{:0.0{}f}'.format(float(price_1), precision)
    order_1_amt = float(trade_amt) / float(price_1)
    order_1_new_amt = (float(order_1_amt) - (float(order_1_amt) % float(exchange_data[symbol_1]["minQty"])))
    print("Buying ",symbol_1,order_1_new_amt," : Price : ",price_1)
    out_curr = str.replace(symbol_1, "BTC", "")
    order_1 = client.order_limit_buy(symbol=symbol_1,price=price_1,quantity=float(order_1_new_amt),timeInForce=TIME_IN_FORCE_GTC)
    while True:
        open_order_count = client.get_open_orders()
        if not open_order_count:
            print("Orders is Empty")
            break
        else:
            print("Not Empty...!")
        time.sleep(2)
        print("Order 1: Trying.... ")
    time.sleep(3)

    balance = client.get_asset_balance(asset=out_curr)
    print balance
    trade_amt = balance['free']
    print(trade_amt)
    while trade_amt==0:
        balance = client.get_asset_balance(asset=out_curr)
        trade_amt = balance['free']
    print(trade_amt)

#calculate order_2 amt
    print("Order 2")

    test = client.get_order_book(symbol=symbol_2)
    price_2 = float(test["bids"][0][0])
    price_2 = price_2 + (float(exchange_data[symbol_2]['tickSize'])*2)
    precision = 8

    while price_2 > price_2_org:
        test = client.get_order_book(symbol=symbol_2)
        price_2 = float(test["bids"][0][0])
        price_2 = price_2 + (float(exchange_data[symbol_2]['tickSize']) * 2)
        time.sleep(1)


    price_2 = '{:0.0{}f}'.format(float(price_2), precision)

    order_2_amt = float(trade_amt)/float(price_2)
    #order_2_amt = order_2_amt - (order_2_amt * .01)
    order_2_new_amt =(float(order_2_amt) - (float(order_2_amt) % float(exchange_data[symbol_2]["minQty"])))
    print("Buying ", symbol_2, order_2_new_amt)

    out_rate_curr = str.replace(str(symbol_2), out_curr, "")
    balance_before = client.get_asset_balance(asset=out_rate_curr)

    print(" Price ", symbol_2, price_2)
    order_2 = client.order_limit_buy(symbol=symbol_2,price=price_2,quantity=float(order_2_new_amt),timeInForce=TIME_IN_FORCE_GTC)
    time.sleep(2)
    while True:
        open_order_count = client.get_open_orders()
        if not open_order_count:
            print("Orders is Empty")
            break
        else:
            print("Not Empty...!")
        time.sleep(2)
        print("Order 2: Trying.... ")
    time.sleep(2)
    balance = client.get_asset_balance(asset=out_rate_curr)
    trade_amt = balance['free']

#     calculate order_3 amt
    print("Order3")
    order_3_amt = trade_amt
    order_3_new_amt = (float(order_3_amt) - (float(order_3_amt) % float(exchange_data[symbol_3]["minQty"])))
    print("Selling ", symbol_3, order_3_new_amt)
    #balance_before = client.get_asset_balance(asset="BTC")

    test = client.get_order_book(symbol=symbol_3)
   # print(float(test["bids"][0][0]),price_3)
    price_3 = float(test['bids'][0][0])+(float(exchange_data[symbol_3]['tickSize'])*2)

    while price_3 < price_3_org:
        test = client.get_order_book(symbol=symbol_3)
        price_3 = float(test["bids"][0][0])
        price_3 = price_3 + (float(exchange_data[symbol_3]['tickSize']) * 2)
        time.sleep(1)
    #price_3 = float(test["bids"][0][0])
    #price_3 = float(price_3)
    precision = 8
    price_3 = '{:0.0{}f}'.format(float(price_3), precision)
    print(" Price ",symbol_3,price_3)
    order_3 = client.order_limit_sell(symbol=symbol_3,price=price_3,quantity=float(order_3_new_amt),timeInForce=TIME_IN_FORCE_GTC)
    while True:
        open_order_count = client.get_open_orders()
        if not open_order_count:
            print("Orders is Empty")
            break
        else:
            print("Not Empty...!")
        time.sleep(5)
        print("Order 3: Trying.... ")
    balance = client.get_asset_balance(asset="BTC") #last balance -- result
    print("Finished at: ",str(datetime.now()))
    print("Ending BTC Ammoount : ", balance["free"])
    NotifyUsers("Starting BTC : "+str(start_btc)+ " Ending BTC ammount : "+str(balance["free"]))

    ##Printing log of created orders

    ##Sending emails of created orders



def Exchange_info():
    result = dict(dict())
    exch_data = client.get_exchange_info()
    data = exch_data["symbols"]
    for item_0 in data:
        symbol = item_0['symbol']
        for item_1 in item_0['filters']:
           for key_1,item_2 in item_1.items():
                if key_1 == "tickSize":
                    result[symbol]={"tickSize":item_2}
                if key_1 == "stepSize":
                    result[symbol]["stepSize"]=item_2
                if key_1 == "minQty":
                    result[symbol]["minQty"] = item_2
    return result

def Calc_Fee(x):
    return float(x - ((x * 0.1) / 100))
def Get_Fee(x):
    return ((x * 0.1) / 100)
def New_Calc(trade_amt,symbols,exchange_data):
    tickers = client.get_orderbook_tickers()
    amt_1=0
    amt_2=0
    amt_3 = 0
    ethPrice = 0
    bnbPrice = 0
    count = 0
    for item in tickers:
        if count == 2:
            break
        if item['symbol'] == "ETHBTC":
            count = count + 1
            ethPrice = (float(item['bidPrice']))
            x1 = ((float(trade_amt) / float(ethPrice)))

        if item['symbol'] == "BNBBTC":
            bnbPrice = (float(item['bidPrice']))
            count = count + 1
            x2 = (float(trade_amt) / float(bnbPrice))

    Arb_List_ETH = []
    Arb_List_BNB = []
    z1=0
    z2=0
    out_amt=0
    out_base = ''
    out_crrn_1 = ''
    out_crrn_2 = ''
    out_perc = 0
    for item in tickers:
        curr = item['symbol']
        if float(item["askPrice"]) ==0.0:
            continue
        if "BTC" in curr:
            continue
        if "USDT" in curr:
            continue
        if "HOT" in curr:
            continue
        if "ETH" in curr:
            continue
            price2 = float(item["bidPrice"])
            y1 = (float(x1) / float(price2))
            symbol2 = item["symbol"]
            curr2 = str.replace(str(symbol2),"ETH","")
            symbol3 = curr2 + "BTC"
            for item2 in tickers:
                if item2['symbol'] == symbol3:
                    price3 = float(item2["bidPrice"])
                    z1= float(y1)*float(price3)
                    temp_perc = ((z1 - trade_amt) / trade_amt) * 100
                    if float(temp_perc) > 0 and  z1> out_amt:
                        out_amt = z1
                        out_base = "ETHBTC"
                        out_crrn_1 = symbol2
                        out_crrn_2 = symbol3
                        out_perc = temp_perc
                        price_1 = ethPrice
                        price_2 = price2
                        price_3 = price3
                        amt_1 = x1
                        amt_2 = y1
                        amt_3 = z1
                    break
        elif "BNB" in curr:
            price2 = float(item["bidPrice"])
            y2 = (float(x2) / float(price2))
            symbol2_ = item["symbol"]
            curr2_ = str.replace(str(symbol2_), "BNB", "")
            symbol3_ = curr2_ + "BTC"
            for item2_ in tickers:
                if item2_['symbol'] == symbol3_:
                    price3 = float(item2_["bidPrice"])
                    z2 = float(y2) * float(price3)
                    temp_perc = ((z2 - trade_amt) / trade_amt) * 100
                    if float(temp_perc) > 0 and  z2> out_amt  :
                        out_amt = z2
                        out_base = "BNBBTC"
                        out_crrn_1 = symbol2_
                        out_crrn_2 = symbol3_
                        out_perc = float(((z2 - trade_amt) / trade_amt) * 100)
                        price_1 = bnbPrice
                        price_2 = price2
                        price_3 = price3
                        amt_1 = x2
                        amt_2 = y2
                        amt_3 = z2
                    break
    return out_base,out_crrn_1,out_crrn_2,out_amt,out_perc,amt_1,amt_2,amt_3

def Check2(out_base,out_crrn_1,out_crrn_2,exchange_data,trade_amt):
    temp_amt = float(trade_amt)
    trade_amt = float(trade_amt)
    symbol_1 = client.get_order_book(symbol=out_base)
    symbol_2 = client.get_order_book(symbol=out_crrn_1)
    symbol_3 = client.get_order_book(symbol=out_crrn_2)
    #price_1 = float(symbol_1['asks'][0][0])
    #price_1 = (float(symbol_1['bids'][0][0])+float(symbol_1['asks'][0][0]))/2
    price_1 = float(symbol_1['bids'][0][0]) +(float(exchange_data[out_base]['tickSize']) *10)
    #price_1 = price_1 - (float(price_1) % float(exchange_data[out_base]['tickSize']))
    print "Before : ",trade_amt
    trade_amt = prepare_trade_amt(float(trade_amt/price_1),out_base,exchange_data)
    price_2 = float(symbol_2['bids'][0][0])
    price_2 = price_2+ (float(exchange_data[out_crrn_1]['tickSize'])*10)
    #price_2 = (float(symbol_2['bids'][0][0]) + float(symbol_2['asks'][0][0])) / 2
    #price_2 = price_2 - (float(price_2) % float(exchange_data[out_crrn_1]['tickSize']))
    trade_amt = prepare_trade_amt(float(trade_amt/price_2),out_crrn_1,exchange_data)
   # price_3 = (float(symbol_3['bids'][0][0]) + float(symbol_3['asks'][0][0])) / 2
   # print price_3
    price_3 = float(symbol_3['bids'][0][0])- (float(exchange_data[out_crrn_2]['tickSize'])*2)
    #print price_3
    #price_3 = price_3 - (float(price_3) % float(exchange_data[out_crrn_2]['tickSize']))
    trade_amt = prepare_trade_amt(float(trade_amt*price_3),out_crrn_2,exchange_data,False)
    print "After : ",trade_amt
    perc =(((trade_amt-temp_amt)/temp_amt)*100)
    return price_1,price_2,price_3,perc

def prepare_trade_amt(amount,symbol,exchange_data,flag=True):
    if flag:
        amount = (float(amount) - (float(amount) % float(exchange_data[symbol]["minQty"])))
    amount = Calc_Fee(amount)
    return amount

def Calc_Max(rate,trade_amt, symbols,flag):
    print(client.get_orderbook_tickers())
    return
    x = float(trade_amt) /float(rate)
    #x = float(x)-float(x*0.0001)
    max = -9999999999999999;
    out_curr = ''

    for curr_id,curr_info in symbols.items():
        if curr_id == "BTC":
            continue
        if curr_id == "USDT":
            continue
        if curr_id == "ETH":
            continue
        if curr_id == "BNB":
            continue
        if curr_id == "HOT":
            continue
        if curr_id == "QSP":
            continue

        if curr_info.has_key(flag):
            symbol_1 =curr_id+flag
            temp_1 = client.get_order_book(symbol=symbol_1)
            y = float(x)/float(temp_1["bids"][0][0])
            #y = float(y) - float(y * 0.0001)
            symbol_2 = curr_id+"BTC"
            temp_1 = client.get_order_book(symbol=symbol_2)
            out= float(y)*float(temp_1["asks"][0][0])
            #out = float(out) - float(out * 0.0001)
            if out>max:
                max = out
                out_curr=curr_id
                out_curr_price=curr_info[flag]
                curr_rate_btc_price = float(curr_info["BTC"])
    return out_curr,max,out_curr_price,curr_rate_btc_price


def run_alg(symbols,ETHBTC,BNBBTC,trade_amt):
    out_amt = 0
    balance = client.get_asset_balance(asset="BTC")
    trade_amt = balance["free"]
    count = 1
    while True:
        print "Try #",count
        exchange_data = Exchange_info()
        out_base, out_crrn_1, out_crrn_2, out_amt, out_perc,amt_1,amt_2,amt_3 =\
            New_Calc(float(trade_amt),symbols,exchange_data)
    #print "Percentag : ",out_perc
        if is_empty(out_base):
            count = count + 1
            continue
        trade_amt = balance["free"]
        price_1, price_2, price_3, out_perc = Check2(out_base, out_crrn_1, out_crrn_2, exchange_data, trade_amt)
        out_curr = out_base
        out_curr_btc_rate = ETHBTC
        out = out_amt
        symbol_1 = out_base
        symbol_2 = out_crrn_1
        symbol_3 = out_crrn_2
       ## print trade_amt,out_amt
       # print out_base, out_crrn_1, out_crrn_2, out_perc
       # print price_1, price_2, price_3,amt_1,amt_2,amt_3
        if out_perc > 0.2:
            print " Arbitrage.",out_perc,symbol_1, symbol_2, symbol_3
            try:
                CreateOrders(trade_amt, symbol_1, symbol_2, symbol_3, price_1, price_2, price_3, exchange_data)
            except:
                NotifyUsers("Except, Arbitrage Error ! Please check !!!!! ")
            else:
                NotifyUsers("Else, Arbitrage Error ! Please check !!!!! ")
            break
        #time.sleep(5)
        count=count+1

# usdt_btc_cal = Calc_Max(ETHBTC, trade_amt, symbols,"USDT")



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
        currRate = ''
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

def data_log_to_file(message):
    with open('myLog.txt', 'a+') as f:
        f.write(message)
        f.write("\n")
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
