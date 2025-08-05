
import google.generativeai as genai
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Mensagem
from django.utils.crypto import get_random_string


genai.configure(api_key="AIzaSyCTtyuCBklDxUEKN-cM000O-qwT2xBMnVg")

@csrf_exempt
def chat_gemini(request):
    # Gera ou obtém o ID da sessão do usuário
    sessao_id = request.session.get("sessao_id")
    if not sessao_id:
        sessao_id = get_random_string(32)
        request.session["sessao_id"] = sessao_id

    if request.method == "POST":
        pergunta = request.POST.get("pergunta", "").strip()
        print("➡️ Pergunta recebida:", pergunta)

        if pergunta:
            # Salva a pergunta no banco
            Mensagem.objects.create(autor="usuario", mensagem=pergunta, sessao_id=sessao_id)

            try:
                # Recupera as últimas N mensagens para contexto (opcional: limite de 6 a 10)
                historico = Mensagem.objects.filter(sessao_id=sessao_id).order_by("criado_em")
                contexto = ""
                for msg in historico:
                    prefixo = "Usuário:" if msg.autor == "usuario" else "Agente:"
                    contexto += f"{prefixo} {msg.mensagem}\n"

                prompt = f"""{contexto}
Responda a última mensagem do usuário, levando em conta o contexto acima.
Você é o agente de IA da Olimpo Real Estate. Fale em português, de forma objetiva e profissional."""

                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                resposta = response.text.strip()

            except Exception as e:
                import traceback
                traceback_str = traceback.format_exc()
                print("❌ ERRO COMPLETO AO CHAMAR IA:\n", traceback_str)
                resposta = f"Erro ao gerar resposta com IA: {str(e)}"

            # Salva a resposta no banco
            Mensagem.objects.create(autor="bot", mensagem=resposta, sessao_id=sessao_id)

    # Pega todo o histórico para exibir no chat
    conversa = Mensagem.objects.filter(sessao_id=sessao_id).order_by("criado_em")

    return render(request, "agente/index.html", {"conversa": conversa})


#TESTES

'''
import google.generativeai as genai
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key="AIzaSyCTtyuCBklDxUEKN-cM000O-qwT2xBMnVg")

conversas = []

@csrf_exempt  # apenas para testes locais. Em produção, mantenha o CSRF ativo.

def chat_gemini(request):
    # Obtém histórico ou inicializa
    if "conversa" not in request.session:
        request.session["conversa"] = []

    conversa = request.session["conversa"]

    if request.method == "POST":
        pergunta = request.POST.get("pergunta", "").strip()
        print("➡️ Pergunta recebida:", pergunta)

        if pergunta:
            # Adiciona a pergunta ao histórico
            conversa.append({"autor": "usuario", "mensagem": pergunta})

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = fPergunta: {pergunta}
Você é especialista no mercado imobiliário. Responda de forma clara e objetiva em português.
Se o usuário fizer te comprimentar, se apresente como Tey Magia, o agente de IA da Olimpo Real Estate e se disponha a ajudar.
Caso contrário, apenas responda a pergunta.

                response = model.generate_content(prompt)
                resposta = response.text.strip()

            except Exception as e:
                import traceback
                traceback_str = traceback.format_exc()
                print("❌ ERRO COMPLETO AO CHAMAR IA:\n", traceback_str)
                resposta = f"Erro ao gerar resposta com IA: {str(e)}"

            # Adiciona a resposta ao histórico
            conversa.append({"autor": "bot", "mensagem": resposta})
            request.session["conversa"] = conversa  # salva sessão
        else:
            print("⚠️ Pergunta vazia.")

    return render(request, "agente/index.html", {"conversa": conversa})


def home(request):
    return render(request, "agente/index.html")
'''