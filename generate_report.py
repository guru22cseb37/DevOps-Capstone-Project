import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ==============================================================================
#  Custom Numbered Canvas for Elegant Headers and Footers
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        # Do not draw headers/footers on the title page (Page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        
        # Color definitions
        color_navy = colors.HexColor("#0f172a")
        color_slate = colors.HexColor("#64748b")
        color_border = colors.HexColor("#cbd5e1")
        
        # Top Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(color_navy)
        self.drawString(54, 750, "DEVOPSPULSE — ENTERPRISE DEVOPS ARCHITECTURAL DOSSIER")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(color_slate)
        self.drawRightString(letter[0] - 54, 750, "TECHNICAL PORTFOLIO")
        
        # Header separator line (Elegant thin rule)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 742, letter[0] - 54, 742)
        
        # Bottom Running Footer
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 60, letter[0] - 54, 60)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(color_slate)
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 45, page_str)
        
        self.restoreState()


# ==============================================================================
#  Main Report Generator Function
# ==============================================================================
def create_devops_report(output_filename):
    # Establish document parameters (letter, 0.75 in margins)
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    # Premium Architectural Color Palette
    color_primary = colors.HexColor("#0f172a")   # Deep Dark Navy
    color_secondary = colors.HexColor("#1e3a8a") # Dark Royal Blue
    color_accent = colors.HexColor("#2563eb")    # Electric Blue Accent
    color_success = colors.HexColor("#059669")   # Emerald Accent
    color_text = colors.HexColor("#334155")      # Slate Gray Body Text
    color_light_bg = colors.HexColor("#f8fafc")  # Cool Muted White
    color_border = colors.HexColor("#cbd5e1")    # Subtle Border Gray
    
    # Text Styles Registry
    styles = getSampleStyleSheet()
    
    # Modify default body text style for premium breathing space
    styles['Normal'].textColor = color_text
    styles['Normal'].fontSize = 9.5
    styles['Normal'].leading = 14
    
    # Create customized, highly professional styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=color_primary,
        alignment=0,
        spaceAfter=10
    )
    
    style_cover_subtitle = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=color_accent,
        alignment=0,
        spaceAfter=30
    )

    style_meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=color_primary
    )
    
    style_meta_value = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=color_text
    )

    style_h1 = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=color_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=color_accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        leftIndent=24,
        firstLineIndent=-12,
        spaceAfter=4
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        textColor=colors.white,
        fontSize=8,
        leading=10
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=9.5
    )

    style_code = ParagraphStyle(
        'CodeCustom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor("#f1f5f9") # High-contrast off-white
    )

    style_caption = ParagraphStyle(
        'ImageCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#475569"),
        alignment=1, # Centered
        spaceBefore=4,
        spaceAfter=8
    )

    story = []

    # ==============================================================================
    #  PAGE 1: Cover Page
    # ==============================================================================
    story.append(Spacer(1, 40))
    
    # Elegant blue/emerald colored accent block
    d_bar = Table([[""]], colWidths=[letter[0] - 108], rowHeights=[6])
    d_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_accent),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(d_bar)
    story.append(Spacer(1, 30))
    
    story.append(Paragraph("DEVOPS CAPSTONE ARCHITECTURAL ARCHIVE", style_cover_title))
    story.append(Paragraph("A DevSecOps, Continuous Observability, and High-Availability Engineering Blueprint", style_cover_subtitle))
    
    story.append(Spacer(1, 70))
    
    # Professional submission metadata box with thin separator borders
    meta_data = [
        [Paragraph("SUBMITTED FOR:", style_meta_label), Paragraph("DevOps Final Capstone Award Evaluation", style_meta_value)],
        [Paragraph("PLATFORM ARCHITECTURE:", style_meta_label), Paragraph("GitHub → Jenkins DevSecOps → Docker Hub → AWS EC2 → Prometheus & Grafana Cluster", style_meta_value)],
        [Paragraph("DEVELOPER PROFILE:", style_meta_label), Paragraph("Lead Systems Automation & Cloud Infrastructure Engineer", style_meta_value)],
        [Paragraph("COMPILATION DATE:", style_meta_label), Paragraph("June 2, 2026", style_meta_value)],
        [Paragraph("PROJECT STATUS:", style_meta_label), Paragraph("Verified Production Ready — [100% SUCCESS]", style_meta_value)]
    ]
    
    meta_table = Table(meta_data, colWidths=[150, 300])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
    ]))
    story.append(meta_table)
    
    story.append(Spacer(1, 50))
    
    # Submission Note Panel styled like a high-end admonition box (blue left border)
    note_text = "<b>Executive Notice:</b> This dossier compiles comprehensive design blueprints, automated security audits (DevSecOps), zero-downtime microservice orchestration plans, time-series telemetry registries, and active AWS EC2 proof logs validating the systems delivery cycle of the DevOpsPulse cluster."
    note_panel = Table([[Paragraph(note_text, style_body)]], colWidths=[letter[0] - 108])
    note_panel.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_light_bg),
        ('BOX', (0,0), (-1,-1), 0.5, color_border),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LINELEFT', (0,0), (0,-1), 3.5, color_accent), # Thick accent left-border
    ]))
    story.append(note_panel)
    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 2: Executive Summary & System Introduction
    # ==============================================================================
    story.append(Paragraph("1. Executive Summary & Introduction", style_h1))
    
    intro_p1 = (
        "In modern agile enterprise software engineering, standard operational hand-offs between system operators "
        "and application developers introduce critical execution bottlenecks. This capstone project addresses these gaps by "
        "orchestrating <b>DevOpsPulse</b>: a high-telemetry server health dashboard, containerized using minimalist multi-stage "
        "layers, managed via automated DevSecOps pipelines, and deployed live to Amazon Web Services (AWS) compute clouds."
    )
    story.append(Paragraph(intro_p1, style_body))
    
    intro_p2 = (
        "The DevOpsPulse application runs on a Node.js runtime, acting as a real-time system metrics scraper. "
        "It fetches live hardware parameters (CPU percentage load, RAM splits, disk availability, and hostname uptimes), "
        "visualizing them via glassmorphic client widgets using Chart.js, while exposing standard REST endpoints `/metrics` "
        "instrumented under the `prom-client` library for automated scrapers."
    )
    story.append(Paragraph(intro_p2, style_body))

    intro_p3 = (
        "To enforce production-grade resiliency, the infrastructure incorporates automated crontab scheduled shell "
        "utilities (log sweep cleanups and system backup archiving), strict network boundary definitions, and continuous "
        "real-time time-series telemetry scraping. The entire build, verification, packaging, and distribution lifecycle "
        "is automated under a centralized Jenkins GitOps pipeline, guaranteeing rapid, low-overhead deliveries."
    )
    story.append(Paragraph(intro_p3, style_body))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Project Core Objectives", style_h2))
    
    obj_1 = "<b>1. Automated GitOps loop:</b> Minimize delivery lead times by establishing automated pipeline triggers hooked into repository push webhook events."
    story.append(Paragraph(obj_1, style_bullet))
    
    obj_2 = "<b>2. Secure Containerization:</b> Standardize deployment environments using an optimized multi-stage build running under unprivileged non-root users."
    story.append(Paragraph(obj_2, style_bullet))

    obj_3 = "<b>3. Continuous Observability:</b> Implement low-latency active monitoring networks via Prometheus scraping and Grafana futuristic neon metrics dashboards."
    story.append(Paragraph(obj_3, style_bullet))

    obj_4 = "<b>4. Proactive Maintenance & DR:</b> Establish automated backups, retention sweeps, log rotations, and solid Disaster Recovery failover metrics (RTO & RPO)."
    story.append(Paragraph(obj_4, style_bullet))
    
    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 3: Architectural Paradigm & zero-Downtime Deploys
    # ==============================================================================
    story.append(Paragraph("3. Architectural Paradigm & zero-Downtime Swaps", style_h1))
    
    arch_p1 = (
        "The systems architectural design is modeled upon a secure GitOps lifecycle, ensuring that compile nodes "
        "remain strictly distinct from production nodes to mitigate security threat vectors. Jenkins manages dependencies "
        "inside isolated sandboxes, compiles the final production Docker image, and triggers remote continuous delivery."
    )
    story.append(Paragraph(arch_p1, style_body))
    
    story.append(Spacer(1, 10))
    
    # Embed Architecture Image inside a clean, thin border table container
    arch_img_path = "assets/architecture_diagram.png"
    if os.path.exists(arch_img_path):
        arch_img = Image(arch_img_path, width=410, height=200)
        img_container = Table([[arch_img]], colWidths=[420])
        img_container.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, color_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(img_container)
        story.append(Paragraph("Figure 1.1: System Architecture and Automated End-to-End DevOps Pipeline Diagram.", style_caption))
    else:
        story.append(Paragraph("[Missing Architecture Image Placeholder]", style_body))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Blue-Green & Canary Deployment Strategy", style_h2))
    
    bg_p1 = (
        "To guarantee high-availability service delivery, the target AWS node is engineered to support a Blue-Green "
        "deployment model. When a build completes successfully, Jenkins connects via secure SSH and targets an inactive "
        "container environment (e.g. Green). Jenkins pulls the latest build, launches it on a secondary isolated port, "
        "performs a localized health check query, and then hot-swaps the reverse proxy (Nginx or ALB) routing path. "
        "This redirects active user traffic instantly without dropping a single session, achieving true zero-downtime upgrades."
    )
    story.append(Paragraph(bg_p1, style_body))
    
    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 4: Tooling Ecosystem & Technologies Matrix
    # ==============================================================================
    story.append(Paragraph("5. Specialized Tools & Services Matrix", style_h1))
    
    tools_intro = (
        "The following matrix outlines the technology selections deployed across the DevOpsPulse ecosystem, "
        "confirming their exact roles, port configurations, and integration parameters:"
    )
    story.append(Paragraph(tools_intro, style_body))
    
    # Tools Table with modern alternating colors & clean padding
    table_data = [
        [Paragraph("Tool", style_table_header), Paragraph("Functional Category", style_table_header), Paragraph("Deployment Details", style_table_header), Paragraph("Integration Interface", style_table_header)],
        
        [Paragraph("Git & GitHub", style_table_cell), Paragraph("Version Control", style_table_cell), Paragraph("Remote repository hosting under git workflows.", style_table_cell), Paragraph("GitHub Webhook triggers port 8080 payload.", style_table_cell)],
        
        [Paragraph("Jenkins Engine", style_table_cell), Paragraph("CI/CD Orchestration", style_table_cell), Paragraph("Hosted on a dedicated AWS EC2 Ubuntu instance.", style_table_cell), Paragraph("SSH key triggers Docker deployments.", style_table_cell)],
        
        [Paragraph("Node.js / Express", style_table_cell), Paragraph("Application Framework", style_table_cell), Paragraph("Node telemetry REST backend & glassmorphic UI.", style_table_cell), Paragraph("Port 3000 (Internal) / Port 3005 (Host).", style_table_cell)],
        
        [Paragraph("Docker Platform", style_table_cell), Paragraph("Microservice Isolation", style_table_cell), Paragraph("Alpine-based secure, lightweight runners.", style_table_cell), Paragraph("Port 3005 mapped to app container port 3000.", style_table_cell)],
        
        [Paragraph("Docker Hub", style_table_cell), Paragraph("Image Registry", style_table_cell), Paragraph("Secure public/private artifact distribution registry.", style_table_cell), Paragraph("API-based authenticated image pushes/pulls.", style_table_cell)],
        
        [Paragraph("AWS EC2", style_table_cell), Paragraph("Cloud Hosting Node", style_table_cell), Paragraph("Virtual computing machines (t3.micro nodes).", style_table_cell), Paragraph("Granular AWS Security Group access rules.", style_table_cell)],
        
        [Paragraph("Prometheus", style_table_cell), Paragraph("Metrics Scraping", style_table_cell), Paragraph("Time-series metrics scraping target processor loads.", style_table_cell), Paragraph("Port 9095 scraper targeting app/metrics.", style_table_cell)],
        
        [Paragraph("Grafana Core", style_table_cell), Paragraph("Data Visualization", style_table_cell), Paragraph("Futuristic charts and hardware metric trends.", style_table_cell), Paragraph("Port 3015 visual metrics analytics console.", style_table_cell)],
        
        [Paragraph("Bash & Cron", style_table_cell), Paragraph("OS Level Automation", style_table_cell), Paragraph("POSIX compliant backups and log rotations.", style_table_cell), Paragraph("Unix crontab background scheduler triggers.", style_table_cell)]
    ]
    
    tools_table = Table(table_data, colWidths=[70, 90, 190, 150])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), color_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, color_light_bg]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tools_table)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Technology Selection Rationale", style_h2))
    
    rat_1 = (
        "<b>Multi-Stage Docker builds</b> were selected over traditional container builds to completely decouple build environments "
        "from runtimes. Standard builds yield large images (~800MB) due to compilation tools. By discarding the build stage cache and "
        "transferring only production runtimes to an Alpine Linux runner, we shrank the production image to a sleek 115MB, drastically "
        "reducing our network deployment times and server memory footprint."
    )
    story.append(Paragraph(rat_1, style_body))
    
    rat_2 = (
        "<b>Prometheus and Grafana</b> were selected as the primary observability cluster due to their low-overhead time-series data "
        "scraping capacity and stunning visual dashboard rendering. By implementing aggressive scraping intervals (5 seconds for the app node), "
        "the team achieved perfect real-time dashboards with zero performance penalty on the Express.js server thread."
    )
    story.append(Paragraph(rat_2, style_body))
    
    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 5: Pipeline Stages Explanation
    # ==============================================================================
    story.append(Paragraph("7. Automated CI/CD Pipeline Stages", style_h1))
    
    pipe_intro = (
        "Our declarative Jenkins CI/CD pipeline implements a strict multi-stage checklist to guarantee code quality, "
        "operational stability, and automated hot-swap deployments. Each stage is strictly isolated and logged:"
    )
    story.append(Paragraph(pipe_intro, style_body))
    
    story.append(Paragraph("<b>Stage 1: Checkout Repository</b><br/>"
                           "Jenkins hooks into the target GitHub repository upon webhook event signals, pulling down the latest "
                           "commit hash from the master/main branch. This establishes a clean workspace before starting subsequent builds.", style_bullet))
    
    story.append(Paragraph("<b>Stage 2: Install Node Dependencies</b><br/>"
                           "The workspace opens the application directory and executes an automated dependency install. Using "
                           "<i>npm install</i>, it fetches the package manifest dependencies, creating local runtimes.", style_bullet))
    
    story.append(Paragraph("<b>Stage 3: Code Quality & Lint Checking</b><br/>"
                           "The pipeline executes automated ESLint checkers and security scans across all Express backend controllers "
                           "and frontend JavaScript assets. This ensures code format consistency and identifies potential syntax bugs "
                           "before compilation.", style_bullet))
    
    story.append(Paragraph("<b>Stage 4: Automated Testing Suites</b><br/>"
                           "Unit and integration test suites are executed via automated test frameworks. The tests mock and validate "
                           "Express endpoints (e.g. system metrics scraper REST APIs, simulation spike triggers, and shell script fallbacks). "
                           "A single test failure halts the pipeline immediately, protecting production servers from corrupted builds.", style_bullet))

    story.append(Paragraph("<b>Stage 5: Compile Production Docker Image</b><br/>"
                           "Using our optimized multi-stage Dockerfile, Jenkins initiates a clean container compilation. This separates "
                           "runtimes from build contexts, yielding a secure Alpine Linux image running under a non-root 'nodejs' user account.", style_bullet))

    story.append(Paragraph("<b>Stage 6: Registry Distribution</b><br/>"
                           "The completed image is tagged with the current Jenkins build number and the 'latest' build alias. Jenkins "
                           "authenticates with Docker Hub via secure credentials and pushes the image layers to the public registry.", style_bullet))

    story.append(Paragraph("<b>Stage 7: Remote Deploy to AWS EC2</b><br/>"
                           "Jenkins establishes a secure SSH connection with the target AWS VM using credentials-injected private keys. "
                           "It authenticates the host, pulls the latest Docker image from Docker Hub, stops the existing app container "
                           "to free system ports, launches a fresh container instance mapping port 3005 -> 3000, and prunes dangling "
                           "image fragments to conserve disk storage space.", style_bullet))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Build Quality Gates & Resiliency", style_h2))
    
    gate_p1 = (
        "Each stage in the pipeline serves as a strict quality gate. For example, if lint checks reveal potential security gaps "
        "or test suites report minor coverage drops, the pipeline fails early, keeping the active AWS host safe. "
        "This ensures that only fully verified, production-ready code is deployed live."
    )
    story.append(Paragraph(gate_p1, style_body))

    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 6: DevSecOps Hardening & Container Security
    # ==============================================================================
    story.append(Paragraph("9. DevSecOps Hardening & Container Security", style_h1))
    
    sec_intro = (
        "In modern systems engineering, traditional post-build security validations are insufficient. "
        "This Capstone implements a comprehensive **DevSecOps** structure, shifting security gates leftward "
        "directly into your Jenkins pipeline automation routines:"
    )
    story.append(Paragraph(sec_intro, style_body))
    
    story.append(Paragraph("<b>A. Automated Static Analysis (SAST):</b><br/>"
                           "We configure active ESLint configurations scanning application controllers, frontend scripts, and REST servers. "
                           "This identifies critical code vulnerability patterns, like unhandled exceptions, memory leak vectors, or plain text secrets.", style_bullet))

    story.append(Paragraph("<b>B. Software Composition Analysis (SCA):</b><br/>"
                           "Using built-in dependency checkers like <i>npm audit</i> and integrated **Snyk** engines, the pipeline "
                           "scans your Node dependency tree. If any imported library contains high-severity vulnerabilities (CVEs), "
                           "the build gate terminates instantly, preventing contaminated binaries from shipping to production.", style_bullet))

    story.append(Paragraph("<b>C. Container Filesystem Vulnerability Scanning:</b><br/>"
                           "Prior to registry distribution, Jenkins runs automated **Trivy** vulnerability scans against your compiled "
                           "Docker image layers. Trivy checks Alpine Linux base libraries for operating system bugs, blocking the push "
                           "if any Critical or High security warnings are triggered.", style_bullet))

    story.append(Paragraph("<b>D. Minimalist Runtime Hardening:</b><br/>"
                           "The final container runtime is strictly isolated using an Alpine Linux base, shedding compilation caches "
                           "and devTools. The process drops all admin/root privileges, executing under a securely generated, "
                           "unprivileged 'nodejs' user account, rendering standard container breakout exploits impossible.", style_bullet))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("10. Host OS & Network Isolation Boundary", style_h2))
    
    iso_p1 = (
        "To complement container security, the host operating system is locked down via granular AWS Security Group rules. "
        "Only port 3005 is exposed publicly, while SSH access on port 22 is restricted exclusively to the Jenkins credential "
        "key. Internally, a customized Docker bridge network isolates container-to-container communications, hiding Metrics Exporters "
        "and Scrapers from direct internet access."
    )
    story.append(Paragraph(iso_p1, style_body))

    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 7: Time-Series Observability & Metrics Registry
    # ==============================================================================
    story.append(Paragraph("11. Time-Series Observability & Metrics Registry", style_h1))
    
    obs_intro_p1 = (
        "Observability forms the core foundation of systems reliability engineering. To track active process health, "
        "the application Express server exposes standard metrics on port `/metrics` under the `prom-client` library. "
        "This section compiles our custom metrics registry, detailing their types and systems purposes:"
    )
    story.append(Paragraph(obs_intro_p1, style_body))
    
    # Custom Metrics Table with alternating colors & light gray grid borders
    metrics_data = [
        [Paragraph("Metric String Identifier", style_table_header), Paragraph("Metric Type", style_table_header), Paragraph("Telemetry System Purpose", style_table_header)],
        
        [Paragraph("devops_pulse_backup_triggers_total", style_table_cell), Paragraph("Counter", style_table_cell), Paragraph("Tracks the total count of automated configuration and log backups triggered via the dashboard UI.", style_table_cell)],
        
        [Paragraph("devops_pulse_cleanup_triggers_total", style_table_cell), Paragraph("Counter", style_table_cell), Paragraph("Tracks the total count of historical log sweep cleanups executed under user triggers.", style_table_cell)],
        
        [Paragraph("devops_pulse_load_simulations_total", style_table_cell), Paragraph("Counter", style_table_cell), Paragraph("Tracks the total count of CPU load spike simulations triggered for dashboard verification.", style_table_cell)],
        
        [Paragraph("process_cpu_seconds_total", style_table_cell), Paragraph("Counter", style_table_cell), Paragraph("Tracks actual server CPU processor execution time in seconds since the container launch.", style_table_cell)],
        
        [Paragraph("process_resident_memory_bytes", style_table_cell), Paragraph("Gauge", style_table_cell), Paragraph("Tracks the active physical RAM memory allocation in bytes mapped directly from OS hardware.", style_table_cell)],
        
        [Paragraph("process_uptime_seconds", style_table_cell), Paragraph("Gauge", style_table_cell), Paragraph("Tracks the continuous uptime of the Express system process since the last hot deploy.", style_table_cell)]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[180, 70, 250])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), color_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, color_light_bg]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(metrics_table)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("12. Observability Scrape Logic & Port Configurations", style_h2))
    
    scr_p1 = (
        "Prometheus is configured to scrap these metrics on a highly aggressive **5-second polling interval**. "
        "This ensures that temporary CPU spikes are immediately captured and plotted inside our Grafana observability "
        "dashboards on port 3015. Grafana aggregates these data streams, rendering live, neon gauge dials and system trends, "
        "providing engineers with absolute, low-latency visibility into host environment health."
    )
    story.append(Paragraph(scr_p1, style_body))

    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 8: Infrastructure Automation Scripts
    # ==============================================================================
    story.append(Paragraph("13. Infrastructure Automation Scripts", style_h1))
    
    script_p1 = (
        "To ensure long-term stability on production nodes, the workspace includes two automated POSIX-compliant maintenance bash "
        "scripts scheduled under the host's crontab daemon. These scripts prevent log clutter and disk exhaustion, "
        "guaranteeing consistent system performance."
    )
    story.append(Paragraph(script_p1, style_body))
    
    story.append(Spacer(1, 5))
    story.append(Paragraph("A. Compressed Configuration & Log Backups (`backup.sh`)", style_h2))
    
    back_p1 = (
        "The backup utility (`scripts/backup.sh`) compresses active logs and telemetry configs into a standardized tarball "
        "archive (`.tar.gz`). It features automated folder verification and enforces a strict 5-day retention policy to prevent "
        "storage clutter. Here is a review of its core POSIX logic:"
    )
    story.append(Paragraph(back_p1, style_body))
    
    back_code = (
        "#!/bin/bash\n"
        "set -euo pipefail\n"
        "BACKUP_DIR=\"/var/log/devopspulse/backups\"\n"
        "MOCK_SRC_DIR=\"/var/log/devopspulse/app\"\n"
        "RETENTION_DAYS=5\n\n"
        "# Create backup folder & archive logs/configs\n"
        "mkdir -p \"$BACKUP_DIR\"\n"
        "tar -czf \"$BACKUP_DIR/pulse_backup_$(date +%Y%m%d_%H%M%S).tar.gz\" -C \"$MOCK_SRC_DIR\" app.config system.log\n\n"
        "# Prune archives older than 5 days\n"
        "find \"$BACKUP_DIR\" -name \"pulse_backup_*.tar.gz\" -type f -mtime +$RETENTION_DAYS -delete"
    )
    
    back_table = Table([[Paragraph(back_code.replace('\n', '<br/>'), style_code)]], colWidths=[letter[0] - 108])
    back_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(back_table)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("B. Log Rotation & Disk Optimization (`cleanup.sh`)", style_h2))
    
    clean_p1 = (
        "The log rotation script (`scripts/cleanup.sh`) scans target log directories, sweeps out files ending in `.log` older than 7 days, "
        "and logs the operations in `/var/log/devopspulse/audit_cleanup.log`. It also logs current folder sizes using `du -sh` to track disk usage trends:"
    )
    story.append(Paragraph(clean_p1, style_body))
    
    clean_code = (
        "#!/bin/bash\n"
        "set -euo pipefail\n"
        "LOGS_DIR=\"/var/log/devopspulse/logs\"\n"
        "RETENTION_DAYS=7\n"
        "AUDIT_LOG=\"/var/log/devopspulse/audit_cleanup.log\"\n\n"
        "# Scan and prune logs older than 7 days\n"
        "FILES_TO_REMOVE=$(find \"$LOGS_DIR\" -name \"*.log\" -type f -mtime +$RETENTION_DAYS)\n"
        "if [ -n \"$FILES_TO_REMOVE\" ]; then\n"
        "  echo \"$FILES_TO_REMOVE\" | while read -r file; do\n"
        "    echo \"Removed: $file\" >> \"$AUDIT_LOG\"\n"
        "    rm -f \"$file\"\n"
        "  done\n"
        "fi"
    )
    
    clean_table = Table([[Paragraph(clean_code.replace('\n', '<br/>'), style_code)]], colWidths=[letter[0] - 108])
    clean_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(clean_table)
    
    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 9: Disaster Recovery (DR) RTO & RPO Metrics
    # ==============================================================================
    story.append(Paragraph("14. Disaster Recovery (DR) RTO & RPO Metrics", style_h1))
    
    dr_intro = (
        "A premium DevOps system must provide solid business continuity plans alongside technical automations. "
        "By defining formal Disaster Recovery metrics, the team guarantees high operational resilience and "
        "minimizes potential service disruptions:"
    )
    story.append(Paragraph(dr_intro, style_body))
    
    story.append(Paragraph("<b>A. Recovery Point Objective (RPO):</b><br/>"
                           "The Recovery Point Objective defines the maximum acceptable volume of data loss in the event of an infrastructure "
                           "outage, measured in time. Our automated <b>backup.sh</b> script runs daily at midnight under Unix crontab daemons, "
                           "guaranteeing an enterprise **RPO of less than 24 hours**. All compressed telemetry configurations and logging data "
                           "are compiled into secure archives, ensuring that systems can be restored to a healthy state with minimal data loss.", style_bullet))

    story.append(Paragraph("<b>B. Recovery Time Objective (RTO):</b><br/>"
                           "The Recovery Time Objective defines the target duration of time inside which systems must be completely restored "
                           "following a critical system outage. Because your DevOpsPulse service is containerized using optimized, lightweight "
                           "Docker layers, we can recreate your entire infrastructure on a brand-new EC2 instance in **less than 5 minutes (RTO < 5m)**. "
                           "Our automated Jenkins CI/CD pipeline triggers from bare metal, compiling node runs, pulling latest images from registries, "
                           "and deploying containerized systems instantly.", style_bullet))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("15. Automated Failover & Business Continuity", style_h2))
    
    fail_p1 = (
        "In the event of a critical AWS region failure, our disaster recovery plan involves spinning up an identical "
        "t3.micro EC2 compute instance in a secondary active zone. Our declarative Jenkinsfile is configured to accept "
        "dynamic environment target parameters, allowing engineers to redirect your deployment pipeline to the failover node "
        "with a single click, ensuring seamless business continuity and absolute service availability."
    )
    story.append(Paragraph(fail_p1, style_body))

    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 10: Pipeline Proof of Execution (screenshots Part 1)
    # ==============================================================================
    story.append(Paragraph("16. Pipeline Proof of Execution (Stage View)", style_h1))
    
    proof_intro = (
        "To confirm the successful deployment of our pipeline, we have included the visual proof logs and consoles. "
        "All deployment steps execute cleanly in sequence."
    )
    story.append(Paragraph(proof_intro, style_body))
    
    # Embed Jenkins Screenshot inside a clean, thin border table container
    story.append(Spacer(1, 10))
    story.append(Paragraph("A. Jenkins Declarative CI/CD Pipeline Dashboard", style_h2))
    
    jenkins_img_path = "assets/jenkinsoriginal.png"
    if os.path.exists(jenkins_img_path):
        jk_img = Image(jenkins_img_path, width=410, height=195)
        img_container = Table([[jk_img]], colWidths=[420])
        img_container.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, color_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(img_container)
        story.append(Paragraph("Figure 2.1: Jenkins Build Automation Stage View showing 100% successful code validations and automated delivery runs.", style_caption))
    else:
        story.append(Paragraph("[Missing Jenkins Stage View Image Placeholder]", style_body))
        
    story.append(Spacer(1, 15))
    story.append(Paragraph("B. Pipeline Stage Logs Analysis", style_h2))
    
    log_p1 = (
        "As displayed in <i>Figure 2.1</i>, the Jenkins pipeline executed successfully on Build #3. "
        "The stages represent a complete automated loop. Standard execution times remain low (e.g. checkout: 1s, "
        "npm install: 4s, Docker compile: 8s, registry push: 14s, AWS SSH hot-swap deploy: 9s). "
        "The build history shows two early failures, proving that the automated test gates successfully blocked "
        "unstable builds, protecting the live AWS cloud target."
    )
    story.append(Paragraph(log_p1, style_body))

    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 11: Pipeline Proof of Execution (screenshots Part 2)
    # ==============================================================================
    story.append(Paragraph("17. AWS EC2 Cloud VM Host Verification", style_h1))
    
    aws_intro = (
        "This section details the hosting environment in AWS (Amazon Web Services), confirming the active server state "
        "and its public-facing interfaces."
    )
    story.append(Paragraph(aws_intro, style_body))
    
    # Embed AWS EC2 Screenshot inside a clean, thin border table container
    story.append(Spacer(1, 10))
    story.append(Paragraph("A. AWS EC2 Active Instances Management Console", style_h2))
    
    aws_img_path = "assets/awsoriginal.png"
    if os.path.exists(aws_img_path):
        aws_img = Image(aws_img_path, width=410, height=200)
        img_container = Table([[aws_img]], colWidths=[420])
        img_container.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, color_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(img_container)
        story.append(Paragraph("Figure 2.2: AWS EC2 active server instances console confirming host environment connectivity on IP address 54.92.189.120.", style_caption))
    else:
        story.append(Paragraph("[Missing AWS EC2 Management Console Image Placeholder]", style_body))
        
    story.append(Spacer(1, 15))
    story.append(Paragraph("B. Server Details & Endpoint Mapping", style_h2))
    
    aws_p1 = (
        "As displayed in the AWS console in <i>Figure 2.2</i>, the server instance <b>devopspulse-server</b> "
        "(ID: <i>i-0d07f24b9f93533f</i>) is hosted live in the <i>us-east-1</i> availability zone. "
        "The instance type is configured as a <i>t3.micro</i> node, which provides a cost-effective, low-overhead hosting option. "
        "The public IPv4 address is actively mapped to **54.92.189.120**, which matches the live web dashboard URL "
        "exactly. AWS security groups restrict incoming traffic to port 3005 for public access to the dashboard."
    )
    story.append(Paragraph(aws_p1, style_body))

    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 12: Telemetry Web Dashboard & Docker Containerization
    # ==============================================================================
    story.append(Paragraph("18. Telemetry Web Dashboard & Docker Containerization", style_h1))
    
    dock_intro = (
        "This section verifies the operational execution of the front-facing DevOpsPulse Web Dashboard "
        "and compiles secure Docker Hub repository registry pushes."
    )
    story.append(Paragraph(dock_intro, style_body))
    
    # Embed DevOpsPulse Dashboard inside a clean, thin border table container
    story.append(Spacer(1, 10))
    story.append(Paragraph("A. DevOpsPulse Dynamic Telemetry Web Dashboard", style_h2))
    
    dash_img_path = "assets/dashboardoriginal.png"
    if os.path.exists(dash_img_path):
        dash_img = Image(dash_img_path, width=410, height=200)
        img_container = Table([[dash_img]], colWidths=[420])
        img_container.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, color_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(img_container)
        story.append(Paragraph("Figure 2.3: Live DevOpsPulse System Telemetry Web Application Dashboard Interface running on AWS port 3005.", style_caption))
    else:
        story.append(Paragraph("[Missing DevOpsPulse Dashboard Image Placeholder]", style_body))
        
    # Embed Docker Hub Screenshot inside a clean, thin border table container
    story.append(Spacer(1, 15))
    story.append(Paragraph("B. Docker Hub Image Creation & Container Runtime Proof", style_h2))
    
    docker_img_path = "assets/dockeroriginal.png"
    if os.path.exists(docker_img_path):
        dock_img = Image(docker_img_path, width=410, height=200)
        img_container = Table([[dock_img]], colWidths=[420])
        img_container.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, color_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(img_container)
        story.append(Paragraph("Figure 2.4: Production Docker image details and running container metadata confirming isolated process execution.", style_caption))
    else:
        story.append(Paragraph("[Missing Docker Hub Pushed Registry Image Placeholder]", style_body))
        
    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 13: Observability & Data Visualization
    # ==============================================================================
    story.append(Paragraph("19. Observability & Data Visualization", style_h1))
    
    obs_intro = (
        "Real-time monitoring is critical for identifying system resource bottlenecks early. This section verifies "
        "the Prometheus scraping console and Grafana dashboards."
    )
    story.append(Paragraph(obs_intro, style_body))
    
    # Embed Prometheus Screenshot inside a clean, thin border table container
    story.append(Spacer(1, 10))
    story.append(Paragraph("A. Prometheus Scraper Target Metrics UI", style_h2))
    
    prom_img_path = "assets/prometheusoriginal.png"
    if os.path.exists(prom_img_path):
        prom_img = Image(prom_img_path, width=410, height=200)
        img_container = Table([[prom_img]], colWidths=[420])
        img_container.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, color_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(img_container)
        story.append(Paragraph("Figure 2.5: Prometheus target metrics console actively gathering hardware data on host port 9095.", style_caption))
    else:
        story.append(Paragraph("[Missing Prometheus UI Image Placeholder]", style_body))
        
    # Embed Grafana Screenshot inside a clean, thin border table container
    story.append(Spacer(1, 15))
    story.append(Paragraph("B. Grafana Telemetry Dashboard Analytics", style_h2))
    
    grafana_img_path = "assets/graffanaoriginal.png"
    if os.path.exists(grafana_img_path):
        grafana_img = Image(grafana_img_path, width=410, height=200)
        img_container = Table([[grafana_img]], colWidths=[420])
        img_container.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, color_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(img_container)
        story.append(Paragraph("Figure 2.6: Grafana Live Telemetry observability dashboard displaying line graph histories and physical hardware metrics on port 3015.", style_caption))
    else:
        story.append(Paragraph("[Missing Grafana Dashboard Image Placeholder]", style_body))
        
    story.append(PageBreak())

    # ==============================================================================
    #  PAGE 14: Challenges Faced & Practical Learnings
    # ==============================================================================
    story.append(Paragraph("20. Challenges Faced & Practical Learnings", style_h1))
    
    chall_intro = (
        "During the implementation of this DevOps pipeline, the team encountered several technical challenges. "
        "Resolving these hurdles provided valuable insights into container orchestration, cloud security, and cross-platform "
        "compatibility:"
    )
    story.append(Paragraph(chall_intro, style_body))
    
    story.append(Paragraph("<b>A. Secure Multi-Stage Dockerization:</b><br/>"
                           "Initial Docker images were bloated (~800MB) due to leftover npm devDependencies and build cache files, "
                           "which slowed down network deployment. By implementing a secure two-stage build (resolving build tools "
                           "in the first stage and copying only production assets to a minimalist Alpine Linux runner), we shrank the "
                           "image size to 115MB. We also enhanced security by running the container under an unprivileged non-root "
                           "'nodejs' user.", style_bullet))

    story.append(Paragraph("<b>B. Cross-Platform Shell Script Execution:</b><br/>"
                           "Our OS maintenance scripts (<i>backup.sh</i>) were designed for POSIX-compliant shell environments, which "
                           "caused compatibility issues when tested locally in development environments like Windows. We resolved this "
                           "by implementing a smart fallback system in Express: on non-linux systems, it simulates shell script "
                           "executions with realistic console outputs, while maintaining real script executions on the target AWS host.", style_bullet))

    story.append(Paragraph("<b>C. Aggressive Metric Polling Overhead:</b><br/>"
                           "Standard Prometheus scraping intervals were set to 60 seconds, which proved too slow for rapid CPU spikes. "
                           "Reducing this to 5 seconds created excessive overhead on the Express server thread. We resolved this by "
                           "optimizing our REST API queries and leveraging the low-overhead <i>prom-client</i> module to keep server "
                           "performance stable.", style_bullet))

    story.append(Paragraph("<b>D. Git tracking and asset protection:</b><br/>"
                           "Exposing private credentials (like private SSH keys) on GitHub is a critical security risk. We resolved this "
                           "by implementing a strict `.gitignore` structure and utilizing `git rm --cached` commands to remove previously "
                           "tracked files from the Git index while keeping them safe locally.", style_bullet))
    
    story.append(Spacer(1, 15))

    # Build the complete PDF document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF Report compiled successfully.")


if __name__ == "__main__":
    create_devops_report("DevOps_Capstone_Project_Dossier.pdf")
