from fastapi import FastAPI
from faker import Faker
import pandas as pd
import random

app = FastAPI()
fake = Faker()
file_name = 'backend/fakeapi/products.csv'
df = pd.read_csv(file_name)
df['indice'] = range(1, len(df) + 1)
df.set_index('indice', inplace=True)

@app.get("/gerar_compra")
async def gerar_compra():
    index = random.randint(1, len(df)-1)
    tuple = df.iloc[index]

    return [{
        "client": fake.name(),
        "creditcard": fake.credit_card_provider(),
        "product_name": tuple['Product Name'],
        "ean": int(tuple['EAN']),
        "price": round(float(tuple['Price']*1.2),2),
        "store": 11,
        "dateTime": fake.iso8601(),
    }]

@app.get("/gerar_compras/{numero_registros}")
async def gerar_compras(numero_registros):
    nr_registros = int(numero_registros)
    if nr_registros < 1:
        return {"error" : "O número de registros deve ser maior que 1"}
    
    respostas = []
    
    for _ in range(nr_registros):
        index = random.randint(1, len(df)-1)
        tuple = df.iloc[index]

        compra = {
            "client": fake.name(),
            "creditcard": fake.credit_card_provider(),
            "product_name": tuple['Product Name'],
            "ean": int(tuple['EAN']),
            "price": round(float(tuple['Price']*1.2),2),
            "store": 11,
            "dateTime": fake.iso8601(),
        }
        respostas.append(compra)

    return respostas