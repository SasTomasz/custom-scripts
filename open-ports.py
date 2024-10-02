import socket

def check_port(host, port):
    """
    Attempts to connect to the specified host on the given port.
    Returns True if the connection is successful, otherwise False.
    """
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.timeout, socket.error):
        return False

def scan_ports(host, start_port, end_port):
    """
    Scans ports in the range from start_port to end_port and logs which ports are open.
    """
    open_ports = []
    for port in range(start_port, end_port + 1):
        if check_port(host, port):
            print(f"Port {port} is open.")
            open_ports.append(port)
        else:
            print(f"Port {port} is closed or blocked.")
    
    return open_ports

if __name__ == "__main__":
    host = "portquiz.net"
    start_port = 1    # Starting port number
    end_port = 1024   # Ending port number (adjust as needed)

    print(f"Scanning ports {start_port}-{end_port} on {host}...\n")
    open_ports = scan_ports(host, start_port, end_port)
    
    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            print(f"Port {port}")
    else:
        print("\nNo open ports found in the specified range.")
