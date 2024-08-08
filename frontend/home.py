import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_candlestick_with_risk(data: pd.DataFrame) -> None:
    """Plot a candlestick chart with a risk subplot using Plotly.

    Args:
    df (pd.DataFrame): DataFrame containing the columns "DateTime", "open", "high",
    "low", "close", and "risk".

    """
    _temp = data.copy(deep=True)
    
    if "DateTime" in _temp.columns:
        _temp.set_index("DateTime", inplace=True)
    
    # Create a candlestick chart with Plotly
    fig = go.Figure()
    
    # Add candlestick trace
    fig.add_trace(go.Candlestick(
        x=_temp.index,
        open=_temp['open'],
        high=_temp['high'],
        low=_temp['low'],
        close=_temp['close'],
        name='Candlestick'
    ))

    # Apply logarithmic scale to y-axis
    fig.update_layout(
        yaxis_type='log',
        title='Candlestick Chart with Logarithmic Scale',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True,
        xaxis_rangeslider=dict(visible=True),
        autosize=True,  # Ensure the plot resizes with the container
    )
    
    # Add risk subplot
    fig_risk = go.Figure()
    fig_risk.add_trace(go.Scatter(
        x=_temp.index,
        y=_temp['total_risk'],
        mode='lines',
        name='Risk'
    ))

    fig_risk.update_layout(
        title='Risk Over Time',
        xaxis_title='Date',
        yaxis_title='Risk',
        autosize=True,  # Ensure the plot resizes with the container
    )
    
    # Combine plots in a single figure
    fig.add_trace(go.Scatter(
        x=_temp.index,
        y=_temp['total_risk'],
        mode='lines',
        name='Risk',
        yaxis='y2'
    ))

    fig.update_layout(
        yaxis2=dict(
            title='Risk',
            overlaying='y',
            side='right',
        ),
        autosize=True,  # Ensure the plot resizes with the container
    )
    
    # Display the plot with Streamlit
    st.plotly_chart(fig, use_container_width=True)


def main(data):
    st.title('Candlestick Chart with Risk Indicator')

    # Display data
    st.subheader('Data')
    st.write(data)

    # Plot candlestick chart with risk
    st.subheader('Candlestick Chart with Risk')
    plot_candlestick_with_risk(data)
