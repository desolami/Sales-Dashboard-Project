import streamlit as st
import pandas as pd
import plotly.express as px

st.title(' Product Insights')

df = pd.read_csv('../Data/superstore.csv', encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, format='mixed')

# Sidebar filters
st.sidebar.header('🔍 Filters')
category = st.sidebar.multiselect('Category', df['Category'].unique(), default=df['Category'].unique())
filtered_df = df[df['Category'].isin(category)]

# Top 10 by Sales & Profit
col1, col2 = st.columns(2)
with col1:
    top_sales = filtered_df.groupby('Product Name')['Sales'].sum()\
        .sort_values(ascending=False).head(10).reset_index()
    fig1 = px.bar(top_sales, x='Sales', y='Product Name', orientation='h',
        color='Sales', color_continuous_scale='Blues', title='💰 Top 10 by Sales')
    fig1.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    top_profit = filtered_df.groupby('Product Name')['Profit'].sum()\
        .sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(top_profit, x='Profit', y='Product Name', orientation='h',
        color='Profit', color_continuous_scale='Greens', title='📈 Top 10 by Profit')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Sub-Category Drill Down
st.subheader('🔍 Sub-Category Drill-Down')
selected_cat = st.selectbox('Select Category', filtered_df['Category'].unique())
subcat_df = filtered_df[filtered_df['Category'] == selected_cat]\
    .groupby('Sub-Category').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()

col3, col4 = st.columns(2)
with col3:
    fig3 = px.bar(subcat_df, x='Sales', y='Sub-Category', orientation='h',
        color='Sub-Category', title=f'💰 Sales — {selected_cat}')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.bar(subcat_df, x='Profit', y='Sub-Category', orientation='h',
        color='Sub-Category', title=f'📈 Profit — {selected_cat}')
    st.plotly_chart(fig4, use_container_width=True)