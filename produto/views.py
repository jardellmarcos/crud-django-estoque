from django.shortcuts import get_object_or_404, render, redirect
from .models import Produtos
from .forms import ProdutoForm



def list_produto(request): 
  produtos = Produtos.objects.all() 
  template_name = 'list_produto.html' 
  context = { 
    'produtos': produtos, 
  } 
  return render(request, template_name, context)

 
def new_produto(request): 
    if request.method == 'POST': 
        form = ProdutoForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('produto:list_produto') 
    else: 
        template_name = 'new_produto.html' 
        context = { 
        'form': ProdutoForm(), 
        } 
        return render(request, template_name, context) 
    
def update_produto(request, pk): 
        # produto = Produtos.objects.get(pk=pk) 
        produto = get_object_or_404(Produtos, pk=pk)
        if request.method == 'POST': 
            form = ProdutoForm(request.POST, instance=produto) 
            if form.is_valid(): 
                form.save() 
                return redirect('produto:list_produto') 
        else: 
            form = ProdutoForm(instance=produto)

        return render(request, 'update_produto.html', {
        'form': form,
        'pk': produto.pk,
        })

def delete_produto(request, pk): 
    produto = Produtos.objects.get(pk=pk) 
    produto.delete() 
    return redirect('index')