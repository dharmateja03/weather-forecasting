import os
import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb



owm=pyowm.OWM('ffd13df7ab936bfc133064b9b7b4cedd')

mgr=owm.weather_manager()

degree_sign= u'\N{DEGREE SIGN}'

st.title("5 Day Weather Forecast")


st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")

place=st.text_input("NAME OF THE CITY :", "")


if place == None:
    st.write("Input a CITY!")



unit=st.selectbox("Select Temperature Unit",("Celsius","Fahrenheit"))

g_type=st.selectbox("Select Graph Type",("Line Graph","Bar Graph"))

if unit == 'Celsius':
    unit_c = 'celsius'
else:
    unit_c = 'fahrenheit'


def get_temperature():
    days = []
    dates = []
    temp_min = []
    temp_max = []
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast=forecaster.forecast
    for weather in forecast:
        day=datetime.utcfromtimestamp(weather.reference_time())
        #day = gmt_to_eastern(weather.reference_time())
        date = day.date()
        if date not in dates:
            dates.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not temp_min[-1] or temperature < temp_min[-1]:
            temp_min[-1] = temperature
        if not temp_max[-1] or temperature > temp_max[-1]:
            temp_max[-1] = temperature
    return(days, temp_min, temp_max)

def init_plot():
     plt.figure('PyOWM Weather', figsize=(5,4))
     plt.xlabel('Day')
     plt.ylabel(f'Temperature ({degree_sign}F)')
     plt.title('Weekly Forecast')



def plot_temperatures(days, temp_min, temp_max):
    # days = dates.date2num(days)
    fig = go.Figure(
        data=[
            go.Bar(name='minimum temperatures', x=days, y=temp_min),
            go.Bar(name='maximum temperatures', x=days, y=temp_max)
        ]
    )
    fig.update_layout(barmode='group')
    return fig


def plot_temperatures_line(days, temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temp_min, name='minimum temperatures'))
    fig.add_trace(go.Scatter(x=days, y=temp_max, name='maximimum temperatures'))
    return fig

def label_xaxis(days):
    plt.xticks(days)
    axes = plt.gca()
    xaxis_format = dates.DateFormatter('%m/%d')
    axes.xaxis.set_major_formatter(xaxis_format)

def draw_bar_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures(days, temp_min, temp_max)
    # write_temperatures_on_bar_chart(bar_min, bar_max)
    st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperatures")
    for i in range (0,5):
        st.write("### ",temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)


def draw_line_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures_line(days, temp_min, temp_max)
    st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperatures")
    for i in range (0,5):
        st.write("### ",temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)

def other_weather_updates():
    forecaster = mgr.forecast_at_place(place, '3h')
    st.title("Impending Temperature Changes :")
    if forecaster.will_have_fog():
        st.write("### FOG Alert!")
    if forecaster.will_have_rain():
        st.write("### Rain Alert")
    if forecaster.will_have_storm():
        st.write("### Storm Alert!")
    if forecaster.will_have_snow():
        st.write("### Snow Alert!")
    if forecaster.will_have_tornado():
        st.write("### Tornado Alert!")
    if forecaster.will_have_hurricane():
        st.write("### Hurricane Alert!")
    if forecaster.will_have_clouds():
        st.write("### Cloudy Skies")    
    if forecaster.will_have_clear():
        st.write("### Clear Weather!")

def cloud_and_wind():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    cloud_cov=weather.clouds
    winds=weather.wind()['speed']
    st.title("Cloud coverage and wind speed")
    st.write('### The current cloud coverage for',place,'is',cloud_cov,'%')
    st.write('### The current wind speed for',place, 'is',winds,'mph')

def sunrise_and_sunset():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    st.title("Sunrise and Sunset Times :")
    india = pytz.timezone("Asia/Kolkata")
    ss=weather.sunset_time(timeformat='iso')
    sr=weather.sunrise_time(timeformat='iso')  
    st.write("### Sunrise time in",place,"is",sr)
    st.write("### Sunset time in",place,"is",ss)

def updates():
    other_weather_updates()
    cloud_and_wind()
    sunrise_and_sunset()

hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)
def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 100px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(1, 1, "auto", "auto"),
        border_style="inset",
        border_width=px(0)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def footer():
    myargs = [
    "Made in ",
    image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
          width=px(35), height=px(35)),
    " with ❤️ by DharmaTeja",
    br(),
    link("https://www.linkedin.com/in/dharma-t-015402132/", image('https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.IfuhJTGsN34WQqAZIdufvQHaHa%26pid%3DApi&f=1',width=px(35), height=px(35))),
    
    link("https://github.com/dharmateja03", image('https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.w4Zs5bS5enpd8KSYe7s5JQHaHa%26pid%3DApi&f=1',width=px(35), height=px(35))),
    
    
]
    layout(*myargs)


if __name__ == '__main__':
    footer()
    
    if st.button("SUBMIT"):
        if g_type == 'Line Graph':
            draw_line_chart()    
        else:
            draw_bar_chart()
        updates()
