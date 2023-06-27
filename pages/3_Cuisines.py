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
st.set_page_config(page_title='Cuisines', layout='wide')

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

restaurantes_selecionados = st.sidebar.slider(
    'Select the number of Restaurants you want to view',
    value = 10,
    min_value = 1,
    max_value = 20)

linhas_selecionadas = df1['restaurant_id'] <= restaurantes_selecionados
df2 = df1.loc[linhas_selecionadas, :]

cuisinesdf1 = df1['cuisines'].unique().tolist()

cuisines_selecionadas = st.sidebar.multiselect(
    'Choose types of Cuisine',
    cuisinesdf1,
    default = ['Home-made', 'BBQ', 'Japanese', 'Brazilian','Arabian','American','Italian'])

linhas_selecionadas = df1['country'].isin(paises_selecionados)
df2 = df1.loc[linhas_selecionadas, :]
   
linhas_selecionadas = df1['cuisines'].isin(cuisines_selecionadas)
df3 = df2.loc[linhas_selecionadas, :]

st.sidebar.markdown("""---""")
st.sidebar.markdown('#### Powered BY Raphael Pimentel')

#inicio pagina
st.title('Cuisines Perspective')
st.markdown("""---""")

st.markdown('## Best Restaurants of the Main Type of Cuisine')

with st.container():
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        
        restaurante = df1[df1['cuisines']\
                .str.contains('Italian')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italian: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Country: {restaurante.iloc[0, 3]} 
                  \nCity: {restaurante.iloc[0, 4]} 
                  \nAverage cost for two: {restaurante.iloc[0, 5]}''')
        
    with col2:
        
        restaurante = df1[df1['cuisines']\
                .str.contains('American')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italian: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Country: {restaurante.iloc[0, 3]} 
                  \nCity: {restaurante.iloc[0, 4]} 
                  \nAverage cost for two: {restaurante.iloc[0, 5]}''')
        
    with col3:
        
        restaurante = df1[df1['cuisines']\
                .str.contains('Arabian')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italian: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Country: {restaurante.iloc[0, 3]} 
                  \nCity: {restaurante.iloc[0, 4]} 
                  \nAverage cost for two: {restaurante.iloc[0, 5]}''')
    with col4:
        
        restaurante = df1[df1['cuisines']\
                .str.contains('Japanese')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italian: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Country: {restaurante.iloc[0, 3]} 
                  \nCity: {restaurante.iloc[0, 4]} 
                  \nAverage cost for two: {restaurante.iloc[0, 5]}''')
    with col5:
        
        restaurante = df1[df1['cuisines']\
                .str.contains('Brazilian')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italian: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Country: {restaurante.iloc[0, 3]} 
                  \nCity: {restaurante.iloc[0, 4]} 
                  \nAverage cost for two: {restaurante.iloc[0, 5]}''')
        
with st.container():       

    st.markdown(f'## Top {restaurantes_selecionados} Restaurants')
    cols = ['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']
    restaurante = df3.loc[:, cols].sort_values('aggregate_rating', ascending=False)
    st.dataframe(restaurante.head(restaurantes_selecionados))
    
    
st.markdown("""---""")

with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown(f'##### Top {restaurantes_selecionados} best types of Cuisine')
        cols = ['aggregate_rating', 'cuisines']
        df4 = df2.loc[:, cols].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=False).reset_index()
        df4.columns = ['Types of Cuisines', 'Average Ratings']
        df4final = df4.head(restaurantes_selecionados)
        fig = px.bar(df4final, x='Types of Cuisines', y='Average Ratings')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        
        st.markdown(f'##### Top {restaurantes_selecionados} worst types of Cuisine')
        cols = ['aggregate_rating', 'cuisines']
        df4 = df2.loc[:, cols].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=True).reset_index()
        df4.columns = ['Types of Cuisines', 'Average Ratings']
        df4final = df4.head(restaurantes_selecionados)
        fig = px.bar(df4final, x='Types of Cuisines', y='Average Ratings')
        st.plotly_chart(fig, use_container_width=True)
        