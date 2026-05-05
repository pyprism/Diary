# Diary Deployment with Ansible (Docker)

Automated Docker-based deployment of the Diary Django application using Ansible.

## Super Quick Start 🚀

```bash
cd deployment
ansible-playbook -i inventories/production deploy.yml -K
```

---

## Quick Start

### 1. Prerequisites

- Ansible installed on your local machine: `pip install ansible`
- SSH access to target server(s)
- Server running Ubuntu/Debian or RedHat/CentOS
- Git repository access (SSH key or token)
- PostgreSQL running on the target server (or accessible from it)

> **Note**: Docker and Docker Compose are automatically installed on the server by the deployment playbook.

### 2. Setup

```bash
# 1. Navigate to deployment directory
cd deployment

# 2. Install Ansible dependencies
pip install -r requirements.txt

# 3. Copy and configure secrets
cp vars/secrets.yml.example vars/secrets.yml
# Edit vars/secrets.yml with your actual values

# 4. Configure inventory
cp inventories/production/hosts.example inventories/production/hosts
# Edit hosts file with your server IP/hostname

# 5. Test connection
ansible -i inventories/production webservers -m ping
```

### 3. Configure Git Access

**For Private Repositories**, choose one option:

#### Option A: Deploy SSH Key to Server (Recommended)
```bash
# Generate deploy key
ssh-keygen -t rsa -b 4096 -C "deploy@diary" -f deploy_key

# Add deploy_key.pub to GitHub repo as deploy key

# Add to vars/secrets.yml:
git_ssh_private_key: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  [paste private key content]
  -----END OPENSSH PRIVATE KEY-----
```

#### Option B: HTTPS with Personal Access Token
```yaml
# In group_vars/all.yml:
project_repo: "https://{{ github_username }}:{{ github_token }}@github.com/pyprism/Diary.git"

# In vars/secrets.yml:
github_username: "your-username"
github_token: "ghp_your_token_here"
```

### 4. Deploy

```bash
# Full deployment (installs Docker, clones repo, builds & starts containers)
ansible-playbook -i inventories/production deploy.yml -K

# With verbose output (debugging)
ansible-playbook -i inventories/production deploy.yml -K -vvv

# Specific tags only
ansible-playbook -i inventories/production deploy.yml -K --tags docker
```

## How It Works

The deployment uses Docker Compose to run the application:

1. **common** role: Installs basic system packages (git, curl, etc.)
2. **deployment_user** role: Creates a deploy user with Docker group access
3. **docker** role:
   - Installs Docker Engine and Docker Compose plugin
   - Stops any legacy bare-metal services (uWSGI/systemd)
   - Clones/pulls the git repository
   - Deploys `.env` file from Ansible secrets
   - Builds the Docker image and starts containers via `docker compose up`
   - Runs Django migrations and collects static files

## Available Playbooks

| Playbook | Description |
|----------|-------------|
| `deploy.yml` | Full deployment (first time or updates) |
| `update.yml` | Pull code, rebuild containers, run migrations |
| `rollback.yml` | Rollback to a specific git commit/tag |
| `healthcheck.yml` | Check deployment health |
| `setup-backups.yml` | Configure automated database backups |

## Available Tags

```bash
--tags common       # System packages only
--tags user         # User creation only
--tags docker       # Docker setup + application deployment
--tags deploy       # Application deployment
```

## Configuration

### vars/secrets.yml (Required)

Contains sensitive configuration — **never commit to git**:

```yaml
django_secret_key: "your-production-secret-key"
django_debug: false
django_allowed_hosts: "yourdomain.com,your-server-ip"
db_name: diary_db
db_user: diary_user
db_password: "your-db-password"
db_host: host-gateway        # Docker host networking
db_port: 5432
server_port: 8001            # Host port mapped to container
sentry_dsn: ""               # Optional
```

### group_vars/all.yml

Non-sensitive configuration:
- Git repository URL and branch
- Project paths
- Container name
- Django settings module

### .env File

The deployment generates a `.env` file on the server from Ansible secrets.
For local development, copy `.env.example`:

```bash
cp .env.example .env
# Edit .env with your local values
```

## Common Tasks

### Update Application Code
```bash
ansible-playbook -i inventories/production update.yml
```

### Restart Containers
```bash
ansible -i inventories/production webservers -b -a "cd /opt/diary && docker compose restart"
```

### Check Container Status
```bash
ansible -i inventories/production webservers -b -a "cd /opt/diary && docker compose ps"
```

### View Logs
```bash
ansible -i inventories/production webservers -b -a "cd /opt/diary && docker compose logs --tail=50"
```

### Run Django Management Command
```bash
ansible -i inventories/production webservers -b -a "cd /opt/diary && docker compose exec web python manage.py <command>"
```

### Rollback to Previous Version
```bash
ansible-playbook -i inventories/production rollback.yml
# You will be prompted for the git commit hash or tag
```

### Health Check
```bash
ansible-playbook -i inventories/production healthcheck.yml
```

## Environment-Specific Deployment

### Production
```bash
ansible-playbook -i inventories/production deploy.yml
```

### Staging
```bash
ansible-playbook -i inventories/staging deploy.yml
```

## Troubleshooting

```bash
# Test Ansible connectivity
ansible -i inventories/production webservers -m ping

# Check Docker status on server
ansible -i inventories/production webservers -a "docker info"

# Check container status
ansible -i inventories/production webservers -b -a "cd /opt/diary && docker compose ps"

# View container logs
ansible -i inventories/production webservers -b -a "cd /opt/diary && docker compose logs --tail=30"

# Rebuild from scratch
ansible -i inventories/production webservers -b -a "cd /opt/diary && docker compose down && docker compose up -d --build"

# Check disk space
ansible -i inventories/production webservers -a "df -h"

# Clean unused Docker resources
ansible -i inventories/production webservers -a "docker system prune -f"
```

## Security Notes

1. **Never commit secrets**: `vars/secrets.yml` and `.env` are gitignored
2. **SSH Keys**: Rotate deploy keys regularly
3. **Passwords**: Use strong, unique passwords
4. **Firewall**: Only expose the mapped port (default `8001`) behind nginx/caddy
5. **HTTPS**: Use a reverse proxy (nginx/caddy) with TLS in production
6. **Docker**: Keep Docker updated; the deployment user has docker group access

## Default Paths on Server

```
/opt/diary/                    # Project root (configurable)
├── docker-compose.yaml      # Docker Compose configuration
├── Dockerfile               # Multi-stage Docker build
├── .env                     # Environment variables (generated by Ansible)
├── logs/                    # Application logs (Docker volume)
└── [application code]
```


## Quick Commands Summary

```bash
# Full deployment (installs Docker, clones repo, builds & starts containers)
ansible-playbook -i inventories/production deploy.yml -K

# Update only (pull code, rebuild, migrate)
ansible-playbook -i inventories/production update.yml -K

# Rollback to a specific commit
ansible-playbook -i inventories/production rollback.yml -K

# Health check
ansible-playbook -i inventories/production healthcheck.yml -K

```
