import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from plotly import graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import plotly.figure_factory as ff

def draw_hist(df, labels):
    # x1 = df
    # x1 = df.loc[df["action"] == "checkout", "hour_of_day"]
    # x2 = df.loc[df["action"] == "view", "hour_of_day"]
    # x3 = df.loc[df["action"] == "add", "hour_of_day"]
    # x4 = df.loc[df["action"] == "remove", "hour_of_day"]
    # Group data together
    hist_data = [df.loc[df["action"] == labels, "hour_of_day"]]

    # st.write(hist_data)
    group_labels = [labels]

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[.1])

    # Plot!
    st.plotly_chart(fig, use_container_width=True)

def draw_bar(brand_count, color="#3FA2F6"):
    chart_data = pd.DataFrame(
        {"col1": list(brand_count.iloc[:, 0]), "col2": brand_count.iloc[:, 1]}
    )
    # st.write(chart_data)
    st.bar_chart(
        chart_data, x="col1", y=["col2"], color=[color]  # Optional
    )

def draw_line(data_chart):
   chart_data = pd.DataFrame(
        {
        "time in a day": list(data_chart.iloc[:, 0]),
        "view": data_chart.loc[data_chart["action"] == "view" , "hour_count"],
        "add": data_chart.loc[data_chart["action"] == "add" , "hour_count"], 
        "remove": data_chart.loc[data_chart["action"] == "remove" , "hour_count"],
        "checkout": data_chart.loc[data_chart["action"] == "checkout" , "hour_count"]
         }
    )
   chart_data = chart_data.groupby("time in a day", as_index=False).sum()
#    st.write(chart_data)
   st.line_chart(chart_data, x="time in a day", y=["view", "add", "remove", "checkout"]) 


def draw_wordcloud(text_df):
    doc = text_df.iloc[0, 0]
    wc = WordCloud(
        background_color='white',
        stopwords=STOPWORDS,
        height=600,
        width=400
    )
    wc.generate(doc)
    # wc.to_file("test_wc.png")
    print(doc)

def draw_pie(gender_count):
    labels = 'male', 'female'
    sizes = gender_count
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # st.pyplot(fig1)
    return fig1

def draw_funnel(action_count):
    fig = go.Figure(go.Funnel(
    y = ["Website visit", "View product", "Add to cart/wishlist", "Checkout"],
    x = action_count,
    textposition = "inside",
    textinfo = "value+percent initial",
    opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal"],
    "line": {"width": [4, 2, 2, 3, 1], "color": ["wheat", "wheat", "blue", "wheat"]}},
    connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
    )

    return fig

def draw_map(cordinate):
    chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [21.02, 105.78],
    columns=['latitude', 'longitude'])
    # st.write(cordinate)
    # df_duplicate = pd.concat([cordinate]*10, ignore_index=True)
    # chart_data = cordinate

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=21.02,
            longitude=105.78,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
            'HexagonLayer',
            data=chart_data,
            get_position='[longitude, latitude]',
            radius=200,
            elevation_scale=10,
            elevation_range=[0, len(chart_data)],
            pickable=True,
            extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    )
    )