"""
Módulo responsável pela orquestração e processamento em lote dos dados.
"""
import os
import csv
import time
from config import ConfigManager
from llm_providers import LLMProvider

class BatchProcessor:
    """
    Classe para processar as linhas de um arquivo CSV utilizando um provedor LLM.
    """
    def __init__(self, config: ConfigManager, llm_provider: LLMProvider):
        """
        Inicializa o processador em lote.
        
        Args:
            config (ConfigManager): Objeto contendo as configurações.
            llm_provider (LLMProvider): O provedor LLM instanciado que será utilizado.
        """
        self.config = config
        self.llm = llm_provider

    def process(self):
        """
        Executa a leitura do arquivo de entrada, chama a IA para cada linha e salva no arquivo de saída.
        """
        caminho_out = self.config.arquivo_saida_base.format(provedor=self.config.ia_selecionada.lower())
        os.makedirs(os.path.dirname(caminho_out), exist_ok=True)

        # Lógica para continuar de onde parou (Resume)
        linhas_processadas = 0
        modo_abertura = 'w'
        if os.path.exists(caminho_out):
            with open(caminho_out, 'r', encoding='utf-8-sig') as f_existente:
                reader_existente = csv.reader(f_existente, delimiter=';')
                linhas_processadas = max(0, sum(1 for _ in reader_existente) - 1) # subtrai o cabeçalho
            
            if linhas_processadas > 0:
                modo_abertura = 'a'

        try:
            with open(self.config.arquivo_entrada, 'r', encoding='utf-8') as f_in, \
                 open(caminho_out, modo_abertura, newline='', encoding='utf-8-sig') as f_out:
                
                reader = csv.reader(f_in)
                writer = csv.writer(f_out, delimiter=';')
                
                if modo_abertura == 'w':
                    writer.writerow(['Tema', 'Ano', 'Resposta'])

                linhas = list(reader)
                total_linhas = len(linhas)
                
                if linhas_processadas >= total_linhas:
                    print(f"Todas as {total_linhas} linhas já foram processadas no arquivo de saída!")
                    return

                print(f"Iniciando processamento na IA: {self.config.ia_selecionada.upper()}")
                print(f"Total: {total_linhas} linhas | Já processadas: {linhas_processadas} | Restantes: {total_linhas - linhas_processadas}")
                print("-" * 50)

                for contador, linha in enumerate(linhas, 1):
                    # Pula as linhas que já foram processadas anteriormente
                    if contador <= linhas_processadas:
                        continue

                    if len(linha) < 2:
                        print(f"Aviso: Linha {contador} ignorada por falta de colunas: {linha}")
                        continue

                    tema = linha[0].strip()
                    ano = linha[1].strip()

                    prompt_final = self.config.prompt_template.format(tema=tema, ano=ano)
                    
                    print(f"\n[{contador}/{total_linhas}] Processando tema: '{tema}' (Ano: {ano})")
                    print(f"--- Prompt Enviado ---\n{prompt_final}\n----------------------")
                    print(f"Aguardando resposta da IA ({self.config.ia_selecionada.upper()})...")
                    
                    # Lógica de Retry (tentar novamente) em caso de Erro de Rate Limit (429)
                    tentativas = 0
                    max_tentativas = 3
                    while tentativas < max_tentativas:
                        resposta = self.llm.generate_response(prompt_final)
                        
                        # Verifica se a IA retornou erro de limite de requisições
                        if "Erro na API" in resposta and ("429" in resposta or "Too Many Requests" in resposta or "exhausted" in resposta.lower()):
                            tentativas += 1
                            if tentativas < max_tentativas:
                                tempo_espera = self.config.rate_limit_delay * 2
                                print(f"⚠️ Alerta: Muitas solicitações enviadas (Rate Limit). Aguardando {tempo_espera}s para tentar de novo (Tentativa {tentativas}/{max_tentativas})...")
                                time.sleep(tempo_espera)
                            else:
                                print("❌ Falha após várias tentativas. O erro será salvo no CSV.")
                        else:
                            break # Sai do loop se a resposta foi sucesso ou outro erro não relacionado a limite

                    writer.writerow([tema, ano, resposta])
                    f_out.flush() # Força o salvamento imediato no arquivo a cada linha
                    
                    print(f"[{contador}/{total_linhas}] Resposta recebida e salva com sucesso!")

                    # Pausa para respeitar o Rate Limit (429) se não for o último
                    if contador < total_linhas:
                        print(f"Aguardando {self.config.rate_limit_delay} segundos (Rate Limit) antes da próxima chamada...")
                        time.sleep(self.config.rate_limit_delay)

            print("-" * 50)
            print(f"Sucesso! Lote concluído. Arquivo salvo em: {caminho_out}")

        except FileNotFoundError:
            print(f"Erro: O arquivo de entrada '{self.config.arquivo_entrada}' não foi encontrado.")
        except Exception as e:
            print(f"Erro crítico no processamento: {e}")
