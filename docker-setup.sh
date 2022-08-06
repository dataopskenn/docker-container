sudo snap install docker 
sudo docker run hello-world
sudo docker build -t test:pycontainer
sudo docker run -it test:pycontainer
python pipeline.py
