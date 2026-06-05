import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Page Config ---
st.set_page_config(
    page_title='Sales Analytics Dashboard',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# --- Custom Color Theme ---
COLORS = {
    'primary': '#2563EB',
    'success': '#16A34A',
    'warning': '#D97706',
    'danger': '#DC2626',
    'purple': '#7C3AED'
}

CATEGORY_COLORS = {
    'Furniture': '#2563EB',
    'Technology': '#16A34A',
    'Office Supplies': '#D97706'
}

REGION_COLORS = ['#2563EB', '#16A34A', '#D97706', '#DC2626']

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('../Data/superstore.csv', encoding='latin-1')
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, format='mixed')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, format='mixed')
    df['Month'] = df['Order Date'].dt.month_name()
    df['Year'] = df['Order Date'].dt.year
    df['Ship Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    return df

superstore_df = load_data()

# --- Sidebar ---
st.sidebar.image('https://img.icons8.com/color/96/combo-chart--v2.png', width=80)
st.sidebar.title('Dashboard Menu')
st.sidebar.markdown('Go To')

page = st.sidebar.radio(
    '',
    [
        'Overview',
        'Sales Analysis',
        'Profit Analysis',
        'Forecast Analysis',
        'Customer Segmentation',
        'Geographical Map',
        'Business Insights',
        'Conclusion'
    ]
)

st.sidebar.divider()
st.sidebar.subheader('Global Filters')
region = st.sidebar.multiselect('Region', options=superstore_df['Region'].unique(), default=superstore_df['Region'].unique())
category = st.sidebar.multiselect('Category', options=superstore_df['Category'].unique(), default=superstore_df['Category'].unique())
segment = st.sidebar.multiselect('Segment', options=superstore_df['Segment'].unique(), default=superstore_df['Segment'].unique())

st.sidebar.divider()
st.sidebar.subheader('Date Range')
min_date = superstore_df['Order Date'].min().date()
max_date = superstore_df['Order Date'].max().date()
start_date = st.sidebar.date_input('Start Date', min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input('End Date', max_date, min_value=min_date, max_value=max_date)

st.sidebar.divider()

# --- Filter Data ---
filtered_df = superstore_df[
    (superstore_df['Region'].isin(region)) &
    (superstore_df['Category'].isin(category)) &
    (superstore_df['Segment'].isin(segment)) &
    (superstore_df['Order Date'].dt.date >= start_date) &
    (superstore_df['Order Date'].dt.date <= end_date)
]

# =====================
# PAGE: OVERVIEW
# =====================
if page == 'Overview':
    st.title('Sales Analytics Dashboard')
    st.markdown('A professional overview of sales performance, trends, and insights.')
    st.divider()

    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = filtered_df['Order ID'].nunique()
    total_quantity = filtered_df['Quantity'].sum()
    avg_sales = filtered_df['Sales'].mean()
    avg_discount = filtered_df['Discount'].mean()
    profit_margin = (total_profit / total_sales) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Sales', f"${total_sales:,.2f}")
    col2.metric('Total Profit', f"${total_profit:,.2f}")
    col3.metric('Total Orders', f"{total_orders:,}")
    col4.metric('Total Quantity', f"{total_quantity:,}")

    col5, col6, col7 = st.columns(3)
    col5.metric('Avg Sales per Order', f"${avg_sales:,.2f}")
    col6.metric('Avg Discount', f"{avg_discount:.1%}")
    col7.metric('Profit Margin', f"{profit_margin:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        cat_df = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        fig1 = px.bar(cat_df, x='Category', y='Sales', color='Category',
            color_discrete_map=CATEGORY_COLORS,
            title='Sales by Category', text_auto='.2s')
        fig1.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        reg_df = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        fig2 = px.pie(reg_df, names='Region', values='Sales',
            color_discrete_sequence=REGION_COLORS,
            title='Sales by Region', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    monthly = filtered_df.groupby(
        filtered_df['Order Date'].dt.to_period('M')
    ).agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)

    col1, col2 = st.columns(2)
    with col1:
        fig3 = px.line(monthly, x='Order Date', y='Sales', markers=True,
            title='Monthly Sales Trend', color_discrete_sequence=['#2563EB'])
        fig3.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        fig4 = px.line(monthly, x='Order Date', y='Profit', markers=True,
            title='Monthly Profit Trend', color_discrete_sequence=['#16A34A'])
        fig4.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig4, use_container_width=True)

# --- Download Button ---
    st.divider()
    st.subheader('Export Data')
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='Download Filtered Data as CSV',
        data=csv,
        file_name='filtered_superstore_data.csv',
        mime='text/csv'
    )
