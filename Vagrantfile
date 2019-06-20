Vagrant.configure("2") do |config|
  config.vm.box = "debian/stretch64"

  #config.vm.post_up_message = <<-END
  #   yoyaku available at http://localhost:8000 (on the host).
  #END

 config.vm.network :private_network, ip: '10.11.12.13'

 # Make lib.reviews reachable via http://localhost:8000/ on the host.
 config.vm.network :forwarded_port, guest: 8000, host: 8000

 config.vm.synced_folder '.', '/vagrant',
  :nfs => true,
  :mount_options => ['noatime', 'nodiratime']

  config.vm.provision 'shell', path: './utils/vmsetup.sh'
end
