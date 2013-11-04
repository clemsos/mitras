use ansible !

    apt-get install python-dev python-pip
    pip install PyYAML Jinja2 paramiko

    git submodule update

    cd setup/ansible
    source ./hacking/env-setup
    
    ansible all -m ping --ask-pass -i /home/clement/Dev/mitras/config/hosts.ini


Optimized BLAS Installation for numpy

http://williamjohnbert.com/2012/03/how-to-install-accelerated-blas-into-a-python-virtualenv/