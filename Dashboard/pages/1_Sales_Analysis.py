import streamlit as st
import pandas as pd
import plotly.express as px

st.title(' Sales Analysis')

df = pd.read_csv('../Data/superstore.csv', encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, format='mixed')

# Sidebar filters
st.sidebar.header('🔍 Filters')
region = st.sidebar.multiselect('Region', df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect('Category', df['Category'].unique(), default=df['Category'].unique())
filtered_df = df[(df['Region'].isin(region)) & (df['Category'].isin(category))]

# Monthly Sales Trend
monthly = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly['Order Date'] = monthly['Order Date'].astype(str)
fig1 = px.line(monthly, x='Order Date', y='Sales', markers=True, title='📅 Monthly Sales Trend')
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# Sales by Category
col1, col2 = st.columns(2)
with col1:
    cat_df = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    fig2 = px.bar(cat_df, x='Category', y='Sales', color='Category', title='💰 Sales by Category')
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    reg_df = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    fig3 = px.bar(reg_df, x='Region', y='Sales', color='Region', title='🌍 Sales by Region')
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# State Map
state_df = filtered_df.groupby('State')['Sales'].sum().reset_index()
fig4 = px.choropleth(state_df, locations='State', locationmode='USA-states',
    color='Sales', scope='usa', color_continuous_scale='Blues',
    title='🗺️ Sales by State')
st.plotly_chart(fig4, use_container_width=True)