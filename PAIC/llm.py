from openai import OpenAI
from phi.assistant import Assistant
from cookbook.llm_os.assistant import get_llm_os

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
llm_os = get_llm_os(
    llm_id="local-llm",
    calculator=True,
    ddg_search=True,
    file_tools=True,
    shell_tools=True,
    data_analyst=True,
    python_assistant=True,
    research_assistant=True,
    investment_assistant=True,
)

def generate_content(prompt):
    if not prompt.strip():
        return "Desculpe, não entendi o comando."

    # Adicione um contexto inicial ao prompt
    initial_context = """Você é um assistente virtual que ajuda pessoas com deficiencia visual a usar e executar ações em um computador.
    Responda SEMPRE EM PORTUGUES, SEJA MUITO BREVE e JAMAIS UTILIZE caracteres "*" na sua resposta, EVITE RESPONDER EM TOPICOS,
    Lempre-se que sua resposta será utilizada num conversor de texto para voz, então responda sempre sabendo disso.
    Você possui várias ferramentas, como calculadora, pesquisador duckduckgo na internet, ferramentas de shell e de arquivos,
    pesquisa e investimentos, utilize sempre que possivei esses assistentes"""
    full_prompt = f"{initial_context}\n\n{prompt}"

    response = llm_os.run(full_prompt)
    response_text = ""

    try:
        for chunk in response:
            print("Debug: chunk content:", chunk)
            if hasattr(chunk, 'choices') and hasattr(chunk.choices[0].delta, 'content'):
                chunk_content = chunk.choices[0].delta.content
                response_text += chunk_content
            elif isinstance(chunk, str):
                response_text += chunk
    except Exception as e:
        response_text = "Não foi possível processar a resposta do assistente."

    return response_text
