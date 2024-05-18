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
#items with the most stock - table
#price_per_category - bar graph
#total_no_of_items - constant
#total_price_of_items - constant
#total_no_of_categories

#constants
total_no_of_products = df['sub_category'].nunique()
total_stock = df['stock'].sum()
total_price_of_items = round(df['price'].sum())
total_no_categories = df['category'].nunique()

price_per_category = df.groupby('category').agg(price=('price','mean')).reset_index()
fig_bar = px.bar(price_per_category, x='category', y='price', color='category', 
                 color_discrete_map={'Furniture' : 'rgb(3, 3, 182)', 'Office Supplies' : 'rgb(1, 156, 1)', 
                                     'Technology':'rgb(178, 8, 8)'})
fig_bar.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=440,
        height=340,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Price per Category', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
fig_bar.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_bar.update_yaxes(showgrid=True, gridcolor='dimgray')

fig_scatter = px.scatter(df, x='stock', y='price',
                 title='Product Stock vs Price',
                 labels={'stock': 'Stock Quantity', 'price': 'Price (Ksh)'},
                 color='category',  # Color-code points by category
                 hover_data=['sub_category']) 
fig_scatter.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=410,
        height=340,
        margin=dict(l=5, r=5, t=90, b=3),
        title=dict(text='Stock vs Price', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
fig_scatter.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_scatter.update_yaxes(showgrid=True, gridcolor='dimgray')

stock_per_category = df.groupby('category').agg(stock=('stock','sum')).reset_index()
fig_pie = px.pie(stock_per_category, names='category', values='stock', color='category', hole=0.2,
                color_discrete_map={'Furniture' : 'rgb(3, 3, 182)', 'Office Supplies' : 'rgb(1, 156, 1)', 
                'Technology':'rgb(178, 8, 8)'})
fig_pie.update_layout(margin=dict(l=40, r=0, t=40, b=0), 
                      paper_bgcolor='#212121', width=300, height=200, 
                      title=dict(text='Stock by Category', font=dict(family='Arial', color='#f0e8e7')))

greatest_stock = df.groupby(['category','sub_category']).agg(stock=('stock','sum'),price=('price','mean')).reset_index()
def get_top_products(df, n=10):
    df_sorted = df.sort_values(by='stock', ascending=False)
    top_products = df_sorted.head(n)
    return top_products

external_stylesheets = ['static/css/products_styles.css', dbc.themes.DARKLY]

app = Dash(__name__, external_stylesheets=external_stylesheets)
sidebar = html.Div(
    [
        html.Img(src='assets/logo2.png', className='logo-img'),
        html.Hr(style={'margin':0}),
        html.Nav([
        html.Ul([
            html.Li(html.A(children=[DashIconify(icon="ant-design:home-outlined", className='icon'),'Home'], href='../templates/static/index.html', style={'display':'block'})),
            html.Li(html.A(children=[DashIconify(icon="ant-design:database-outlined", className='icon'),'Products Dashboard'], href='/products-dashboard')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:team-outlined", className='icon'),'Customers Dashboard'], href='/')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:aim-outlined", className='icon'),'Goals'], href='/')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:stock-outlined", className='icon'),'Analysis'], href='/')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:search-outlined", className='icon'),'Queries'], href='/')),
            html.Li(html.A(children=[DashIconify(icon="carbon:settings-check", className='icon'),'Visualization'], href='/'))
        ], className='nav'),
    ], className='navbar')],
)
content = html.Div(
    [
        html.Div(id='header', children=['INVENTORY DASHBOARD']),
        dmc.Divider(label = 'Stats',  labelPosition='center', size=2, style={'margin-bottom':'10px'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dmc.Group(
                            #position='center',
                            className='stats stats_one',
                            spacing='xs',
                            style={'flex-direction':'column'},
                            children=[
                                html.Div(id='dummy-input', style={'display':'none'}),
                                dmc.Text('TOTAL PRODUCTS', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                dmc.Text(id='totalprod', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dmc.Group(
                            #position='center',
                            className='stats stats_two',
                            spacing='xs',
                            style={'flex-direction':'column'},
                            children=[
                                html.Div(id='dummy-input_two', style={'display':'none'}),
                                dmc.Text('TOTAL STOCK', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                dmc.Text(id='totalstock', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dmc.Group(
                            #position='center',
                            className='stats stats_three',
                            spacing='xs',
                            style={'flex-direction':'column'},
                            children=[
                                html.Div(id='dummy-input_three', style={'display':'none'}),
                                dmc.Text('AVERAGE PRICE', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                dmc.Text(id='totalprice', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dmc.Group(
                            #position='center',
                            className='stats stats_four',
                            spacing='xs',
                            style={'flex-direction':'column'},
                            children=[
                                html.Div(id='dummy-input_four', style={'display':'none'}),
                                dmc.Text('CATEGORIES', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                dmc.Text(id='totalcat', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                            ]
                        )
                    ]
                )
            ]
        ),
        dmc.Divider(label = 'Graphs',  labelPosition='center', size=2),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id='bar-chart', className='chart', children=[dcc.Graph(figure=fig_bar, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Div(
                            id='scatter-chart', className='chart', children=[dcc.Graph(figure=fig_scatter, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                        )
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id='data-table', className='table', 
                            children=[dash_table.DataTable(data=get_top_products(greatest_stock).to_dict('records'), 
                                                               page_size=10, style_data={ 'border': '0px'},
                                                               style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(40, 37, 37)',}])]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Div(
                            id='pie_chart', className='chart', children=[dcc.Graph(figure=fig_pie)]
                        )
                    ]
                )
            ]
        )
    ]
)
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='sidebar'),
                dbc.Col(content, width=9),
            ],
            style={"height": "100vh"}
        ),
    ],
    fluid=True
)

#callbacks
#update total products
@callback(
        Output('totalprod','children'),
        Input('dummy-input', 'children')
)
def update_products(dummy_input):
    total_items = df['sub_category'].nunique()
    return "{:,}".format(total_items)
#update total stock
@callback(
        Output('totalstock','children'),
        Input('dummy-input_two', 'children')
)
def update_stock(dummy_input_two):
    total_stock = df['stock'].sum()
    return "{:,}".format(total_stock)
#update total price
@callback(
        Output('totalprice','children'),
        Input('dummy-input_three', 'children')
)
def update_stock(dummy_input_three):
    avg_price = round(df['price'].mean())
    return "{:,}".format(avg_price)
#update number of categories
@callback(
        Output('totalcat','children'),
        Input('dummy-input_four', 'children')
)
def update_stock(dummy_input_four):
    total_categories = df['category'].nunique()
    return "{:,}".format(total_categories)
if __name__ == '__main__':
    app.run(debug=True, port=8052)





