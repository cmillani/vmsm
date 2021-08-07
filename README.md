# VM Simple Manager

Simple python API using flask to turn on and off a remote VM.

## What is it?
This simple project is intended to provide an easy way to turn my gaming VM (libvirt) on and off.

By exposing this action through a web API it becomes easy to integrate it with other systems, in my case, [Home Assistant](https://www.home-assistant.io). With this, I can turn of my gaming VM from my sofa!

Keep in mind that the exposed API has no form of authentication, so access to it should be restricted.

## How to use?

### Setup the server
To start a server you need to configure some environment variables (see the docker-compose in this repo for a quick start example):

* `CONNSTRING`: This is the [connection uri](https://libvirt.org/uri.html) that will be used to connect with libvirt. In the libvirt documentation there are many possibilities, for my current use case I'm using `qemu+ssh`, since the host is not the same machine where I run this server. To avoid having to configure addicional information about the host, `no_verify` flag is used in my example.
* `VMNAME`: VMSM supports one single vm for now, and this is set here. 

In my example, I set an additional volume with my ssh keys to be used in the connection string.

VMSM will then create a connection to the libvirt host using `CONNSTRING` and turn `VMNAME` on and off using the exposed endpoints.

### Configuring Home Assistant
By adding the following configuration to a Home Assistant yaml file a switch will be created calling the endpoints to turn the VM on or off, and fetching its status.

```
switch:
  - platform: rest
    name: Videogame
    resource: <SERVER_URL>/videogame
    body_on: '{"active": true}'
    body_off: '{"active": false}'
    is_on_template: "{{ value_json.is_active }}"
    headers:
      Content-Type: application/json
    verify_ssl: false
```


## Next Steps

This project is intended to be a simple bridge between libvirt and some smart home application. That being said, there are some features that I imagine could be useful:

* Allow more than one VM to be managed
* Allow mutually exclusive VMs (for example, VMs with GPU passthrough, where one need to be turned off to turn the other on)

And I'm open to any kind of feedback and requests! :)

Feel free to open an issue or a PR!