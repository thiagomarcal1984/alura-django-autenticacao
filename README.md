# Preparando o ambiente
Basicamente baixando os arquivos, criando o ambiente virtual, realizando as migrações , coletando arquivos estáticos etc.

Lembrando que o banco de dados estava vazio até então. Por isso foi necessário subir imagem por imagem novamente no banco.

O diretório `media` na raiz é o que vai receber os arquivos enviados via upload do usuário. Como ele está ignorado no `.gitignore`, isso não é claramente visível no repositório.

# Criando nova app
Comando para a criação do novo app `usuários`:
```shell
(.venv) PS D:\alura\django-autenticacao> python manage.py startapp usuarios
```

Atualização dos aplicativos disponíveis no projeto dentro do arquivo `settings.py`:
```python
# Resto do código
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'galeria.apps.GaleriaConfig',
    # Aqui fica a classe UsuariosConfig que está no novo app usuarios.
    'usuarios.apps.UsuariosConfig', 
]
# Resto do código
```

Criação do arquivo `urls.py` interno ao projeto `usuarios`:
```python
from django.urls import path

urlpatterns = [
    # path('', view), # A view será inserida posteriormente.
]
```

Atualização do arquivo `urls.py` interno ao projeto raiz `setup`:
```python
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('galeria.urls')),
    path('usuarios/', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
Na próxima aula criaremos as views associadas ao app `usuarios`.

# URLs e Views
Criação das views `login` e `cadastro` no arquivo `usuarios/urls.py`:

```python
from django.shortcuts import render

def login(request):
    return render(request, 'usuarios/login.html')

def cadastro(request):
    return render(request, 'usuarios/cadastro.html')
```
> Os arquivos HTML foram criados dentro da pasta de templates, localizados na raiz do projeto, conforme arquivo `settings.py`:
> ```python
> # Resto do código
> TEMPLATES = [
>     {
>        'BACKEND': 'django.template.backends.django.DjangoTemplates',
>        'DIRS': [os.path.join(BASE_DIR, 'templates')],
>        # Resto do código
>     }
> ]
> ```
> Assim, o caminho completo dos arquivos HTML são `/templates/usuarios/login.html` e `/templates/usuarios/cadastro.html`. Cada arquivo contém uma tag `h1` com seu título.

Atualização das rotas no arquivo `usuarios/urls.py`:
```python
from django.urls import path

from usuarios.views import login, cadastro

urlpatterns = [
    path('login', login, name='login'),
    path('cadastro', cadastro, name='cadastro'),
]
```
# Templates
Os arquivos HTML `/templates/usuarios/login.html` e `/templates/usuarios/cadastro.html` foram copiados a partir dos exemplos da aula.

O foco será no arquivo `templates\galeria\partials\_menu.html`:
```HTML
<nav class="menu-lateral__navegacao">
    <a href="{% url 'index' %}"><img src="{% static '/assets/ícones/1x/Home - ativo.png' %}"> Home</a>
    <a href="{% url 'login' %}"><img src="{% static '/assets/ícones/1x/Mais vistas - inativo.png' %}">Login</a>
    <a href="{% url 'cadastro'%}"><img src="{% static '/assets/ícones/1x/Novas - inativo.png' %}">Cadastrar</a>
    <a href="#"><img src="{% static '/assets/ícones/1x/Surpreenda-me - inativo.png' %}"> Surpreenda-me</a>
