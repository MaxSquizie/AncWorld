import sqlite3
from graphviz import Digraph

def extract_db_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}

    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()

        schema[table_name] = {
            "columns": columns,
            "foreign_keys": foreign_keys
        }

    conn.close()
    return schema

def visualize_schema(schema, output_path):
    dot = Digraph()

    for table, details in schema.items():
        columns = details["columns"]
        foreign_keys = details["foreign_keys"]

        table_desc = f"{table}\n" + "\n".join([f"{col[1]} ({col[2]})" for col in columns])
        dot.node(table, table_desc)

        for fk in foreign_keys:
            from_table = table
            to_table = fk[2]
            from_column = fk[3]
            to_column = fk[4]
            dot.edge(from_table, to_table, label=f"{from_column} -> {to_column}")

        # Сохраняем и отображаем визуализацию
    dot.render(output_path, format='png', cleanup=True)

db_path = "C:/Users/Илья/PycharmProjects/pythonProject/anc_world/project.db"
output_path = 'db_schema'
schema = extract_db_schema(db_path)
visualize_schema(schema, output_path)

print(f"Схема базы данных сохранена в файл: {output_path}.png")

