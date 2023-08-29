import pandas as pd


"""
Prof. Dr. Renato C. Müller Vasquez Callo
Prof. em. Dr. Norbert Thom Prof. h.c. Dr. h.c. mult. († April 2019)
"""


remove_strings = [
    'dr','med', 'prof', 'vet',
    'm.a', 'phil', 'pd', 'msc',
    'phd', 'em', 'lic', 'von',
    'mlaw', 'nat', 'iur', 'sc',
    'dent','(†)','decvdi','advocate',
    '(verh. kaboğan)','blaw',
    'rechtsanwalt','rechtsanwältin',
    'und', 'notarin','fürsprecher',
    'projektverantwortlicher', 'forschungsstelle','gewalt',
    'bei', 'sportveranstaltungen',  'sozialanthropologie', 'senior',
    'researcher', 'lawyer','pediatrician','mph','hr-', 'fachfrau',
    'physics','ecvp'
    ]

def parse_raw_name(raw_name):
    raw_name = raw_name.replace(',', '')
    raw_name = raw_name.replace('(', '')
    raw_name = raw_name.replace(')', '')
    
    splitted_list = raw_name.split()
    splitted_list = [s for s in splitted_list if '.' not in s]
    splitted_list = [s.lower() for s in splitted_list]
    splitted_list = [s for s in splitted_list if len(s) > 2]
    splitted_list = [s for s in splitted_list if s not in remove_strings]
    
    first_name = splitted_list[0] if splitted_list else ''
    last_name = splitted_list[-1] if splitted_list else ''
    
    return first_name, last_name

input_filename = 'fail2.csv'
output_filename = 'customparsednames.csv'

# Read input CSV using Pandas
data = pd.read_csv(input_filename)

# Apply parsing function to raw_name column
data[['first_name', 'last_name']] = data['raw_name'].apply(lambda x: pd.Series(parse_raw_name(x)))

# Save the updated data to output CSV
data.to_csv(output_filename, index=False)

print(f"Data has been processed and saved to '{output_filename}'.")
