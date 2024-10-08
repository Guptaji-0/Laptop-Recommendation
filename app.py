
import pandas as pd
import streamlit as st

# Load the data
laptop_data = pd.read_csv('Cleaned_Laptop_data.csv')  # Adjusted to load from the current directory

# Clean the data
laptop_data['ram_gb'] = laptop_data['ram_gb'].replace(r'[^\d]', '', regex=True)
laptop_data['ram_gb'] = laptop_data['ram_gb'].astype(int)

# Streamlit app setup
st.title("Laptop Recommendation System")

# User inputs
budget = st.number_input("Enter your budget:", min_value=0, value=24990)
preferred_brands = st.multiselect("Select your preferred brands:", options=laptop_data['brand'].unique())
usage = st.selectbox("Select your usage:", options=['ThinNlight', 'Casual', 'Gaming'])
min_ram = st.number_input("Enter minimum RAM (GB):", min_value=0, value=4)
min_storage = st.number_input("Enter minimum storage (GB):", min_value=0, value=256)

# Encode usage preference
usage_mapping = {
    'ThinNlight': 'Office work',
    'Casual': 'Balanced performance',
    'Gaming': 'High performance'
}
usage_encoded = usage_mapping.get(usage, 'average performance')

# User preferences dictionary
user_preferences = {
    'budget': budget,
    'preferred_brands': preferred_brands,
    'usage': usage_encoded,
    'min_ram': min_ram,
    'min_storage': min_storage
}

def filter_laptops(laptop_data, user_preferences):
    # Filter by budget
    filtered_data = laptop_data[laptop_data['latest_price'] <= user_preferences['budget']]
    # Filter by brand preferences
    if user_preferences['preferred_brands']:
        filtered_data = filtered_data[filtered_data['brand'].isin(user_preferences['preferred_brands'])]
    # Filter by minimum RAM
    filtered_data['ram_gb'] = pd.to_numeric(filtered_data['ram_gb'], errors='coerce')
    filtered_data = filtered_data[filtered_data['ram_gb'] >= user_preferences['min_ram']]
    # Filter by minimum storage
    filtered_data['ssd'] = pd.to_numeric(filtered_data['ssd'], errors='coerce').fillna(256)
    filtered_data['hdd'] = pd.to_numeric(filtered_data['hdd'], errors='coerce').fillna(1024)
    filtered_data['total_storage'] = filtered_data['ssd'] + filtered_data['hdd']
    filtered_data = filtered_data[filtered_data['total_storage'] >= user_preferences['min_storage']]
    return filtered_data

def recommend_laptops(filtered_data, num_recommendations=5):
    if filtered_data.empty:
        return "No laptops match your preferences. Try adjusting your filters."
    else:
        recommended_laptops = filtered_data.sort_values(by='latest_price').head(num_recommendations)
        recommendations = []
        for index, laptop in recommended_laptops.iterrows():
            recommendations.append(f"{laptop['brand']} {laptop['model']} - {laptop['processor_name']}, "
                                   f"{laptop['ram_gb']}GB RAM, {laptop['ssd']}GB SSD, {laptop['hdd']}GB HDD, "
                                   f"${laptop['latest_price']}, Rating: {laptop['star_rating']} stars")
        return recommendations

if st.button("Get Recommendations"):
    filtered_laptops = filter_laptops(laptop_data, user_preferences)
    recommendations = recommend_laptops(filtered_laptops)

    if isinstance(recommendations, str):
        st.write(recommendations)
    else:
        for laptop in recommendations:
            st.write(laptop)
