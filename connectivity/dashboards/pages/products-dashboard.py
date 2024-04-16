import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

df = pd.read_csv('inventory_table.csv')
df.drop(columns=['productID'], inplace=True)
#items_in_each_category - pie chart
#stock_per_category - bar graph
#items with the highest price - table
#price_per_category - bar graph
#total_no_of_items - constant
#total_price_of_items - constant
#total_no_of_categories

#constants
total_no_of_items = df['sub_category'].nunique()
dash.register_page(
    __name__,
    path='/products-dashboard',
    title='Our Products Dashboard',
    name='Our Products Dashboard'
)

layout = html.Div(
    [
        html.P('This will be the new page')
    ]
)



