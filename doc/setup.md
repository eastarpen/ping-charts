# Quick Setup

**Work fine under Debian, not test other OS**

To quickly and easily set up this project with the default configuration, you can use the provided one-click scripts. However, it is recommended to read the documentation before proceeding.

## Client

1. Download the [client setup script](../scripts/client.sh) and execute it with root permission.
2. The script will perform the following tasks:
   - Attempt to create the directory "/opt/ping-charts".
   - Download the pre-compiled client from the [releases](https://github.com/eastarpen/ping-charts/releases) page.
   - Download the [client template configuration](../doc/templates/client.yaml).
   - Download the client systemd service configuration files to "/etc/systemd/system/".

After executing the script, follow these steps:

1. Rewrite the '/opt/ping-charts/client.yaml' file with your server configuration.
2. Run the command `systemctl start pingChartsClient.timer` to start the client. This will ping your targets and upload data to the server once a minute.
3. If desired, run the command `systemctl enable pingChartsClient.timer` to make the client start automatically after the OS reboot.

**Attention:**
- If you do not change the service configuration file, the client configuration file must be named 'client.yaml'.

## Server

1. Download the [server setup script](../scripts/server.sh) and execute it with root permission.
2. The script will perform the following tasks:
   - Attempt to create the directory "/opt/ping-charts".
   - Download the pre-compiled server from the [releases](https://github.com/eastarpen/ping-charts/releases) page.
   - Download the [server template configuration](../doc/templates/server.yaml).
   - Download the server systemd service configuration file to "/etc/systemd/system/".

After executing the script, follow these steps:

1. Rewrite the '/opt/ping-charts/server.yaml' file with your client configuration.
2. Run the command `systemctl start pingChartsServer` to start the server.
3. If desired, run the command `systemctl enable pingChartsServer` to make the server start automatically after the OS reboot.

**Attention:**
- If you do not change the service configuration file, the server configuration file must be named 'server.yaml'.
- The server will run on port 8000.
- The service will listen for requests from '0.0.0.0'.

## Customization

**Before making any changes, ensure that you understand what you are doing.**

If you are not satisfied with the default settings, you can customize the service files to meet your needs.

Firstly, ensure that the client and server are running correctly. For more information, refer to the [Usage](../README.md#Usage) section.

Next, modify the service configuration files:

- Server: "/etc/systemd/system/pingChartsServer.service"
- Client: "/etc/systemd/system/pingChartsClient.service" and "/etc/systemd/system/pingChartsClient.timer"
