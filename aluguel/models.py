import datetime

from django.db import models

from pathlib import Path
from artigo.models import Produto

from usuarios.models import Usuario

class Aluguel(models.Model):
    usuario         = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    prod            = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    user_returned   = models.BooleanField(default=False)
    rented          = models.BooleanField(default=False)
    rented_at       = models.DateTimeField(default=None)


    # DEVEMOS DAR UPDATE NO ATUAL ESTADO DO PRODUTO RELACIONADO ASSIM QUE O OBJETO ALUGUEL FOR CRIADO

    @property
    def delete_after_two_hours(self):
        '''
        Se nada acontecer, a instância do aluguel será deletada em cinco horas e o status do artigo vai de reservado para disponível.
        '''

        time = datetime.datetime.now() - datetime.timedelta(minutes=120)
        if (self.created_at < time) and not self.alugado:
            produto = Produto.objects.get(id=self.prod)
            produto.update(disp=True)
            produto.update(rese=False)
            # Talvez implementar aqui também o ban do usuário?
            aluguel = Aluguel.objects.get(pk=self.id)
            aluguel.delete()
            return True
        else:
            return False

    @property
    def item_rented(self):
        '''
        Se o usuário pegar o artigo em menos de cinco horas, muda o status do artigo para alugado.
        '''

        if self.alugado:
            produto = Produto.objects.get(id=self.prod)
            produto.update(alug=True)
            produto.update(rese=False)


    @property
    def delete_after_item_returned(self):
        '''
        Se o usuário retornar o artigo, muda o status do artigo de alugado para disponível e
        deleta a instância do aluguel.
        '''

        if self.user_returned:
            produto = self.prod
            aluguel = Aluguel.objects.get(pk=self.id)
            produto = Produto.objects.get(nome=produto)
            produto.update(disp=True)
            produto.update(alug=False)
            aluguel.delete()
            return True
        else:
            return False
    


'''

Provavelmente não vamos precisar da implementação do ItemDeAluguel,
mas ta aqui pra não se perder caso formos precisar

produto   = models.ManyToManyField(Produto, through='ItemDeAluguel')

class ItemDeAluguel(models.Model):
    aluguel = models.ForeignKey(Aluguel, default="deafult", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, default="default", on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Itens De Aluguel"

'''