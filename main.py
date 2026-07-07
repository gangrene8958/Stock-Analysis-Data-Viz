import streamlit as st
import pandas as pd
import plotly.express as px
from scraping import ticker_info

st.title('Stock Analysis Data Viz')

ticker_input = st.text_input('Write Ticker (only US markets)')
df = ticker_info(ticker_input)

st.divider()

if df is not None:

    
    
    years = df.index.to_list()
    start_year, end_year = st.select_slider(
    "Select years range:",
    options=years,
    value=(years[0], years[-1])
    )
    filtered_df = df.loc[start_year: end_year]

    st.dataframe(filtered_df)

    available_fields = filtered_df.columns.tolist()
    selection = st.multiselect(
    "Select columns to plot",
    options=available_fields
    )

    if selection:
        st.subheader("Bar Plot")
        

        fig = px.bar(
            filtered_df, 
            x=filtered_df.index, 
            y=selection, 
            title=f"Evolution of {', '.join(selection)} - {ticker_input.upper()}",
            barmode='group',
            height=500,
            text_auto = True
        )
        fig.update_traces(
        textposition='outside', 
        cliponaxis=False
        )
        fig.update_xaxes(type='category')
        
        fig.update_layout(
            xaxis_title="Fiscal Year",
            yaxis_title="(M$)",
            legend_title="Metrics"
        )
        
        

        on = st.toggle('View CAGR growth')

        if on:
            for i in selection:
                initial_value = float(filtered_df[i].iloc[0])
                final_value = float(filtered_df[i].iloc[-1])

                cagr = ((final_value / initial_value) ** (1 / len(filtered_df.index)) - 1) * 100

                fig.add_shape(
                type="line",
                x0=filtered_df.index[0], y0=initial_value,
                x1=filtered_df.index[-1], y1=final_value,
                line=dict(color="#51A49E", width=2, dash="dash"),
                )

                idx_middle = len(filtered_df) // 2
                x_middle = filtered_df.index[idx_middle]
                
                y_middle = initial_value + (final_value - initial_value) * (idx_middle / (len(filtered_df) - 1))
                
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
