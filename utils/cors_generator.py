def generate_cors_regex_from_hosts(hosts):
    """Generate CORS regex patterns from ALLOWED_HOSTS"""
    patterns = []
    for host in hosts:
        # Remove any wildcard prefixes
        host = host.lstrip("*.")
        # Escape dots for regex
        escaped_host = host.replace(".", r"\.")
        # Allow both http and https, with or without www
        patterns.append(rf"^https?://.*{escaped_host}$")
    return patterns
