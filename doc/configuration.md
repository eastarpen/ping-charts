# Configuration

Make sure the configuration in the client matches the server configuration. The server will ignore your upload request if the configurations do not match.

## Client

[Client Template](./templates/client.yaml)

- Ensure that the client "name", "clientId", and "passw" are the same as the server configuration.
- The value of `uploadUrl` should be 'http(s)://service.address/upload'.  
  
  For example:

  | Service Address        | uploadUrl                     |
  | ---------------------- | ----------------------------- |
  | http://127.0.0.1:8000  | http://127.0.0.1:8000/upload  |
  | http://domain.com      | http://domain.com/upload      |
  | http://domain.com/ping | http://domain.com/ping/upload |

- Targets must be registered in the server configuration, or they will be ignored.


```yaml
name: client                # Client name (allow repeat)
clientId: 1                 # Client ID (integer, do not allow repeat)
passw: password             # Client password (string)
uploadUrl: url              # Server upload URL
targets:                    # Targets list
- id: 1                     # Target ID (integer, do not allow repeat)
  name: chinanet            # Target name (string, allow repeat)
  port: 80                  # Target port (integer)
  addr: ct.tz.cloudcpp.com  # Target address (can be IP or domain)
- id: 2
  name: chinaunicom
  port: 80
  addr: cu.tz.cloudcpp.com
```

## Server

[Server Template](./templates/server.yaml)

```yaml
targets:               # Register targets
  - name: chinanet     # Target name (string, allow repeat)
    id: 1              # Target ID (integer, do not allow repeat)
  - name: chinaunicom
    id: 2
  - name: chinamobile
    id: 3
clients:
  - name: client       # Client name (allow repeat)
    label: US          # Client label (string, it will show on the web page)
    pass: password     # Client password (string)
    id: 1              # Client ID (integer, do not allow repeat)
```
