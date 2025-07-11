import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

# --- CONFIGURAÇÕES ---

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'etl_db'
}

# Caminho para o arquivo CSV
CSV_PATH = os.path.join('data', 'Titanic.csv')


# --- EXTRAÇÃO (EXTRACT) ---

def extrair_dados(caminho_arquivo):
    """
    Extrai dados de um arquivo CSV.
    Retorna um DataFrame do Pandas.
    """
    print(f"Iniciando extração do arquivo: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo)
        print("Extração concluída com sucesso.")
        return df
    except FileNotFoundError:
        print(f"Erro: O arquivo não foi encontrado em '{caminho_arquivo}'")
        return None


# --- TRANSFORMAÇÃO (TRANSFORM) ---

def transformar_dados(df):
    """
    Aplica transformações nos dados do Titanic.
    """
    if df is None:
        return None

    print("Iniciando transformação dos dados...")

    # 1. Mapear valores da coluna 'Survived' para textos mais claros
    df['Survived'] = df['Survived'].map({0: 'Não Sobreviveu', 1: 'Sobreviveu'})

    # 2. Mapear valores da coluna 'Pclass'
    df['Pclass'] = df['Pclass'].map({1: 'Primeira Classe', 2: 'Segunda Classe', 3: 'Terceira Classe'})
    
    # 3. Preencher valores de idade ausentes com a média
    media_idade = df['Age'].mean()
    df['Age'].fillna(media_idade, inplace=True)
    
    # 4. Remover colunas que não serão usadas na análise final
    df.drop(columns=['Cabin', 'Ticket', 'Name'], inplace=True)

    # 5. Renomear colunas para maior clareza no banco de dados
    df.rename(columns={
        'PassengerId': 'id_passageiro',
        'Survived': 'sobreviveu',
        'Pclass': 'classe_passagem',
        'Sex': 'sexo',
        'Age': 'idade',
        'SibSp': 'familiares_a_bordo',
        'Parch': 'agregados_a_bordo',
        'Fare': 'tarifa_paga',
        'Embarked': 'porto_embarque'
    }, inplace=True)
    
    # 6. Preencher valores ausentes em 'porto_embarque' com a moda (valor mais comum)
    moda_embarque = df['porto_embarque'].mode()[0]
    df['porto_embarque'].fillna(moda_embarque, inplace=True)

    print("Transformação concluída.")
    return df


# --- CARGA (LOAD) ---

def carregar_dados(df):
    """
    Carrega os dados transformados em uma tabela do MySQL.
    """
    if df is None:
        print("Nenhum dado para carregar. Processo interrompido.")
        return

    conn = None
    try:
        print("Conectando ao banco de dados MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        
        if conn.is_connected():
            cursor = conn.cursor()
            print("Conexão bem-sucedida. Iniciando carga de dados...")

            # Limpar a tabela antes de carregar novos dados para evitar duplicatas
            cursor.execute("TRUNCATE TABLE passageiros_titanic")
            print("Tabela 'passageiros_titanic' limpa.")

            # Preparar a query de inserção
            query = """
                INSERT INTO passageiros_titanic (
                    id_passageiro, sobreviveu, classe_passagem, sexo, idade,
                    familiares_a_bordo, agregados_a_bordo, tarifa_paga, porto_embarque
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Converter DataFrame para uma lista de tuplas para inserção
            dados_para_inserir = [tuple(row) for row in df.to_numpy()]

            # Executar a inserção em massa
            cursor.executemany(query, dados_para_inserir)
            conn.commit()

            print(f"{cursor.rowcount} registros foram inseridos com sucesso na tabela 'passageiros_titanic'.")

    except Error as e:
        print(f"Erro durante a carga no MySQL: {e}")

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexão com o MySQL foi encerrada.")


# --- ORQUESTRADOR DO ETL ---

if __name__ == "__main__":
    print("--- INICIANDO PROCESSO ETL: Titanic CSV para MySQL ---")
    
    # 1. Extração
    dados_brutos = extrair_dados(CSV_PATH)
    
    # 2. Transformação
    dados_transformados = transformar_dados(dados_brutos)
    
    # 3. Carga
    carregar_dados(dados_transformados)
    
    print("--- PROCESSO ETL CONCLUÍDO ---")