# uri-docker-generator
Python script that generates a Docker container based on a given URI. This example is simplified and cover the FTP service generation scenario.

This approach is for educational or proof-of-concept purposes and may not be well-suited for production environments without more comprehensive planning and security analysis.


For each additional protocol, you would need to do the following:

1. Define a new `setup_<protocol>` function to create the Dockerfile and other setups required for that protocol.
2. In `build_and_run_container`, add the protocol and its corresponding function to the `protocol_to_docker_setup` dictionary.
3. Define default ports in `get_default_port_for_protocol` if required.

Remember, creating Docker containers for all these protocols would also typically involve configuration of various files, security measures (especially for protocols like DHCP, DNS, HTTP/S, SSH, etc.), and possibly other system setup steps that are specific to each protocol. 

  
Let's discuss the general approach you'd take to handle multiple protocols:

1. Parse the URI and determine the protocol
2. According to the protocol, create a Dockerfile with the appropriate base image and settings
3. Build the Docker image
4. Run the Docker container with the necessary configurations



+ [uri_docker_generator](uri_docker_generator.py)

To execute this script, run:

```sh
python uri_docker_generator.py ftp://127.0.0.2:21/movies/first.mp4
```

## TODO:

+ templating for different protocoll
+ operations incuded per protocoll
+ documentation generated

+ building structure based on docker compose  



## Protocols

+ [List of network protocols (OSI model) - Wikipedia](https://en.wikipedia.org/wiki/List_of_network_protocols_(OSI_model))

the docker should be generated for different protocols like: 
DHCP Dynamic Host Configuration Protocol
DNS Domain Name System
BOOTP Bootstrap Protocol
HTTP Hyper Text Transfer Protocol
HTTPS
NFS
POP3 Post Office Protocol
SMTP
SNMP
FTP
NTP
IRC
Telnet Tele Communication Protocol
SSH
TFTP
IMAP