# =====================
# PAGE: SALES ANALYSIS
# =====================
elif page == 'Sales Analysis':
    st.title('Sales Analysis')
    st.divider()

    monthly = filtered_df.groupby(
        filtered_df['Order Date'].dt.to_period('M')
    )['Sales'].sum().reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)

    fig1 = px.line(monthly, x='Order Date', y='Sales', markers=True,
        title='Monthly Sales Trend', color_discrete_sequence=['#2563EB'])
    fig1.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        cat_df = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        fig2 = px.bar(cat_df, x='Category', y='Sales', color='Category',
            color_discrete_map=CATEGORY_COLORS,
            title='Sales by Category', text_auto='.2s')
        fig2.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        subcat_df = filtered_df.groupby('Sub-Category')['Sales'].sum()\
            .sort_values(ascending=False).head(10).reset_index()
        fig3 = px.bar(subcat_df, x='Sales', y='Sub-Category',
            orientation='h', color='Sales',
            color_continuous_scale='Blues',
            title='Top 10 Sub-Categories by Sales')
        fig3.update_layout(yaxis={'categoryorder':'total ascending'},
            plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        top_sales = filtered_df.groupby('Product Name')['Sales'].sum()\
            .sort_values(ascending=False).head(10).reset_index()
        fig4 = px.bar(top_sales, x='Sales', y='Product Name',
            orientation='h', color='Sales',
            color_continuous_scale='Blues',
            title='Top 10 Products by Sales')
        fig4.update_layout(yaxis={'categoryorder':'total ascending'},
            plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        reg_df = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        fig5 = px.bar(reg_df, x='Region', y='Sales', color='Region',
            color_discrete_sequence=REGION_COLORS,
            title='Sales by Region', text_auto='.2s')
        fig5.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig5, use_container_width=True)

# =====================
# PAGE: PROFIT ANALYSIS
# =====================
elif page == 'Profit Analysis':
    st.title('Profit Analysis')
    st.divider()

    monthly = filtered_df.groupby(
        filtered_df['Order Date'].dt.to_period('M')
    )['Profit'].sum().reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)

    fig1 = px.line(monthly, x='Order Date', y='Profit', markers=True,
        title='Monthly Profit Trend', color_discrete_sequence=['#16A34A'])
    fig1.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        cat_df = filtered_df.groupby('Category')['Profit'].sum().reset_index()
        fig2 = px.bar(cat_df, x='Category', y='Profit', color='Category',
            color_discrete_map=CATEGORY_COLORS,
            title='Profit by Category', text_auto='.2s')
        fig2.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = px.scatter(filtered_df, x='Discount', y='Profit',
            color='Category', opacity=0.6,
            color_discrete_map=CATEGORY_COLORS,
            hover_data=['Product Name', 'Sales'],
            title='Discount vs Profit')
        fig3.add_hline(y=0, line_dash='dash', line_color='red',
            annotation_text='Break-even')
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        reg_df = filtered_df.groupby('Region')['Profit'].sum().reset_index()
        fig4 = px.bar(reg_df, x='Region', y='Profit', color='Region',
            color_discrete_sequence=REGION_COLORS,
            title='Profit by Region', text_auto='.2s')
        fig4.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        top_profit = filtered_df.groupby('Product Name')['Profit'].sum()\
            .sort_values(ascending=False).head(10).reset_index()
        fig5 = px.bar(top_profit, x='Profit', y='Product Name',
            orientation='h', color='Profit',
            color_continuous_scale='Greens',
            title='Top 10 Products by Profit')
        fig5.update_layout(yaxis={'categoryorder':'total ascending'},
            plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig5, use_container_width=True)

