import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from numpy import random

class OrderBook:
    def __init__(self):
        self.bids = deque()
        self.asks = deque()
        self.record = set()
# price, size, side, trader_id, timestamp, type

        
    def add_order(self, order: tuple[float, int, str, int, float, str]):
        price, size, side, trade_id, timestamp, type = order
        if trade_id in self.record:
            print("Duplicate order")
        else:
            self.record.add(trade_id)
        if side == "buy":
            self.bids.append((price, size, trade_id, timestamp, type))
        else:
            self.asks.append((price, size, trade_id, timestamp, type))
        # if type == 'market':
        #     self.execute_order()
    
    def execute_order(self):
        self.bids = deque(sorted(self.bids, key=lambda x: x[0], reverse=True))
        # self.bids = deque(sorted(self.bids, key = lambda x: x[3]))
        self.asks = deque(sorted(self.asks, key=lambda x: x[0]))
        # self.asks = deque(sorted(self.asks, key = lambda x: x[3]))
        bid = None
        ask = None
        # print(self.asks)
        if not self.bids or not self.asks:
            return
        best_bid = self.bids[0][0]
        best_ask = self.asks[0][0]
        while self.bids and self.asks and self.bids[0][0] >= self.asks[0][0]:
            if not bid:
                bid = self.bids.popleft()
            if not ask:
                ask = self.asks.popleft()
            # print(bid)
            # print(ask)
            best_bid = bid[0]
            best_ask = ask[0]
            if best_bid < best_ask:
                break
            if bid[1] > ask[1]:
                if bid[4] != 'limit':        
                    print(f"Trade {ask[1]} at {ask[0]}")
                    bid = (bid[0], bid[1] - ask[1], bid[2], bid[3], bid[4])
                    ask = None
                else:
                    self.bids.append(bid)
            elif bid[1] < ask[1]:
                if ask[4] != 'limit':
                    print(f"Trade {bid[1]} at {ask[0]}")
                    ask = (ask[0], ask[1] - bid[1], ask[2], ask[3], ask[4])
                    bid = None
                else:
                    self.asks.append(ask)
            else:
                print(f"Trade {bid[1]} at {ask[0]}")
                bid = None
                ask = None
        
    def cancel_order(self, order: tuple[float, int, str, int, float, str]):
        price, size, side, trade_id, timestamp, type = order
        if side == "buy":
            self.bids = deque([x for x in self.bids if x[2] != trade_id])
        else:
            self.asks = deque([x for x in self.asks if x[2] != trade_id])
    
    def report(self):
        bid = sorted([(x[0], x[1]) for x in self.bids], key = lambda x: x[0])
        ask = sorted([(x[0], x[1]) for x in self.asks], key = lambda x: x[0], reverse = True)
        bid_price = [x[0] for x in bid]
        bid_cummulative_size = [sum([x[1] for x in bid[:i + 1]]) for i in range(len(bid))]
        ask_price = [x[0] for x in ask]
        ask_cummulative_size = [sum([x[1] for x in ask[:i + 1]]) for i in range(len(ask))]
        print(f"Best bid: {max([x[0] for x in self.bids])}")
        print(f"Best ask: {min([x[0] for x in self.asks])}")
        print(f"Total bid size: {sum([x[1] for x in self.bids])}")
        print(f"Total ask size: {sum([x[1] for x in self.asks])}")
        print(f'spread: {max([x[0] for x in self.bids]) - min([x[0] for x in self.asks])}')
        plt.figure(figsize = (10, 5))
        plt.plot(bid_price, bid_cummulative_size, label = 'bids', color = 'r')
        plt.plot(ask_price, ask_cummulative_size, label = 'asks', color = 'b')
        plt.legend()
        plt.title('Call Auction Table')
        plt.xlabel('Price')
        plt.ylabel('Quantity')
        plt.show()

if __name__ == "__main__":
    Book = OrderBook()
    for i in range(10):
        Book.add_order((i, random.randint(i, 2 * i + 2), 'buy', i, i, 'market'))
        Book.add_order((11-i, random.randint(i + 1, 2 * i + 3), 'sell', 1000 + i, i, 'market'))
    Book.report()
    Book.execute_order()
    Book.report()
