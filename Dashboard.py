import streamlit as st
import pandas as pd
import calendar
import visualization as vis

st.set_page_config(layout='wide')

@st.cache_data
def load_data(path):
    return pd.read_excel(path, engine='openpyxl')

df = load_data("CoffeeShopSales.xlsx")

df['sales'] = df['transaction_qty'] * df['unit_price']
df['week_name'] = df['transaction_date'].dt.day_name()
df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S')
df['Hour']= pd.to_datetime(df.transaction_time).dt.hour
df.product_category.unique()

st.title("Coffee Dashboard")

## SideBar
store_selection = st.sidebar.multiselect('Select Store',df.store_location.unique().tolist(),default = df.store_location.unique().tolist())

date_range = st.sidebar.date_input(' Select Date Range',[df.transaction_date.min(),df.transaction_date.max()])

##

filtered_df = df.loc[
    (df['store_location'].isin(store_selection)) &
    (df['transaction_date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]


##  KPI
a,b,c,d = st.columns(4)

Total_sales = df.sales.sum()
a.metric(label="Total Revenue", value=f'{Total_sales:.2f}')

No_Trans = filtered_df.transaction_id.nunique()
b.metric(label="Number of Transaction", value=f'{No_Trans:.2f}')

Average_sales=filtered_df.sales.mean()
c.metric(label="Average sales", value=f'{Average_sales:.2f}')


Average_trans=filtered_df.transaction_qty.mean()
d.metric(label="Average Transaction", value=f'{Average_trans:.2f}')

## Tabs
tab1,tab2,tab3,tab4=st.tabs(["Sales Trend Overtime","Time of Day analysis","Top Selling Products","Store Performance"])
with tab1:
    sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period('M'))['sales'].sum()
    daily_growth = sales.pct_change() * 100

    sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period('M'))['sales'].sum()
    mov_avg = sales.rolling(window=2).mean()

    sales_revenueM = filtered_df.groupby(filtered_df['transaction_date'].dt.to_period('M'))['sales'].sum()

    daily_analysis = filtered_df.groupby([filtered_df['transaction_date'].dt.date, 'week_name'])['sales'].sum().reset_index()
    Avg_daily_analysis = daily_analysis.groupby('week_name')['sales'].mean()
    Avg_daily_analysis = Avg_daily_analysis.reindex(list(calendar.day_name))

    Month_data=df.groupby(df.transaction_date.dt.to_period('M')).size()

    tab1_columns = st.columns([0.6, 0.4], gap='small')
    

    with tab1_columns[0]:
        sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period('M'))['sales'].sum()
        mov_avg = sales.rolling(window=2).mean()
        st.plotly_chart(vis.mon_sales(sales_revenueM))
    with tab1_columns[1]:
        sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period('M'))['sales'].sum()
        daily_growth = sales.pct_change() * 100
        st.plotly_chart(vis.mom_growth(daily_growth))
        st.plotly_chart(vis.mon_data(Month_data))

with tab2:
    filtered_df['transaction_time'] = pd.to_datetime(filtered_df['transaction_time'], format='%H:%M:%S')
    filtered_df['Hour']= pd.to_datetime(df.transaction_time).dt.hour
    hour_analysis = filtered_df.groupby([df.transaction_date.dt.date,'Hour'])['sales'].sum().reset_index()
    avg_hourly_analysis = hour_analysis.groupby('Hour')['sales'].mean()
    daily_analysis = filtered_df.groupby([df['transaction_date'].dt.date,'week_name'])['sales'].sum().reset_index()
    avg_daily_analysis = daily_analysis.groupby('week_name')['sales'].mean()
    avg_daily_analysis = avg_daily_analysis.reindex(list(calendar.day_name))
    av_analysis = avg_daily_analysis

    tab2_columns = st.columns([0.6, 0.4], gap='small')

    with tab2_columns[0]:
        st.plotly_chart(vis.avgdaily_analysis(av_analysis))
    
    
    with tab2_columns[1]:
        st.plotly_chart(vis.avghourly_analysis(avg_hourly_analysis))
        st.plotly_chart(vis.avg_sale(filtered_df))



with tab3:
    category_salesS = df.groupby('product_category')['sales'].sum().reset_index()
    Category_distribution = df.groupby('product_category')['transaction_qty'].sum().reset_index()
    category_sales2 = df.groupby(['product_category','product_type'])['sales'].sum().reset_index()

    coffee_data = df[df.product_category == 'Coffee']
    tea_data = df[df.product_category == 'Tea']
    bakery_data = df[df.product_category == 'Bakery']
    PCS_coffee = coffee_data.groupby('product_type')['sales'].sum().nlargest().reset_index()
    PCS_tea = tea_data.groupby('product_type')['sales'].sum().nlargest().reset_index()
    PCS_bakery = bakery_data.groupby('product_type')['sales'].sum().nlargest().reset_index()

    tab3_columns = st.columns([0.5,0.5], gap='small')

    with tab3_columns[0]:
        st.plotly_chart(vis.productcat_sales(category_salesS))
    
    with tab3_columns[1]:
        st.plotly_chart(vis.productcat_trans(Category_distribution))
        st.plotly_chart(vis.coffee_sales(PCS_coffee))
        st.plotly_chart(vis.tea_sales(PCS_tea))
        st.plotly_chart(vis.bakery_sales(PCS_bakery))

    #with tab3_columns[2]:

with tab4:
    hell = df[df.store_location =="Hell's Kitchen"]
    lm = df[df.store_location =="Lower Manhattan"]
    a = df[df.store_location =="Astoria"]
    hsale = hell.groupby(hell.transaction_date.dt.to_period('M'))['sales'].sum()
    hmonthly_growth = hsale.pct_change()*100
    lmsale = lm.groupby(lm.transaction_date.dt.to_period('M'))['sales'].sum()
    lmonthly_growth = lmsale.pct_change()*100
    asale = a.groupby(a.transaction_date.dt.to_period('M'))['sales'].sum()
    amonthly_growth = asale.pct_change()*100

    store1= hell.groupby(hell.transaction_date.dt.to_period('M'))["sales"].sum()
    store2= lm.groupby(lm.transaction_date.dt.to_period('M'))["sales"].sum()
    store3= a.groupby(a.transaction_date.dt.to_period('M'))["sales"].sum()


    tab4_columns = st.columns([0.66,0.33], gap='small')

    with tab4_columns[0]:
        st.plotly_chart(vis.store_rank(store1,store2,store3))
        tab4_inner_columns = st.columns(2, gap='small')
        with tab4_inner_columns[0]:
            st.plotly_chart(vis.hell_mom_grow(hmonthly_growth))
        with tab4_inner_columns[1]:
            st.plotly_chart(vis.lm_mom_grow(lmonthly_growth))
    with tab4_columns[1]:
        with st.container(height=450, border=False):
            st.write('''
                Hell’s Kitchen: Best-performing store with the highest growth, climbing from ₹27.8K in January to ₹56.9K in June. Shows strong demand and consistent momentum.June.

                Lower Manhattan: Consistent but slightly behind the other two (₹54.4K in June). Still growing well but not as fast as Hell’s Kitchen. Store is performing well and maintaining customer engagement. 

                Astoria: Stable performer, slightly ahead of Lower Manhattan in May–June (₹55K in June). Competitive and reliable. Astoria has a pattern very similar to Lower Manhattan

            ''')
        st.plotly_chart(vis.a_mom_grow(amonthly_growth))

