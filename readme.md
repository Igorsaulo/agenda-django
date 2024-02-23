# Agenda-Django
Este projeto é uma agenda de contatos compartilhada, onde somente os donos daqueles contatos tem permissão de apaga-los ou edita-los

## Iniciando o projeto:

#### Instale as depêndencias:

```bash
pip install -r requirements.txt
```

#### Faça as migrações:

```bash
python manage.py migrate
```

#### Utilize o script para popular o banco(Opcional):

No Linux
```bash
python ./utils/create_contacts.py
```

No Windows
```cmd
python .\utils\create_contacts.py
```

#### Iniciando o projeto:

```bash
python manage.py runserver
```

- Você pode acessar a pagina inicial em http://127.0.0.1:8000/