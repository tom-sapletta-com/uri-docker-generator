import sys
import docker
from urllib.parse import urlparse

def build_and_run_container(protocol, port, folder, filename):
    # Map the protocol to the appropriate Dockerfile creation function
    protocol_to_docker_setup = {
        'ftp': setup_ftp,
        # Add a setup entry for each protocol you want to support...
        # 'http': setup_http,
        # 'dhcp': setup_dhcp,
        # 'dns': setup_dns,
        'ssh': setup_ssh,
        # ... more protocols
    }

    # Check if the protocol is supported
    if protocol in protocol_to_docker_setup:
        # Generate the Dockerfile and other necessary setup
        dockerfile, tag, expose_port = protocol_to_docker_setup[protocol](port, folder, filename)
        
        # Build and run the container
        build_docker_image(dockerfile, tag)
        container_id = run_container(tag, expose_port)
        
        print(f"{protocol.upper()} service is running in container ID: {container_id}")
    else:
        print(f"Protocol {protocol} is not supported by this script.")

def setup_ftp(port, folder, filename):
    # This is where you'll prepare the Dockerfile contents and return them
    # along with the image tag and the port to expose
    return ("DockerfileContentsHere", "ftp-image-tag", 21)

def setup_ssh(port, folder, filename):
    # Setup Dockerfile for SSH service
    return ("DockerfileContentsHere", "ssh-image-tag", 22)

# You would define additional setup functions for the other protocols
# def setup_http(port, folder, filename):
#     # Setup for HTTP
# ...

def build_docker_image(dockerfile, tag):
    # Use Docker SDK for Python to build the image from the Dockerfile
    client = docker.from_env()
    image, _ = client.images.build(fileobj=io.StringIO(dockerfile), tag=tag)

def run_container(image_tag, port):
    # Use Docker SDK for Python to run the container
    client = docker.from_env()
    container = client.containers.run(
        image_tag,
        ports={f"{port}/tcp": port},
        detach=True
    )
    return container.id

def main(uri):
    parsed_uri = urlparse(uri)
    protocol = parsed_uri.scheme
    port = parsed_uri.port or get_default_port_for_protocol(protocol)
    path_parts = parsed_uri.path.strip('/').split('/')
    folder = path_parts[0]
    filename = path_parts[-1]

    build_and_run_container(protocol, port, folder, filename)

def get_default_port_for_protocol(protocol):
    # Return the default port for the given protocol
    return {
        'ftp': 21,
        'http': 80,
        'ssh': 22,
        # ... and so on for each supported protocol
    }.get(protocol, None)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python docker_generator.py <URI>")
        sys.exit(1)

    input_uri = sys.argv[1]
    main(input_uri)
