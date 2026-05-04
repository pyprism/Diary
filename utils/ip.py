import socket


def get_local_ip():
    hostname = socket.gethostname()
    _internal_ips = ["127.0.0.1"]
    try:
        _internal_ips += socket.gethostbyname_ex(hostname)[2]
        # also add the typical Docker gateway
        _internal_ips += [
            ip.rsplit(".", 1)[0] + ".1" for ip in socket.gethostbyname_ex(hostname)[2]
        ]
        return _internal_ips
    except Exception:
        raise RuntimeError("Failed to determine internal IPs for debug toolbar")
