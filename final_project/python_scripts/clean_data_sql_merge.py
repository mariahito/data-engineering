# %%
import pandas as pd
from pathlib import Path
import json

# load in covid data

# path to data folder
covid_file_path = Path("/home/jhu/data/time_series_covid19_confirmed_US.csv")

# load in csv
df = pd.read_csv(covid_file_path)


# %%
# remove unnecessary columns
df = df.drop(columns=['UID','iso2', 'iso3','code3','FIPS','Country_Region','Lat','Long_'])
# unpivot date columns to get one date column
df_unpivot = df.melt(id_vars=['Admin2', 'Province_State','Combined_Key'], var_name='Date', value_name='Cases')

# group by states and sum the cases per cities in each state
df_states = df_unpivot.groupby(['Date', 'Province_State'], as_index=False)['Cases'].sum()

# Filter data to desired states
df_filtered = df_states[df_states['Province_State'].isin(['California','Connecticut','Florida','Georgia',
                                                          'Maryland','Michigan','New York','Pennsylvania',
                                                          'Texas', 'Washington'])]

## copy of the df
df_filtered = df_filtered.copy()

# set date as string
df_filtered['Date'] = df_filtered['Date'].astype('string')

# extract before first and after last / for month and year columns
df_filtered['month'] = df_filtered['Date'].str.split('/').str[0]
df_filtered['year'] = df_filtered['Date'].str.split('/').str[-1]

# adding leading 0s to month
df_filtered['month'] = df_filtered['month'].astype(str).str.zfill(2)

# merge month and year column by /
df_filtered['month/year'] = df_filtered['month'] + '/' + df_filtered['year']

# filter data to 2021
df_2021= df_filtered[df_filtered['year'] == '2021']

# aggreggate by month
df_clean = df_2021.groupby(['month/year', 'Province_State'], as_index=False)['Cases'].sum()
df_clean = df_clean.rename(columns={'Province_State': 'state','Cases':'cases'})
df_clean['month/year'] = df_clean['month/year'].astype('string')


output_path_covid = Path("/home/jhu/data/cleaned_covid.xlsx")

# save as csv to data folder
df_clean.to_excel(output_path_covid, index=False)


# %%
# load in unemployment data

# path to data folder
unemp_file_path = Path("/home/jhu/data/Unemployment in America Per US State.csv")

# load in csv
unem_df = pd.read_csv(unemp_file_path)


# Standardize column names for database compatibility
unem_df.columns = [
    "fips_code", "state", "year", "month", "civilian_population", "labor_force",
    "population_percent", "employment", "employment_percent", "unemployment", "unemployment_percent"
]

# Convert numeric columns from string with commas to integers
numeric_cols = ["civilian_population", "labor_force", "employment", "unemployment"]
for col in numeric_cols:
    unem_df[col] = unem_df[col].str.replace(",", "").astype(int)

# Create a single 'month/year' column in MM/YYYY format
unem_df["month/year"] = unem_df.apply(lambda x: f"{int(x['month']):02d}/{int(x['year'])}", axis=1)

# Drop the original year and month columns
unem_df.drop(columns=["year", "month"], inplace=True)

# Filter data for the year 2021
unem_df = unem_df[unem_df["month/year"].str.endswith("/2021")]

# Standardize the state column
unem_df["state"] = unem_df["state"].str.strip().str.title()

# Filter for specific states
selected_states = ["California", "Connecticut", "Florida", "Georgia", "Maryland", "Michigan", "New York", "Pennsylvania", "Texas", "Washington"]
unem_df = unem_df[unem_df["state"].isin(selected_states)]

# Convert FIPS code to string to retain leading zeros
unem_df["fips_code"] = unem_df["fips_code"].astype(str).str.zfill(2)

# Creating Additional Features
unem_df["employment_to_population_ratio"] = unem_df["employment"] / unem_df["civilian_population"]
unem_df["unemployment_rate"] = unem_df["unemployment"] / unem_df["labor_force"]

# Remove duplicates
unem_df.drop_duplicates(inplace=True)

# Handle missing values (Drop rows where state or date is missing)
unem_df.dropna(subset=["state", "month/year"], inplace=True)


output_path_unem = Path("/home/jhu/data/cleaned_unemployment_data.csv")

# save as csv to data folder
unem_df.to_csv(output_path_unem, index=False)



# %%
# load in weather data 


# path to data folder
weather_folder_path = Path("/home/jhu/data/weather_data_json")

json_files = list(weather_folder_path.glob("weather_data_*.json"))

all_records = []

