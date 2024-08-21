import pandas as pd

# Load the metadata and other data files
metadata = pd.read_csv('C-CLAMP_metadata_gender.txt', sep='\t')
print(metadata)

Bel_data = pd.read_excel('Gemeenten_Belgie.xlsx')
print(Bel_data)

Ned_data = pd.read_excel('Gemeenten_Nederland.xls')
print(Ned_data)

# Convert the "Gemeentenaam" columns to lowercase to ensure case-insensitive matching
Bel_data["Gemeentenaam"] = Bel_data["Gemeentenaam"].str.lower()
Ned_data["Gemeentenaam"] = Ned_data["Gemeentenaam"].str.lower()
metadata["POB"] = metadata["POB"].str.lower()
metadata["POD"] = metadata["POD"].str.lower()

# Initialize new columns with default values
metadata["Country_POB"] = ""
metadata["Country_POD"] = ""
metadata["Region_POB"] = ""
metadata["Region_POD"] = ""

# Create lookup dictionaries for faster access
bel_country_dict = pd.Series("Belgium", index=Bel_data["Gemeentenaam"].dropna()).to_dict()
ned_country_dict = pd.Series("Netherlands", index=Ned_data["Gemeentenaam"].dropna()).to_dict()

bel_region_dict = pd.Series(Bel_data["Provincie"].values, index=Bel_data["Gemeentenaam"].dropna()).to_dict()
ned_region_dict = pd.Series(Ned_data["Provincie"].values, index=Ned_data["Gemeentenaam"].dropna()).to_dict()


# Function to determine the country and region based on POB or POD values
def determine_country_and_region(location_values):
    if isinstance(location_values, float) and pd.isna(location_values):
        return "NA", "NA"

    for loc in location_values.split(';'):
        loc = loc.strip().lower()
        if loc in bel_country_dict:
            return bel_country_dict[loc], bel_region_dict[loc]
        elif loc in ned_country_dict:
            return ned_country_dict[loc], ned_region_dict[loc]

    return "NA", "NA"


# Update the 'Country_POB' and 'Region_POB' columns
metadata[["Country_POB", "Region_POB"]] = metadata["POB"].apply(determine_country_and_region).apply(pd.Series)

# Update the 'Country_POD' and 'Region_POD' columns
metadata[["Country_POD", "Region_POD"]] = metadata["POD"].apply(determine_country_and_region).apply(pd.Series)

print(metadata[["Country_POB", "Region_POB", "Country_POD", "Region_POD"]])

# Save the updated metadata to a new text file
metadata.to_csv('C-CLAMP_metadata_gender_location.txt', sep='\t', index=False)
