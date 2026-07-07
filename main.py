import streamlit as st
import pandas as pd
import plotly.express as px
from scraping import ticker_info

st.title('Stock Analysis Data Viz')

df_snp500 = pd.read_csv('SP500_tickers_and_names.csv', sep = ';')

selectbox_options = {}

for _, i in df_snp500.iterrows():
    selectbox_options[i['Ticker']] = f'{i['Name']}   ({i['Ticker']})'




ticker_input =  st.selectbox("Select Ticker",options=df_snp500['Ticker'].tolist(),index = None, format_func=lambda x: selectbox_options.get(x, x))

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
                
                n_periods = len(filtered_df.index) - 1
                
                if n_periods > 0 and initial_value > 0:
                    cagr = ((final_value / initial_value) ** (1 / n_periods) - 1) * 100
                    
                    fig.add_shape(
                        type="line",
                        x0=0, y0=initial_value,                       
                        x1=len(filtered_df.index) - 1, y1=final_value, 
                        line=dict(color="#51A49E", width=2, dash="dash"),
                    )
                    
    
                    idx_middle = len(filtered_df) // 2
                    x_middle = idx_middle 
                    
                    y_middle = initial_value + (final_value - initial_value) * (idx_middle / (len(filtered_df) - 1))
                    
                    fig.add_annotation(
                        x=x_middle, y=y_middle,
                        text=f"<b>CAGR: {cagr:.1f}%</b>",
                        showarrow=False,
                        font=dict(color="white", size=13),
                        bgcolor="#51A49E", borderpad=6, yshift=15
                    )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select a field to plot")
