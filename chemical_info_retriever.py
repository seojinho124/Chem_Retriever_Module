import pandas as pd
import requests

def get_chemical_info(chemical_name):
    base_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/property/InChIKey,CanonicalSMILES/JSON'
    url = base_url.format(chemical_name)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'PropertyTable' in data and 'Properties' in data['PropertyTable']:
            properties = data['PropertyTable']['Properties'][0]
            inchi_key = properties.get('InChIKey', 'Not found')
            smiles = properties.get('CanonicalSMILES', 'Not found')
            return inchi_key, smiles
    return 'Not found', 'Not found'

def process_excel(file_path):
    df = pd.read_excel(file_path)
    df['InChIKey'] = ''
    df['SMILES'] = ''

    for index, row in df.iterrows():
        chemical_name = row[0]
        inchi_key, smiles = get_chemical_info(chemical_name)
        df.at[index, 'InChIKey'] = inchi_key
        df.at[index, 'SMILES'] = smiles

    output_file_path = 'chemical_info_output.xlsx'
    df.to_excel(output_file_path, index=False)
    print(f'Results saved to {output_file_path}')
