import streamlit as st
from datasource.csv import CSVCollector
from contract.catalogo import Catalogo
from aws.client import S3Client

st.title("Portal de dados")

# st.file_uploader("Upload a file", type=["xls", "xlsx", "csv"])

# if st.button("Say hello"):
#     st.write("Helloooooo")

aws = S3Client()
catalogo_de_produtos = CSVCollector(Catalogo, aws, "A1:G51")
catalogo_de_produtos.start()