</nav>
```
Essa é a configuração proposta pela aula, presumindo que o arquivo `usuarios/urls.py` foi importado pelo arquivo `setup/urls.py` sem algum prefixo (com prefixo vazio):
```python
# Arquivo setup/urls.py
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('galeria.urls')),
    path('', include('usuarios.urls')), # Aqui o prefixo está vazio
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## E se o prefixo não estiver vazio?
Nesse caso, precisamos incluir a variável `app_name` no arquivo `usuarios/urls.py`. Essa variável vai representar o namespace que será usado como prefixo no arquivo `setup/urls.py`:
```python
# Arquivo usuarios/urls.py
from django.urls import path

from usuarios.views import login, cadastro

app_name = 'usuarios' # Variável que representa o namespace.
urlpatterns = [
    path('login', login, name='login'),
    path('cadastro', cadastro, name='cadastro'),
]
```
```python
# Arquivo setup/urls.py
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('galeria.urls')),
    # Note que o prefixo não é vazio: ele é o mesmo que a variável app_name no arquivo usuarios/urls.py.
    path('usuarios/', include('usuarios.urls')), 
    # path('', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
Finalmente, o namespace é referenciado pela função `url` no template do Django e separado do nome da rota por dois pontos. Veja isso no arquivo `templates\galeria\partials\_menu.html`:

```HTML
<nav class="menu-lateral__navegacao">
    <a href="{% url 'index' %}"><img src="{% static '/assets/ícones/1x/Home - ativo.png' %}"> Home</a>
    <a href="{% url 'usuarios:login' %}"><img src="{% static '/assets/ícones/1x/Mais vistas - inativo.png' %}">Login</a>
    <a href="{% url 'usuarios:cadastro'%}"><img src="{% static '/assets/ícones/1x/Novas - inativo.png' %}">Cadastrar</a>
    <a href="#"><img src="{% static '/assets/ícones/1x/Surpreenda-me - inativo.png' %}"> Surpreenda-me</a>
</nav>
```
> Note que as rotas para as views `login` e `cadastro` que pertencem o aplicativo `usuarios` seguem o padrão `namespace:nome_da_view`. Ex.: 
> ```HTML
> <a href="{% url 'usuarios:login'%}" ...>Login</a>
> <a href="{% url 'usuarios:cadastro'%}" ...>Cadastro</a>
> ```

# Criando formulários
Vamos substituir o formulário em HTML puro pelo formulário gerado pelo template do Django.

Para isso, precisamos primeiro criar a classe do formulário no novo arquivo `usuarios/forms.py`:
```python
from django import forms

class LoginForm(forms.Form):
    nome_login = forms.CharField(
        label='Nome de Login',
        required=True,
        max_length=100,
    )
    senha = forms.CharField(
        label='Senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(),
    )
```
> Note que o campo `senha` tem um parâmetro a mais, o `widget`. Nele podemos instanciar um objeto que representará o controle que será renderizado com o campo.

Criado o formulário vamos instanciá-lo na view `login` no arquivo `usuarios/views.py`:
```python
# Resto do código
from usuarios.forms import LoginForm

def login(request):
    form = LoginForm()
    return render(request, 'usuarios/login.html', { 'form' : form })
# Resto do código
```

E por último, substituímos os elementos do formulário em HTML pelos elementos de template do Django:
```HTML
<!-- Resto do código -->
<form action="" method="">
    {% csrf_token %}
    <div class="row">
        {% for field in form.visible_fields %}
            <div>
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
            </div>
        {% endfor %}
    </div>
</form>
<!-- Resto do código -->
```
> Pontos importantes: 
> 1. O campo `{% csrf_token %}`, para impedir ataques de Cross Site Request Forgery;
> 2. Dentro do formulário, o objeto que será iterado para gerar os campos é o `visible_fields`;
> 3. Para personalizarmos a tag label corretamente, definimos no atributo `for` o campo de template `{{ field.id_for_label }}`;
> 4. Para inserir o texto do rótulo, basta usarmos o campo de template `{{ field.label }}`;
> 5. Para inserir o campo do formulário, basta usarmos o campo de template `{{ field }}`.

# Estilizando formulário
Para formatar os estilos dos campos de formulário, é necessário acrescentar um dicionário no parâmetro `attrs` do widget do campo. Veja o exemplo no arquivo `usuarios/forms.py`:

```python
from django import forms

