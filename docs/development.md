# Local Development Setup - Nepal Compliance

## Recommended: Dev Container (one-click setup)

The fastest way to get a fully working development environment is via [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) or [GitHub Codespaces](https://github.com/features/codespaces). All dependencies (MariaDB, Redis, Frappe bench, ERPNext, HRMS) are provisioned automatically.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Steps

1. Clone your fork and open in VS Code:
   ```bash
   git clone https://github.com/<your-username>/nepal-compliance.git
   code nepal-compliance
   ```

2. VS Code will detect `.devcontainer/` and prompt **"Reopen in Container"** — click it.

3. The first build takes **10–15 minutes** (downloads base image, installs ERPNext + HRMS + Nepal Compliance). Subsequent opens are instant.

4. Once setup completes, open the VS Code terminal and start the dev server:
   ```bash
   cd ~/frappe-bench
   bench start
   ```

5. Access ERPNext at **http://localhost:8000**
   - Username: `Administrator`
   - Password: `admin`

That's it. The `nepal-compliance` source directory is live-mounted inside the container — any file you edit is reflected immediately without rebuilding.

---

### Using GitHub Codespaces

Click **Code → Codespaces → Create codespace on develop** from the GitHub repo page. The same `.devcontainer/` config runs in the cloud. No local Docker needed.

---

## Manual Setup (without Docker)

If you prefer a native install, ensure the following are available:

| Dependency | Version | Check |
|---|---|---|
| Python | 3.10 / 3.11 / 3.12 | `python3 --version` |
| Node.js | 18 or 20 | `node --version` |
| yarn | 1.12+ | `yarn --version` |
| MariaDB | 10.6.6+ (11.3 recommended) | `mariadb --version` |
| Redis | 6+ | `redis-server --version` |
| wkhtmltopdf | 0.12.5 with patched qt | `wkhtmltopdf --version` |
| frappe-bench | latest | `bench --version` |

For a full system-level setup, refer to [Frappe's official installation guide](https://docs.frappe.io/framework/user/en/installation).

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/nepal-compliance.git
git remote add upstream https://github.com/yarsa/nepal-compliance.git
```

### 2. Initialize bench and create a site

```bash
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
bench new-site nepal.localhost --mariadb-root-password <root-password> --admin-password admin
bench use nepal.localhost
```

### 3. Install ERPNext and HRMS

```bash
bench get-app erpnext --branch version-15
bench --site nepal.localhost install-app erpnext

bench get-app hrms --branch version-15
bench --site nepal.localhost install-app hrms
```

### 4. Link and install Nepal Compliance

```bash
ln -s /path/to/nepal-compliance apps/nepal_compliance
bench --site nepal.localhost install-app nepal_compliance
```

### 5. Enable developer mode and install JS hooks

```bash
bench --site nepal.localhost set-config developer_mode 1
bench clear-cache

cd /path/to/nepal-compliance
yarn install
```

### 6. Start the server

```bash
cd frappe-bench
bench start
```

Access at **http://localhost:8000**.

---

## Day-to-day development

### Applying changes

| Change type | Command |
|---|---|
| Python file edits | Picked up automatically in developer mode |
| JS / CSS edits | `bench build --app nepal_compliance` |
| Schema / fixture changes | `bench --site nepal.localhost migrate` |

### Running tests

```bash
# All tests
bench --site nepal.localhost run-tests --app nepal_compliance

# Specific module
bench --site nepal.localhost run-tests --module nepal_compliance.tests.test_salary_structure
```

### Keeping your fork up to date

```bash
git fetch upstream
git checkout develop
git merge upstream/develop
```

### Commit message format

Commits are linted via `commitlint`. The required format is:

```
type(scope): short description

# Examples:
feat(payroll): add SSF contribution calculation
fix(invoice): correct VAT rounding on credit notes
docs(setup): update development guide
```

Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

---

## Troubleshooting

**`custom_type_of_company` missing from Company DocType**

Re-run the install hook:
```bash
bench --site nepal.localhost execute nepal_compliance.install.after_install
```

**Changes not reflected**

```bash
bench clear-cache
bench --site nepal.localhost migrate
bench build --app nepal_compliance
```

**MariaDB connection refused (native setup)**

Ensure MariaDB is running: `sudo systemctl start mariadb`

---

## Next Steps

- [Contributing Guide](/CONTRIBUTING.md)
- [Manual Install](/docs/manual-install.md) — production install without Docker
- [Docker Install](/docs/docker-install.md) — production install with Docker
