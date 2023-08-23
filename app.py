import os
import warnings

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
warnings.filterwarnings('ignore')
st.set_page_config(page_title = "Demo Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Alfa-TKG Dashboard Demo")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

# Read data
df = pd.read_csv("1_data.csv")
# Date selection
df['date'] = pd.to_datetime(df['date'])

start_date1 = df['date'].min()
end_date2 = df['date'].max()
coll1, coll2 = st.columns(2)
with coll1:
    start_date = pd.to_datetime(st.date_input("Start Date", start_date1))
    
with coll2:
    end_date = pd.to_datetime(st.date_input("End Date", end_date2))
    
df = df[(df["date"]>=start_date) & (df["date"]<=end_date)].copy()
# =============================================================================

# side bar
st.sidebar.title("Filter")
region = st.sidebar.multiselect("Month", df["month"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["month"].isin(region)].copy()

state = st.sidebar.multiselect("Material", df2["material"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["material"].isin(state)].copy()
# =============================================

# PREVIOUS DAY TIMELINE
st.markdown("<h2 style='text-align: center; color: #0095eb;'>Previous day timeline</h2>", unsafe_allow_html=True)
wrk = pd.DataFrame([
    dict(Start='2022-01-01 09:00:00', Finish='2022-01-01 10:30:00', Resource="Working hours"),
    dict(Start='2022-01-01 10:45:00', Finish='2022-01-01 11:30:00', Resource="Working hours"),
    dict(Start='2022-01-01 12:00:00', Finish='2022-01-01 13:00:00', Resource="Working hours"),
    dict(Start='2022-01-01 14:00:00', Finish='2022-01-01 16:30:00', Resource="Working hours"),
    dict(Start='2022-01-01 17:00:00', Finish='2022-01-01 17:30:00', Resource="Working hours"),
    dict(Start='2022-01-01 18:00:00', Finish='2022-01-01 21:00:00', Resource="Working hours"),

    dict(Start='2022-01-01 10:30:00', Finish='2022-01-01 10:45:00', Resource="Break Time"),
    dict(Start='2022-01-01 13:00:00', Finish='2022-01-01 14:00:00', Resource="Break Time"),
    dict(Start='2022-01-01 17:30:00', Finish='2022-01-01 18:00:00', Resource="Break Time"),

    dict(Start='2022-01-01 11:30:00', Finish='2022-01-01 12:00:00', Resource="Repair Time"),
    dict(Start='2022-01-01 16:30:00', Finish='2022-01-01 17:00:00', Resource="Repair Time")
])

fig = px.timeline(wrk, x_start="Start", x_end="Finish", y="Resource", color="Resource", 
                  color_discrete_sequence=["#00D100", "orange", "red"])

fig.update_layout(xaxis=dict(title='Timestamp', tickformat = '%Y/%m/%d-%H:%M'),
                  title={'text': "Work Timings",
                        # 'y':0.9,
                        # 'x':0.5,
                        # 'xanchor': 'center',
                        # 'yanchor': 'top',
                        'font':dict(size=25)},
                  yaxis_title=None,
                  title_font_family="Times New Roman",
                  title_font_color="#ffdd00")
# https://community.plotly.com/t/border-line-plot-with-different-line-width-styling-a-figure-corporate-design/53331
fig.update_yaxes(showline=True, linewidth=1.5, linecolor='white', 
                  gridcolor='#757575', gridwidth=1,
                   zeroline=True, zerolinewidth=1.5, zerolinecolor='white',
)

st.plotly_chart(fig, use_container_width=True)
# ========================================================================================================================

# OVERALL PERFORMANCE
st.markdown("<h2 style='text-align: center; color: #0095eb;'>Overall Performance</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns((4))
with col1:
    pro = df2.groupby('material')['good_products'].sum().rename('Good_products').reset_index()
    pi_pro = px.pie(pro, values='Good_products', names='material', title='Good Products')
    pi_pro.update_traces(hole=.4,)
    pi_pro.update_layout(showlegend=False)
    pi_pro.update_layout(title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top','font':dict(size=20)},
                  title_font_family="Times New Roman",
                  title_font_color="#ffdd00")
    st.plotly_chart(pi_pro, use_container_width=True)
    
with col2:
    defe = df2.groupby('material')['defeacted_product'].sum().rename('Defected_products').reset_index()
    pi_defe = px.pie(defe, values='Defected_products', names='material', title='Defected Products')
    pi_defe.update_layout(showlegend=False)
    pi_defe.update_traces(hole=.4,)
    pi_defe.update_layout(title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top','font':dict(size=20)},
                  title_font_family="Times New Roman",
                  title_font_color="#ffdd00")
    st.plotly_chart(pi_defe, use_container_width=True)
    
with col3:
    wrk_time = df2.groupby('material')['total_work_time'].sum().rename('Total_work_time').reset_index()
    pi_wrk_time = px.pie(wrk_time, values='Total_work_time', names='material', title='Total Working Hours')
    pi_wrk_time.update_layout(showlegend=False)
    pi_wrk_time.update_traces(hole=.4,)
    pi_wrk_time.update_layout(title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top','font':dict(size=20)},
                  title_font_family="Times New Roman",
                  title_font_color="#ffdd00")
    st.plotly_chart(pi_wrk_time, use_container_width=True)
with col4:
    wrk_repair_time = df2.groupby('material')['total_repair_time'].sum().rename('Total_repair_time').reset_index()
    pi_wrk_repair_time = px.pie(wrk_repair_time, values='Total_repair_time', names='material', title='Total Repair Hours')
    pi_wrk_repair_time.update_layout(showlegend=False)
    pi_wrk_repair_time.update_traces(hole=.4,)
    pi_wrk_repair_time.update_layout(title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top','font':dict(size=20)},
                  title_font_family="Times New Roman",
                  title_font_color="#ffdd00")
    st.plotly_chart(pi_wrk_repair_time, use_container_width=True)
# ========================================================================================================================
    
# BARCHART
### Total Working Hours
st.markdown("<h2 style='text-align: center; color: #0095eb;'>Overall Performance Hours</h2>", unsafe_allow_html=True)

work_hours = df3.groupby('month')['total_work_time'].sum().rename('Total_hours').reset_index()
wrk_hrs = px.bar(work_hours, x='month', y='Total_hours', title='Total Working Time', color_discrete_sequence=['#02c235'])
wrk_hrs.update_layout(title={'font':dict(size=25)},
                  title_font_family="Times New Roman",
                  title_font_color="#ffdd00")
st.plotly_chart(wrk_hrs, use_container_width=True)
### Total Repair Hours
work_repair_hours = df3.groupby('month')['total_repair_time'].sum().rename('Total_repair_hours').reset_index()
wrk__rpe_hrs = px.bar(work_repair_hours, x='month', y='Total_repair_hours', title='Total Repair Time', color_discrete_sequence=['red'])
wrk__rpe_hrs.update_layout(title={'font':dict(size=25)},
                  title_font_family="Times New Roman",
                  title_font_color="#ffdd00")
st.plotly_chart(wrk__rpe_hrs, use_container_width=True)
# ========================================================================================================================


# ABOUT PRODUCTS
st.markdown("<h2 style='text-align: center; color: #0095eb;'>About Products</h2>", unsafe_allow_html=True)
chart1, chart2 = st.columns((2))
with chart1:
    # st.markdown("<h3 style='text-align: center; color: #0095eb;'>Good products</h3>", unsafe_allow_html=True)
    good_products = df3.groupby('month')['good_products'].sum().rename('Good_products').reset_index()
    good_productss = good_products.sort_values(by='Good_products', ascending=False)
    print(good_productss)
    good_product = px.bar(good_productss, x='month', y='Good_products', color_discrete_sequence=['#02c235'], title="Good Products")
    st.plotly_chart(good_product, use_container_width=True)
with chart2:
    # st.markdown("<h3 style='text-align: center; color: #0095eb;'>Defected products</h3>", unsafe_allow_html=True)
    defected_products = df3.groupby('month')['defeacted_product'].sum().rename('Defected_products').reset_index()
    defected_productss = defected_products.sort_values(by='Defected_products', ascending=False)
    print( defected_productss)
    defected_products = px.bar(defected_products, x='month', y='Defected_products', color_discrete_sequence=['red'], title="Defected Products")
    st.plotly_chart(defected_products, use_container_width=True)
    
# ========================================================================================================================
