from datasource.api import APICollector
from contracts.schema import CompraSchema
from aws.client import S3Client


schema = CompraSchema
aws = S3Client()

apiCollector = APICollector(schema, aws).start(5)
print(apiCollector)