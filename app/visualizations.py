import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_price_distribution(prices):
    """Generate price distribution plot."""
    plt.figure(figsize=(15, 6))
    sns.histplot(prices, kde=True, color='blue')  # Pass the list directly
    plt.title("Price Distribution of Annonces")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.show()

def plot_surface_price_relation(df):
    """Generate surface vs price scatter plot."""
    if "surface" in df.columns and "prix" in df.columns:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x="surface", y="prix", color='green')
        plt.title("Surface vs Price Relation")
        plt.xlabel("Surface")
        plt.ylabel("Price")
        plt.show()
    else:
        print("DataFrame must contain 'surface' and 'prix' columns.")

def plot_price_boxplot_by_ville(price_data):
    """Generate price distribution boxplot by city."""
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=price_data, x="City", y="Price", palette="Set2")
    plt.title("Price Distribution by City")
    plt.xlabel("City")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.show()

def plot_average_rooms_and_baths_by_ville(df):
    """Generate a bar plot for average rooms and baths by city."""
    plt.figure(figsize=(12, 7))
    sns.barplot(x="City", y="Average_Rooms", data=df, color='skyblue', label="Average Rooms")
    sns.barplot(x="City", y="Average_Baths", data=df, color='orange', label="Average Baths")
    plt.title("Average Rooms and Baths by City")
    plt.xlabel("City")
    plt.ylabel("Average Count")
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def plot_annonces_over_time(df):
    """Generate time series plot for annonces over time."""
    plt.figure(figsize=(12, 6))
    sns.lineplot(x="Month", y="Count", data=df, color='purple', marker='o')
    plt.title("Annonces Over Time")
    plt.xlabel("Month")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()

def plot_equipment_distribution(df):
    """Generate bar plot for equipment distribution."""
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Equipment", y="Count", data=df, palette="muted")
    plt.title("Equipment Distribution in Annonces")
    plt.xlabel("Equipment")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()
