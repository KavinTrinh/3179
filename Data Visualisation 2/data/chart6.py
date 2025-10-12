import pandas as pd
import numpy as np



# Read the CSV
df = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\Australian Energy Statistics 2025 Table O(State summary 2024).csv', skiprows=4)
df.columns = ['Fuel_Type', 'NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT', 'AUS']

# Clean data
df = df[df['Fuel_Type'].notna()]
for col in ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT']:
    df[col] = df[col].str.replace(',', '').replace('', '0').astype(float)

# Define fuel categories
fuel_types = {
    'Black coal': 'Non-Renewable',
    'Brown coal': 'Non-Renewable',
    'Natural gas': 'Non-Renewable',
    'Oil products': 'Non-Renewable',
    'Biomass': 'Renewable',
    'Wind': 'Renewable',
    'Hydro': 'Renewable',
    'Large-scale solar PV': 'Renewable',
    'Small-scale solar PV': 'Renewable'
}

# Filter to actual fuel types
df = df[df['Fuel_Type'].isin(fuel_types.keys())].copy()
df['Category'] = df['Fuel_Type'].map(fuel_types)

# Combine solar types for simplicity
df['Fuel_Type'] = df['Fuel_Type'].replace({
    'Large-scale solar PV': 'Solar',
    'Small-scale solar PV': 'Solar'
})

# Aggregate solar
df = df.groupby(['Fuel_Type', 'Category'])[['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT']].sum().reset_index()

# Reshape to long format
df_long = df.melt(
    id_vars=['Fuel_Type', 'Category'],
    value_vars=['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT'],
    var_name='State',
    value_name='Generation_GWh'
)

# Save
df_long.to_csv('state_energy_detailed_2024.csv', index=False)

print("✓ Detailed energy data saved!")
print("\nSample:")
print(df_long.head(15))
print(f"\nFuel types: {df_long['Fuel_Type'].unique()}")