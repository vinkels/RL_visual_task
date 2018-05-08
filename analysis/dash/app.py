import plotly
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('output/pivot_set.csv')
print(data)
plotly.offline.plot({
    "data": [go.Bar(x = df[])],
    "layout": go.Layout(title="hello world")
})
