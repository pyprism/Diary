import re


def generate_cors_regex_from_hosts(hosts):
    """Generate CORS regex patterns from ALLOWED_HOSTS"""
    patterns = []
    for host in hosts:
        host = host.strip()
        if not host or host == "*":
            continue

        if "://" in host:
            host = host.split("://", 1)[1]

        if host.startswith("*."):
            escaped_host = re.escape(host[2:])
            patterns.append(rf"^https?://([A-Za-z0-9-]+\.)+{escaped_host}(?::\d+)?$")
        else:
            escaped_host = re.escape(host)
            patterns.append(rf"^https?://{escaped_host}(?::\d+)?$")
    return patterns
