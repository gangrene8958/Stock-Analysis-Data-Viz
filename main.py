import streamlit as st
import pandas as pd
import plotly.express as px
from scraping import ticker_info

st.title('Stock Analysis Data Viz')

ticker_input = st.text_input('Insert Ticker (US markets only)')
df = ticker_info(ticker_input)

st.divider()

# 3. Selecció dinàmica de columnes
if df is not None:
    st.dataframe(df)
    available_fields = df.columns.tolist()
    selection = st.multiselect(
    "Select columns to plot",
    options=available_fields
    )

    if selection:
        st.subheader("Bar Plot")
        

        # Multiselect: l'usuari pot triar tantes com vulgui
        
        # 4. Crear el gràfic de barres amb Plotly
        # barmode='group' posa les barres una al costat de l'altra si n'hi ha més d'una
        fig = px.bar(
            df, 
            x=df.index, 
            y=selection, 
            title=f"Evolution of {', '.join(selection)} - {ticker_input.upper()}",
            barmode='group',
            height=500,
            text_auto = True
        )
        
        fig.update_layout(
            xaxis_title="Fiscal Year",
            yaxis_title="(M$)",
            legend_title="Metrics"
        )
        
        

        on = st.toggle('View CAGR growth')

        if on:
            for i in selection:
                initial_value = float(df[i].iloc[0])
                final_value = float(df[i].iloc[-1])

                cagr = ((final_value / initial_value) ** (1 / len(df.index)) - 1) * 100

                fig.add_shape(
                type="line",
                x0=df.index[0], y0=initial_value,
                x1=df.index[-1], y1=final_value,
                line=dict(color="#51A49E", width=2, dash="dash"),
                )

                idx_middle = len(df) // 2
                x_middle = df.index[idx_middle]
                
                y_middle = initial_value + (final_value - initial_value) * (idx_middle / (len(df) - 1))
                
                fig.add_annotation(
                    x=x_middle,
                    y=y_middle,
                    text=f"<b>CAGR: {cagr:.1f}%</b>",
                    showarrow=False,
                    font=dict(color="white", size=13, family="Arial"),
                    bgcolor="#51A49E",      # Color de fons de l'etiqueta
                    bordercolor="#51A49E",  # Color de la vora
                    borderpad=6,
                    yshift=15  # Desplaça la lletra una mica cap amunt perquè no la talli la línia
                )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select a field to plot")
