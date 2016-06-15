Scratch playbook
----------------

Use it for testing etc. Example manner to run it.

    - ``ansible-playbook ansible/scratch.yml -i ansible/dev --private-key=~/.vagrant.d/insecure_private_key -vvvv``

    - ``ansible-playbook ansible/development_vagrant.yml -i ansible/dev --private-key=~/.vagrant.d/insecure_private_key -vvvv``

Roles like ``postgres`` are liberally taken from: https://github.com/jcalazan/ansible-django-stack (called ``db`` in it.)
