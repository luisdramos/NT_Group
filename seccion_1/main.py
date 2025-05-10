import pandas as pd, uuid, asyncio, os

def clear_file(filename):
    df = pd.read_csv('data_prueba_tecnica.csv')

    # Eliminar filas completamente vacías
    df = df.dropna(how='all')

    # Reemplazar strings vacios o con solo espacios por NaN
    df['company_id'] = df['company_id'].astype(str).str.strip().replace('', pd.NA)
    df['name'] = df['name'].astype(str).str.strip().replace('', pd.NA)      
    df['amount'] = df['amount'].astype(str).str.strip().replace('', pd.NA)  
    df['status'] = df['status'].astype(str).str.strip().replace('', pd.NA)  
    df['created_at'] = df['created_at'].astype(str).str.strip().replace('', pd.NA)  

    # eliminar columnas donde vengan vacias 
    df = df.dropna(subset=['company_id'], how='all')
    df = df.dropna(subset=['name'], how='all')
    df = df.dropna(subset=['amount'], how='all')
    df = df.dropna(subset=['status'], how='all')
    df = df.dropna(subset=['created_at'], how='all')

    df.to_csv(filename, index=False)

async def get_companies(filename):
    df = pd.read_csv(filename)
    # Extraer pares únicos sin modificar el DataFrame original
    unique_companies = df[['company_id', 'name']].drop_duplicates().copy()
    return unique_companies


async def main():
    _file_name = f"{uuid.uuid4().hex}.csv"
    print(_file_name)
    clear_file(_file_name)

    get_companies = lambda file_name: pd.read_csv(file_name)[['company_id', 'name']].drop_duplicates().copy()    
    companies = get_companies(_file_name)
    print(companies)

    #os.remove(_file_name)

asyncio.run(main())