class LoginForm(forms.Form):
    nome_login = forms.CharField(
        label='Nome de Login',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Ex.: João Silva',
            }
        )
    )
    senha = forms.CharField(
        label='Senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Digite sua senha',
            }
        ),
    )
```
> Note que o dicionário `attrs` recebe os atributos HTML que queremos acrescentar aos widgets (`TextInput` e `PasswordInput`). No caso, colocamos a classe `form-control` do Bootstrap usando o atributo `class` e um placeholder usando o atributlo `placeholder`.

Já a formatação dos rótulos e do botão de login são bem simples: basta aplicar os estilos do Bootstrap (conforme folha de estilo compartilhada pelas páginas).

Arquivo `templates\usuarios\login.html`:
```HTML
<form action="" method="">
    {% csrf_token %}
    <div class="row">
        {% for field in form.visible_fields %}
            <div class="col-12 col-lg-12" style="margin-bottom: 10px;">
                <label for="{{ field.id_for_label }}" style="color:#D9D9D9; margin-bottom: 5px;">{{ field.label }}</label>
                {{ field }}
            </div>
        {% endfor %}
    </div>
    <div>
        <button class="btn btn-success col-12" style="padding: top 5px;" type="submit">Logar</button>
    </div>
</form>
```
# Formulários de cadastro
Os passos para a atualização da tela de cadastro são os mesmos da tela de login: 

1. criar o formulário em `usuarios/forms.py` e especificar os atributos HTML de cada campo/widget; 
2. atualizar a view em `usuarios/views.py`, inserindo o formulário; e
3. atualizar o código HTML com os códigos de template Django.

Arquivo `usuarios/forms.py`:
```python
# Resto do código 
class CadastroForm(forms.Form):
    nome_cadastro = forms.CharField(
        label='Nome de Cadastro',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Ex.: João Silva'
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Ex.: joaosilva@xpto.com'
            }
        )
    )
    senha_1 = forms.CharField(
        label='Senha',
        required=True,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Digite sua senha'
            }
        )
    )
    senha_2 = forms.CharField(
        label='Confirme sua senha',
        required=True,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Digite sua senha novamente'
            }
        )
    )
```
> Note que o campo de e-mail usa campo de formulário e widget diferentes: `EmailField` é o campo, e `EmailInput` é o widget.

Arquivo `usuarios/views.py`:
```python
from usuarios.forms import LoginForm, CadastroForm
# Resto do código 
def cadastro(request):
    form = CadastroForm
    return render(request, 'usuarios/cadastro.html', { 'form' : form})
```

Arquivo `templates\usuarios\cadastro.html`:
```HTML
<form action="" method="">
    {% csrf_token %}
    <div class="row">
        {% for field in form.visible_fields %}
            <div class="col-12 col-lg-12" style="margin-bottom: 10px;">
                <label for="{{ field.id_for_label}}" style="color:#D9D9D9; margin-bottom: 5px;"><b>{{ field.label }}</b></label>
                {{ field }}
            </div>
        {% endfor %}
        <div class="col-12 text-center">
            <button class="btn btn-success col-12" style="padding: top 5px;" type="submit">Cadastrar</button>
        </div>
    </div>
</form>
```
# Usuários do Django
Os formulários no HTML não tiveram uma ação definida e o método padrão usado neles é o `GET`. Modificamos os formulários para conter a ação correta e o método HTTP correto: 
```html
<!-- login.html -->
<form action="{% url 'usuarios:login' %}" method="post">
<!-- cadastro.html -->
<form action="{% url 'usuarios:cadastro' %}" method="post">
```

Vamos modificar também o comportamento interno da view `usuarios.view.cadastro` no arquivo `usuarios.views.py`:

```python
from django.shortcuts import render, redirect

from usuarios.forms import LoginForm, CadastroForm

