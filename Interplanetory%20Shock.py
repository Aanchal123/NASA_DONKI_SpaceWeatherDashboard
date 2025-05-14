import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Function to fetch data
def fetch_data(start_date, end_date):
    location = 'ALL'  # Default location, change as needed
    catalog = 'ALL'   # Default catalog, change as needed
    url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/IPS?startDate={start_date}&endDate={end_date}&location={location}&catalog={catalog}"
    response = requests.get(url)
    data = response.json()  # Get the JSON response
    return data

# Data Cleansing
def clean_data(df):
    # Convert 'eventTime' to datetime format
    df['eventTime'] = pd.to_datetime(df['eventTime'], errors='coerce')

    # Drop rows where 'eventTime' is missing
    df.dropna(subset=['eventTime'], inplace=True)

    # Fill missing values in 'location' with 'Unknown'
    df['location'] = df['location'].fillna('Unknown')

    # Fill missing values in 'instruments' with 'No instruments'
    df['instruments'] = df['instruments'].apply(lambda x: x if isinstance(x, list) else [])
    df['instruments'] = df['instruments'].apply(lambda x: ['No instruments'] if not x else x)

    # Fill missing values in 'catalog' with 'Unknown'
    df['catalog'] = df['catalog'].fillna('Unknown')

    # Handle missing or invalid values in numerical columns (Latitude, Longitude)
    df['Latitude'] = df['Latitude'].fillna(0)
    df['Longitude'] = df['Longitude'].fillna(0)

    # Check for missing values after cleaning
    print("\nMissing Values After Cleaning:")
    print(df.isnull().sum())

    return df

# Function to aggregate events by month
def aggregate_events_by_month(df):
    # Ensure 'eventTime' is in datetime format
    df['eventTime'] = pd.to_datetime(df['eventTime'])

    # Extract month and year, then group by it
    df['month'] = df['eventTime'].dt.strftime('%B %Y')  # Convert to month name (e.g., January 2024)

    # Aggregate the event count by month
    event_count_by_month = df.groupby('month').size().reset_index(name='Event Count')

    return event_count_by_month

# Bar chart for Event Activity over Time (Aggregated by Month)
def plot_activity_over_time_bar(df):
    # Aggregate the event counts by month
    df_monthly = aggregate_events_by_month(df)
    fig = px.bar(df_monthly,
                 x='month',
                 y='Event Count',
                 title="IPS Activity Over Time (Monthly)",
                 labels={'month': 'Month', 'Event Count': 'Event Count'},
                 color='Event Count',  # Color by event count
                 color_continuous_scale='greens',  # Single green color gradient
                 hover_data={'month': True, 'Event Count': True})  # Display event count on hover

    # Update layout for the chart
    fig.update_layout(
        title_x=0,  # Left-align the title
        template="plotly_dark",  # Dark mode theme for better contrast
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        xaxis=dict(tickformat='%B %Y'),  # Use formatted month names (e.g., January 2024)
    )

    st.subheader("📊 IPS Activity Over Time (Monthly)")  # Title for Bar Chart
    st.plotly_chart(fig)

    # Description under the bar chart
    st.markdown(
        "<div style='font-size:16px;'>📊 This bar chart shows the monthly activity of IPS events. The number of events is depicted along the y-axis, and the months are shown on the x-axis. A darker green color indicates a higher event count. This helps us understand how frequently IPS events occur over time.</div>",
        unsafe_allow_html=True
    )

# Treemap for Event Count by Location and Instrument
def plot_instrument_treemap(df):
    # Function to extract instruments from a list of dictionaries
    def extract_instruments(instruments):
        if isinstance(instruments, list):  # Check if instruments is a list
            # Flatten the list of dictionaries and extract the 'displayName' (or relevant key)
            return [instrument.get('displayName', 'Unknown') for instrument in instruments if isinstance(instrument, dict)]
        return []

    # Exploding instruments into separate rows
    df['instruments'] = df['instruments'].apply(extract_instruments)
    df_exploded = df.explode('instruments')

    # Calculate the Event Count for each combination of location and instrument
    instrument_event_counts = df_exploded.groupby(['location', 'instruments']).size().reset_index(name='Event Count')

    # Create a treemap with a green gradient and transparent background
    fig = px.treemap(instrument_event_counts,
                     path=['location', 'instruments'],  # Hierarchy of categories
                     values='Event Count',  # Size of each rectangle represents event count
                     color='Event Count',  # Color based on event count
                     title="Treemap of IPS Events by Location and Instrument",
                     color_continuous_scale='greens',  # Single green color gradient
                     hover_data=['location', 'instruments', 'Event Count'])  # Add hover data

    fig.update_layout(
        template="plotly_dark",  # Dark mode for better contrast
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
    )

    st.subheader("🗺️ IPS Events by Location and Instrument")  # Title for Treemap
    st.plotly_chart(fig)

    # Description under the treemap
    st.markdown(
        "<div style='font-size:16px;'>🗺️ This treemap visualizes the IPS event counts by location and instrument. The size of each rectangle corresponds to the number of events, and the color scale (from light green to dark green) shows the intensity of the events. This chart helps in understanding which locations and instruments are involved in the most significant events.</div>",
        unsafe_allow_html=True
    )

# Line chart for Event Count by Location Over Time
def plot_event_count_by_location_over_time(df):
    # Aggregate event counts by month and location
    df_monthly_location = df.groupby([df['eventTime'].dt.strftime('%B %Y'), 'location']).size().reset_index(name='Event Count')

    # Create the interactive line chart with a green gradient color scheme
    fig = px.line(df_monthly_location,
                  x='eventTime', 
                  y='Event Count', 
                  color='location',  # Different lines for different locations
                  title="Event Count by Location Over Time",
                  labels={'eventTime': 'Month', 'Event Count': 'Event Count'},
                  markers=True,  # Add markers to each data point
                  color_discrete_sequence=['white', 'green'],  # White for one line and green for another
                  hover_data={'eventTime': True, 'Event Count': True, 'location': True})  # Hover data

    # Update layout for interaction
    fig.update_layout(
        title_x=0,  # Left-align the title
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        hovermode="x unified",  # Hover over the X-axis to see all data points for that month
        template="plotly_dark"  # Dark mode for better contrast
    )

    st.subheader("📉 Event Count by Location Over Time")  # Title for Line Chart
    st.plotly_chart(fig)

    # Description under the line chart
    st.markdown(
        "<div style='font-size:16px;'>📉 This line chart shows the event count by location over time. The x-axis represents the months, and the y-axis represents the number of IPS events. The white and green lines help track the trends across multiple locations, giving insight into which areas had the most significant IPS activities during different periods.</div>",
        unsafe_allow_html=True
    )

# Main Streamlit App
def main():
    # Set up Streamlit widgets for user input
    st.title("🌌 Interplanetary Shock (IPS) Analysis")  # Title with emoji
    start_date = st.date_input("Enter start date", min_value=datetime(2000, 1, 1), max_value=datetime.today(), value=(datetime.today() - pd.DateOffset(30)))
    end_date = st.date_input("Enter end date", min_value=datetime(2000, 1, 1), max_value=datetime.today(), value=datetime.today())

    # Fetch data and normalize the JSON into a pandas DataFrame
    data = fetch_data(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    df = pd.json_normalize(data)

    # Clean the data
    df_cleaned = clean_data(df)

    # Display the charts
    plot_activity_over_time_bar(df_cleaned)
    plot_instrument_treemap(df_cleaned)
    plot_event_count_by_location_over_time(df_cleaned)

# Run the app
if __name__ == '__main__':
    main()