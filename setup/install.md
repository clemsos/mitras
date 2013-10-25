# HOWTO Install Mitras

tested on Ubuntu Server 12.04 


## Setup VirtualBox

#### SSH setup

After Ubuntu install :
* install ssh on the server : ```$ apt-get install openssh-server```
* go to Settings > Network 
* Select NAT
* Then click on Port Forwarding button. 
* Add a new Rule: "Host port 3022, guest port 22, name ssh, other left blank."

You can now ssh on the server : 

    $ ssh -p 3022 mitras@127.0.0.1

#### Port forwarding
(the VM should be shutdown for a 2nd adapter)

Bridge to use the server with a domain name
    * Settings / Network
    * Select Adapter 2 (Adapter 1 is your ssh)

### Prepare server

    sudo apt-get update
    sudo apt-get -y install build-essential libssl-dev curl git
    apt-get upgrade

You may need a specific user : 

    adduser mitras

### Install node/npm via nvm

    cd ~
    git clone git://github.com/creationix/nvm.git
    . ~/nvm/nvm.sh

    nvm install v0.8.8
    nvm use v0.8.8
    nvm alias default v0.8.8
    # npm is now bundled in node !

Add nvm to bash profile

    echo "source ~/nvm/nvm.sh" >> ~/.bashrc
    source ~/.bashrc
    ~/.bashrc

### Install MongoDB

    sudo apt-get install mongodb

    sudo service mongodb status
    # mongodb start/running, process 21090

    # may be useful for newest version of mongo... 
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    touch /etc/apt/sources.list.d/10gen.list
    "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen"
    sudo apt-get update


### Install Nginx

    # install latest version
    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:nginx/stable
    sudo apt-get update
    sudo apt-get install nginx

    # fix apache config 
    sudo service apache2 stop
    update-rc.d apache remove   # prevent apache from loading at start

    sudo service nginx start
    update-rc.d nginx defaults   # ensure be up after reboots


### Install Redis 
    
    sudo apt-get install redis-server
    sudo update-rc.d redis-server defaults

### Install neo4j

    bash setup/install_neo4j.sh

## Deployment & config

### Config Nginx

    sudo cat /etc/nginx/sites-available/default
    
Create a config file for your Nginx host

```sudo nano /etc/nginx/sites-available/mitras```

Copy paste ```mitrax-nginx.conf```

Save and enable the site on nginx

    sudo ln -s /etc/nginx/sites-available/mitras /etc/nginx/sites-enabled/mitras
    # test
    nginx -t
    # reload
    nginx -s reload

### Web server with Capistrano

You need ruby (1.9.7 using rvm recommended)
    
    gem install capistrano
    gem install capistrano-ext

Then you can deploy
    
    cd mitras-conf
    cap -t
    cap deploy:setup
    cap deploy:check
    cap deploy

### Create config files

    cd config
    cp db.json.sample db.json
    cp apikeys.json.sample apikeys.json

Fill the config files with your db information and API credentials
