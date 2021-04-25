# VM Simple Manager

Simple python API using flask to turn on and off a remote VM

## What is it?
This simple project is intended to provide an easy way to turn my gaming VM on and off.

## How to use?
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