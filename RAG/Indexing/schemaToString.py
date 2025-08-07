# import json

# # Load schema metadata from the JSON file
# with open("schema_metadata.json", "r") as f:
#     schema_metadata = json.load(f)

# # Now you can use schema_metadata like before
# documents = []
# for table, columns in schema_metadata.items():
#     formatted_columns = []
#     for col in columns:
#         col_str = f"{col['column']} ({col['data_type']}, nullable={col['nullable']}, max_len={col['max_length']})"
#         formatted_columns.append(col_str)
#     doc = f"Table: {table}\nColumns:\n  - " + "\n  - ".join(formatted_columns)
#     documents.append(doc)

# # Optionally print or save again
# print(documents[0])  # preview one document

# with open("schema_metadata.txt", "w") as f:
#     f.write("\n\n".join(documents))

# print("✅ Formatted schema documentation written to 'schema_metadata.txt'")


import json

# Load schema metadata from the JSON file
with open("schema_metadata.json", "r") as f:
    schema_metadata = json.load(f)

# Process the metadata
documents = []
for table, table_info in schema_metadata.items():
    keywords = table_info.get("keywords", [])
    columns = table_info.get("columns", [])

    # Format keywords
    keywords_str = ", ".join(keywords)

    # Format columns
    formatted_columns = []
    for col in columns:
        max_len = col['max_length'] if col['max_length'] is not None else "N/A"
        col_str = f"{col['column']} ({col['data_type']}, nullable={col['nullable']}, max_len={max_len})"
        formatted_columns.append(col_str)

    # Compose document
    doc = (
        f"Table: {table}\n"
        f"Keywords: {keywords_str}\n"
        f"Columns:\n  - " + "\n  - ".join(formatted_columns)
    )
    documents.append(doc)

# Preview one document
print(documents[0])

# Write to text file
with open("schema_metadata.txt", "w") as f:
    f.write("\n\n".join(documents))

print("✅ Formatted schema documentation written to 'schema_metadata.txt'")
