import pandas as pd, uuid, asyncio, os, json, psycopg2 as pg,math
from psycopg2.extras import RealDictCursor

class postgres:
    def conn(db_name):        
        with open('appsettings.json', 'r') as f:
            datos = json.load(f)
        conn = "postgresql://{0}:{1}@{2}:{3}/{4}".format(datos['postgres']['login'], datos['postgres']['password'], datos['postgres']['host'],datos['postgres']['port'], db_name)
        return conn

async def clear_file(filename):
    df = pd.read_csv('data_prueba_tecnica.csv')

    # Eliminar filas completamente vacías
    df = df.dropna(how='all')

    # Reemplazar strings vacios o con solo espacios por NaN
    df['id'] = df['id'].astype(str).str.strip().replace('', pd.NA)
    df['company_id'] = df['company_id'].astype(str).str.strip().replace('', pd.NA)
    df['name'] = df['name'].astype(str).str.strip().replace('', pd.NA)      
    df['amount'] = df['amount'].astype(str).str.strip().replace('', pd.NA)  
    df['status'] = df['status'].astype(str).str.strip().replace('', pd.NA)  
    df['created_at'] = df['created_at'].astype(str).str.strip().replace('', pd.NA)  

    df = df[df['id'].astype(str).str.lower() != 'nan']
    df = df[df['company_id'].astype(str).str.lower() != 'nan']
    df = df[df['name'].astype(str).str.lower() != 'nan']
    df = df[df['amount'].astype(str).str.lower() != 'nan']
    df = df[df['status'].astype(str).str.lower() != 'nan']
    df = df[df['created_at'].astype(str).str.lower() != 'nan']    

    df = df.drop(columns=['paid_at'], errors='ignore')

    df.to_csv(filename, index=False)

async def load_companies(companies):
    companies_json_str = json.dumps(companies.to_dict(orient='records'), indent=2)
    string_conn = postgres.conn(db_name='nt')

    con = pg.connect(string_conn)
    con.autocommit = True
    cur = con.cursor()

    query = f"call insertar_json_array_comapnies('{companies_json_str}'::jsonb)"
    cur.execute(query)

async def load_data(filename):
    string_conn = postgres.conn(db_name='nt')

    con = pg.connect(string_conn)
    con.autocommit = True
    cur = con.cursor()

    df = pd.read_csv(filename)
    records = df.to_dict(orient='records')

    batch_size = 1000
    total_batches = math.ceil(len(records) / batch_size)    

    for i in range(total_batches):
        start = i * batch_size
        end = start + batch_size
        batch = records[start:end]

        data = json.dumps(batch).replace("'", "''")        

        try:
            query = f"call insertar_json_array_data('{data}'::jsonb)"
            cur.execute(query)
        except Exception as ex:
            pass

        print(f"Enviando batch {i+1}/{total_batches} con {len(batch)} registros")    

async def main():
    _file_name = f"{uuid.uuid4().hex}.csv"
    print(_file_name)
    
    await clear_file(_file_name)

    get_companies = lambda file_name: pd.read_csv(file_name)[['company_id','name']].drop_duplicates().copy()    
    
    companies = get_companies(_file_name)
    await load_companies(companies)

    await load_data(_file_name)

    os.remove(_file_name)

asyncio.run(main())