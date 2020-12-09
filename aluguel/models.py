import datetime    

from django.db import models
from django.utils import timezone

from pathlib import Path
from artigo.models import Produto

from usuarios.models import Usuario

#now = timezone.now()
#utc=pytz.UTC 


class Aluguel(models.Model):
    usuario         = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    prod            = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    rent_in_process = models.BooleanField(default=True)
    not_rented      = models.BooleanField(default=True)
    rented_at       = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Aluguéis"

    def __str__(self):
        return self.prod.nome

    @classmethod
    def delete_after_one_or_five_hours(cls, self):
        '''
        Se nada acontecer, a instância do aluguel será deletada em uma hora (caso o usuário seja aluno) ou
        em cinco horas (caso seja professor) e o status do artigo vai de reservado para disponível.
        '''

        #created_time = self.created_at.replace(tzinfo=utc)

        if self.usuario.is_professor:
            time = datetime.datetime.now() - datetime.timedelta(minutes=300)
        else:
            time = datetime.datetime.now() - datetime.timedelta(minutes=60)
        
        if (self.created_at < time) and self.not_rented:
            produto = Produto.objects.get(id=self.prod.id)
            produto.rese = False
            produto.disp = True
            produto.save(update_fields=["disp", "rese"])
            aluguel = Aluguel.objects.get(pk=self.id)
            aluguel.delete()
            return True
        else:
            return False
        

    @classmethod
    def item_rented(cls, self):
        '''
        Se o usuário pegar o artigo antes , muda o status do artigo para alugado.
        '''
    
        if self.not_rented:
            produto = Produto.objects.get(id=self.prod.id)
            produto.alug = True
            produto.rese = False
            produto.save(update_fields=["alug", "rese"])
            return True
        else:
            return False

    @classmethod
    def delete_after_item_returned(cls, self):
        '''
        Se o usuário retornar o artigo, muda o status do artigo de alugado para disponível e
        deleta a instância do aluguel.
        '''

        produto = Produto.objects.get(id=self.prod.id)
        aluguel = Aluguel.objects.get(id=self.id)
        produto.disp = True
        produto.alug = False
        produto.save(update_fields=["disp", "alug"])
        return


    