# Resto do código
def cadastro(request):
    form = CadastroForm

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form['senha_1'].value() != form['senha_2'].value():
            return redirect('usuarios:cadastro')
        
    return render(request, 'usuarios/cadastro.html', { 'form' : form})
```
> Note que o que está sendo comparado são os valores dos campos `senha_1` e `senha_2` do formulário.
> 1. O formulário se comporta como um dicionário, cuja chave é o nome do campo que estamos procurando.
> 2. O valor do campo na verdade é um método, não é um valor (note em `form['nome_campo'].value()`).

# Lógica de cadastro
```python
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
```
> O sucesso no cadastro é indicado pelo redirecionamento para a tela de login; qualquer falha redireciona o usuário para a tela de cadastro novamente.

# Lógica de login
```python
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
```
> Destaque: o método `django.contrib.auth.authenticate` retorna um usuário para você. Você precisa fornecer apenas a requisição e o dicionário/parâmetros nomeados com as credenciais do usuário:
> ```python
> usuario = auth.authenticate(
>     request,
>     username=nome, 
>     password=senha
> )
> ```

# Alertas e mensagens
O pacote `django.contrib.messages` contém métodos que facilitam a inserção de flash messages no Django. Dentro das views, usamos as funções `messages.error` ou `messages.success`, as quais sempre recebem a requisição como primeiro parâmetro e a mensagem como segundo parâmetro: 
```python
messages.success(request, f'{nome} logado com sucesso.')
messages.error(request, 'Erro ao efetuar login.')
```

Nos templates, inserimos um loop sobre o objeto `messages` para exibir todas as flash messages, cada uma em uma div.
```HTML
{% for message in messages %}
    <div class="alert alert-primary">
        <!-- Mensagens com fundo azul -->
        <p>{{ message }}</p>
    </div>
{% endfor %}
```
# Logout
A lógica de logout no arquivo `usuarios/views.py` fica assim:

```python
from django.contrib import auth, messages
# Resto do código

def logout(request):
    messages.success(request, 'Logout efetuado com sucesso.')
    auth.logout(request)
    return redirect('usuarios:login')
```
> Note que existe o método `django.contrib.auth.logout` facilita a lógica para fazer logout do sistema.

A view de `logout` também precisa ser roteada, conforme atualização no arquivo `usuarios/urls.py`:
```python
from django.urls import path

from usuarios.views import login, cadastro, logout

app_name = 'usuarios'
urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('cadastro', cadastro, name='cadastro'),
]
```

Depois, podemos inserir nos templates o link para a rota de logout:
```HTML
<a href="{% url 'usuarios:logout' %}">Logout</a>
```
# Refatoração e validação
A validação consiste apenas em verificar se o usuário está logado. Caso ele não esteja, ele é redirecionado para a tela de login:

```python
def minha_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado.')
        return redirect('usuarios:login')
    # Resto do código
```

A refatoração consiste apenas em modificar o CSS, de maneira que as classes do Bootstrap não se sobreponham aos estilos aplicados às fotos nas views de `galeria.views.busca` e `galeria.views.index`. Para isso, foi necessário copiar os estilos desejados do Bootstrap para o arquivo `setup/static/styles/style.css`. Depois usamos o comando `python manage.py collectstatic` para que a folha de estilo seja copiada para o diretório `static/styles/style.css`.

# Associando tabelas
Vamos associar as fotografias a um único usuário. Para isso, editaremos o modelo `galeria.models.Fotografia`:
```python
# Resto do código
from django.contrib.auth.models import User

class Fotografia(models.Model):
    # Resto do código
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='user',
    )
# Resto do código
```

Saída dos comandos `makemigrations` e `migrate`:
```
PS D:\alura\django-autenticacao> python manage.py makemigrations
Migrations for 'galeria':
  galeria\migrations\0006_fotografia_usuario.py
    - Add field usuario to fotografia
