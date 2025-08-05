from django.db import models

class Mensagem(models.Model):
    AUTOR_CHOICES = [
        ('usuario', 'Usuário'),
        ('bot', 'IA'),
    ]

    autor = models.CharField(max_length=10, choices=AUTOR_CHOICES)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    sessao_id = models.CharField(max_length=255)  # para identificar usuários/sessões

    def __str__(self):
        return f"[{self.autor}] {self.mensagem[:50]}"
