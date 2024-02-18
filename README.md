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
