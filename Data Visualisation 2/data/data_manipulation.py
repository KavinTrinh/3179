import pandas as pd

# Read the datasets
co2_data = pd.read_csv('annual-co2-emissions-per-country.csv')
population_data = pd.read_csv('world_population.csv')

# Filter CO2 data for 2022 only (or latest year available)
co2_2022 = co2_data[co2_data['Year'] == 2022].copy()

# Merge on the Code/CCA3 columns
merged_data = pd.merge(
    co2_2022,
    population_data,
    left_on='Code',
    right_on='CCA3',
    how='inner'  # Only keep countries that exist in both datasets
)

# Calculate emissions per capita
merged_data['Emissions_per_Capita'] = merged_data['Annual CO₂ emissions'] / merged_data['2022 Population']

# Select only the columns we need for the map
final_data = merged_data[[
    'Entity',
    'Code',
    'Year',
    'Annual CO₂ emissions',
    'Country/Territory',
    '2022 Population',
    'Continent',
    'Growth Rate',
    'Emissions_per_Capita'
]]

# Save the merged dataset
final_data.to_csv('co2_emissions_per_capita_2022.csv', index=False)

print(f"Merged dataset created with {len(final_data)} countries")
print(f"\nFirst few rows:")
print(final_data.head())

print(f"\nEmissions per capita range:")
print(f"Min: {final_data['Emissions_per_Capita'].min():.2f} tons/person")
print(f"Max: {final_data['Emissions_per_Capita'].max():.2f} tons/person")
print(f"Mean: {final_data['Emissions_per_Capita'].mean():.2f} tons/person")

# Check Australia specifically
aus_data = final_data[final_data['Code'] == 'AUS']
if not aus_data.empty:
    print(f"\nAustralia's per capita emissions: {aus_data['Emissions_per_Capita'].values[0]:.2f} tons/person")