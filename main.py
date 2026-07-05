import streamlit as st
import pandas as pd
import plotly.express as px
from scraping import ticker_info

st.title('Stock Analysis Data Viz')

ticker_input = st.text_input('Write Ticker')
df = ticker_info(ticker_input)

st.divider()

# 3. Selecció dinàmica de columnes
if df is not None:
    st.dataframe(df)
    columnes_disponibles = df.columns.tolist()
    seleccio = st.multiselect(
    "Select columns to plot",
    options=columnes_disponibles
    )

    if seleccio:
        st.subheader("Bar Plot")
        

        # Multiselect: l'usuari pot triar tantes com vulgui
        
        # 4. Crear el gràfic de barres amb Plotly
        # barmode='group' posa les barres una al costat de l'altra si n'hi ha més d'una
        fig = px.bar(
            df, 
            x=df.index, 
            y=seleccio, 
            title=f"Evolution of {', '.join(seleccio)} - {ticker_input.upper()}",
            barmode='group',
            height=500
            text_auto = True
        )
        
        fig.update_layout(
            xaxis_title="Fiscal Year",
            yaxis_title="(M$)",
            legend_title="Metrics"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.button('Show YoY Growth')
    else:
        st.info("Select a field to plot")
