import pandas as pd

# Read the datasets
co2_data = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\annual-co2-emissions-per-country.csv')
population_data = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\world_population.csv')

# Years available in population data
years = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]

# Create a list to store data for each year
all_years_data = []

for year in years:
    # Get population column name
    pop_col = f'{year} Population'
    
    # Filter CO2 data for this year
    co2_year = co2_data[co2_data['Year'] == year].copy()
    
    # Rename CO2 column to avoid special characters
    co2_year = co2_year.rename(columns={'Annual CO2 emissions': 'Annual_CO2_emissions'})
    
    # Merge with population data
    merged = pd.merge(
        co2_year,
        population_data[['CCA3', 'Country/Territory', 'Continent', pop_col]],
        left_on='Code',
        right_on='CCA3',
        how='inner'
    )
    
    # Rename population column to a consistent name
    merged = merged.rename(columns={pop_col: 'Population'})
    
    # Calculate emissions per capita
    merged['Emissions_per_Capita'] = merged['Annual_CO2_emissions'] / merged['Population']
    
    # Select and keep only needed columns
    year_data = merged[[
        'Entity',
        'Code',
        'Year',
        'Annual_CO2_emissions',
        'Population',
        'Continent',
        'Emissions_per_Capita'
    ]]
    
    all_years_data.append(year_data)

# Combine all years
final_data = pd.concat(all_years_data, ignore_index=True)

# Save
final_data.to_csv('co2_emissions_per_capita_timeseries.csv', index=False)

print(f"Created dataset with {len(final_data)} records across {len(years)} years")
print(f"Years included: {years}")
print(f"\nData summary:")
print(final_data.groupby('Year').size())