-- create Database
create database ingest_data;
use database ingest_data;
-- create a Temporary table for storing JSON  data 
create table json_temp(
  raw_data VARIANT
);
-- create staging area - specify file path s3 URI
create or replace stage json_data_ingest url = "s3://snowflake-ingest-data/Json/master_data.json" 
credentials =(aws_key_id = 'xxxxx' aws_secret_key = 'xxxxx' )

-- view contents of Staging Area
list @json_data_ingest;

-- copy staging area contents into temporary table ,specify json file format
copy into json_temp 
from @json_data_ingest
file_format = (type = json);
-- view content of temporary table
select * from json_temp;

-- Extract Json Keys that has singular value
select 
raw_data:Invoice_ID,
raw_data:Invoice_Total,
raw_data:VendorName
from json_temp;

-- Use lateral Flatteing to extract values out of keys having a list of Dictionary i.e data.json File BillItems key

create table Invoice_Table as

select 
value:name::String as ItemName,
value:amount::Integer as Total_Item_Amount,
value:quantity::Integer as ItemQuantity,
raw_data:Invoice_ID as InvoiceID,
raw_data:Invoice_Total as Final_Amount,
raw_data:VendorName as ShopName
from json_temp,lateral flatten( input => raw_data:BillItems );


