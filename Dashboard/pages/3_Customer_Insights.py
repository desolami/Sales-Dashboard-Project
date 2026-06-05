import streamlit as st
import pandas as pd
import plotly.express as px

st.title(' Customer Insights')

df = pd.read_csv('../Data/superstore.csv', encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, format='mixed')

# Sidebar filters
st.sidebar.header('🔍 Filters')
segment = st.sidebar.multiselect('Segment', df['Segment'].unique(), default=df['Segment'].unique())
region = st.sidebar.multiselect('Region', df['Region'].unique(), default=df['Region'].unique())
filtered_df = df[(df['Segment'].isin(segment)) & (df['Region'].isin(region))]

# Segment Pie Charts
col1, col2, col3 = st.columns(3)
with col1:
    fig1 = px.pie(filtered_df.groupby('Segment')['Sales'].sum().reset_index(),
        names='Segment', values='Sales', title='💰 Sales by Segment')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(filtered_df.groupby('Segment')['Profit'].sum().reset_index(),
        names='Segment', values='Profit', title='📈 Profit by Segment')
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    fig3 = px.pie(filtered_df.groupby('Segment')['Quantity'].sum().reset_index(),
        names='Segment', values='Quantity', title='📦 Quantity by Segment')
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Segment Bar Comparison
seg_df = filtered_df.groupby('Segment').agg(
    Sales=('Sales','sum'), Profit=('Profit','sum'), Quantity=('Quantity','sum')
).reset_index()

fig4 = px.bar(seg_df, x='Segment', y=['Sales','Profit','Quantity'],
    barmode='group', title='📊 Segment Full Comparison')
st.plotly_chart(fig4, use_container_width=True)