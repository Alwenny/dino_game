import mysql.connector

class BancoDeDados:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""      # Sua senha do MySQL
        self.database = "" # Nome do BD
        
        self.preparar_banco()

    def conectar(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def preparar_banco(self):
        """Cria o Banco e a Tabela 'rankingdb' conforme especificado"""
        try:
            conexao_root = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password
            )
            cursor = conexao_root.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            conexao_root.close()
            
            conexao_db = self.conectar()
            cursor = conexao_db.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rankingdb (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(10),
                    pontos INT
                )
            """)
            print("Tabela 'rankingdb' verificada com sucesso!")
            conexao_db.close()
            
        except Exception as e:
            print(f"ERRO NO MYSQL: {e}")

    def inserir_recorde(self, nome, pontos):
        try:
            conexao = self.conectar()
            cursor = conexao.cursor()
            
            sql = "INSERT INTO rankingdb (nome, pontos) VALUES (%s, %s)"
            valores = (nome, pontos)
            
            cursor.execute(sql, valores)
            conexao.commit()
            
            print(f"MySQL: {nome} salvo na tabela rankingdb!")
            conexao.close()
        except Exception as e:
            print(f"Erro ao salvar: {e}")
    
    def consultar_melhores(self):
        try:
            conexao = self.conectar()
            cursor = conexao.cursor()
            

            sql = "SELECT nome, pontos FROM rankingdb ORDER BY pontos DESC LIMIT 5"
            
            cursor.execute(sql)
            
            resultado = cursor.fetchall() 
            
            conexao.close()
            return resultado
            
        except Exception as e:
            print(f"Erro ao consultar: {e}")
            return []