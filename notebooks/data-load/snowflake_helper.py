import configparser
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

def getSnowflakeEngine(snowflake_database, snowflake_schema, snowflake_warehouse):
  
  config = configparser.ConfigParser()
  config.read('..\..\configuration.properties')
  
  # Define Snowflake connection parameters
  snowflake_username = config['snowflake']['snowflake_username']
  snowflake_password = config['snowflake']['snowflake_password']
  snowflake_account = config['snowflake']['snowflake_account']

  engine = create_engine(URL(
        account=snowflake_account,
        user=snowflake_username,
        password=snowflake_password,
        database=snowflake_database,
        schema=snowflake_schema,
        warehouse=snowflake_warehouse
    ))

  return engine
