import sqlite3

def connect_db():
    conn = sqlite3.connect("caseirinhos.db")
    return conn

def cria_tabela_produto(conn): #id, nome, preco, preco_por_kg
    create_table_query = """
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    preco FLOAT,
    preco_por_kg FLOAT,
    unidade_medida TEXT, 
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
    conn.execute(create_table_query)

def insere_produto(id, nome, preco, preco_por_kg, unidade_medida, timestamp):
    conn = connect_db()
    
    with conn:
        conn.execute(
            """
            INSERT INTO produtos (id, nome, preco, preco_por_kg, unidade_medida, timestamp) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (id, nome, preco, preco_por_kg, unidade_medida, timestamp)
        )

    conn.commit()
    conn.close()

def update_produto(id, preco, preco_por_kg, timestamp):
    conn = connect_db()
    
    with conn:
        conn.execute(
            """
            UPDATE produtos
            SET preco = ?, 
            preco_por_kg = ?,
            timestamp = ?
            WHERE id = ?
            """,
            (preco, preco_por_kg, timestamp, id)
        )

    conn.commit()
    conn.close()

def produto_inserido(id):
    conn = connect_db()
    cursor = conn.execute("""SELECT id FROM produtos WHERE id= ?""", (id,))
    print(type(cursor))
    return cursor

    




if __name__ == "__main__":
    conn = connect_db()
    cria_tabela_produto(conn) 
    conn.close()
