import matplotlib.pyplot as plt
import os
import pandas as pd
import weo


class DataLoader:

    @staticmethod
    def download(**kwargs) -> None:
        filename = kwargs.pop("filename")
        if os.path.exists(os.getcwd() + "/" + filename):
            return
        weo.download(filename=filename, **kwargs)

    @staticmethod
    def download_last(filename: str) -> None:
        last = weo.all_releases()[-1]
        DataLoader.download(year=last[0], release=last[1], filename=filename)

    @staticmethod
    def fillna(df: pd.DataFrame) -> None:
        df.fillna(value=0, inplace=True)

    def __init__(self) -> None:

        plt.figure(1)

        self.filename = "weo.csv"
        DataLoader.download_last(filename=self.filename)
        self.viewer = weo.WEO(self.filename)

        args = {"start_year": 1980, "end_year": 2026}
        self.gdp = self.viewer.gdp_usd(**args)  # in billions USD
        self.gdp_pc = self.viewer.gdp_pc_usd(**args)  # in USD
        self.ppp = self.viewer.gdp_ppp(**args)  # in billions
        DataLoader.fillna(self.gdp)
        DataLoader.fillna(self.gdp_pc)
        DataLoader.fillna(self.ppp)

        self.countries = list(self.viewer.countries()["Country"])
        self.gdp.index = self.countries
        self.gdp_pc.index = self.countries
        self.ppp.index = self.countries

        self.gdp = self.gdp.T
        self.gdp_pc = self.gdp_pc.T
        self.ppp = self.ppp.T

    def plot_gdp(self, *countries: str) -> None:
        countries = list(countries)
        self.gdp[countries].plot()
        plt.xlabel("Year")
        plt.ylabel("GDP in billions USD")

    def plot_gdp_pc(self, *countries: str) -> None:
        countries = list(countries)
        self.gdp_pc[countries].plot()
        plt.xlabel("Year")
        plt.ylabel("GDP per capita")

    def plot_ppp(self, *countries: str) -> None:
        countries = list(countries)
        self.ppp[countries].plot()
        plt.xlabel("Year")
        plt.ylabel("PPP in billions")
