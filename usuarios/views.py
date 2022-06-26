from django.shortcuts import redirect, render

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import auth

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if not nome.strip(): # O método strip remove os espaços em branco do início e do fim da String.
            print('O campo nome não pode ficar em branco.')
            return redirect('cadastro')
        if not email.strip(): # O método strip remove os espaços em branco do início e do fim da String.
            print('O campo e-mail não pode ficar em branco.')
            return redirect('cadastro')
        if password != password2:
            print('As senhas não são iguais.')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            print('Usuário já cadastrado.')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=password)
        user.save()
        print('Usuário cadastrado com sucesso.')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if email == '' or senha == '':
            print('Os campos e-mail e senha não podem ficar em branco.')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            # O método values_list retorna um Queryset com as colunas indicadas como parâmetro.
            # Flat significa retorno de um único objeto por linha, ao invés de uma lista
            # de tuplas que contenham um elemento. Veja:
            # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#values-list
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso.')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html')
    else:
        return redirect('index')

def cria_receita(request):
    return render(request, 'usuarios/cria_receita.html')