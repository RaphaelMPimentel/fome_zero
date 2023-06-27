import pandas as pd
import numpy as np
import inflection
import streamlit as st
from PIL import Image
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px

df = pd.read_csv('zomato.csv')

#limpeza
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(df):
    return COUNTRIES[df]

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(df):
    return COLORS[df]

def rename_columns(df):
    df = df.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

df['country'] = df['Country Code'].apply(country_name)
df['price_type'] = df['Price range'].apply(create_price_type)
df['colors'] = df['Rating color'].apply(color_name)
df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: str(x).split(",")[0])
df = df.dropna()
df_rename = rename_columns(df)
df1 = df_rename

df1 = df1.drop_duplicates()

#------------------------------------------------------------------------
#configuração da pagina
st.set_page_config(page_title='Country', layout='wide')

# filtro paises
st.sidebar.markdown('## Filters')
                    
paises_selecionados = st.sidebar.multiselect(
    'Choose the countries you want to view the Restaurants',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default = ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada'])

linhas_selecionadas = df1['country'].isin(paises_selecionados)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""---""")
st.sidebar.markdown('#### Powered BY Raphael Pimentel')

#inicio pagina
st.title('Country Perspective')
st.markdown("""---""")

with st.container():
    
    st.markdown('##### Number of restaurants registered BY Country')
    cols = ['restaurant_id', 'country']
    df2 = df1.loc[:, cols].groupby('country').count().reset_index()
    df2.columns = ['Country', 'Amount of Restaurants']
    fig = px.bar(df2, x='Country', y='Amount of Restaurants')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    
    st.markdown('##### Number of restaurants registered BY City')
    cols = ['city', 'restaurant_id']
    df2 = df1.loc[:, cols].groupby('city').count().reset_index()
    df2.columns = ['City', 'Amount of Restaurants']
    fig = px.bar(df2, x='City', y='Amount of Restaurants')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown('##### Average ratings BY Country')
        cols = ['country', 'votes']
        df2 = df1.loc[:, cols].groupby('country').mean().reset_index()
        df2.columns = ['Country', 'Amount of Ratings']
        fig = px.bar(df2, x='Country', y='Amount of Ratings')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown('##### Average cost for two BY Country')
        cols = ['country', 'average_cost_for_two']
        df2 = df1.loc[:, cols].groupby('country').mean().reset_index()
        df2.columns = ['Country', 'Average cost for TWO']
        fig = px.bar(df2, x='Country', y='Average cost for TWO')
        st.plotly_chart(fig, use_container_width=True)
