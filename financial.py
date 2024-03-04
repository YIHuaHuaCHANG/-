import pandas as pd
import threading
import tkinter as tk
import time
from datetime import datetime
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class cryberTicker:
    def __init__(self, coins=['ethereum']):
        self.coins = coins
        self.cg = CoinGeckoAPI()
        self.timestamps = []
        self.usd_values = []
        self.pause_flag = False
        self.root = tk.Tk()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.pause_button = tk.Button(self.root, text="stop", command=self.pause_execution)
        self.pause_button.pack(side=tk.BOTTOM)

    def get_data(self, coin):
        coin_price = self.cg.get_price(ids=coin, vs_currencies='usd', include_market_cap='true',
                                       include_24hr_vol='true', include_24hr_change='true',
                                       include_last_updated_at='true')[coin]
        coin_price['coin'] = coin
        coin_price['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return coin_price

    def main(self):
        while True:
            if not self.pause_flag:
                for coin in self.coins:
                    coin_price = self.get_data(coin)
                    self.timestamps.append(coin_price["timestamp"])
                    self.usd_values.append(coin_price["usd"])
                    print(self.timestamps, self.usd_values)
                self.update_plot()
            time.sleep(10)

    def update_plot(self):
        self.ax.clear()
        for i, coin in enumerate(self.coins):
            self.ax.plot(self.timestamps, self.usd_values, label=f'{coin} USD Price')
        self.ax.set_xlabel('Timestamp')
        self.ax.set_ylabel('USD')
        self.ax.set_title('Cryptocurrency Prices')
        self.ax.tick_params(axis='x', rotation=45, labelsize=8)
        self.ax.legend()
        self.canvas.draw()
        if len(self.timestamps) > 40:
            self.timestamps.pop(0)
            self.usd_values.pop(0)
            
    def pause_execution(self):
        if self.pause_button.cget("text") == "Stop":
            self.pause_flag = True
            self.pause_button.config(text="Run")
        else:
            self.pause_flag = False
            self.pause_button.config(text="Stop")


if __name__ == '__main__':
    tracker = cryberTicker()
    thread = threading.Thread(target=tracker.main)
    thread.start()
    tracker.root.mainloop()