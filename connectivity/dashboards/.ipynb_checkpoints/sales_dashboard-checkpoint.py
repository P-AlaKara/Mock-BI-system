from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

df = pd.read_csv('modified_sales.csv')
df.drop(columns=['staff_no', 'staff_name', 'customerID', 'customer_name', 'age', 'productID', 
                 'age', 'segment'], inplace=True)
top_products_df = df.drop(columns=['product_name', 'date', 'time', 'saleID', 'payment_method', 'county'])
grouped_category = top_products_df.groupby('sub_category')
sum_grouped_category = grouped_category['quantity'].sum()
#linked stylesheets
external_stylesheets = ['static/css/sales_styles.css']

#functions
def get_top_products(df, n=10):
    df_sorted = df.sort_values(ascending=False)
    top_products = df_sorted.head(n)
    return top_products
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    html.Nav([
        html.Ul([
            html.Li(html.A('Home', href='/')),
            html.Li(html.A('Products Dashboard', href='/')),
            html.Li(html.A('Customers Dashboard', href='/'))
        ], className='nav'),
    ], className='navbar'),
    html.Div(className='row content', children='SALES DASHBOARD', style={'color':'#f0f0f0', 'fontSize': 30}),
    html.Hr(className='content'),
    html.Div(className='six-columns content', children=[dash_table.DataTable(data=get_top_products(sum_grouped_category).to_dict('records'), page_size=10, style_table={'overflowX': 'auto'})]),
    html.Div(className='row content', children=[dcc.RadioItems(options=['profit', 'price', 'quantity'], value='price', id='controls-and-radio-item', inline=True)]),
    html.Div(className='six-columns content', children=[dcc.Graph(figure={}, id='controls-and-graph')])
])

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='category', y=col_chosen, histfunc='avg')
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='#212121',
        font_color='white'
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
