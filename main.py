from flask import Flask, render_template, request
import plotly
import pyodbc as pypyodbc
import plotly.graph_objects as go
import numpy as np
import json
import pandas as pd

app = Flask(__name__)
conn = pypyodbc.connect('Driver=ODBC Driver 13 for SQL Server;'
                        'Server=localhost\SQLEXPRESS;'
                        'Database=TestDB;'
                        'username=boyd;'
                        'password=P@ssw0rd;'
                        'Trusted_Connection=yes;')


@app.route('/')
def hello_world():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Person')
    rows = cursor.fetchall()
    return render_template("index.html", datas=rows)


@app.route('/simpleGraph1')
def generate_graph1():
    return render_template("json_graph.html")


def get_data():
    # Create sample data
    n = 201
    x = np.linspace(0, 2.0 * np.pi, n)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = y1 + y2

    trace1 = go.Scatter(
        x=x,
        y=y1,
        name="sine curve",
        line=dict(
            color=("red"),
            width=4,
            dash='dash'
        )
    )

    trace2 = go.Scatter(
        x=x,
        y=y2,
        name="cosine curve",
        line=dict(
            color=("green"),
            width=4,
            dash='dot'  # dot, dashdot
        )
    )

    trace3 = go.Scatter(
        x=x,
        y=y3,
        name="sine + cosine curve",
        line=dict(
            color=("blue"),
            width=4,
            dash="dashdot"
        )
    )

    layout = dict(
        xaxis=dict(title="Angle in Radian"),
        yaxis=dict(title="Magnitude")
    )

    # Pack the data
    data = [trace1, trace2, trace3]

    # Create a figure
    fig = dict(data=data, layout=layout)
    # Plot
    # url_plot = ply.plot(fig)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/simpleGraph2')
def graph2():
    data = get_data()
    return render_template("line_graph.html", plot=data)


def create_plot(feature):
    if feature == 'Bar':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y})
        data = [
            go.Bar(
                x=df['x'],
                y=df['y']
            )
        ]
    else:
        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x=random_x,
            y=random_y,
            mode='markers'
        )]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON = create_plot(feature)

    return graphJSON


@app.route('/simpleGraph3')
def go_generate_graph3():
    bar = create_plot('Bar')
    return render_template("simple_plot.html", plot=bar)


def get_data_from_database():
    cursor = conn.cursor()
    cursor.execute('SELECT ContinentName, GDP, LifeExp, Size FROM GDPLifeExp')
    rows = cursor.fetchall()

    africa_GDP = []
    africa_LifeExp = []
    africa_Size = []
    americas_GDP = []
    americas_LifeExp = []
    americas_Size = []
    asia_GDP = []
    asia_LifeExp = []
    asia_Size = []
    europe_GDP = []
    europe_LifeExp = []
    europe_Size = []

    for item in rows:
        if item[0] == "Africa":
            africa_GDP.append(item[1])
            africa_LifeExp.append(item[2])
            africa_Size.append(item[3])
        elif item[0] == "Americas":
            americas_GDP.append(item[1])
            americas_LifeExp.append(item[2])
            americas_Size.append(item[3])
        elif item[0] == "Asia":
            asia_GDP.append(item[1])
            asia_LifeExp.append(item[2])
            asia_Size.append(item[3])
        elif item[0] == "Europe":
            europe_GDP.append(item[1])
            europe_LifeExp.append(item[2])
            europe_Size.append(item[3])

    trace1 = {
        "meta": {"columnNames": {
            "x": "Africa, x",
            "y": "Africa, y"
        }},
        "mode": "markers",
        "name": "Africa",
        "type": "scatter",
        "x": africa_GDP,
        "y": africa_LifeExp,
        "marker": {
            "line": {"width": 2},
            "meta": {"columnNames": {"size": "Africa, size"}},
            "symbol": "circle",
            "sizeref": 0.85,
            "size": africa_Size,
            "sizemode": "diameter"
        }
    }
    trace2 = {
        "meta": {"columnNames": {
            "x": "Americas, x",
            "y": "Americas, y"
        }},
        "mode": "markers",
        "name": "Americas",
        "type": "scatter",
        "x": americas_GDP,
        "y": americas_LifeExp,
        "marker": {
            "line": {"width": 2},
            "meta": {"columnNames": {"size": "Americas, size"}},
            "symbol": "circle",
            "sizeref": 0.85,
            "size": americas_Size,
            "sizemode": "diameter"
        }
    }
    trace3 = {
        "meta": {"columnNames": {
            "x": "Asia, x",
            "y": "Asia, y"
        }},
        "mode": "markers",
        "name": "Asia",
        "type": "scatter",
        "x": asia_GDP,
        "y": asia_LifeExp,
        "marker": {
            "line": {"width": 2},
            "meta": {"columnNames": {"size": "Asia, size"}},
            "symbol": "circle",
            "sizeref": 0.85,
            "size": asia_Size,
            "sizemode": "diameter"
        }
    }
    trace4 = {
        "meta": {"columnNames": {
            "x": "Europe, x",
            "y": "Europe, y"
        }},
        "mode": "markers",
        "name": "Europe",
        "type": "scatter",
        "x": europe_GDP,
        "y": europe_LifeExp,
        "marker": {
            "line": {"width": 2},
            "meta": {"columnNames": {"size": "Europe, size"}},
            "symbol": "circle",
            "sizeref": 0.85,
            "size": europe_Size,
            "sizemode": "diameter"
        }
    }

    data = [trace1, trace2, trace3, trace4]

    layout = {
        "title": {"text": "Life Expectancy v. Per Capita GDP, 2007"},
        "xaxis": {
            "type": "log",
            "range": [2.003297660701705, 5.191505530708712],
            "title": {"text": "GDP per capita (2000 dollars)"},
            "ticklen": 5,
            "gridcolor": "rgb(255, 255, 255)",
            "gridwidth": 2,
            "zerolinewidth": 1
        },
        "yaxis": {
            "type": "linear",
            "range": [36.12621671352166, 91.72921793264332],
            "title": {"text": "Life Expectancy (years)"},
            "ticklen": 5,
            "gridcolor": "rgb(255, 255, 255)",
            "gridwidth": 2,
            "zerolinewidth": 1
        },
        "autosize": True,
        "plot_bgcolor": "rgb(243, 243, 243)",
        "paper_bgcolor": "rgb(243, 243, 243)"
    }

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    layoutJSON = json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, layoutJSON


@app.route('/simpleGraph4')
def show_database_graph():
    data, layout = get_data_from_database()

    return render_template("database_graph.html", plot=data, layout=layout)


if __name__ == '__main__':
    app.run(debug=True)