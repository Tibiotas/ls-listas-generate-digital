sudo wget https://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz && \n
sudo tar xzf Python-2.7.16.tgz && \n
cd Python-2.7.16 && \n
sudo ./configure --enable-optimizations && \n
sudo make altinstall && \n
python2.7 -V python2.7 -V && \n
pip install peewee --user && pip install urllib3 --user && pip install Flask --user && pip install Flask-Cors --user && pip install beautifulsoup4 --user && pip install httpserver --user && pip install win-unicode-console --user