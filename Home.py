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

#configuração da pagina
st.set_page_config(
    page_title='Home',
    layout='wide'
)

#barra lateral
#image = Image.open('logo.png')
#st.sidebar.image(image, width=200)
st.sidebar.title('FOME ZERO')

st.sidebar.markdown("""---""")

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
df2 = df1.loc[linhas_selecionadas, :]

#botao de download dados tratados
csv = df1.to_csv(index=False)
st.sidebar.markdown ('### Cleaned Data')
st.sidebar.download_button(label='Download data as CSV', data=csv, file_name='fome_zero.csv', mime='text/csv')

st.sidebar.markdown("""---""")
st.sidebar.markdown('#### Powered BY Raphael Pimentel')

#pagina inicial 
st.header('FOME ZERO')

st.markdown('### The best place to find your new favorite restaurant!')

with st.container():
    st.markdown('### We have the following brands within our platform:')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        restaurantes_unicos = len(df1['restaurant_id'].unique())
        col1.metric('Registered Restaurants', restaurantes_unicos)
        
    with col2:
        paises_unicos = len(df1['country_code'].unique())
        col2.metric('Registered Countries', paises_unicos)
        
    with col3:
        cidades_unicas = len(df1['city'].unique())
        col3.metric('Registered Cities', cidades_unicas)
        
    with col4:
        avaliacoes = df1['votes'].sum()
        col4.metric('Plataform Ratings', avaliacoes)
    
    with col5:
        culinarias = len(df1['cuisines'].unique())
        col5.metric('Types of Cuisine', culinarias)
        
#with st.container():
#    
#    df_aux = (df2.loc[:, ['city','restaurant_name','latitude','longitude']].groupby(['city','restaurant_name']).median().reset_index())
#
#    # Calcular os limites do mapa
#    min_lat = df2['latitude'].min()
#    max_lat = df2['latitude'].max()
#    min_lon = df2['longitude'].min()
#    max_lon = df2['longitude'].max()
#
#    # Calcular o centro do mapa
#    center_lat = (min_lat + max_lat) / 2
#    center_lon = (min_lon + max_lon) / 2
#
#    # Criar o mapa
#    m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
#
#    # Adicionar marcadores em cluster
#    marker_cluster = MarkerCluster().add_to(m)
#
#    fig = folium.Figure(width=1920, height=1080)
#
#
#    for index, location_info in df2.iterrows():
#
#        folium.Marker(
#            location=(location_info['latitude'], location_info['longitude']),
#            icon=folium.Icon(color=location_info['rating_color'])).add_to(marker_cluster)
#        
#    folium_static(m,width=1024,height=600)
