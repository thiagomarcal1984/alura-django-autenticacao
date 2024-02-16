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
