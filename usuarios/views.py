from django.shortcuts import redirect, render

from django.contrib.auth.models import User

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
        user = User.objects.create(username=nome, email=email, password=password)
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
        print(email, senha)
        return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    pass

def dashboard(request):
    return render(request, 'usuarios/dashboard.html')
