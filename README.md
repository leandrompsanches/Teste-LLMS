# Processamento de Lotes com LLM (OpenAI e Gemini)

Este projeto realiza a leitura de dados a partir de um arquivo CSV, processa cada linha criando um prompt padronizado (como, por exemplo, o planejamento de aulas baseados na BNCC) e então envia essas requisições a uma Inteligência Artificial (OpenAI ou Google Gemini). O resultado é armazenado num novo arquivo CSV.

## Arquitetura do Projeto

O código utiliza Programação Orientada a Objetos (POO), sendo dividido nos seguintes módulos:

- **`config.xml`**: Arquivo responsável por concentrar TODAS as configurações da aplicação.
- **`config.py`**: Contém a classe `ConfigManager`, que faz a leitura do arquivo `config.xml` e disponibiliza as configurações para as outras classes.
- **`llm_providers.py`**: Implementa uma interface/classe abstrata (`LLMProvider`) para padronizar as chamadas a diferentes APIs. Contém as implementações `OpenAIProvider` e `GeminiProvider`.
- **`processor.py`**: A classe `BatchProcessor` é responsável pela lógica principal: leitura e gravação de arquivos CSV, concatenação de templates, tratamento de exceções, e atrasos de limite de tempo (rate limit) entre as chamadas.
- **`main.py`**: O script principal (_entry point_), encarregado apenas de instanciar as classes e orquestrar a execução.

## Instalação das Bibliotecas

Para que o código funcione corretamente, é necessário instalar as bibliotecas oficiais das APIs que serão utilizadas:

1. Assegure-se de ter o Python instalado na sua máquina.
2. Você pode instalar as dependências rodando o seguinte comando no seu terminal:

```bash
pip install -r requirements.txt
```

Ou, instalar manualmente as bibliotecas caso prefira:
```bash
pip install openai google-genai
```

## Configuração (`config.xml`)

Antes de executar, você precisa inserir/verificar as suas Chaves de API no arquivo `config.xml`:

```xml
    <api_keys>
        <openai>sua-chave-aqui</openai>
        <google>sua-chave-aqui</google>
    </api_keys>
```

Você também pode configurar as seguintes sessões no XML:
- **IA Selecionada**: Qual IA será utilizada, na tag `<selected_ai>` (valores: `openai` ou `gemini`).
- **Modelos**: As versões exatas que você deseja invocar na tag `<models>`.
- **Rate Limit**: Tempo de espera (em segundos) entre as chamadas para evitar ser bloqueado pela API (`<rate_limit_delay>`).
- **Prompt**: O texto do prompt base na tag `<prompt><template>`.

## Como Executar

Após ter configurado o `config.xml` e instalado as dependências, execute no terminal:

```bash
python main.py
```

Acompanhe o andamento pelo log no terminal. O script irá criar um arquivo de resultados na pasta configurada, que por padrão é `resultados/experimento_{provedor}.csv`.
