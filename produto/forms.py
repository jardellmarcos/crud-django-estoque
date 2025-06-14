from django.forms import ModelForm,TextInput, Textarea
from .models import Produtos 

class ProdutoForm(ModelForm): 
    class Meta: 
        model = Produtos 
        fields = ['produto', 'cor', 'descricao']
       