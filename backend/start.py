from datasource.api import APICollector
from contracts.schema import CompraSchema


schema = CompraSchema

apiCollector = APICollector(schema).start(2)
print(apiCollector)