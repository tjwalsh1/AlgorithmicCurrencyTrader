from AlgorithmImports import *

class AdaptableLightBrownElephant(QCAlgorithm):

    def Initialize(self):
        self.SetCash(100000)  # Set your initial cash balance
        self.SetStartDate(2023, 10, 19)  # Set your desired start date
        self.SetEndDate(2023, 11, 11)  # Set your desired end date
        
        self.forex_pairs = ["USD/JPY","USD/CHF","USD/CAD","USD/GBP","USD/MXN","USD/EUR","EUR/CHF","EUR/USD","EUR/GBP","EUR/JPY","JPY/CHF","JPY/USD","JPY/GBP","JPY/EUR","GBP/USD","GBP/JPY","GBP/EUR","CHF/GBP","CHF/USD","CHF/JPY","CHF/EUR"]

        for pair in self.forex_pairs:
            self.AddForex(pair, Resolution.Daily)
        
        for pair in self.forex_pairs:
            self.Schedule.On(self.DateRules.EveryDay(pair), self.TimeRules.At(10, 0), self.Invest)

    def Invest(self):
        # Calculate average growth rates for the past week and month for each Forex pair
        forex_data = {}
        for pair in self.forex_pairs:
            # Use the History method to fetch historical data
            try:
                history = self.History(pair, timedelta(30), Resolution.Daily)
                
                if history is not None and len(history) > 0:
                    # Calculate average growth rates
                    week_growth = (history["close"].pct_change() + 1).prod() - 1
                    month_growth = (history["close"].pct_change(periods=30) + 1).prod() - 1
                    
                    # Store the growth rates
                    forex_data[pair] = {"week_growth": week_growth, "month_growth": month_growth}
            except Exception as e:
                self.Debug(f"Error fetching data for {pair}: {str(e)}")

        # Rank Forex pairs based on the weighted formula
        ranked_pairs = pd.DataFrame.from_dict(forex_data, orient='index')
        ranked_pairs["score"] = 0.7 * ranked_pairs["week_growth"] + 0.3 * ranked_pairs["month_growth"]
        ranked_pairs = ranked_pairs.sort_values(by="score", ascending=False)

        top_pair = None
        for pair in ranked_pairs.index:
            if not pair.endswith(ranked_pairs.index[0].split("/")[1]):
                top_pair = pair
                break

        if top_pair is not None:
        # Invest in the highest-ranked Forex pair
            top_pair = ranked_pairs.index[0]
            second_pair = ranked_pairs.index[1]
            third_pair = ranked_pairs.index[2]
            fourth_pair = ranked_pairs.index[3]
            self.SetHoldings(top_pair, 0.2)
            self.SetHoldings(second_pair, 0.15)
            self.SetHoldings(third_pair, 0.1)
            self.SetHoldings(fourth_pair,0.05)

    def OnData(self, data: Slice):
        pass
