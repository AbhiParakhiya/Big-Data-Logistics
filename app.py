import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Set page config
st.set_page_config(
    page_title="Logistics Data Analysis Dashboard",
    page_icon="🚚",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .query-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🚚 Logistics Data Analysis Dashboard")
st.markdown("### Upload your logistics data for detailed analysis")

# File upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.subheader("📂 Upload Your Data")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
st.markdown('</div>', unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None
    return None

# Load the data
df = load_data(uploaded_file)

if df is not None:
    # Display data preview
    st.subheader("📋 Data Preview")
    st.write(f"Total Records: {len(df)}")
    st.dataframe(df.head())

    # Query Selection
    st.sidebar.header("Analysis Options")
    query_options = [
        "Show Schema",
        "Basic Statistics",
        "First Few Records",
        "Total Orders Count",
        "Orders by Traffic Condition",
        "Orders by Weather",
        "Vehicle Type Distribution",
        "Category Distribution",
        "Delivery Time Analysis",
        "Area-wise Analysis",
        "Agent Performance Analysis"
    ]
    selected_queries = st.sidebar.multiselect(
        "Select Analyses to Perform",
        query_options
    )

    # Display selected queries
    for query in selected_queries:
        st.markdown(f'<div class="query-section">', unsafe_allow_html=True)
        
        if query == "Show Schema":
            st.subheader("📊 Data Schema")
            schema_df = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.astype(str)
            })
            st.dataframe(schema_df)

        elif query == "Basic Statistics":
            st.subheader("📈 Basic Statistics")
            st.dataframe(df.describe())

        elif query == "First Few Records":
            st.subheader("👀 First Few Records")
            st.dataframe(df.head())

        elif query == "Total Orders Count":
            st.subheader("🔢 Total Orders")
            st.metric("Total Orders", len(df))

        elif query == "Orders by Traffic Condition":
            if 'Traffic' in df.columns:
                st.subheader("🚦 Orders by Traffic Condition")
                traffic_counts = df['Traffic'].value_counts()
                fig = px.bar(
                    x=traffic_counts.index,
                    y=traffic_counts.values,
                    title="Distribution of Orders by Traffic Condition"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Traffic column not found in the dataset")

        elif query == "Orders by Weather":
            if 'Weather' in df.columns:
                st.subheader("🌤️ Orders by Weather Condition")
                weather_counts = df['Weather'].value_counts()
                fig = px.pie(
                    values=weather_counts.values,
                    names=weather_counts.index,
                    title="Distribution of Orders by Weather"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Weather column not found in the dataset")

        elif query == "Vehicle Type Distribution":
            if 'Vehicle' in df.columns:
                st.subheader("🚗 Vehicle Type Distribution")
                vehicle_counts = df['Vehicle'].value_counts()
                fig = px.pie(
                    values=vehicle_counts.values,
                    names=vehicle_counts.index,
                    title="Distribution of Vehicle Types"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Vehicle column not found in the dataset")

        elif query == "Category Distribution":
            if 'Category' in df.columns:
                st.subheader("📦 Order Category Distribution")
                category_counts = df['Category'].value_counts()
                fig = px.bar(
                    x=category_counts.index,
                    y=category_counts.values,
                    title="Distribution of Orders by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Category column not found in the dataset")

        elif query == "Delivery Time Analysis":
            if 'Delivery_Time' in df.columns:
                st.subheader("⏱️ Delivery Time Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    avg_delivery = df['Delivery_Time'].mean()
                    st.metric("Average Delivery Time (min)", f"{avg_delivery:.2f}")
                
                with col2:
                    fig = px.histogram(
                        df,
                        x='Delivery_Time',
                        title="Distribution of Delivery Times"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Delivery_Time column not found in the dataset")

        elif query == "Area-wise Analysis":
            if 'Area' in df.columns:
                st.subheader("🗺️ Area-wise Analysis")
                area_stats = df.groupby('Area')['Delivery_Time'].agg(['mean', 'count']).reset_index()
                area_stats.columns = ['Area', 'Avg Delivery Time', 'Number of Orders']
                st.dataframe(area_stats)
                
                fig = px.bar(
                    area_stats,
                    x='Area',
                    y='Avg Delivery Time',
                    title="Average Delivery Time by Area"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Area column not found in the dataset")

        elif query == "Agent Performance Analysis":
            if 'Agent_Rating' in df.columns and 'Delivery_Time' in df.columns:
                st.subheader("👤 Agent Performance Analysis")
                fig = px.scatter(
                    df,
                    x='Agent_Rating',
                    y='Delivery_Time',
                    title="Agent Rating vs Delivery Time"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                avg_by_rating = df.groupby('Agent_Rating')['Delivery_Time'].mean().reset_index()
                st.write("Average Delivery Time by Agent Rating:")
                st.dataframe(avg_by_rating)
            else:
                st.warning("Agent_Rating or Delivery_Time columns not found in the dataset")

        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Please upload a CSV file to begin analysis.")

# Add footer
st.markdown("---")
st.markdown("### 📊 Logistics Data Analysis Tool")
st.markdown("Upload your CSV file and select analyses from the sidebar to get started.") 