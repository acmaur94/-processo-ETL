# Projeto de ETL: Importação de Dados do Titanic (CSV) para MySQL

Este projeto foi desenvolvido como parte de uma avaliação para demonstrar um processo completo de **ETL (Extração, Transformação e Carga)**. O script Python realiza a extração de dados de arquivos CSV, neste caso, o famoso dataset do Titanic, e os carrega em um banco de dados MySQL.

## 📜 Descrição do Processo

O fluxo de ETL implementado funciona da seguinte maneira:

1.  **Extração (Extract):** O script lê todos os arquivos com a extensão `.csv` localizados na pasta `/data`.
2.  **Transformação (Transform):** Utilizando a biblioteca `pandas`, os dados do CSV são carregados em um DataFrame. Embora este projeto não realize transformações complexas, esta é a etapa onde limpezas, conversões de tipo ou enriquecimento de dados poderiam ser adicionados.
3.  **Carga (Load):** Os dados do DataFrame são inseridos, linha por linha, em uma tabela específica (`dados_titanic`) no banco de dados MySQL.

## Dataset Utilizado

O conjunto de dados utilizado para este exemplo é o **"Titanic: Machine Learning from Disaster"**, disponível no Kaggle. Ele contém informações demográficas e de viagem dos passageiros do RMS Titanic.

-   **Fonte:** [Kaggle Titanic Dataset](https://www.kaggle.com/c/titanic/data)
-   **Arquivo Exemplo:** `titanic.csv` (deve ser colocado na pasta `/data`)

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Bibliotecas:**
    * `pandas`
    * `mysql-connector-python`
* **Banco de Dados:** MySQL Server

## 📂 Estrutura do Projeto

O projeto está organizado da seguinte forma para manter a clareza e separação de responsabilidades: