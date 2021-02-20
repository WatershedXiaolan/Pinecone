import pandas as pd
import numpy as np
from IPython.core.display import display, HTML
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
from datetime import timedelta
import os
import webbrowser
import sys

display(HTML("<style>.container { width:100% !important; }</style>"))
file = './log/balance_banks.html'

# remove file
if os.path.exists(file):
    os.remove(file)

# load data
# balances = pd.read_csv('./log/balance_banks.csv')
balances = pd.read_csv(sys.argv[1])

# pie chart
row = balances.iloc[0, 2:5]

colors = ['gold', 'lightgreen', 'mediumturquoise']

fig = go.Figure(data=[
    go.Pie(labels=row.index.tolist(),
           values=[round(n, 0) for n in row.values.tolist()],
           title='Total amount: '+str(balances.iloc[0, 1]))])
fig.update_traces(
    hoverinfo='label+percent', textinfo='value', textfont_size=20,
    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.update_layout(
    autosize=False,
    width=500,
    height=500)

with open(file, 'a') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(
        x=balances.Date,
        y=balances.Cash,
        name='Cash',
        stackgroup='one',
        mode='markers',
        marker_color=colors[0]
        ),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(
        x=balances.Date,
        y=balances.Bond,
        name='Bond',
        stackgroup='one',
        mode='markers',
        marker_color=colors[2]
        ),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(
        x=balances.Date,
        y=balances.Stock,
        name='Stock',
        stackgroup='one',
        mode='markers',
        marker_color=colors[1]
        ),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=balances.Date,
               y=balances['S/(S+B) ratio'],
               name='S/(S+B) Ratio'
               ),
    secondary_y=True
)

fig.update_yaxes(title_text="$", range=[0, 500000], secondary_y=False)
fig.update_yaxes(title_text="S/(S+B) Ratio", secondary_y=True, range=[0, 1.0])
fig.update_xaxes(range=[
    pd.to_datetime(balances.Date.iloc[0])-timedelta(days=90),
    pd.to_datetime(balances.Date.iloc[0])+timedelta(days=10)
    ])
fig.update_layout(hovermode='x unified')
with open(file, 'a') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

# Change path to reflect file location
filename = 'file:///'+os.getcwd()+'/' + file
webbrowser.open_new_tab(filename)