PS D:\alura\django-autenticacao> python manage.py migrate   Operations to perform:
  Apply all migrations: admin, auth, contenttypes, galeria, sessions
Running migrations:
  Applying galeria.0006_fotografia_usuario... OK
PS D:\alura\django-autenticacao>
```

Finalmente, vamos acrescentar mais um filtro nas fotografias, por usuário. Para isso, editaremos o modelo de `galeria.admin.ListandoFotografias`:

```python
from django.contrib import admin

from galeria.models import Fotografia

class ListandoFotografias(admin.ModelAdmin):
    list_filter = ("categoria", "usuario")
    # Resto do código

admin.site.register(Fotografia, ListandoFotografias)
```
# Validação clean
Vamos proibir o uso de espaço no campo de nome de usuário (arquivo `usuarios/forms.py`):
```python
from django import forms

# Resto do código
class CadastroForm(forms.Form):
    nome_cadastro = forms.CharField(
        # Resto do código
    )
    # Resto do código
    def clean_nome_cadastro(self):
        nome = self.cleaned_data.get('nome_cadastro')

        if nome:
            # Remove espaços do início e do fim da string.
            nome = nome.strip()
            if " " in nome:
                raise forms.ValidationError("Não é possível inserir espaços dentro do campo usuário.")
            else:
                return nome
```

Destaques:
1. O nome do método deve começar com `clean_` e depois ser serguido do nome do campo de modelo que será validado.
2. Veja o código `raise forms.ValidationError('Mensagem de erro')`. Por enquanto, a mensagem de erro não aparece na tela do navegador, mas isso será corrigido.

# Mensagens de erro
Vamos remover a validação de igualdade de senha que estava em `usuarios/views.py` e movê-la para `usuarios/forms.py`:
```python
class CadastroForm(forms.Form):
    # Resto do código
    senha_2 = forms.CharField(
        # Resto do código
    )
    # Resto do código
    def clean_senha_2(self):
        senha_1 = self.cleaned_data.get('senha_1')
        senha_2 = self.cleaned_data.get('senha_2')
        if senha_1 and senha_2:
            if senha_1 != senha_2:
                raise forms.ValidationError('Senhas não são iguais.')
        return senha_2
```

E no template de cadastro, vamos exibir as mensagens de erro usando o campo `field.errors` de cada elemento do formulário:
```HTML
{% for field in form.visible_fields %}
    <div class="col-12 col-lg-12">
        <label for="{{ field.id_for_label}}">
            <b>{{ field.label }}</b>
        </label>
        {{ field }}
    </div>
    {% for error in field.errors %}
        <div class="alert alert-danger">
            {{ error }}
        </div>
    {% endfor %}
{% endfor %}
```
# Partial para alertas
Primeiro, precisamos mudar as configurações do Django para informar qual classe CSS/Bootstrap será usada para cada tipo de mensagem disparada pela view através dos comandos `django.contrib.messages.error` e  `django.contrib.messages.success`:
```python
# settings.py
from django.contrib.messages import constants

MESSAGE_TAGS = {
    constants.ERROR: 'danger',
    constants.SUCCESS: 'success',
}
# Na documentação do Django, o import das constants usa o alias 
# messages. Segue a versão alternativa do código:
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
}
```

Criação da partial para os alertas:

```HTML
{% if messages %}
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }}">
        {{ message }}
    </div>
    {% endfor %}
{% endif %}
```

Para usar uma partial, usamos o comando `include` no template do Django: `{% include 'galeria/partials/_alertas.html' %}`.

# Reorganizando diretórios
Movemos a pasta `partials` de dentro do diretório `templates/galeria` para o diretório `templates`. Depois atualizamos o HTML das páginas que referenciam essas partials. Bem fácil.

Nas aulas foi proposto remover as repetições presentes nos formulários de login e de cadastro. Isso é apenas um exercício para usar os recursos de template do Django para evitar repetições com extensão e inclusão de código.
