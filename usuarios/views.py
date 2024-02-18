from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib import auth

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
                return redirect('index')
            else:
                return redirect('usuarios:login')
    return render(request, 'usuarios/login.html', { 'form' : form })

def cadastro(request):
    form = CadastroForm

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            if form['senha_1'].value() != form['senha_2'].value():
                return redirect('usuarios:cadastro')
            nome = form['nome_cadastro'].value()
            email = form['email'].value()
            senha = form['senha_1'].value()

            # Usuário existente no banco não pode ser recadastrado.
            if User.objects.filter(username=nome).exists():
                return redirect('usuarios:cadastro')
            
            # Criação do usuário
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            # Persistência dos dados do novo usuário.
            usuario.save()
            return redirect('usuarios:login')
        
    return render(request, 'usuarios/cadastro.html', { 'form' : form})
