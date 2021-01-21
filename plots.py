import pandas as pd
import numpy as np
from IPython.core.display import display, HTML
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
from datetime import timedelta

display(HTML("<style>.container { width:100% !important; }</style>"))


# load data
balances = pd.read_csv('./log/balance_banks.csv')

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(
        x=balances.Date,
        y=balances.Cash,
        name='Cash',
        stackgroup='one'
        ),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(
        x=balances.Date,
        y=balances.Stock,
        name='Stock',
        stackgroup='one'
        ),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(
        x=balances.Date,
        y=balances.Bond,
        name='Bond',
        stackgroup='one'
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
    pd.to_datetime(balances.Date.iloc[0])-timedelta(days=180),
    pd.to_datetime(balances.Date.iloc[0])+timedelta(days=30)
    ])
fig.show()

with open('./log/balance_banks.html', 'a') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
