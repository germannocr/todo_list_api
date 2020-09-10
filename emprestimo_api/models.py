from django.db import models


class Emprestimo(models.Model):
    """
    The Emprestimo represents a loan of money that a user can apply for.
    """

    class Meta:

        db_table = 'emprestimo'

    id = models.AutoField(primary_key=True, unique=True)
    valor_nominal = models.DecimalField(max_digits=8, decimal_places=2)
    taxa_juros = models.DecimalField(max_digits=4, decimal_places=2)
    endereco_ip = models.CharField(max_length=20)
    data_solicitacao = models.CharField(max_length=10)
    banco = models.CharField(max_length=60)
    nome_cliente = models.CharField(max_length=120)
    saldo_devedor = models.DecimalField(max_digits=8, decimal_places=2)
    created_by_user = models.IntegerField()


class Pagamento(models.Model):
    """
    The Pagamento represents a payment that the user can make in connection with a loan made.
    """
    class Meta:
        db_table = 'pagamento'

    id = models.AutoField(primary_key=True, unique=True)
    identificador_emprestimo = models.IntegerField()
    data_pagamento = models.CharField(max_length=10)
    valor_pagamento = models.DecimalField(max_digits=8, decimal_places=2)
    created_by_user = models.IntegerField()
