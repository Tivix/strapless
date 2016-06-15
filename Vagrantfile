# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 80, host: 8086
  config.vm.network "forwarded_port", guest: 8000, host: 8006

  config.vm.network "private_network", ip: "192.168.33.11"

  config.ssh.forward_agent = true

  # config.ssh.username = 'ubuntu'

  config.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  # ansible stuff
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/development_vagrant.yml"
    ansible.verbose = "vv"
  end

end
