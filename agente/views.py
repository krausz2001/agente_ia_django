import google.generativeai as genai
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key="AIzaSyCTtyuCBklDxUEKN-cM000O-qwT2xBMnVg")

@csrf_exempt  # apenas para testes locais. Em produção, mantenha o CSRF ativo.

def chat_gemini(request):
    resposta = None

    if request.method == "POST":
        pergunta = request.POST.get("pergunta", "")
        print("➡️ Pergunta recebida:", pergunta)

        if pergunta.strip():
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")

                prompt= f'''Pergunta: {pergunta}\nVocê é especialista no mercado imobiliário. Responda de forma clara e objetiva em português. 
                Se o usuário fizer te comprimentar, se apresente como Tey Magia, o agente de IA da Olimpo Real Estate e se disponha a ajudar.
                Caso contrário, apenas responda a pergunta.'''

                response = model.generate_content(prompt)
                print("✅ Resposta gerada:", response.text)
                resposta = response.text
            except Exception as e:
                    import traceback
                    traceback_str = traceback.format_exc()
                    print("❌ ERRO COMPLETO AO CHAMAR IA:\n", traceback_str)
                    resposta = f"Erro ao gerar resposta com IA: {str(e)}"
        else:
            print("⚠️ Pergunta vazia.")

    return render(request, "agente/index.html", {"resposta": resposta})


def home(request):
    return render(request, "agente/index.html")