# =====================
# PAGE: FORECAST ANALYSIS
# =====================
elif page == 'Forecast Analysis':
    st.title('Sales Forecasting')
    st.markdown('Linear regression forecast for the next 6 months.')
    st.divider()

    forecast_df = filtered_df.groupby(
        filtered_df['Order Date'].dt.to_period('M')
    )['Sales'].sum().reset_index()
    forecast_df['Order Date'] = forecast_df['Order Date'].astype(str)
    forecast_df['Month Index'] = range(len(forecast_df))

    x = forecast_df['Month Index'].values
    y = forecast_df['Sales'].values
    slope, intercept = np.polyfit(x, y, 1)

    last_index = forecast_df['Month Index'].max()
    future_indices = np.array(range(last_index + 1, last_index + 7))
    future_sales = slope * future_indices + intercept

    last_date = pd.to_datetime(forecast_df['Order Date'].iloc[-1])
    future_months = pd.date_range(start=last_date, periods=7, freq='MS')[1:]
    future_months = [d.strftime('%Y-%m') for d in future_months]

    actual = pd.DataFrame({
        'Month': forecast_df['Order Date'],
        'Sales': forecast_df['Sales'],
        'Type': 'Actual'
    })
    forecast = pd.DataFrame({
        'Month': future_months,
        'Sales': future_sales,
        'Type': 'Forecast'
    })
    combined = pd.concat([actual, forecast], ignore_index=True)

    fig = px.line(combined, x='Month', y='Sales', color='Type',
        color_discrete_map={'Actual': '#2563EB', 'Forecast': '#DC2626'},
        markers=True, title='Sales Forecast - Next 6 Months')
    fig.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.info('Forecast is based on linear regression using historical monthly sales data.')

# =====================
# PAGE: CUSTOMER SEGMENTATION
# =====================
elif page == 'Customer Segmentation':
    st.title('Customer Segmentation')
    st.divider()

    seg_df = filtered_df.groupby('Segment').agg(
        Sales=('Sales','sum'),
        Profit=('Profit','sum'),
        Quantity=('Quantity','sum'),
        Orders=('Order ID','nunique')
    ).reset_index()

    col1, col2, col3 = st.columns(3)
    with col1:
        fig1 = px.pie(seg_df, names='Segment', values='Sales',
            title='Sales by Segment', hole=0.4,
            color_discrete_sequence=REGION_COLORS)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(seg_df, names='Segment', values='Profit',
            title='Profit by Segment', hole=0.4,
            color_discrete_sequence=REGION_COLORS)
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        fig3 = px.pie(seg_df, names='Segment', values='Quantity',
            title='Quantity by Segment', hole=0.4,
            color_discrete_sequence=REGION_COLORS)
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    fig4 = px.bar(seg_df, x='Segment', y=['Sales','Profit','Quantity'],
        barmode='group', title='Full Segment Comparison')
    fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig4, use_container_width=True)

# =====================
# PAGE: GEOGRAPHICAL MAP
# =====================
elif page == 'Geographical Map':
    st.title('Geographical Sales Distribution')
    st.divider()

    state_df = filtered_df.groupby('State').agg(
        Sales=('Sales','sum'),
        Profit=('Profit','sum'),
        Orders=('Order ID','nunique')
    ).reset_index()

    fig1 = px.choropleth(state_df, locations='State',
        locationmode='USA-states', color='Sales',
        scope='usa', color_continuous_scale='Blues',
        title='Sales by State')
    fig1.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    fig2 = px.choropleth(state_df, locations='State',
        locationmode='USA-states', color='Profit',
        scope='usa', color_continuous_scale='Greens',
        title='Profit by State')
    fig2.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig2, use_container_width=True)