# Extract daily records from all JSON files
for file_path in json_files:
    with open(file_path, "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            data = data[0]
        state = data.get("address", "Unknown").strip().title()
        for day in data.get("days", []):
            date = day["datetime"]
            mm_yyyy = f"{date[5:7]}/2021"
            record = {
                "State": state,
                "Month/Year": mm_yyyy,
                "TempMax": day.get("tempmax"),
                "Temp": day.get("temp"),
                "TempMin": day.get("tempmin"),
                "FeelsLike": day.get("feelslike"),
                "Humidity": day.get("humidity"),
                "Precipitation": day.get("precip"),
                "PrecipitationType": ', '.join(day["preciptype"]) if isinstance(day.get("preciptype"), list) else day.get("preciptype"),
                "Conditions": day.get("conditions"),
                "Description": day.get("description"),
            }
            all_records.append(record)

# Create DataFrame
w_df = pd.DataFrame(all_records)

# Filter for selected 10 states
selected_states = [
    "California", "Connecticut", "Florida", "Georgia", "Maryland",
    "Michigan", "New York", "Pennsylvania", "Texas", "Washington"
]
w_df = w_df[w_df["State"].isin(selected_states)]

# Group by Month/Year and State — calculate monthly averages
monthly_summary = w_df.groupby(["Month/Year", "State"]).agg({
    "TempMax": "mean",
    "Temp": "mean",
    "TempMin": "mean",
    "FeelsLike": "mean",
    "Humidity": "mean",
    "Precipitation": "mean",
}).reset_index()

# Find most common values for categorical columns
def get_mode(series):
    return series.mode().iloc[0] if not series.mode().empty else None

modes = w_df.groupby(["Month/Year", "State"]).agg({
    "PrecipitationType": get_mode,
    "Conditions": get_mode,
    "Description": get_mode
}).reset_index()

# Merge summary and modes
monthly_summary = monthly_summary.merge(modes, on=["Month/Year", "State"])

# Round all numeric columns to 1 decimal place
numeric_cols = monthly_summary.select_dtypes(include=["float64", "int64"]).columns
monthly_summary[numeric_cols] = monthly_summary[numeric_cols].round(1)

# Reorder columns and save
final_df = monthly_summary[[
    "Month/Year", "State", "TempMax", "Temp", "TempMin", "FeelsLike",
    "Humidity", "Precipitation", "PrecipitationType", "Conditions", "Description"
]]

# Save to CSV

output_path_w = Path("/home/jhu/data/cleaned_weather_data.csv")

# save as csv to data folder
final_df.to_csv(output_path_w, index=False)

# %%


# %%
unemployment_path = Path("/home/jhu/data/cleaned_unemployment_data.csv")
weather_path = Path("/home/jhu/data/cleaned_weather_data.csv")
covid_path = Path("/home/jhu/data/cleaned_covid.xlsx")

# load in files
df_unemp = pd.read_csv(unemployment_path)
df_weather = pd.read_csv(weather_path)
df_covid = pd.read_excel(covid_path)

# merge covid and unemployment data, merging directly since there is one row per month/year and state
merged_covid_unemp = pd.merge(df_covid, df_unemp, on=['month/year', 'state'], how='inner')

# merge result and weather data
final_df = pd.merge(merged_covid_unemp, df_weather, left_on=['month/year', 'state'], right_on=['Month/Year', 'State'], how='inner')
final_df.rename(columns={'cases': 'covid_cases'}, inplace=True)
final_df.drop(columns=['State','Month/Year'], inplace=True)

# making reference tables for total of 5 tables 
month_year_df = final_df[['month/year']].drop_duplicates().reset_index(drop=True)
state_df = final_df[['state','fips_code']].drop_duplicates().reset_index(drop=True)

# save to folder
output_path_all = Path("/home/jhu/data/combined_data.csv")

# save as csv to data folder
final_df.to_csv(output_path_all, index=False)



final_df = final_df.astype(object)
final_df = final_df.where(pd.notnull(final_df), None)


# %%
## copy excel to sql db and print 5 rows

## Establish the connection
import psycopg2
import pandas as pd
conn = psycopg2.connect(
dbname='final_project',
user='jhu',
password='jhu123',
host='postgres', # Adjust if needed for Docker service name
port='5432'
)
# create a cursor object
cur = conn.cursor() 

#query to make table
create_table = """
    CREATE TABLE project (
            id SERIAL PRIMARY KEY, 
            month_year TEXT,
            state VARCHAR(50),
            covid_cases INTEGER,
            fips_code VARCHAR(10),
            civilian_population INTEGER,
            labor_force INTEGER,
            population_percent REAL,
            employment INTEGER,
            employment_percent REAL,
            unemployment INTEGER,
            unemployment_percent REAL,
            employment_to_population_ratio REAL,
            unemployment_rate REAL,
            TempMax REAL,
            Temp REAL,
            TempMin REAL,
            FeelsLike REAL,
            Humidity REAL,
            Precipitation REAL,
            PrecipitationType VARCHAR(20),
            Conditions VARCHAR(100),
            Description TEXT

    );
    """


# Create table
cur.execute("DROP TABLE IF EXISTS project;")
cur.execute(create_table)


for _, row in final_df.iterrows():
    values = (
        row['month/year'], row['state'], row['covid_cases'], row['fips_code'], row['civilian_population'],
        row['labor_force'], row['population_percent'], row['employment'], row['employment_percent'],
        row['unemployment'], row['unemployment_percent'], row['employment_to_population_ratio'], row['unemployment_rate'],
        row['TempMax'], row['Temp'], row['TempMin'], row['FeelsLike'], row['Humidity'], row['Precipitation'],
        row['PrecipitationType'], row['Conditions'], row['Description']
    )
    cur.execute("""
        INSERT INTO project (
            month_year, state, covid_cases, fips_code, civilian_population, labor_force, population_percent,
            employment, employment_percent, unemployment, unemployment_percent, employment_to_population_ratio,
            unemployment_rate, TempMax, Temp, TempMin, FeelsLike, Humidity, Precipitation, PrecipitationType,
            Conditions, Description
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s
        );
    """, values)


# query table
conn.commit()


cur.execute("SELECT * FROM project LIMIT 5;")
rows = cur.fetchall()

print("First 5 rows:")
for row in rows:
    print(row)

# close connection
cur.close()
conn.close()


# %%
