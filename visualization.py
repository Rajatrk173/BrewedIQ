import plotly.graph_objects as go

def mom_growth(data):
    fig = go.Figure([go.Bar(x=data.index.astype('str'), y=data.values)])
    fig.update_layout(
    title = "Monthly Sales Growth",
    xaxis_title = "Hour of Day",
    yaxis_title = "Average Sales by Hour",
    legend_title = "Product Category",
    width=500,  
    height=400
    )
    return fig

def mon_data(data):
   fig = go.Figure(data=go.Scatter(x=data.index.astype('str'), y=data.values))
   fig.update_layout(
    width=500,  
    height=400
)
   return fig

def mon_sales(data):
   fig = go.Figure(data=go.Scatter(x=data.index.astype('str'), y=data.values))
   fig.update_layout(
    title_text="Sales Revenue",
    width=500,  
    height=800
)
   return fig

def avgdaily_analysis(data):
    fig = go.Figure([go.Bar(x=data.index, y=data.values)])
    fig.update_layout(
    title_text="Average Daily Analysis",
    xaxis_title = "X",
    yaxis_title = "Y",
    width=500,  
    height=800
    )
    return fig
    
def avg_sale(data):
    fig = go.Figure()
    for i in data.product_category.unique():
        category = data[data.product_category == i]
        hourly_analysis = category.groupby([category.transaction_date.dt.date,'Hour'])['sales'].sum().reset_index()
        avg_hourly_analysis = hourly_analysis.groupby('Hour')['sales'].mean()
        #plt.plot(avg_hourly_analysis.index, avg_hourly_analysis.values,label=i)
        fig.add_trace(
            go.Scatter(
                x = avg_hourly_analysis.index,
                y = avg_hourly_analysis.values,
                mode = 'lines',
                name = i
            )
        )
    fig.update_layout(
    title = "Average Sales by Hour of Day (Product Category Wise)",
    xaxis_title = "Hour of Day",
    yaxis_title = "Average Sales by Hour",
    legend_title = "Product Category",
    width=400,  
    height=400
    )
    return fig

def avghourly_analysis(data):
    fig = go.Figure(go.Scatter(x=data.index.astype('str'), y=data.values))
    fig.update_layout(
    title = "Average Hourly Analysis",
    xaxis_title = "Hour",
    yaxis_title = "Average Sales by Hour",
    legend_title = "Product Category",
    width=350,  
    height=350
    )
    return fig

def hour_sales(data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = data.index.astype('str'),
            y = data.values,
            mode = 'lines',
        )
    )
    return fig

def store_rank(data,data1,data2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index.astype(str), y=data.values,
                    mode='lines',
                    name="Hell's Kitchen"))
    fig.add_trace(go.Scatter(x=data1.index.astype(str), y=data1.values, 
                    mode='lines+markers',
                    name="Lower Manhattan"))
    fig.add_trace(go.Scatter(x=data2.index.astype(str), y=data2.values,
                    mode="lines", 
                    name='Astoria'))
    fig.update_layout(
        title = 'Store Rank',
        xaxis_title = 'Month',
        yaxis_title = 'Growth Percent'
    )
    return fig

def hell_mom_grow(data):
    fig = go.Figure([go.Bar(x= data.index.astype('str'), y= data.values)])
    fig.update_layout(
        title = 'Hell’s Kitchen Month on Month Growth',
        xaxis_title = 'X',
        yaxis_title = 'Y'
    )
    return fig

def lm_mom_grow(data):
    fig = go.Figure([go.Bar(x= data.index.astype('str'), y= data.values)])
    fig.update_layout(
        title = 'Lower Manhattan Month on Month Growth',
        xaxis_title = 'X',
        yaxis_title = 'Y'
    )
    return fig

def a_mom_grow(data):
    fig = go.Figure([go.Bar(x= data.index.astype('str'), y= data.values)])
    fig.update_layout(
        title = 'Astoria Month on Month Growth',
        xaxis_title = 'X',
        yaxis_title = 'Y'
    )
    return fig

def productcat_sales(data):
    fig = go.Figure([go.Bar(x=data['product_category'], y=data['sales'])])
    fig.update_layout(
        title = 'Product Category Distribution (by sales)',
        xaxis_title = 'Total Sales',
        yaxis_title = 'Product Category',
        width=500,  
        height=700
    )
    return fig

def productcat_trans(data):
    fig = go.Figure([go.Bar(x=data['product_category'], y= data['transaction_qty'])])
    fig.update_layout(
        title = 'Product Category Distribution (by Transaction)',
        xaxis_title = 'Total Transaction',
        yaxis_title = 'Product Category'
    )
    return fig

def coffee_sales(data):
    lables = data['product_type']
    values = data['sales']
    fig = go.Figure(data=[go.Pie(labels=lables , values=values,textinfo='label+percent',
                             insidetextorientation='radial')])
    fig.update_layout(
    title_text="Product Category (Coffee) Distribution by Sales",
    width=300,  
    height=400
)
    return fig

def tea_sales(data):
    lables = data['product_type']
    values = data['sales']
    fig = go.Figure(data=[go.Pie(labels=lables , values=values,textinfo='label+percent',
                             insidetextorientation='radial')])
    
    fig.update_layout(
    title_text="Product Category (Tea) Distribution by Sales",
)
    return fig

def bakery_sales(data):
    lables = data['product_type']
    values = data['sales']
    fig = go.Figure(data=[go.Pie(labels=lables , values=values,textinfo='label+percent',
                             insidetextorientation='radial')])
    
    fig.update_layout(
    title_text="Product Category (Bakery) Distribution by Sales",
    
)
    return fig


