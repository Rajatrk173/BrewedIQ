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
    # Radio
    measure = st.radio('Select parameters: ', ['Sales', 'Transactions'], horizontal = True)

    period = st.radio('Select Time Period:',['Daily','Week','Month'])

    if period == "Daily":
        temp = 'D'
    elif period == "Week":
        temp = 'W'
    elif period == 'Month':
        temp = 'M'
        

    if measure == 'Sales':
        # Data Extraction
        sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period(temp))['sales'].sum()
        daily_growth = sales.pct_change() * 100

        mov_avg = sales.rolling(window=2).mean()

        sales_revenueM = filtered_df.groupby(filtered_df['transaction_date'].dt.to_period(temp))['sales'].sum()

    elif measure == 'Transactions':
        # Data Extractions
        sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period(temp)).size()
        daily_growth = sales.pct_change() * 100

        mov_avg = sales.rolling(window=2).mean()

        sales_revenueM = filtered_df.groupby(filtered_df['transaction_date'].dt.to_period(temp)).size()
    
    sales.index = sales.index.to_timestamp()
    
    tab1_columns = st.columns([0.6, 0.4], gap='small')
    
    with tab1_columns[0]:
        st.plotly_chart(vis.mon_sales(sales_revenueM))
    with tab1_columns[1]:
        st.plotly_chart(vis.mom_growth(daily_growth))
        st.plotly_chart(vis.moving_avg(sales,mov_avg))

with tab2:
    # Radio
    measure = st.radio('Select parameters:',['Sales', 'Transactions'], horizontal = True)

    if measure == 'Sales':
        # Data Extraction
        filtered_df['transaction_time'] = pd.to_datetime(filtered_df['transaction_time'], format='%H:%M:%S')
        filtered_df['Hour']= pd.to_datetime(df.transaction_time).dt.hour
        hour_analysis = filtered_df.groupby([df.transaction_date.dt.date,'Hour'])['sales'].sum().reset_index()
        avg_hourly_analysis = hour_analysis.groupby('Hour')['sales'].mean()
        daily_analysis = filtered_df.groupby([df['transaction_date'].dt.date,'week_name'])['sales'].sum().reset_index()
        avg_daily_analysis = daily_analysis.groupby('week_name')['sales'].mean()
        avg_daily_analysis = avg_daily_analysis.reindex(list(calendar.day_name))
        av_analysis = avg_daily_analysis

    if measure == 'Transactions':
        # Data Extractions
        filtered_df['transaction_time'] = pd.to_datetime(filtered_df['transaction_time'], format='%H:%M:%S')
        filtered_df['Hour']= pd.to_datetime(df.transaction_time).dt.hour
        hour_analysis = filtered_df.groupby([df.transaction_date.dt.date,'Hour']).size()
        avg_hourly_analysis = hour_analysis.groupby('Hour').size()
        daily_analysis = filtered_df.groupby([df['transaction_date'].dt.date,'week_name']).size()
        avg_daily_analysis = daily_analysis.groupby('week_name').size()
        avg_daily_analysis = avg_daily_analysis.reindex(list(calendar.day_name))
        av_analysis = avg_daily_analysis

    tab2_columns = st.columns([0.6, 0.4], gap='small')

    with tab2_columns[0]:
        st.plotly_chart(vis.avgdaily_analysis(av_analysis))
    
    
    with tab2_columns[1]:
        st.plotly_chart(vis.avghourly_analysis(avg_hourly_analysis))
        st.plotly_chart(vis.avg_sale(filtered_df))


with tab3:
    # Radio
    measure = st.radio('Select parameters:',['Sales', 'Transactions'],horizontal = True, key = "Top Selling Products" )


    if measure == 'Sales':
        #Data Extractions
        category_salesS = filtered_df.groupby('product_category')['sales'].sum()
        Category_distribution = filtered_df.groupby('product_category')['transaction_qty'].sum()
        category_sales2 = filtered_df.groupby(['product_category','product_type'])['sales'].sum()

        # coffee_data = df[df.product_category == category_selection]
        # tea_data = df[df.product_category == 'Tea']
        # bakery_data = df[df.product_category == 'Bakery']
        PCS_coffee = filtered_df.groupby(['product_category', 'product_type'])['sales'].sum()
        # PCS_tea = tea_data.groupby('product_type')['sales'].sum().nlargest()
        # PCS_bakery = bakery_data.groupby('product_type')['sales'].sum().nlargest()
    if measure == 'Transactions':
        # Data Extractions
        category_salesS = filtered_df.groupby('product_category').size()
        Category_distribution = filtered_df.groupby('product_category')['transaction_qty'].size()
        category_sales2 = filtered_df.groupby(['product_category','product_type']).size()

        # coffee_data = df[df.product_category == category_selection]
        # tea_data = df[df.product_category == 'Tea']
        # bakery_data = df[df.product_category == 'Bakery']
        PCS_coffee = filtered_df.groupby(['product_category', 'product_type']).size()
        
        # PCS_tea = tea_data.groupby('product_type').size()
        # PCS_bakery = bakery_data.groupby('product_type').size()
    Total_bevrage = filtered_df.groupby('product_type')['sales'].sum().sort_values(ascending=False).reset_index(name='Total_sales').head(5)
    tab3_columns = st.columns([0.5,0.5], gap='small')

    with tab3_columns[0]:
        st.plotly_chart(vis.productcat_sales(category_salesS))

    with tab3_columns[1]:
        #st.plotly_chart(vis.productcat_trans(Category_distribution))
        st.dataframe(Total_bevrage)
        category_selection = st.selectbox('select category', filtered_df.product_category.unique().tolist())
        st.plotly_chart(vis.coffee_sales(PCS_coffee, category_selection))
        # st.plotly_chart(vis.tea_sales(PCS_tea))
        # st.plotly_chart(vis.bakery_sales(PCS_bakery))


with tab4:
    # Radio
    measure = st.radio('Select parameters: ',['Sales', 'Transactions'], key="measure_selector", horizontal = True,)

    if measure == 'Sales':
        # Data Extractions
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


    if measure == 'Transactions':
        #Data Extractions
        hell = df[df.store_location =="Hell's Kitchen"]
        lm = df[df.store_location =="Lower Manhattan"]
        a = df[df.store_location =="Astoria"]
        hsale = hell.groupby(hell.transaction_date.dt.to_period('M')).size()
        hmonthly_growth = hsale.pct_change()*100
        lmsale = lm.groupby(lm.transaction_date.dt.to_period('M')).size()
        lmonthly_growth = lmsale.pct_change()*100
        asale = a.groupby(a.transaction_date.dt.to_period('M')).size()
        amonthly_growth = asale.pct_change()*100

        store1= hell.groupby(hell.transaction_date.dt.to_period('M')).size()
        store2= lm.groupby(lm.transaction_date.dt.to_period('M')).size()
        store3= a.groupby(a.transaction_date.dt.to_period('M')).size()


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

# with st.container(height=450, border=False):
#             st.write('''
              
#               ''')
#         st.plotly_chart(vis.a_mom_grow(amonthly_growth))