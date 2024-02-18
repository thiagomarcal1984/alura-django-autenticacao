from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib import auth, messages

from usuarios.forms import LoginForm, CadastroForm

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()

            usuario = auth.authenticate(
                request,
                username=nome, 
                password=senha
            )
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f'{nome} logado com sucesso.')
                return redirect('index')
            else:
                messages.error(request, 'Erro ao efetuar login.')
                return redirect('usuarios:login')
    return render(request, 'usuarios/login.html', { 'form' : form })

def cadastro(request):
    form = CadastroForm

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            if form['senha_1'].value() != form['senha_2'].value():
                messages.error(request, 'Senhas não são iguais.')
                return redirect('usuarios:cadastro')
            nome = form['nome_cadastro'].value()
            email = form['email'].value()
            senha = form['senha_1'].value()

            # Usuário existente no banco não pode ser recadastrado.
            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existente.')
                return redirect('usuarios:cadastro')
            
            # Criação do usuário
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            # Persistência dos dados do novo usuário.
            usuario.save()
            messages.success(request, 'Cadastro efetuado com sucesso.')
            return redirect('usuarios:login')
        
    return render(request, 'usuarios/cadastro.html', { 'form' : form})

def logout(request):
    messages.success(request, 'Logout efetuado com sucesso.')
    auth.logout(request)
    return redirect('usuarios:login')
