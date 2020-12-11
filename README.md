# CEPEguel

O presente repositório contém todo o projeto do sistema de informação CEPEguel, proposto pelo grupo "Q" da disciplina de PMR3304 (Sistemas de Informação), do ano de 2020.

### Pré-requisitos

É necessária a instalação do framework Django (a versão utilizada foi a 3.1.3) e a biblioteca Pillow, para vizualização das imagens.
Para tal, se não os tiver instalados, utilize os comandos no prompt:

```
pip install Django==3.1.3
pip install Pillow
```

## Testes

Após a clonagem do repositório, para rodar o servidor é necessário digitar o seguinte comando no prompt:

```
python manage.py runserver
```

Em seguida prosseguir ao endereço http://127.0.0.1:8000/
Há um banco de dados alocado com produtos, modalidades, usuários (alunos, professores e administradores) já existente e que pode ser utilizado facilmente para testes, muito embora instâncias de qualquer classe também possam ser criadas ou deletadas livremente.

Para a visualização do banco de dados de uma forma organizada, basta ir à página http://127.0.0.1:8000/admin e autenticar-se com algum usuário que tenha permissão de administrador.

Usuários para teste (se não quiser ter o trabalho de criar algum):

Email            | Senha         | Tipo
---------------- | ------------- |-------------
admin@usp.br     | admin         | Administrador
professor@usp.br | 6hv58mgq      | Professor
aluno@usp.br     | 72xrp5p9      | Aluno

## Feito com

* [Django](https://www.djangoproject.com/) - O framework web utilizado

## Autores

* **Gustavo Torrico**
* **Felipe Pascutti**
* **Lucas Fiori**
