import json
import os
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Categorias e suas frases
CATEGORIAS = {
    "trava_lingua": "Trava-Língua",
    "palavras_dificeis": "Palavras Difíceis",
    "fonemas_especificos": "Fonemas Específicos",
    "vogais_ditongos": "Vogais e Ditongos",
    "saudacoes": "Saudações",
    "expressoes_comuns": "Expressões Comuns",
    "comidas": "Comidas",
    "cores": "Cores",
    "animais": "Animais",
    "profissoes": "Profissões"
}

# Frases por categoria
FRASES = {
    "trava_lingua": [
        "O rato roeu a roupa do rei de Roma",
        "A aranha arranha a rã",
        "O doce perguntou ao doce qual é o doce mais doce",
        "Três pratos de trigo para três tigres tristes",
        "O tempo perguntou ao tempo quanto tempo o tempo tem"
    ],
    "palavras_dificeis": [
        "Paralelepípedo",
        "Otorrinolaringologista",
        "Pneumoultramicroscopicossilicovulcanoconiose",
        "Inconstitucionalissimamente",
        "Anticonstitucionalissimamente"
    ],
    "fonemas_especificos": [
        "O cachorro corre no campo",
        "A xícara está cheia de chá",
        "O gato mia no telhado",
        "A zebra corre na savana",
        "O jacaré nada no rio"
    ],
    "vogais_ditongos": [
        "O céu está azul",
        "A águia voa alto",
        "O boi pasta no campo",
        "A noite cai suave",
        "O rei governa o país"
    ],
    "saudacoes": [
        "Bom dia, tudo bem?",
        "Boa tarde, como vai?",
        "Boa noite, prazer em conhecer",
        "Olá, tudo bem com você?",
        "Oi, como você está?"
    ],
    "expressoes_comuns": [
        "Por favor, me ajude",
        "Muito obrigado pela ajuda",
        "Desculpe pelo transtorno",
        "Pode me ajudar com isso?",
        "Não entendi, pode repetir?"
    ],
    "comidas": [
        "O arroz está quente",
        "A feijoada é uma comida típica",
        "O brigadeiro é muito doce",
        "A pizza está deliciosa",
        "O churrasco é uma tradição"
    ],
    "cores": [
        "Vermelho, azul, amarelo",
        "Verde, roxo, laranja",
        "Rosa, marrom, preto",
        "Branco, cinza, bege",
        "Roxo, lilás, turquesa"
    ],
    "animais": [
        "O leão é o rei da selva",
        "O elefante é um animal grande",
        "A girafa tem pescoço comprido",
        "O macaco pula de galho em galho",
        "O tigre tem listras pretas"
    ],
    "profissoes": [
        "O médico cuida dos doentes",
        "O professor ensina os alunos",
        "O engenheiro constrói prédios",
        "O advogado defende as pessoas",
        "O chef cozinha com amor"
    ]
}

def dashboard(request):
    return render(request, 'dashboard.html', {"categorias": CATEGORIAS})

def frase_view(request, categoria):
    # Obtém a lista de frases para a categoria
    frases = FRASES.get(categoria, [])
    
    # Obtém a última frase usada da sessão
    ultima_frase = request.session.get('ultima_frase', '')
    
    # Remove a última frase da lista (se existir e se houver mais de uma frase)
    if ultima_frase in frases and len(frases) > 1:
        frases.remove(ultima_frase)
    
    # Escolhe uma frase aleatória
    if frases:
        frase = random.choice(frases)
        request.session['ultima_frase'] = frase
    else:
        frase = "Nenhuma frase disponível para esta categoria."
    
    return render(request, 'frase.html', {
        "frase": frase,
        "categoria": categoria,
        "nome_categoria": CATEGORIAS.get(categoria, categoria)
    })
