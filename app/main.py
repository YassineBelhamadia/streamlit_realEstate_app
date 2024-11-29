import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from queries import (
    get_annonces_filtered,
    get_annonces_count_by_ville,
    get_price_distribution,
    get_price_boxplot_by_ville,
    get_equipment_distribution,
    get_average_rooms_and_baths_by_ville,
    get_annonces_over_time,
    get_all_cities,
    get_all_equipments
)
st.set_page_config(layout="wide")


# Step 1: Sidebar Filters
st.sidebar.header("Filters")

# Slider for Price Range
min_price, max_price = st.sidebar.slider("Price Range", 0, 5000000, (100000, 2000000))

# Slider for Rooms and Bathrooms
min_rooms, max_rooms = st.sidebar.slider("Number of Rooms", 0, 10, (1, 5))
min_baths, max_baths = st.sidebar.slider("Number of Bathrooms", 0, 5, (1, 3))

# Get dynamic filter options from the database
cities = get_all_cities()
equipments = get_all_equipments()

# Sidebar Filters for Cities and Equipments
selected_villes = st.sidebar.multiselect("Select Cities", cities)
selected_equipments = st.sidebar.multiselect("Select Equipments", equipments)

# Date Range Picker
start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=[pd.to_datetime("2024-01-01"), pd.to_datetime("2024-12-31")],
)

# Step 2: Fetch Filtered Data
filtered_annonces = get_annonces_filtered(
    min_price=min_price,
    max_price=max_price,
    min_rooms=min_rooms,
    max_rooms=max_rooms,
    min_baths=min_baths,
    max_baths=max_baths,
    ville_names=selected_villes,
    equipment_ids=selected_equipments,  # Send selected equipment IDs to the query
    start_date=start_date,
    end_date=end_date,
)

# Convert to DataFrame for visualizations
filtered_annonces_df = pd.DataFrame([annonce for annonce in filtered_annonces])

# Step 3: Main Page - Display Filtered Data
st.header("Real Estate Listings")
st.dataframe(filtered_annonces_df)

# Download filtered data as CSV
csv = filtered_annonces_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_annonces.csv",
    mime="text/csv",
)

# Step 4: Visualizations

# 1. Count of Annonces by Ville
st.subheader("Count of Annonces by City")
city_data = pd.DataFrame(get_annonces_count_by_ville(), columns=["City", "Count"])
city_bar_chart = px.bar(city_data, x="City", y="Count", title="Annonces by City")
st.plotly_chart(city_bar_chart)

# 2. Price Distribution
st.subheader("Price Distribution")
price_data =  get_price_distribution()
price_histogram = px.histogram(price_data, x="Price", title="Price Distribution")
st.plotly_chart(price_histogram)

# 3. Price Boxplot by Ville
st.subheader("Price Range by City")
price_box_data = pd.DataFrame(get_price_boxplot_by_ville(), columns=["City", "Price"])
price_boxplot = px.box(price_box_data, x="City", y="Price", title="Price Range by City")
st.plotly_chart(price_boxplot)

# 4. Equipment Distribution
st.subheader("Equipment Distribution")
equipment_data = pd.DataFrame(get_equipment_distribution(), columns=["Equipment", "Count"])
equipment_pie_chart = px.pie(equipment_data, names="Equipment", values="Count", title="Equipment Distribution")
st.plotly_chart(equipment_pie_chart)

# 5. Average Rooms and Baths by Ville
st.subheader("Average Number of Rooms and Bathrooms by City")
rooms_baths_data = pd.DataFrame(
    get_average_rooms_and_baths_by_ville(),
    columns=["City", "Avg Rooms", "Avg Baths"],
)
rooms_baths_bar_chart = go.Figure()
rooms_baths_bar_chart.add_trace(
    go.Bar(x=rooms_baths_data["City"], y=rooms_baths_data["Avg Rooms"], name="Average Rooms")
)
rooms_baths_bar_chart.add_trace(
    go.Bar(x=rooms_baths_data["City"], y=rooms_baths_data["Avg Baths"], name="Average Bathrooms")
)
rooms_baths_bar_chart.update_layout(barmode="group", title="Average Rooms and Bathrooms by City")
st.plotly_chart(rooms_baths_bar_chart)

# 6. Temporal Evolution of Annonces
st.subheader("Temporal Evolution of Annonces")
temporal_data = pd.DataFrame(
    get_annonces_over_time(),
    columns=["Month", "Count"],
)
temporal_line_chart = px.line(temporal_data, x="Month", y="Count", title="Temporal Evolution of Annonces")
st.plotly_chart(temporal_line_chart)

# Step 5: Add Interactivity
st.sidebar.success("Filters applied. Visualizations updated dynamically.")
