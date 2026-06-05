import streamlit as st
import pandas as pd
import plotly.express as px

st.title(' Profit Analysis')

df = pd.read_csv('../Data/superstore.csv', encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, format='mixed')

# Sidebar filters
st.sidebar.header('🔍 Filters')
region = st.sidebar.multiselect('Region', df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect('Category', df['Category'].unique(), default=df['Category'].unique())
filtered_df = df[(df['Region'].isin(region)) & (df['Category'].isin(category))]

# Monthly Profit Trend
monthly = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Profit'].sum().reset_index()
monthly['Order Date'] = monthly['Order Date'].astype(str)
fig1 = px.line(monthly, x='Order Date', y='Profit', markers=True,
    title='📅 Monthly Profit Trend', color_discrete_sequence=['green'])
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# Profit by Category & Region
col1, col2 = st.columns(2)
with col1:
    cat_df = filtered_df.groupby('Category')['Profit'].sum().reset_index()
    fig2 = px.bar(cat_df, x='Category', y='Profit', color='Category', title='📈 Profit by Category')
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    reg_df = filtered_df.groupby('Region')['Profit'].sum().reset_index()
    fig3 = px.bar(reg_df, x='Region', y='Profit', color='Region', title='🌍 Profit by Region')
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Discount vs Profit
fig4 = px.scatter(filtered_df, x='Discount', y='Profit', color='Category',
    hover_data=['Product Name', 'Sales'], opacity=0.6,
    title='🏷️ Discount vs Profit')
fig4.add_hline(y=0, line_dash='dash', line_color='red', annotation_text='Break-even')
st.plotly_chart(fig4, use_container_width=True)