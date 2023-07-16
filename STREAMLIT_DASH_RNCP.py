import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import ipywidgets
import time
import random
from pySankey.sankey import sankey
import matplotlib.pyplot as plt
import random
from random import randint
import streamlit as st

from streamlit_echarts import JsCode
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Geo
from pyecharts.charts import Liquid
from pyecharts.charts import Timeline
from pyecharts.charts import WordCloud
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType




df = pd.read_csv("df_coord.csv", sep = ",")
gp = pd.pivot_table(df, index = ["year", "geo", "lon", "lat"], values="review", aggfunc ="count").reset_index()

df_1 = pd.read_csv("df_pred.csv", sep = ",")
df_1.dropna(subset ="sentiment", axis = 0, inplace =True)


df_count = df_1.groupby(["type","sentiment"]).count().reset_index()

df_count = df_count[["type","sentiment","review"]]


#DATA PIE
pie = df_1["sentiment"].value_counts()
pie  = pd.Series.to_frame(pie)

list_x = pie.index.tolist()
list_y = pie.sentiment.tolist()

dict_1 = pie.to_dict()

x_data = list_x
y_data = list_y
data_pair = [list(z) for z in zip(x_data, y_data)]
data_pair.sort(key=lambda x: x[1])


#--------------------------------------------------------------------------- MISE EN PAGE
#Suppréssion des bordures droite et gauches
st.set_page_config(layout="wide")

#Suppréssion des bordures Haute
page_Top = f"""<style>
.appview-container .main .block-container{{
max-width: 100%;
padding-top: {0.5}rem;
padding-right: {1}rem;
padding-left: {1}rem;
padding-bottom: {1}rem}}
</style>"""

st.markdown(page_Top, unsafe_allow_html=True)

#Supprime le header blanc en partie suppérieur
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url(https://image.noelshack.com/fichiers/2023/21/3/1684934164-degrade-fin.png);
background-size: 0%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

#--------------------------------------------------------------------------- MAP ANIMATION  + SLIDER


c1,c2,c3, c4 = st.columns([0.5,8,0.2,5])

#Reduit l'espace entre ligne
st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(4) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)

    
with c1 :
    animations = {"OFF": None, "ON": 1}
    animate = st.radio("", options=list(animations.keys()), index=1)
    animation_speed = animations[animate]
with c2 : 
    year_slider = st.empty()
with c1 :
    deck_map = st.empty()



    def render_slider(year):
        key = random.random() if animation_speed else None

        year_value = year_slider.slider(
            "",
            min_value=2012,
            max_value=2023,
            value= year,
            key=key,
        )
        

        
         
        
        #Return les value de la slide
        year = year_value
        return year



    def render_map(year):

        df_year = gp[gp['year'] == year]

        deck_map.pydeck_chart(
            pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v11",
            initial_view_state=pdk.ViewState(
            latitude=48.2,
            longitude=2.48,
            zoom=4,
            pitch=40,
            height=500, 
            width= 900,
        ),  
       layers = pdk.Layer(
            'ColumnLayer',
            data=df_year,
            get_position=['lon', 'lat'],
            get_elevation='review',
            elevation_scale=100000,
            radius=10000,
            get_color="[223,10,225/ review *40, 50, 80]",
            pickable=True,
            auto_highlight=True,
            )
    ))

    if animation_speed :
        for year in range (2012,2024,1):

            time.sleep(animation_speed)
            render_slider(year)
            render_map(year)

    else:
        year = render_slider(2022)
        render_map(year)
   

#COULEUR CURSEUR

ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)


Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
background-color: rgb(212, 146, 222); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)


Slider_Number = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div > div
                        { color: rgb(14, 38, 74); } </style>''', unsafe_allow_html = True)


col = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div {{
    background: linear-gradient(to right, rgb(223, 223, 223) 0%, 
                            rgb(1, 183, 158) {year}%, 
                            rgba(151, 166, 195, 0.25) {year}%, 
                            rgba(151, 166, 195, 0.25) 100%); }} </style>'''
        
ColorSlider = st.markdown(col, unsafe_allow_html = True) 

#--------------------------------------------------------------------------- Pyechart
        


#PIE RADIUS VIDE
c = (
    Pie()
    .add(
        "",
        data_pair,
        radius=["30%", "70%"],
        center=["70%", "50%"],
        rosetype="radius",

    )
    .set_colors(["#E8DAEF", "#D2B4DE", "#A569BD"])
    .set_global_opts(title_opts=opts.TitleOpts(title="Pie"))


)



#PIE RADIUS PLEIN
d = (
    Pie(init_opts=opts.InitOpts(bg_color="#FFFFFF"))
    .add(
        series_name="访问来源",
        data_pair=data_pair,
        rosetype="radius",
        radius="60%",
        center=["70%", "50%"],
        label_opts=opts.LabelOpts(is_show=True, position="center",)
    )
    .set_colors(["#FCF3CF", "#F9E79F", "#F7DC6F"])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="Customized Pie",
            pos_left="right",
            pos_top="20",
            title_textstyle_opts=opts.TextStyleOpts(color="#808080"),
        ),
        legend_opts=opts.LegendOpts(is_show=True),
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(color="rgba(100, 100, 100, 1)"),
    )

)



#PIE RADIUS PLEIN 2

d_2 = {
    "backgroundColor": "#FFF",
    "title": {
        "text": "Customized Pie",
        "left": "center",
        "top": 20,
        "textStyle": {"color": "#808080"},
    },
    "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b} : {c} ({d}%)"},
    "visualMap": {
        "show": False,
        "min": 80,
        "max": 600,
        "inRange": {"colorLightness": [0, 1]},
    },
    "series": [
        {
            "name": "Source of interview",
            "type": "pie",
            "radius": "60%",
            "center": ["70%", "50%"],
            "data": [
                {"value": 235, "name": "Video Ad"},
                {"value": 274, "name": "Affiliate Ad"},
                {"value": 310, "name": "Email marketing"},
                {"value": 335, "name": "Direct access"},
                {"value": 400, "name": "Search engine"},
            ],
            "roseType": "radius",
            "label": {"color": "rgba(30, 30, 30, 0.3)"},
            "labelLine": {
                "lineStyle": {"color": "rgba(30, 30, 30, 0.3)"},
                "smooth": 0.2,
                "length": 10,
                "length2": 20,
            },
            "itemStyle": {
                "color": "#E8DAEF",
                "shadowBlur": 200,
                "shadowColor": "rgba(0, 0, 0, 0)",
            },
            "animationType": "scale",
            "animationEasing": "elasticOut",
        }
    ],
}








#--------------------------------------------------------------------------- SANKEY


color = { 
    "Google Play" : "#D2B4DE",
    "glassdoor" : "#7D3C98",
    "indeed" : "#D4E6F1",
    "trustpilot" : "#7FB3D5",
    1 : "#BDC3C7",
    0 : "#BDC3C7",
    -1 : "#BDC3C7"
}


sankey(
    left = df_count["type"], right = df_count["sentiment"],
    leftWeight = df_count["review"], rightWeight = df_count["review"],
    fontsize = 12,
    colorDict = color
)

plt.gcf().set_size_inches((8,4))
plt.title('Distribution par type')






#--------------------------------------------------------------------------- grid


c5, c6, c7 = st.columns([6,0.2,5])


with c4 :
    st_pyecharts(c)
    st_pyecharts(d, key = random.random())
    
    
with c5 :
    st.pyplot(plt)
    
with c7 :    
    st_echarts(options=d_2)
