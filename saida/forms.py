from django import forms
from .models import Saidas

class SaidaForm(forms.ModelForm):
    class Meta:
        model = Saidas
        fields = ['produto', 'quantidade', 'preco']

    def clean_quantidade(self):
        qtd = self.cleaned_data.get('quantidade')
        produto = self.cleaned_data.get('produto')

        if self.instance.pk:
            qtd_antiga = self.instance.quantidade
            disponivel = produto.quantidade + qtd_antiga
        else:
            disponivel = produto.quantidade

        if qtd > disponivel:
            raise forms.ValidationError(
                f'Voce so tem {disponivel} unidades disponiveis no estoque.'
            )
        return qtd


       