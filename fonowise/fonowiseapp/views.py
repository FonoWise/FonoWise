import random
from django.shortcuts import render, redirect
from .models import Categoria, ProgressoUsuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('fonowiseapp:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('fonowiseapp:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('fonowiseapp:login')

@login_required
def dashboard(request):
    categorias = Categoria.objects.all()
    return render(request, 'dashboard.html', {"categorias": categorias})

@login_required
def progresso_view(request):
    progresso_por_categoria = ProgressoUsuario.objects.filter(usuario=request.user).order_by('categoria__nome')
    return render(request, 'progresso.html', {
        'progresso_list': progresso_por_categoria
    })

@login_required
def frase_view(request, categoria_id):
    try:
        categoria = Categoria.objects.get(id=categoria_id)

        # Garante que o progresso para esta categoria existe
        progresso, created = ProgressoUsuario.objects.get_or_create(
            usuario=request.user, 
            categoria=categoria
        )
        
        # Pega as frases que o usuário AINDA NÃO VIU
        frases_vistas_ids = progresso.frases_vistas.values_list('id', flat=True)
        frases_nao_vistas = categoria.frases.exclude(id__in=frases_vistas_ids)

        if frases_nao_vistas.exists():
            # Escolhe uma frase aleatória das não vistas
            frase = random.choice(list(frases_nao_vistas))
            frase_texto = frase.texto
            
            # Adiciona a nova frase ao progresso
            progresso.frases_vistas.add(frase)
            
        else:
            # O usuário já viu todas as frases desta categoria
            frase_texto = "Parabéns! Você concluiu todas as frases desta categoria."

    except Categoria.DoesNotExist:
        categoria = None
        frase_texto = "Categoria não encontrada."

    return render(request, 'frase.html', {
        "frase": frase_texto,
        "categoria": categoria,
        "nome_categoria": categoria.nome if categoria else "Inválida"
    })
