import pandas as pd
import streamlit as st
import plotly.express as px  
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import requests



st.set_page_config(page_title="Industrial Human Resource Geo-Visualization",
                   layout="wide",
                   initial_sidebar_state ="auto",
                   menu_items={'About': "This was done by Narmadha Devi B"})


with st.sidebar:
    selected = option_menu(None, ["Home", "Explore Data", "Data Visualization"],
                           icons=["house", "graph-up-arrow", "bar-chart-line"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link-selected": {"background-color": "#FF5A5F"}}
                           )

df = pd.read_csv("Final_IHR.csv")


if selected == "Home":
    st.title(':red[Industrial Human Resource Geo-Visualization]')
    st.subheader(':blue[Domain:] Resource Management')
    st.subheader(':blue[Overview:] Created a Dashboard with Streamlit using Plotly to Visualize the workers population of various industries with respect to various geographies and Analyze some Facts and Figures for the Business Problem')
    st.subheader(':blue[Skills Take Away:] Python Scripting, Data Preprocessing, EDA (Exploratory Data Analysis) , Visualization, NLP (Natural Language Processing), Streamlit')



if selected == "Explore Data":
    
    st.header(':red[Industrial Human Resource Geo-Visualization]')

    Workers_Type = st.sidebar.selectbox("****Workers_Type****", ("Overall Workers", "Workers Types"))
    
    if Workers_Type == "Overall Workers":
        
        data = df.groupby('State Name')[['Total Workers']].sum().reset_index()
        
        fig = px.scatter(
            data,
            x='State Name',
            y='Total Workers',
            title="TOTAL WORKERS POPULATION BY STATE",
            labels={'State Name': 'States', 'Total Workers': 'Number of Workers'},
            size='Total Workers',  # Bubble size based on population
            color='State Name',  
            )
        st.plotly_chart(fig)


        data = df.groupby('State Name')[['Total Male Works', 'Total Women Works']].sum().reset_index()

        fig = px.bar(
            data,
            x='State Name',
            y=['Total Male Works', 'Total Women Works'],
            title="TOTAL MALE AND FEMALE WORKERS BY STATE",  
            labels={'State Name': 'States', 'Total Male Works': 'Total Male Workers', 'Total Women Works': 'Total Female Workers'},  
            barmode='stack',  # Stacked bar
            color='State Name' 
            
        )
        st.plotly_chart(fig)

    if Workers_Type == "Workers Types":

        # Define the data columns
        Rural_data = ['Main Workers Rural Persons', 'Main Workers Rural Males', 'Main Workers Rural Females']
        Urban_data = ['Main Workers Urban Persons', 'Main Workers Urban Males', 'Main Workers Urban Females']
        Total_data = df[['Main Workers Total Persons', 'Main Workers Total Males', 'Main Workers Total Females']].iloc[0].values

        # Sum the data
        Sum_of_Rural = df[Rural_data].sum().values
        Sum_of_Urban = df[Urban_data].sum().values

        # Create the bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(x=['Total Persons', 'Total Males', 'Total Females'], y=Sum_of_Rural, name='Rural Workers'))
        fig.add_trace(go.Bar(x=['Total Persons', 'Total Males', 'Total Females'], y=Total_data, name='Total Workers'))
        fig.add_trace(go.Bar(x=['Total Persons', 'Total Males', 'Total Females'], y=Sum_of_Urban, name='Urban Workers'))

 
        fig.update_layout(
            title="COMPARISION OF MAIN RURAL, URBAN AND TOTAL WORKERS ",
            xaxis_title="Category of Workers",
            yaxis_title="Number of Workers",
            barmode='stack',  # Stacked bars
            legend_title="Worker Type",
            template="plotly_dark"  
        )
        st.plotly_chart(fig)



        marginal_cols_rural = ['Marginal Workers Rural Persons', 'Marginal Workers Rural Males', 'Marginal Workers Rural Females']
        marginal_cols_urban = ['Marginal Workers Urban Persons', 'Marginal Workers Urban Males', 'Marginal Workers Urban Females']
        # Sum the data for each category
        marginal_data_rural = df[marginal_cols_rural].sum().values
        marginal_data_urban = df[marginal_cols_urban].sum().values
        categories = ['Total Persons', 'Males Workers', 'Females Workers']
        fig = go.Figure()

        # Add bars for Rural workers
        fig.add_trace(go.Bar(
            x=categories, 
            y=marginal_data_rural, 
            name='Rural'  
        ))

        # Add bars for Urban workers
        fig.add_trace(go.Bar(
            x=categories, 
            y=marginal_data_urban, 
            name='Urban'  
        ))

        fig.update_layout(
            title="COMPARISION OF MARGINAL RURAL, URBAN AND TOTAL WORKERS",
            xaxis_title="Category of Workers",  
            yaxis_title="Number of Workers",  
            barmode='group',  # Grouped bar chart
            legend_title="Worker Type",  
            height=500
        )
        st.plotly_chart(fig)
    
       
        rural_cols = ['Main Workers Rural Persons', 'Marginal Workers Rural Persons']
        urban_cols = ['Main Workers Urban Persons', 'Marginal Workers Urban Persons']

        # Group and sum the data by State Name
        rural_data = df[['State Name'] + rural_cols].groupby('State Name').sum().reset_index()
        urban_data = df[['State Name'] + urban_cols].groupby('State Name').sum().reset_index()

        # Melt the data to long format
        rural_data_melted = rural_data.melt(id_vars='State Name', var_name='WorkerType', value_name='Count')
        urban_data_melted = urban_data.melt(id_vars='State Name', var_name='WorkerType', value_name='Count')

        # Combine the data (if necessary, for one plot)
        combined_data = pd.concat([rural_data_melted, urban_data_melted])

        # Create the line plot using Plotly 
        fig = px.line(combined_data, x='State Name', y='Count', color='WorkerType',
                    title='Worker Distribution by State: Rural vs Urban (Main & Marginal)',
                    labels={'Count': 'Total Workers Count', 'State Name': 'States'},
                    markers=True,  
                    template='plotly_white')

        fig.update_layout(
            xaxis_title='State Name',
            yaxis_title='Total Workers Count',
            showlegend=True,
            height=600,  
            width=1000   
        )
        st.plotly_chart(fig)




if selected == "Data Visualization":

    st.header(':red[Industrial Human Resource Geo-Visualization]')

    def fetch_geojson():
        geojson_url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson"
        response = requests.get(geojson_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch GeoJSON data")
            return None  
        
    # Fetch the GeoJSON data
    geojson_data = fetch_geojson()

    if geojson_data:  
        
        geojson_state_names = set(feature['properties']['NAME_1'] for feature in geojson_data['features'])

        # State names from DataFrame
        dataframe_state_names = set(df['State Name'])
        col1, col2, col3 = st.columns(3)
        with col1:

        # Select box for type of worker type
            Workers_Type = st.selectbox('Select Workers Type', ['Main Workers', 'Marginal Workers'])
        with col2:
        # Select box for gender
            Gender_Type = st.selectbox('Select Gender', ['Males', 'Females'], key="sex_type_selectbox")
        with col3:
        # Select box for area
            Area_Type = st.selectbox('Select Area Type', ['Rural', 'Urban'], key="area_type_selectbox")

        # Construct column name based on selected worker type, sex, and area
        column_name = f'{Workers_Type} {Area_Type} {Gender_Type}'  #

        if column_name in df.columns:
            fig = go.Figure(go.Choroplethmapbox(
                geojson=geojson_data,
                locations=df['State Name'],  # Use the column with state names
                featureidkey="properties.NAME_1",  # Key in geojson to match with DataFrame
                z=df[column_name],  # Use the column for analysis
                colorscale='Viridis',
                zmin=df[column_name].min(),
                zmax=df[column_name].max(),
                marker_opacity=0.7,
                marker_line_width=0,
            ))

            fig.update_layout(
                mapbox_style="carto-positron",
                mapbox_zoom=3,
                mapbox_center={"lat": 20.5937, "lon": 78.9629},
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                title=f"{Workers_Type} ({Gender_Type}, {Area_Type}) Population Across Indian States",
                title_x=0.5
            )
            st.plotly_chart(fig)
      































