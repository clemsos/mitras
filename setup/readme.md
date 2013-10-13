use ansible !

    apt-get install python-dev python-pip
    pip install PyYAML Jinja2 paramiko

    git submodule update

    cd setup/ansible
    source ./hacking/env-setup
    
    ansible all -m ping --ask-pass -i /home/clement/Dev/mitras/config/hosts.ini