# =====================
# PAGE: BUSINESS INSIGHTS
# =====================
elif page == 'Business Insights':
    st.title('Business Insights')
    st.markdown('Key recommendations based on dashboard findings.')
    st.divider()

    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100

    best_region = filtered_df.groupby('Region')['Profit'].sum().idxmax()
    worst_region = filtered_df.groupby('Region')['Profit'].sum().idxmin()
    best_category = filtered_df.groupby('Category')['Sales'].sum().idxmax()
    worst_category = filtered_df.groupby('Category')['Profit'].sum().idxmin()
    best_month = filtered_df.groupby('Month')['Sales'].sum().idxmax()
    worst_month = filtered_df.groupby('Month')['Sales'].sum().idxmin()

    col1, col2 = st.columns(2)
    with col1:
        st.success(f'**Best Performing Region:** {best_region}')
        st.success(f'**Highest Sales Category:** {best_category}')
        st.success(f'**Best Sales Month:** {best_month}')

    with col2:
        st.error(f'**Least Profitable Region:** {worst_region}')
        st.error(f'**Least Profitable Category:** {worst_category}')
        st.error(f'**Lowest Sales Month:** {worst_month}')

    st.divider()
    st.subheader('Recommendations')
    st.markdown(f'''
    1. **Focus marketing on {best_region}** — it is the most profitable region.
    2. **Reduce discounts on {worst_category}** — heavy discounting is hurting profit margins.
    3. **Increase inventory for {best_category}** — it generates the highest sales.
    4. **Run campaigns in {worst_month}** — sales are lowest during this period.
    5. **Current profit margin is {profit_margin:.1f}%** — target above 15% for healthy growth.
    ''')

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        reg_profit = filtered_df.groupby('Region')['Profit'].sum().reset_index()
        fig1 = px.bar(reg_profit, x='Region', y='Profit', color='Region',
            color_discrete_sequence=REGION_COLORS,
            title='Profit by Region', text_auto='.2s')
        fig1.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        cat_profit = filtered_df.groupby('Category')['Profit'].sum().reset_index()
        fig2 = px.bar(cat_profit, x='Category', y='Profit', color='Category',
            color_discrete_map=CATEGORY_COLORS,
            title='Profit by Category', text_auto='.2s')
        fig2.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

# =====================
# PAGE: CONCLUSION
# =====================
elif page == 'Conclusion':
    st.title('Conclusion')
    st.divider()

    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = filtered_df['Order ID'].nunique()
    profit_margin = (total_profit / total_sales) * 100
    best_region = filtered_df.groupby('Region')['Profit'].sum().idxmax()
    best_category = filtered_df.groupby('Category')['Sales'].sum().idxmax()

    st.markdown(f'''
    ### Project Summary

    This dashboard was built to analyze the Superstore Sales Dataset and uncover
    key business insights using Python, Pandas, Plotly, and Streamlit.

    ### Key Findings

    - **Total Revenue Generated:** ${total_sales:,.2f}
    - **Total Profit Earned:** ${total_profit:,.2f}
    - **Overall Profit Margin:** {profit_margin:.1f}%
    - **Total Orders Processed:** {total_orders:,}
    - **Most Profitable Region:** {best_region}
    - **Highest Selling Category:** {best_category}

    ### Skills Demonstrated

    - Data Cleaning & Preparation
    - Exploratory Data Analysis (EDA)
    - KPI Calculations
    - Interactive Data Visualization
    - Dashboard Development
    - Sales Forecasting
    - Business Recommendations

    ### Tools Used

    - **Python** — Core programming language
    - **Pandas** — Data manipulation
    - **Plotly** — Interactive charts
    - **Streamlit** — Dashboard framework
    - **NumPy** — Forecasting calculations
    ''')

    st.divider()
    st.success('Thank you for exploring the Sales Analytics Dashboard!')
    st.balloons()

st.divider()
