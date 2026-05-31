# 📊 DevOpsPulse: End-to-End DevOps Pipeline & Web Application

Welcome to **DevOpsPulse**, a complete production-grade DevOps Capstone Project showcasing a resilient continuous delivery pipeline for a high-performance Node.js system telemetry application. This workspace integrates modern DevOps practices, including containerized microservices, CI/CD automation, cloud system hosting, automated shell utilities, and comprehensive Prometheus and Grafana infrastructure monitoring.

---

## 🚀 Architectural Paradigm

Our automated pipeline follows a standard GitOps flow to deliver quick, reliable builds:

```mermaid
graph TD
    Developer([💻 Developer]) -->|Git Push| GitHub[🐙 GitHub Repository]
    GitHub -->|Webhook Trigger| Jenkins[👷 Jenkins CI/CD on AWS EC2]
    
    subgraph Jenkins Pipeline
        direction TB
        J1[1. Lint & Code Quality] --> J2[2. Unit Testing Suite]
        J2 --> J3[3. Multi-Stage Docker Build]
        J3 --> J4[4. Push to Docker Hub]
    end
    
    Jenkins --> Jenkins-Build{Build Success?}
    Jenkins-Build -->|Yes| PushReg[🐳 Docker Hub Registry]
    PushReg --> SSHDeploy[🚀 SSH Continuous Deployment]
    
    subgraph Target Host Server (AWS EC2)
        direction TB
        SSHDeploy --> PullImg[Pull Latest Image]
        PullImg --> RunCont[Launch DevOpsPulse Container]
        RunCont --> Prometheus[📊 Prometheus Metrics Scraper]
        Prometheus --> Grafana[📈 Grafana Dashboard Visualization]
    end
    
    subgraph Local Server Crontab
        Cron[⏰ Cron Scheduler] -->|Hourly / Daily| Bsh[backup.sh Archive utility]
        Cron -->|Weekly| Csh[cleanup.sh Pruning utility]
    end
```

---

## 🛠️ Technology Stack Ecosystem

| Layer | Tools & Technologies |
| :--- | :--- |
| **Code & Repository** | Git, GitHub |
| **Pipeline Automation (CI/CD)** | Jenkins Declarative Pipeline |
| **Application Services** | Node.js (v20+), Express.js, `prom-client` telemetry instrumentation |
| **Microservices Containerization** | Docker, multi-stage `Dockerfile`, Docker Compose orchestrations |
| **Cloud Hosting (IaaS)** | AWS EC2 (Ubuntu 22.04 LTS), Security Groups, Elastic IPs |
| **Telemetry & Observability** | Prometheus, Grafana, Node Exporter metrics |
| **Operating System Automation** | POSIX Bash Shell, Crontab scheduling |

---

## 📁 Repository Directory Taxonomy

```
devops-capstone-project/
├── app/                          # Primary System Dashboard Application
│   ├── public/                   # Client-side web assets (Dashboard Frontend)
│   │   ├── css/style.css         # Glassmorphic, dark-mode CSS styling system
│   │   ├── js/dashboard.js       # Chart.js plotting & command handlers
│   │   └── index.html            # Primary index landing layout
│   └── src/server.js             # Express.js REST server & scripts trigger
├── docker/                       # Containerization & Scraper configurations
│   ├── docker-compose.yml        # Multi-container Compose runner
│   └── prometheus.yml            # Prometheus targets & interval details
├── scripts/                      # OS Automation script utilities
│   ├── backup.sh                 # Archive compiler & retention swept
│   └── cleanup.sh                # Logs rotator & directory pruner
├── assets/                       # Custom telemetry diagram visual assets
│   ├── architecture_diagram.png
│   ├── jenkins_pipeline.png
│   ├── grafana_dashboard.png
│   └── aws_deployment.png
├── Dockerfile                    # Production multi-stage build manifest
├── .dockerignore                 # Excludes development folders
├── Jenkinsfile                   # Multi-stage CI/CD configuration
├── generate_report.py            # Python report generator script
└── README.md                     # Current workspace documentation
```

---

## 💻 Local Launch & Setup Instructions

### Prerequisites
* [Node.js (v18+)](https://nodejs.org/) & `npm`
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 1. Manual Local Execution (Aesthetic Dashboard)
To run the Node.js telemetry application locally outside container sandboxes:
```bash
# Navigate to application workspace
cd app

# Install dependencies
npm install

# Run backend telemetry server
npm start
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser to explore the dashboard.

### 2. Multi-Container Execution (Docker Compose Orchestration)
To spin up the entire monitoring framework (Application + Node Exporter + Prometheus + Grafana) simultaneously:
```bash
# Start Docker compose inside the docker folder
cd docker
docker-compose up -d --build
```
This orchestrates the following endpoints across your machine:
* **💻 DevOpsPulse Application UI**: [http://localhost:3005](http://localhost:3005)
* **📊 Prometheus Scraper Console**: [http://localhost:9095](http://localhost:9095)
* **📈 Grafana UI Metrics**: [http://localhost:3015](http://localhost:3015) *(Default Credentials: `admin` / `admin`)*
* **⚙️ Node Exporter Endpoint**: [http://localhost:9105/metrics](http://localhost:9105/metrics)

---

## ⚙️ Cron Schedule Script Automations

We use two automated maintenance bash scripts:
1. **`scripts/backup.sh`**: Compresses config and log files into `.tar.gz` and prunes backups older than 5 days.
2. **`scripts/cleanup.sh`**: Rotates log archives, sweeping files ending in `.log` older than 7 days to conserve disk space.

### Cron Installation
To automatically schedule these scripts on your hosting machine:
```bash
# Edit crontab schedules
crontab -e
```
Add the following entries to run backups daily at midnight and cleanups weekly on Sunday at 2 AM:
```cron
# Execute daily backup
0 0 * * * /bin/bash /usr/src/app/scripts/backup.sh >> /var/log/devopspulse/backup_cron.log 2>&1

# Execute weekly log cleanup
0 2 * * 0 /bin/bash /usr/src/app/scripts/cleanup.sh >> /var/log/devopspulse/cleanup_cron.log 2>&1
```

---

## 🎓 Capstone Credentials & Report
A beautiful, publication-grade project report has been compiled for submission:
📂 **[DevOps_Capstone_Project_Report.pdf](file:///c:/Users/cguru/Downloads/devops%20final%20project/DevOps_Capstone_Project_Report.pdf)**

*Developed with ❤️ as part of the DevOps Capstone Program.*
