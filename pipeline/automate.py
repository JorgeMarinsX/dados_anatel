import zipfile
import os
import requests
from loguru import logger

class ProcessadorDeArquivosZip:
    def __init__(self, url, zip_path, extracao_caminho, processamento_caminho):
        self.url = url
        self.zip_path = zip_path
        self.extracao_caminho = extracao_caminho
        self.processamento_caminho = processamento_caminho

        # Cria os diretórios de extração e processamento, se não existirem
        os.makedirs(self.extracao_caminho, exist_ok=True)
        os.makedirs(self.processamento_caminho, exist_ok=True)

        # Configuração do Loguru
        logger.add("processador_zip.log", rotation="10 MB", retention="10 days")

    def baixar_arquivo_zip(self):
        """
        Baixa o arquivo ZIP da URL especificada.
        """
        try:
            logger.info(f"Iniciando download do arquivo de {self.url} para {self.zip_path}")
            response = requests.get(self.url, stream=True)
            response.raise_for_status()  # Verifica se houve algum erro na requisição

            with open(self.zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logger.info(f"Download concluído com sucesso: {self.zip_path}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao baixar o arquivo: {e}")
            raise

    def extrair_arquivo(self, arquivo):
        """
        Extrai um arquivo específico do ZIP para o caminho de extração.
        """
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extract(arquivo, self.extracao_caminho)
                arquivo_extraido_caminho = os.path.join(self.extracao_caminho, arquivo)
                logger.info(f"Arquivo {arquivo} extraído com sucesso para {arquivo_extraido_caminho}")
                return arquivo_extraido_caminho
        except (zipfile.BadZipFile, zipfile.LargeZipFile) as e:
            logger.error(f"Erro ao extrair o arquivo {arquivo}: {e}")
            raise

    def processar_arquivo(self, arquivo_caminho):
        """
        Processa o arquivo extraído.
        Esta função pode ser personalizada para realizar qualquer processamento necessário.
        """
        try:
            # Exemplo de processamento, substituir com lógica real
            logger.info(f"Processando arquivo {arquivo_caminho}")
            pass
        except Exception as e:
            logger.error(f"Erro ao processar o arquivo {arquivo_caminho}: {e}")
            raise

    def salvar_arquivo(self, arquivo_origem, arquivo_nome):
        """
        Move ou salva o arquivo processado para o caminho de processamento final.
        """
        try:
            caminho_final = os.path.join(self.processamento_caminho, arquivo_nome)
            os.rename(arquivo_origem, caminho_final)
            logger.info(f"Arquivo {arquivo_nome} processado e salvo em {caminho_final}")
        except OSError as e:
            logger.error(f"Erro ao salvar o arquivo {arquivo_nome}: {e}")
            raise

    def processar_zip(self):
        """
        Itera sobre cada arquivo no ZIP, extraindo, processando e salvando.
        """
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                for arquivo in zip_ref.namelist():
                    arquivo_extraido_caminho = self.extrair_arquivo(arquivo)
                    self.processar_arquivo(arquivo_extraido_caminho)
                    self.salvar_arquivo(arquivo_extraido_caminho, arquivo)
        except Exception as e:
            logger.error(f"Erro ao processar o arquivo ZIP: {e}")
            raise

    def executar(self):
        """
        Método principal para baixar, extrair, processar e salvar arquivos.
        """
        try:
            self.baixar_arquivo_zip()
            self.processar_zip()
        except Exception as e:
            logger.critical(f"Falha no processo completo: {e}")
            raise

# Uso da classe

# URL do arquivo ZIP
url = 'https://www.anatel.gov.br/dadosabertos/paineis_de_dados/acessos/acessos_banda_larga_fixa.zip'

# Caminhos
zip_path = 'zipdownloader/arquivo.zip'
extracao_caminho = 'zipdownloader/temporarioextracao'
processamento_caminho = 'zipdownloader/processados'

# Instanciando e usando a classe
processador = ProcessadorDeArquivosZip(url, zip_path, extracao_caminho, processamento_caminho)
processador.executar()

