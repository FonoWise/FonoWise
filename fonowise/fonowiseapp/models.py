from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Frase(models.Model):
    texto = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='frases')

    def __str__(self):
        return self.texto

class ProgressoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    frases_vistas = models.ManyToManyField('Frase', blank=True)
    acertos = models.IntegerField(default=0)
    erros = models.IntegerField(default=0)
    data_ultimo_acesso = models.DateTimeField(auto_now=True)

    def total_frases(self):
        return self.categoria.frases.count()

    def frases_concluidas(self):
        return self.frases_vistas.count()

    def porcentagem(self):
        total = self.total_frases()
        return int((self.frases_concluidas() / total) * 100) if total else 0

    def __str__(self):
        return f"{self.usuario.username} - {self.categoria.nome}"
