import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\Australian Energy Statistics 2025 Table O(State summary 2024).csv')

# Find where the actual data starts (after "GWh" row)
# Skip the header rows and get to the data
df_clean = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\Australian Energy Statistics 2025 Table O(State summary 2024).csv', skiprows=4)

# Set the first column as index (fuel types)
df_clean.columns = ['Fuel_Type', 'NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT', 'AUS']

# Remove empty rows and summary rows
df_clean = df_clean[df_clean['Fuel_Type'].notna()]
df_clean = df_clean[~df_clean['Fuel_Type'].str.contains('Total|Per cent|Notes|Totals', na=False)]

# Clean the data - remove commas and convert to float
for col in ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT', 'AUS']:
    df_clean[col] = df_clean[col].str.replace(',', '').astype(float)

# Separate renewable and non-renewable
renewables = ['Biomass', 'Wind', 'Hydro', 'Large-scale solar PV', 'Small-scale solar PV', 'Geothermal']
non_renewables = ['Black coal', 'Brown coal', 'Natural gas', 'Oil products']

df_renewable = df_clean[df_clean['Fuel_Type'].isin(renewables)]
df_non_renewable = df_clean[df_clean['Fuel_Type'].isin(non_renewables)]

# Calculate totals by state
renewable_totals = df_renewable[['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT']].sum()
non_renewable_totals = df_non_renewable[['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT']].sum()

# Create final dataframe for grouped bar chart
states_data = []
for state in ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT']:
    fossil = non_renewable_totals[state]
    renewable = renewable_totals[state]
    total = fossil + renewable
    renewable_pct = (renewable / total * 100) if total > 0 else 0
    
    states_data.append({
        'State': state,
        'Fossil_GWh': fossil,
        'Renewable_GWh': renewable,
        'Total_GWh': total,
        'Renewable_Percentage': renewable_pct
    })

df_final = pd.DataFrame(states_data)

# Save
df_final.to_csv('state_electricity_generation_2024.csv', index=False)

print("✓ Cleaned data saved!")
print("\nFinal data:")
print(df_final)
print(f"\nRenewable percentages:")
print(df_final[['State', 'Renewable_Percentage']].sort_values('Renewable_Percentage', ascending=False))