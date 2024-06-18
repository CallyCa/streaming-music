### Configuração do Ambiente Virtual com Conda

#### Passo 1: Instalar Conda

Se você ainda não tiver o Conda instalado, pode instalá-lo baixando e instalando o [Anaconda](https://www.anaconda.com/products/distribution) ou o [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

#### Passo 2: Criar o Ambiente Virtual

1. **Abra o terminal ou o prompt de comando.**
2. **Crie um novo ambiente virtual.** Você pode nomear o ambiente como preferir, neste exemplo, usaremos `music-streaming-env`:
   
   ```bash
   conda create -n music-streaming-env python=3.8
   ```

3. **Ative o ambiente virtual:**
   
   ```bash
   conda activate music-streaming-env
   ```

#### Passo 3: Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Passo 4: Inicializar o Projeto

Depois de instalar as dependências, você pode inicializar o projeto. Vamos relembrar os comandos para configurar as migrações e rodar a aplicação:

1. **Inicializar as Migrações:**

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

2. **Rodar a Aplicação:**

   ```bash
   python app.py
   ```

3. **Rodar os Testes Unitários:**

   ```bash
   python -m unittest discover -s tests
   ```

4. **Rodar os Testes de Carga com Locust:**

   ```bash
   locust -f tests/load_tests/locustfile.py --host=http://localhost:5000
   ```

### Arquivo `requirements.txt`

Certifique-se de que o arquivo `requirements.txt` está atualizado com todas as dependências necessárias:

```plaintext
Flask==2.0.2
Flask-SQLAlchemy==2.5.1
Flask-HTTPAuth==4.4.0
Flask-Migrate==3.1.0
locust==2.5.1
```

### Recapitulando a Estrutura do Projeto

Para facilitar a compreensão, segue novamente a estrutura do projeto:

```
servico-streaming-musicas/
└── REST/
    └── flask_app/
        ├── app.py
        ├── config.py
        ├── auth.py
        ├── extensions.py
        ├── requirements.txt
        ├── routes/
        │   ├── users_routes.py
        │   ├── songs_routes.py
        │   ├── playlists_routes.py
        │   └── __init__.py
        ├── models/
        │   ├── user.py
        │   ├── song.py
        │   ├── playlist.py
        │   ├── playlistsong.py
        │   └── __init__.py
        ├── factory/
        │   ├── model_factory.py
        │   └── __init__.py
        ├── tests/
        │   ├── test_users.py
        │   ├── test_songs.py
        │   ├── test_playlists.py
        │   └── load_tests/
        │       └── locustfile.py
        ├── migrations/
```

### Instruções para Configurar o Ambiente Virtual com Conda

1. **Instale o Conda se ainda não o tiver.**
2. **Crie e ative o ambiente virtual:**
   ```bash
   conda create -n music-streaming-env python=3.8
   conda activate music-streaming-env
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Inicialize as migrações, rode a aplicação e os testes conforme descrito acima.**
