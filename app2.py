import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import json
from datetime import datetime

st.set_page_config(
    page_title="Silver Price Analysis & Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_historical_data():
    df = pd.read_csv("historical_silver_price.csv")
    return df

@st.cache_data
def load_state_data():
    df = pd.read_csv("state_wise_silver_purchased_kg.csv")
    return df

try:
    historical_df = load_historical_data()
    state_df = load_state_data()
except FileNotFoundError:
    st.error("Error: file not found.")
    st.stop()

st.title(" Silver Price Calculator & Sales Analysis Dashboard")

tab1, tab2 = st.tabs(["Silver Price Calculator", "Silver Sales Dashboard"])

with tab1:
    st.header("Silver Price Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Calculate Silver Cost")
        
        weight_unit = st.radio("Select weight unit:", ["Grams", "Kilograms"])
        weight = st.number_input(f"Enter weight of silver ({weight_unit.lower()}):", min_value=0.0, value=100.0, step=1.0)
        price_per_gram = st.number_input("Current price of silver per gram (INR):", min_value=0.0, value=80.0, step=1.0)
        
        if weight_unit == "Kilograms":
            weight_in_grams = weight * 1000
        else:
            weight_in_grams = weight
        
        total_cost_inr = weight_in_grams * price_per_gram
        
        st.success(f"**Total Cost: ₹{total_cost_inr:,.2f}**")
        
        st.subheader("Currency Conversion")
        currency = st.selectbox("Convert to:", ["USD"])
        
        conversion_rates = {
            "USD": 0.012,
       
        }
        
        converted_amount = total_cost_inr * conversion_rates[currency]
        st.info(f"**Converted Amount: {currency} {converted_amount:,.2f}**")

            
with tab2:
    indian_states = ['Kerala', 'Tamil Nadu', 'Karnataka', 'Andhra Pradesh', 'Gujarat']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    st.header("Sales Data visualization in month of Januray")
    st.write("Top 5 States with Highest Silver Purchases")
    top_5_states = state_df.nlargest(5, 'Silver_Purchased_kg')
        
    fig_bar = px.bar(top_5_states, 
                        x='State', 
                        y='Silver_Purchased_kg',
                        title='Top 5 States - Silver Purchases',
                        labels={'Silver_Purchased_kg': 'Silver Purchased (kg)', 'State': 'State'},
                        color='Silver_Purchased_kg',
                        color_continuous_scale='Blues')
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)
    
