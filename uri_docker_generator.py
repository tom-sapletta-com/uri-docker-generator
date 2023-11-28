import sys
import subprocess
from urllib.parse import urlparse

def generate_ftp_dockerfile(port, directory, filename):
    dockerfile_content = f"""
    FROM stilliard/pure-ftpd:hardened
    RUN mkdir -p /home/ftpusers/{directory}
    RUN echo "test\n test " | pure-pw useradd admin -u ftpuser -d /home/ftpusers/{directory}
    RUN pure-pw mkdb
    RUN echo "welcome to ftp server" > /home/ftpusers/{directory}/{filename}
    EXPOSE {port}
    CMD ["/run.sh", "-c", "30", "-C", "5", "-l", "puredb:/etc/pure-ftpd/pureftpd.pdb", "-E", "-j", "-R"]
    """
    return dockerfile_content

def build_docker_image(dockerfile, tag):
    client = docker.from_env()
    print("Building Docker image...")
    image, build_log = client.images.build(fileobj=io.StringIO(dockerfile), tag=tag)
    for log in build_log:
        if 'stream' in log:
            print(log['stream'].strip())

def run_ftp_container(image, port):
    client = docker.from_env()
    print("Running Docker container...")
    container = client.containers.run(
        image,
        ports={'21/tcp': port},
        detach=True
    )
    return container.id

def main(uri):
    parsed_uri = urlparse(uri)
    
    if parsed_uri.scheme == 'ftp':
        port = parsed_uri.port or 21
        path_parts = parsed_uri.path.strip('/').split('/')
        directory = path_parts[0]
        filename = path_parts[-1]

        dockerfile = generate_ftp_dockerfile(port, directory, filename)
        image_tag = f"ftp-service-{port}"
        build_docker_image(dockerfile, image_tag)
        container_id = run_ftp_container(image_tag, port)
        print(f"FTP server is running in container ID: {container_id}")
    else:
        print(f"Protocol {parsed_uri.scheme} is not supported in this script.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python docker_generator.py <URI>")
        sys.exit(1)

    input_uri = sys.argv[1]
    main(input_uri)
