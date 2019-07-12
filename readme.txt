在Django2以上使用xadmin

1. pip install git+git://github.com/sshwsfc/xadmin.git@django2

2. 项目setting.py INSTALLED_APPS 加入
    'xadmin',
    #  xadmin 的依赖库
    'crispy_forms',

3. 项目url.py
import xadmin

urlpatterns = [
    # 使用xadmin的后台管理
    path('xadmin/', xadmin.site.urls),
    ... 其他

]

4. 生成表
   python manager.py makemigrations
   python manager.py migrate


ubuntu上部署Django项目

1。 安装 python3 和 pip3

sudo apt install python3-pip

2. 建立文件夹
// 用于存放虚拟目录
sudo mkdir -p /data/env

// 用于放项目
sudo mkdir -p /data/wwwroot


3。 安装 virtualenv

sudo pip install virtualenv

cd /data/env

sudo virtualenv -p /usr/bin/python3 pyweb


4. 启动虚拟环境
source /data/env/pyweb/bin/activate

5。把项目上传到 /data/wwwroot/目录，进入目录。先安装所需依赖包，再重启项目
 pip install -r requirements.txt

 python manage.py runserver
观察是否正常启动


6. 安装 uwsgi, 现在系统安装一次 ， 再在虚拟环境下安装一次
pip install uwsgi
在/data/wwwroot/mysite下新建一个mysite.xml文件
<uwsgi>
   <socket>127.0.0.1:8997</socket><!-- 内部端口，自定义 -->
   <chdir>/data/wwwroot/untitled1/</chdir><!-- 项目路径 -->
   <module>untitled1.wsgi</module>
   <processes>4</processes> <!-- 进程数 -->
   <daemonize>uwsgi.log</daemonize><!-- 日志文件 -->
</uwsgi>


7。 安装nginx
/usr/local目录下下载nginx源码

wget http://nginx.org/download/nginx-1.13.7.tar.gz

解压
tar -zxvf nginx-1.13.7.tar.gz

进入目录 执行
sudo ./configure
sudo make
sudo make install

进入/usr/local/nginx/conf 目录更改 nginx.conf文件

events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    server {
        listen       80;
        server_name  www.django.cn;
        charset utf-8;
        location / {
           include uwsgi_params;
           // 这部分需要和uwsgi的配置文件填写一致
           uwsgi_pass 127.0.0.1:8997;
           uwsgi_param UWSGI_SCRIPT mysite.wsgi;
           uwsgi_param UWSGI_CHDIR /data/wwwroot/mysite/; #项目路径

        }
        location /static/ {
        alias /data/wwwroot/mysite/static/; #静态资源路径
        }
    }
}

8。 进入/usr/local/nginx/sbin 目录
./nginx -t  检查配置文件是否有错

./nginx  启动nginx


9。进入项目目录
/data/wwwroot/mysite 启动uwsgi
uwsgi -x mysite.xml


10. 再进入/usr/local/nginx/sbin系统目录下 重启nginx
./nginx -s reload


11.最后 浏览器上访问项目

12。 其他  注意后台样式掉失问题