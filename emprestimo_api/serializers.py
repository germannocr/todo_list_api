from rest_framework import serializers
from emprestimo_api.models import (
    Emprestimo,
    Pagamento
)


class EmprestimoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Emprestimo
        fields = '__all__'


class PagamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pagamento
        fields = '__all__'
