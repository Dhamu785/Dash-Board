import os
import warnings

import altair as at
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.figure_factory as ff

# Basic setups
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Alfa-TKG Dashboard")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)
# =============================================================================


# File upload
f1 = st.file_uploader(":file_folder: Upload file", type=["csv", "xlsx"])
if f1 is not None:
    file_name = f1.name
    st.write(f"File name: {file_name}")
    df = pd.read_csv(file_name)
else:
    df = pd.read_csv("data.csv")
    st.write("Data loaded from local")
# =============================================================================

# Date selection
df['Order Date'] = pd.to_datetime(df['Order Date'])
startdata = df['Order Date'].min()
enddata = df['Order Date'].max()

coll1, coll2 = st.columns(2)
with coll1:
    start_date = pd.to_datetime(st.date_input("Start Date", startdata))
    
with coll2:
    end_date = pd.to_datetime(st.date_input("End Date", enddata))
    
df = df[(df["Order Date"]>=start_date) & (df["Order Date"]<=end_date)].copy()
# =============================================================================

# side bar
st.sidebar.title("Filter")
region = st.sidebar.multiselect("Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)].copy()
# =============================================
    
state = st.sidebar.multiselect("State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)].copy()
# =============================================
    
city = st.sidebar.multiselect("City", df3["City"].unique())
    
if len(region) == 0 and len(state) == 0 and len(city) == 0:
    filtered_df = df.copy()
elif len(region) > 0 and len(state) == 0 and len(city) == 0:
    filtered_df = df[df['Region'].isin(region)].copy()
elif len(region) == 0 and len(state) > 0 and len(city) == 0:
    filtered_df = df[df['State'].isin(state)].copy()
elif len(region) == 0 and len(state) == 0 and len(city) > 0:
    filtered_df = df[df['City'].isin(city)].copy()
elif len(region) > 0 and len(state) > 0 and len(city) == 0:
    filtered_df = df[df['Region'].isin(region) & df['State'].isin(state)].copy()
elif len(region) > 0 and len(state) == 0 and len(city) > 0:
    filtered_df = df[df['Region'].isin(region) & df['City'].isin(city)].copy()
elif len(region) == 0 and len(state) > 0 and len(city) > 0:
    filtered_df = df[df['State'].isin(state) & df['City'].isin(city)].copy()
else:
    filtered_df = df[df['Region'].isin(region) & df['State'].isin(state) & df['City'].isin(city)].copy()
    
category_df = filtered_df.groupby(by=['Category'], as_index=False,)['Sales'].sum()
# ================================================================================

# Create a Gantt chart
source = pd.DataFrame([
        {"Machine": "A", "start": 1, "end": 3},
        {"Machine": "B", "start": 3, "end": 8},
        {"Machine": "C", "start": 9, "end": 10},
        {"Machine": "D", "start": 8, "end": 9},
        {"Machine": "E", "start": 10, "end": 13},
        {"Machine": "F", "start": 15, "end": 17},
        {"Machine": "G", "start": 13, "end": 15}    
    ])
chart = at.Chart(source).mark_bar().encode(x='start', x2='end', y='Machine')
st.subheader("Machine performance")
st.altair_chart(chart, use_container_width=True)

df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
      dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
      dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
      dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
      dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
      dict(Task="Job-3", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
      dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
      dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')]

colors = {'Not Started': 'rgb(220, 0, 0)',
          'Incomplete': (1, 0.9, 0.16),
          'Complete': 'rgb(0, 255, 100)'}

fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                      group_tasks=True, showgrid_y=True)
st.plotly_chart(fig, use_container_width=True)
# =============================================================================

# Create a bar chart
col1, col2 = st.columns(2)
with col1:
    st.subheader("Sales by Category")
    fig = px.bar(category_df, x="Category", y="Sales", color="Category", height=300)
    st.plotly_chart(fig, use_container_width=True, height=300)

with col2:
    st.subheader("Sales by region")
    fig = px.pie(filtered_df, values="Sales", names="Region", height=340, hole=0.5)
    fig.update_traces(text = filtered_df['Region'], textposition='inside')
    st.plotly_chart(fig, use_container_width=True, height=300)
# =============================================================================

co1, co2 = st.columns(2)
with co1:
    with st.expander("Sales by category"):
        st.write(category_df)
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
    
with co2:
    with st.expander("Sales by Region"):
        st.write(filtered_df.groupby(by=['Region'], as_index=False)['Sales'].sum())
        csv1 = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv1, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
# =============================================================================
        
filtered_df['year_month'] = filtered_df['Order Date'].dt.strftime('%Y-%m')
line_chart= pd.DataFrame(filtered_df.groupby(by=['year_month'], as_index=False)['Sales'].sum())
fig_line = px.line(line_chart, x="year_month", y="Sales", height=500, 
                   labels={'year_month':'Year-Month', 'Sales':'Sales in USD'},
                   template='gridon')
st.plotly_chart(fig_line, use_container_width=True, height=500)

# =============================================================================
# Create a treem based on Region, category, sub-Category
st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(filtered_df, path=['Region', 'Category', 'Sub-Category'], values='Sales',
                  hover_data = ["Sales"], color = "Sub-Category")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)
# =============================================================================

# Pie charts
chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Category", template = "gridon")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)
    
# Create a scatter plot
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity", color = "Category")
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)
    
