-- specify database to use
use database ingest_data;

-- create staging area
create or replace stage snowpipe url = "s3://snowflake-ingest-data/SnowPipe-Streaming/" 
credentials =(aws_key_id = 'xxxxx' aws_secret_key = 'xxxxxx' )

-- view contents of staging area
list @snowpipe 

-- create a Table
CREATE TABLE transactions
(

Transaction_Date DATE,
Customer_ID NUMBER,
Transaction_ID NUMBER,
Amount NUMBER
);

-- create SnowPipe and copy contents into transactions table
CREATE OR REPLACE PIPE transaction_pipe 
auto_ingest = true
AS COPY INTO transactions FROM @snowpipe
-- Format to ingest csv data
file_format = (type = csv field_delimiter = '|' skip_header = 1);

-- view created pipes,select the intended pipe and copy it's  notification channel value (x)
-- In the s3 Bucket (snowflake-ingest-data) properties add event notifications - On create Events -  SQS Queue - Add the value (x)
show pipes
-- Upload the file and test if the table gets updated 
SELECT count(*) FROM transactions;

