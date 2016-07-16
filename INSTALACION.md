# Instalación del proyecto en Digital Ocean
#### 1. Crear dropplet
Entrar a www.digitalocean.com, loguearse y crear el droplet. Escoger Ubuntu 14.04.
#### 2. Creamos un usuario y le damos todos los permisos
```sh
$ sudo adduser devjd
$ visudo

devstaff ALL=(ALL:ALL) ALL
```

#### 3. Instalación de OpenCV 3
Instalamos las siguientes dependencias.

```sh
$ sudo apt-get install --assume-yes libopencv-dev build-essential cmake git libgtk2.0-dev pkg-config python-dev python-numpy libdc1394-22 libdc1394-22-dev libjpeg-dev libpng12-dev libtiff5-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libxine2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libv4l-dev libtbb-dev libqt4-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils unzip
    
$ sudo apt-get install build-essential cmake git
    
$ sudo apt-get install ffmpeg libopencv-dev libgtk-3-dev python-numpy python3-numpy libdc1394-22 libdc1394-22-dev libjpeg-dev libpng12-dev libtiff5-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libxine2-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libv4l-dev libtbb-dev qtbase5-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils unzip
```

Descargamos opencv y descomprimimos:
```sh
$ cd 
$ wget https://github.com/Itseez/opencv/archive/3.1.0.zip
$ unzip 3.1.0.zip
```

Entramos a la carpeta descomprimida y ejecutamos:
```sh
$ mkdir build
$ cd build/
$ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D WITH_V4L=ON -D WITH_QT=ON -D WITH_OPENGL=ON ..
$ make
```

Procedemos a instalar:
```sh
$ sudo make install
$ sudo /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
$ sudo ldconfig
$ sudo apt-get update
```

#### 4. Instalación de pip y configuración del entorno virtual
Descargamos el archivo get-pip.py:
```sh
$  wget https://bootstrap.pypa.io/get-pip.py
```
Ejecutamos:
```sh
$ sudo python get-pip.py
```

Instalamos virtualenvwraper:
```sh
$ sudo pip install virtualenvwrapper
```

Agregamos estás línas en el archivo .bashrc
```
    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh
```

Hacemos un reload:
```sh
$ source ~/.bashrc
```

Creamos el entorno virtual
```sh
$ mkvirtualenv devjd
```

Enlazamos opencv para usarlo dentro del entorno virtual.
```sh
$ ln -s /usr/local/lib/python2.7/dist-packages/cv2.so .virtualenvs/django_1_9/lib/python2.7/site-packages/cv2.so
```
#### 5. Instalación y configuración de PostgreSQL
Actualizamos el sistema e instalamos postgresql:
```sh
$ sudo apt-get update
$ sudo apt-get install postgresql postgresql-contrib
```
Nos logueamos usando el usuario postgres:
```sh
$ sudo -i -u postgres
```
Creamos un nuevo rol(usuario: devjd, password: 142857):
```sh
$ createuser --interactive -P
```

Creamos una nueva base de datos:
```sh
$ createdb django_db
```

Entramos a psql, le damos privilegios al usuario devjd sobre la bd django_db:
```sh
$ psql
GRANT ALL PRIVILEGES ON DATABASE django_db TO devjd;
\q
```

Finalmente salimos del usuario postgres:
```sh
$ exit
```
#### 4. Instalación y configuración del proyecto
Ejecutamos los siguientes comandos:
```sh
$ cd
$ mkdir webapps && cd webpps
$ mkdir media_facedetector static_facedetector
$ git clone git@github.com:luhego/facedetector-api.git
```

Creamos el archivo de configuración setting.json con los datos del proyecto.
```sh
$ cd facedetector-api
$ nano src/settings/settings.json
```

