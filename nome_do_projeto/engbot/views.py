from django.shortcuts import render, redirect
from .utilits import AI
from django.shortcuts import get_object_or_404

#entender o cache do gemini, criação de chats auxiliares (evita sobreuso de tokens)

# Create your views here.
def chat(request, chat_id):
    chat = AI()
    if request.method == "POST":
        data = request.POST.get('data')
        chat.make_ai_request(chat_id=chat_id, current_data=data)
    chatobj = chat.get_chat(chat_id=chat_id)
    messages = chat.render_chat(chatobj)
    return render(request, 'index.html', {'messages': messages})

def gerar_relatorio(request):
    if request.method == "POST":
        return AI().gerar_relatorio(request.POST)        
    return render(request, 'gerar_relatorio.html')

def index(request):
    return render(request, "lanpage.html")