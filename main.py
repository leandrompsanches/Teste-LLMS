"""
Ponto de entrada principal da aplicação.
Orquestra a configuração, provedor de IA e processamento em lote.
"""
from config import ConfigManager
from llm_providers import OpenAIProvider, GeminiProvider
from processor import BatchProcessor

def main():
    try:
        # 1. Carrega as configurações do XML
        config = ConfigManager("config.xml")
        
        # 2. Instancia o provedor de LLM correto com base na configuração
        provedor_nome = config.ia_selecionada.lower()
        if provedor_nome == "openai":
            llm_provider = OpenAIProvider(api_key=config.openai_api_key, model_name=config.modelo_openai)
        elif provedor_nome == "gemini":
            llm_provider = GeminiProvider(api_key=config.google_api_key, model_name=config.modelo_gemini)
        else:
            raise ValueError(f"Provedor IA '{provedor_nome}' não suportado.")
            
        # 3. Inicializa e executa o processamento em lote
        processor = BatchProcessor(config, llm_provider)
        processor.process()
        
    except Exception as e:
        print(f"Erro fatal na inicialização da aplicação: {e}")

if __name__ == "__main__":
    main()