Archivo settings.json
```
    {
        "DB_NAME": "django_db",
        "DB_USER": "devjd",
        "DB_PASSWORD": "142857",
        "URL_SITE": "http://45.55.231.112",
        "SECRET_KEY": "2w1fj0jktjo4^qh*&wm82eeoawccfy%(9!-kj-j=j9@2biam+j",
        "EMAIL_HOST": "",
        "EMAIL_HOST_USER": "",
        "EMAIL_HOST_PASSWORD": "",
        "DEFAULT_FROM_EMAIL": "",
        "SERVER_EMAIL": "",
        "EMAIL_PORT": 587,
        "MEDIA_ROOT": "/home/devjd/webapps/media_facedetector/",
        "MEDIA_URL": "/media_facedetector/",
        "STATIC_ROOT": "/home/devjd/webapps/static_facedetector/",
        "STATIC_URL": "/static_facedetector/",
        "ALLOWED_HOSTS": ["45.55.231.112"],
        "WORKON_HOME": "/home/luhego/.virtualenvs",
        "ENV": "django_1_9",
        "SENTRY_DSN": ""
}
```
Ubicados dentro del proyecto, instalamos los requirementents:
```sh
$ pip install -r requirements/base.txt
```
Instalamos uwsgi a nivel global:
```sh
$ sudo pip install uwsgi
```
Creamos el archivo uwsgi.ini dentro del proyecto:
```sh
$ nano uwsgit.ini

[uwsgi]
;placeholders
home = /home/devjd
webapps = %(home)/webapps/
app = %(webapps)/facedetector-api

;config
env = %(app)/src/settings/production.py
venv = %(home)/.virtualenvs/django_1_9
chdir = %(app)/src
module = wsgi

; spawn the master and 2 processes
uwsgi-socket = %(app)/uwsgi.sock
master = true
processes = 2
threads = 2
thread-stacksize = 512
reload-on-rss = 60

; cheaper
cheaper = N
cheaper-algo = spare
cheaper = 1
cheaper-initial = 1
cheaper-step = 1
harakiri = 30 ;numero máximo de segundos a mantener un request activo
vacuum = True

; log
logto = %(app)/uwsgi.log
```

#### 5. Instalación y configuración de de supervisor
Instalamos supervisor a nivel global:
```sh
$ sudo pip install supervisor
$ echo_supervisord_conf > ~/etc/supervisord.conf
```
Agregamos al final  del archivo ~/etc/supervisord.conf
```sh
[include]
files = ini/*.ini
```

Creamos el archivo base.ini en ~/etc/ini/
```sh
$ cd ~/etc
$ mdir ini
$ nano ini/base.ini
```
Archivo base.ini
```
[program:base]
command=/usr/local/bin/uwsgi /home/devjd/webapps/facedetector-api/uwsgi.ini
```
Iniciamos supervisor:
```
$ supervisord -c ~/etc/supervisord.conf
```
#### 6. Instalación y configuración de nginx
Instalamos nginx:
```sh
$ sudo apt-get install nginx
```

Modificamos el archivo nginx.conf:
```sh
$ sudo nano /etc/nginx/nginx.conf
```

Archivo nginx.conf:
```
user devjd;
worker_processes 4;
pid /run/nginx.pid;

events {
        worker_connections 1024;
        use epoll;
        multi_accept on;
}

http {

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        server_tokens off;


        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        gzip  on;
        gzip_min_length 10240;
        gzip_types    text/plain application/javascript application/x-javascript text/javascript text/xml text/css;

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}
```
Creamos el archivo base.conf dentor de la carpeta sites-available:
```
$ sudo nano /etc/nginx/sites-available/base.conf
```
Archivo base.conf:
```
server {
    listen       80;
    server_name  45.55.231.112;
    #location = /favicon.ico  {
    #    rewrite "/favicon.ico" "/static_ciudaris/img/favicon/favicon-256.png";
    #    expires 7d;
    #}

    location /static_facedetector {
        alias /home/devjd/webapps/static_facedetector/ ;
        expires 7d;
    }

    location /media_facedetector {
        alias /home/devjd/webapps/media_facedetector/ ;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///home/devjd/webapps/facedetector-api/uwsgi.sock;
    }

    #error_page  404              /404.html;

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }
}
```
Ejecutamos el siguiente comando:
```
$ sudo ln -s /etc/nginx/sites-available/base.conf /etc/nginx/sites-enabled/
```

Levantamos nginx:
```
$ sudo service nginx start
```
Eso es todo:

#### 7. Referencias
* https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04
* https://github.com/BVLC/caffe/wiki/Ubuntu-16.04-or-15.10-OpenCV-3.1-Installation-Guide
* http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
* Gists de Alexander Ayasca


