from dataloader import DataLoader

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg


class GUI:
    # credit: https://github.com/PySimpleGUI/PySimpleGUI/blob/Master/DemoPrograms/Demo_Matplotlib.py
    def draw_figure(self, figure):
        if self.figure_canvas_agg is not None:
            self.figure_canvas_agg.get_tk_widget().forget()
        self.figure_canvas_agg = FigureCanvasTkAgg(figure, self.window["canvas"].TKCanvas)
        self.figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.figure_canvas_agg.draw()

    def add_row(self):
        self.rows += 1
        row = [[sg.Text("Country: "), sg.InputText(key=("country", self.rows))]]
        self.window.extend_layout(self.window["column"], row)

    def __init__(self):
        self.figure_canvas_agg = None
        self.data = DataLoader()
        self.column_layout = [[sg.Button("Add Country", key="add")],
                              [sg.Text("Country: "), sg.InputText(key=("country", 0))]]
        self.layout = [[sg.Canvas(key="canvas")],
                       [sg.Combo(["GDP", "GDP Per Capita", "PPP"], key="combo", default_value="GDP")],
                       [sg.Column(self.column_layout, key="column")],
                       [sg.Button("Generate Plot", key="gen"), sg.Exit()]]
        self.window = sg.Window("Plot GDP", self.layout, finalize=True, element_justification="center")
        self.rows = 0

    def gen(self, values):
        countries = []
        for i in range(self.rows + 1):
            country = values.get(("country", i))
            if country:
                countries.append(country)
        mode = values["combo"]
        if mode == "GDP":
            self.data.plot_gdp(*countries)
        elif mode == "GDP Per Capita":
            self.data.plot_gdp_pc(*countries)
        else:
            self.data.plot_ppp(*countries)
        self.draw_figure(plt.gcf())

    def run(self):
        self.window.finalize()
        while True:
            event, values = self.window.read()
            print(event, values)
            if event in (sg.WIN_CLOSED, "Exit"):
                break
            elif event == "add":
                self.add_row()
            elif event == "gen":
                self.gen(values)
        self.window.close()


gui = GUI()
gui.run()
