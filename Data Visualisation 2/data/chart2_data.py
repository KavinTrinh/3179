import pandas as pd

# Read datasets
co2_data = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\annual-co2-emissions-per-country.csv')
gdp_data = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\world_country_gdp_usd.csv')
population_data = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\world_population.csv')

# Rename GDP column if needed
gdp_data = gdp_data.rename(columns={
    'Country Name': 'Entity',
    'Country Code': 'Code',
    'year': 'Year'
})

# Filter years 1970-2020
co2_filtered = co2_data[(co2_data['Year'] >= 1970) & (co2_data['Year'] <= 2020)].copy()
gdp_filtered = gdp_data[(gdp_data['Year'] >= 1970) & (gdp_data['Year'] <= 2020)].copy()

# Rename CO2 column to avoid special characters
co2_filtered = co2_filtered.rename(columns={'Annual CO2 emissions': 'Annual_CO2_emissions'})

# Merge CO2 and GDP
merged = pd.merge(
    co2_filtered,
    gdp_filtered[['Code', 'Year', 'GDP_USD', 'GDP_per_capita_USD']],
    on=['Code', 'Year'],
    how='inner'
)

# Get continent data from population dataset
continent_map = population_data[['CCA3', 'Continent', 'Country/Territory']].drop_duplicates()

# Merge with continent data
merged = pd.merge(
    merged,
    continent_map,
    left_on='Code',
    right_on='CCA3',
    how='left'
)

# Get population for each year
# We'll need to interpolate between available years
population_years = {
    1970: '1970 Population',
    1980: '1980 Population',
    1990: '1990 Population',
    2000: '2000 Population',
    2010: '2010 Population',
    2015: '2015 Population',
    2020: '2020 Population'
}

# Function to get population for a given year (with interpolation)
def get_population_for_year(row):
    year = row['Year']
    code = row['Code']
    
    # Find the population data for this country
    pop_data = population_data[population_data['CCA3'] == code]
    
    if pop_data.empty:
        return None
    
    # If exact year exists, use it
    if year in population_years:
        col = population_years[year]
        return pop_data[col].values[0]
    
    # Otherwise, interpolate
    # Find closest years
    available_years = sorted([y for y in population_years.keys() if y <= year])
    if not available_years:
        return pop_data['1970 Population'].values[0]
    
    lower_year = max([y for y in available_years if y <= year])
    upper_years = [y for y in population_years.keys() if y > year]
    
    if not upper_years:
        return pop_data[population_years[lower_year]].values[0]
    
    upper_year = min(upper_years)
    
    # Linear interpolation
    lower_pop = pop_data[population_years[lower_year]].values[0]
    upper_pop = pop_data[population_years[upper_year]].values[0]
    
    ratio = (year - lower_year) / (upper_year - lower_year)
    interpolated_pop = lower_pop + ratio * (upper_pop - lower_pop)
    
    return interpolated_pop

# Apply population calculation
merged['Population'] = merged.apply(get_population_for_year, axis=1)

# Calculate CO2 per capita
merged['CO2_per_capita'] = merged['Annual_CO2_emissions'] / merged['Population']

# Select final columns
final_data = merged[[
    'Entity',
    'Code',
    'Year',
    'Annual_CO2_emissions',
    'GDP_USD',
    'GDP_per_capita_USD',
    'Population',
    'CO2_per_capita',
    'Continent'
]].copy()

# Remove rows with missing data
final_data = final_data.dropna()

# Save
final_data.to_csv('co2_gdp_bubble_chart_data.csv', index=False)

print(f"Created dataset with {len(final_data)} records")
print(f"Years: {final_data['Year'].min()} - {final_data['Year'].max()}")
print(f"Countries: {final_data['Entity'].nunique()}")
print(f"\nData by continent:")
print(final_data.groupby('Continent')['Entity'].nunique())