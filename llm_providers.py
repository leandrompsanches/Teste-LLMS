"""
Módulo responsável pela integração com os provedores de Inteligência Artificial (LLMs).
"""
from abc import ABC, abstractmethod
import openai
from google import genai
from google.genai import types

class LLMProvider(ABC):
    """
    Classe base abstrata para provedores de LLM.
    
    Nota de Arquitetura:
    Parâmetros como `api_key` e `model_name` foram intencionalmente omitidos. Embora comuns hoje, os requisitos de inicialização podem variar em novas implementações (ex: URLs para endpoints dedicados ou modelos locais sem credenciais).
    """
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Gera uma resposta baseada no prompt fornecido.
        
        Args:
            prompt (str): O texto de entrada para o LLM.
            
        Returns:
            str: O texto gerado pelo modelo.
        """
        pass

class OpenAIProvider(LLMProvider):
    """
    Implementação do provedor de LLM da OpenAI.
    """
    def __init__(self, api_key: str, model_name: str):
        """
        Inicializa o provedor OpenAI com a chave de API e modelo específicos.
        
        Args:
            api_key (str): A chave de API da OpenAI.
            model_name (str): O nome do modelo a ser utilizado (ex: gpt-3.5-turbo).
        """
        openai.api_key = api_key
        self.model_name = model_name

    def generate_response(self, prompt: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0 
            )
            return response.choices[0].message.content.replace('\n', ' \\ ')
        except Exception as e:
            return f"Erro na API OpenAI: {str(e)}"

class GeminiProvider(LLMProvider):
    """
    Implementação do provedor de LLM do Google Gemini.
    """
    def __init__(self, api_key: str, model_name: str):
        """
        Inicializa o provedor Gemini com a chave de API e modelo específicos.
        
        Args:
            api_key (str): A chave de API do Google.
            model_name (str): O nome do modelo a ser utilizado (ex: gemini-2.5-flash).
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.config = types.GenerateContentConfig(temperature=0.0)

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.config
            )
            return response.text.replace('\n', ' ')
        except Exception as e:
            return f"Erro na API Gemini: {str(e)}"
