"""
Módulo responsável por gerenciar as configurações da aplicação.
"""
import xml.etree.ElementTree as ET

class ConfigManager:
    """
    Lê e armazena as configurações a partir de um arquivo XML.
    """
    def __init__(self, xml_path: str = "config.xml"):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            xml_path (str): Caminho para o arquivo XML de configuração.
        """
        self.xml_path = xml_path
        self.openai_api_key = ""
        self.google_api_key = ""
        self.modelo_openai = ""
        self.modelo_gemini = ""
        self.ia_selecionada = ""
        self.rate_limit_delay = 0
        self.arquivo_entrada = ""
        self.arquivo_saida_base = ""
        self.prompt_template = ""
        
        self._carregar_configuracoes()

    def _carregar_configuracoes(self):
        """
        Lê o arquivo XML e popula os atributos da classe.
        """
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
            
            # Chaves de API
            self.openai_api_key = root.findtext('api_keys/openai', default="").strip()
            self.google_api_key = root.findtext('api_keys/google', default="").strip()
            
            # Modelos
            self.modelo_openai = root.findtext('models/openai', default="").strip()
            self.modelo_gemini = root.findtext('models/gemini', default="").strip()
            
            # Execução
            self.ia_selecionada = root.findtext('execution/selected_ai', default="").strip()
            self.rate_limit_delay = int(root.findtext('execution/rate_limit_delay', default="30").strip())
            
            # Arquivos
            self.arquivo_entrada = root.findtext('files/input', default="").strip()
            self.arquivo_saida_base = root.findtext('files/output_base', default="").strip()
            
            # Prompt
            self.prompt_template = root.findtext('prompt/template', default="").strip()
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de configuração '{self.xml_path}' não encontrado.")
        except ET.ParseError as e:
            raise ValueError(f"Erro ao fazer o parse do arquivo XML '{self.xml_path}': {e}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao carregar configurações: {e}")
