import os
import pyodbc
import json
import time

# Table-keyword mapping (you provided this)
table_keywords_map = {
    "dbo.Amagi_Daily": ["Amagi"],
    "dbo.Amazon_Earnings_PVD": ["Amazon PVD", "Earnings"],
    "dbo.Amazon_VC_Weekly_US": ["Vendor Weekly"],
    "dbo.amazon_vendor_central_All_Territory_daily": ["Vendor Central"],
    "dbo.AmazonData_Reports": ["Performance Matrix"],
    "dbo.Googleplay(TVOD)": ["Youtube"],
    "dbo.Hoopla_Daily": ["Hoopla"],
    "dbo.ITunes_Daily": ["ITunes"],
    "dbo.peacock_Ad_Revenue": ["Peacock Ad Revenue"],
    "dbo.Peacock_Sub_Revenue": ["Peacock Sub Revenue"],
    "dbo.Plex_Daily": ["Plex"],
    "dbo.Roku_Daily": ["Roku"],
    "dbo.Summary_Table": ["Combined"],
    "dbo.tbl_all_amazon_new": ["amazon", "Total_Revenue"],
    "dbo.tbl_avod_revenue": ["Avod"],
    "dbo.tbl_fixedfee_revenue": ["Fixedfee"],
    "dbo.Tbl_PlutoData": ["Pluto"],
    "dbo.tbl_tvod_revenue": ["Tvod"],
    "dbo.tbl_vudo_daily": ["Vudo"],
    "dbo.Tubi_By_Episode_Daily": ["Tubi By Episode"],
    "dbo.Tubi_By_Platform_Daily": ["Tubi By Platform"],
    "dbo.VizioData": ["Vizio"],
    "dbo.xumo": ["Xumo"],
    "dbo.Youtube_AVOD_Rental": ["GooglePlay"],
    "dbo.Comscore_Daily": ["ComScore"]
}

# Fetch database credentials from environment variables
server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# Connect to SQL Server
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={user};"
    f"PWD={password}"
)

cursor = conn.cursor()

# Query schema metadata
cursor.execute("""
SELECT 
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION;
""")

rows = cursor.fetchall()
total = len(rows)

# Process only selected tables
allowed_tables = set(table_keywords_map.keys())
schema_metadata = {}
start_time = time.time()

filtered_rows = [row for row in rows if f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}" in allowed_tables]
total_filtered = len(filtered_rows)

for i, row in enumerate(filtered_rows, start=1):
    table_full_name = f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}"
    column_details = {
        "column": row.COLUMN_NAME,
        "data_type": row.DATA_TYPE,
        "nullable": row.IS_NULLABLE,
        "max_length": row.CHARACTER_MAXIMUM_LENGTH
    }

    if table_full_name not in schema_metadata:
        schema_metadata[table_full_name] = {
            "keywords": table_keywords_map.get(table_full_name, []),
            "columns": []
        }

    schema_metadata[table_full_name]["columns"].append(column_details)

    # Progress update
    if i % 25 == 0 or i == total_filtered:
        elapsed = time.time() - start_time
        avg_time_per_item = elapsed / i
        remaining = (total_filtered - i) * avg_time_per_item
        print(f"Processed {i}/{total_filtered} columns | Est. time left: {remaining:.1f} sec")

# Close connection
cursor.close()
conn.close()

# Save metadata to file
with open("schema_metadata.json", "w") as f:
    json.dump(schema_metadata, f, indent=4)

print("\nFiltered schema metadata written to 'schema_metadata.json'")
