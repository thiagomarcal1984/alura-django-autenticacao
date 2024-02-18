from django.shortcuts import render, redirect

from usuarios.forms import LoginForm, CadastroForm

def login(request):
    form = LoginForm()
    return render(request, 'usuarios/login.html', { 'form' : form })

def cadastro(request):
    form = CadastroForm

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form['senha_1'].value() != form['senha_2'].value():
            return redirect('usuarios:cadastro')
        
    return render(request, 'usuarios/cadastro.html', { 'form' : form})
