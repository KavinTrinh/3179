import pandas as pd

# Read the CSV
df = pd.read_csv(r'C:\Users\Khanh\OneDrive - z55rs\Documents\Monash\SEM2 2025\FIT3179\A2\3179\Data Visualisation 2\data\Emissions by state and territory.csv')

# Melt/unpivot the data from wide to long format
df_long = df.melt(
    id_vars=['Financial Year'],
    value_vars=['ACT (Mt)', 'NSW (Mt)', 'NT (Mt)', 'QLD (Mt)', 'SA (Mt)', 'TAS (Mt)', 'VIC (Mt)', 'WA (Mt)'],
    var_name='State_Code_Raw',
    value_name='Emissions'
)

# Clean up state codes
df_long['State_Code'] = df_long['State_Code_Raw'].str.replace(' (Mt)', '', regex=False)

# Add full state names
state_mapping = {
    'ACT': 'Australian Capital Territory',
    'NSW': 'New South Wales',
    'NT': 'Northern Territory',
    'QLD': 'Queensland',
    'SA': 'South Australia',
    'TAS': 'Tasmania',
    'VIC': 'Victoria',
    'WA': 'Western Australia'
}

df_long['State_Full_Name'] = df_long['State_Code'].map(state_mapping)

# Select final columns
df_final = df_long[['Financial Year', 'State_Code', 'State_Full_Name', 'Emissions']]

# Save
df_final.to_csv('australia_state_emissions_long.csv', index=False)

print(f"✓ Created long format with {len(df_final)} rows")
print(f"\nSample data:")
print(df_final.head(10))
print(f"\nYear range: {df_final['Financial Year'].min()} - {df_final['Financial Year'].max()}")
print(f"States: {df_final['State_Code'].unique().tolist()}")