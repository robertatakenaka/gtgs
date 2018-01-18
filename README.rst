Equipe (gtgs)
=============


A short description of the project.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT


Configuração: Variáveis de ambiente:
====================================

Docker:
-------

* ``USE_DOCKER`` - se o ambiente é feito com docker, definir como: 'yes'

Database:
---------

* ``POSTGRES_USER`` - usuário postgres (requerido)
* ``POSTGRES_PASSWORD`` - senha do usuário postgres (requerido)


Django:
-------

* ``DJANGO_SETTINGS_MODULE``- caminho do modulo de settings. (default: 'config.settings.production')
* ``DJANGO_DEBUG`` - habilita/deshabilita modo debug da webapp (default: False)
* ``DJANGO_ACCOUNT_ALLOW_REGISTRATION`` - habilita/deshabilita cadastro de usuários (default: True)
* ``DJANGO_ADMIN_URL`` - URL do admin (default: quando acessar /admin gera erro)
* ``DJANGO_SECRET_KEY`` - segredo para segurança (default: gera erro)
* ``DJANGO_ALLOWED_HOSTS`` - host permitidos (default: '*' (aceita tudo, deveria ser somente o host da aplicação somente))
* ``DJANGO_SECURE_SSL_REDIRECT`` -

Django (email):
---------------

* ``DJANGO_DEFAULT_FROM_EMAIL`` - email padrão no from (default: 'Equipe <noreply@example.com>')
* ``DJANGO_EMAIL_SUBJECT_PREFIX`` - email padrão no from (default: '[Equipe] ')
* ``DJANGO_EMAIL_HOST`` - host do servidor de envio de emails (default: 'mailhog')
* ``DJANGO_EMAIL_PORT`` - porta do servidor de envio de emails (default: 1025)
* ``DJANGO_EMAIL_HOST_USER`` - usuário do servidor de envio de email (default: '')
* ``DJANGO_EMAIL_HOST_PASSWORD`` - senha do usuário do servidor de envio de email (default: '')
* ``DJANGO_EMAIL_USE_TLS`` - True/False dependendo se o servidor de envio de email usa TLS na autenticação (default: False)
* ``DJANGO_EMAIL_USE_SSL`` - True/False dependendo se o servidor de envio de email usa SSL na autenticação (default: False)


Redis:
------

* ``REDIS_URL`` - URL de conexão para o servidor Redis (default: "redis://127.0.0.1:6379", no entrypoint.sh definido como: "redis://redis:6379")

