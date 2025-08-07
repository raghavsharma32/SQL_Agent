import re

def get_best_matching_schema(prompt: str) -> str:
    schema_file_path = "/Users/raghavsharma/Desktop/aiPoweredAssistant/RAG/Indexing/schema_metadata.txt"
    
    def parse_schema_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        table_blocks = content.split('Table:')
        schemas = []

        for block in table_blocks[1:]:
            lines = block.strip().split('\n')
            table_name = lines[0].strip()
            keywords_line = next((line for line in lines if line.lower().startswith('keywords:')), '')
            
            # Extract full schema block
            schema_block = "\n".join(lines)

            # Extract keywords
            keyword_matches = re.findall(r'\w+', keywords_line.lower())
            keywords = set(keyword_matches)

            schemas.append({
                "table": table_name,
                "keywords": keywords,
                "schema": schema_block.strip()
            })

        return schemas

    def find_best_match(prompt, schemas):
        prompt_words = set(re.findall(r'\w+', prompt.lower()))
        best_schema = None
        best_score = 0

        for schema in schemas:
            score = len(prompt_words & schema["keywords"])
            if score > best_score:
                best_schema = schema
                best_score = score

        return best_schema

    schemas = parse_schema_file(schema_file_path)
    best_match = find_best_match(prompt, schemas)

    return best_match['schema'] if best_match else "No relevant schema found."
