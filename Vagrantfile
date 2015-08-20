Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |vb|
    vb.memory="2048"
  end
  config.vm.network :forwarded_port, host: 80, guest: 80
  config.vm.network :forwarded_port, host: 8888, guest: 8888
  config.vm.provision :shell, inline: <<-SHELL
# uncomment to switch to pair.com mirrors
# sudo sed -i 's#archive.ubuntu.com#ubuntu.mirrors.pair.com/archive#' /etc/apt/sources.list
sudo apt-get update

# utilities
sudo apt-get install -y aptitude emacs24-nox git curl python-pip cifs-utils

# apache, flask, wsgi
sudo apt-get install -y apache2 python-flask libapache2-mod-wsgi
sudo apt-get install -y python-flask python-flask-login

# various python incl numpy/scipy
sudo apt-get install -y python-lxml python-imaging
sudo apt-get install -y python-numpy python-scipy python-skimage python-sklearn

# postgres 9.3
sudo apt-get install -y python-psycopg2 python-sqlalchemy
SHELL
end

