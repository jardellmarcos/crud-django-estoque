from django.shortcuts import render, redirect, get_object_or_404
from .models import Saidas
from .forms import SaidaForm

def list_saida(request):
    saidas = Saidas.objects.all()
    template_name = 'list_saida.html'
    context = {
        'saidas': saidas,
        }
    return render(request, template_name, context)

def new_saida(request):
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.cleaned_data['produto'].quantidade = form.cleaned_data['produto'].quantidade - form.cleaned_data['quantidade']
            form.cleaned_data['produto'].preco = form.cleaned_data['preco']
        
            form.cleaned_data['produto'].save_base()
            form.save()
            return redirect('saida:list_saida')
    
    else:
        form = SaidaForm()

    return render(request, 'new_saida.html', {'form': form})
    
def update_saida(request, pk):
    saida = get_object_or_404(Saidas, pk=pk)
    # saida = Saidas.objects.get(pk=pk)
    qtd_antiga = saida.quantidade

    print('==> ', qtd_antiga)
    if request.method == 'POST':
        form = SaidaForm(request.POST, instance=saida)

        if form.is_valid():
            produto = form.cleaned_data['produto']
            nova_qtd = form.cleaned_data['quantidade']
            disponivel = produto.quantidade + qtd_antiga

            if nova_qtd > disponivel:
                form.add_error('quantidade', 
                                f'So ha disponivel {disponivel} unidades no estoque.'
                    )
            
            else:
                produto.quantidade = disponivel - nova_qtd
                produto.preco = form.cleaned_data['preco']
                produto.save()
                form.save()
                return redirect('saida:list_saida')
    else:
        form = SaidaForm(instance=saida)    
    
    return render(request, 'update_saida.html', 
            {
                'form': form,
                'pk': pk,
            })
    
def delete_saida(request, pk):
    saida = Saidas.objects.get(pk=pk)
    saida.produto.quantidade = saida.produto.quantidade + saida.quantidade
    saida.produto.save()
    saida.delete()
    return redirect('saida:list_saida')