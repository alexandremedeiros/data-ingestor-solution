import streamlit as st
import openpyxl
import pandas as pd
from pydantic import ValidationError
from io import BytesIO
import datetime

class CSVCollector:
    def __init__(self, schema, aws, cell_range):
        self._schema = schema
        self._aws = aws
        self._buffer = None
        self.cell_range = cell_range
        return
    
    def start(self):
        getData = self.getData()
        
        extractData = None
        if getData is not None:
            extractData = self.extractData(getData)
        if extractData is not None:
            validateData = self.validateData(extractData)
            return validateData
        
    
    def getData(self):
        dados_excel = st.file_uploader("Selecione seu arquivo do Excel", type=[".xls", ".xlsx", ".csv"])
        return dados_excel
    
    
    def extractData(self, dados_excel):
        workbook = openpyxl.load_workbook(dados_excel)
        sheet = workbook.active
        range_cell = sheet[self.cell_range]

        # to pegando o meu índice 0, que é o cabeçalho
        headers = [cell.value for cell in range_cell[0]]

        data = []
        for row in range_cell[1:]:
            data.append([cell.value for cell in row])

        dataframe = pd.DataFrame(data, columns=headers)
        return dataframe
    

    def validateData(self, dataframe):
        error = []
        valid_rows = []  # To store valid rows

        for index, row in dataframe.iterrows():
            try:
                # Create an instance of the Pydantic model for each row
                valid_row = self._schema(**row.to_dict())
                valid_rows.append(valid_row)  # Add the valid row to the list
            except ValidationError as e:
                # Append error message for rows that fail validation
                error.append(f"Erro na linha {index + 1}: {str(e)}")

        if error:
            st.error("\n".join(error))  # Displaying errors in Streamlit
            return None  # Return None if there are errors

        st.success("Planilha convertida para parquet e enviado ao S3!")

        parquet = self.convertToParquet(dataframe)
        if self._buffer is not None:
            file_name = self.fileName()
            print(file_name)
            self._aws.upload_file(parquet, file_name)

        return dataframe
    

    def loadData(self):
        pass
    
    def convertToParquet(self, response):
        self._buffer = BytesIO()
        try:
            response.to_parquet(self._buffer)
            return self._buffer
        except:
            print("Erro ao transformar o DF em Parquet")
            self._buffer = None

    def fileName(self):
        data_atual = datetime.datetime.now().isoformat()
        match = data_atual.split(".")
        return f"api/catalogo_produtos{match[0]}.parquet"
