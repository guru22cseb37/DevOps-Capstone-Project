#!/bin/bash

# ==============================================================================
#  DevOpsPulse Automated Logs Cleanup & Pruning Script
#  Description: Rotates and sweeps log directories to optimize server disk space.
#  Author: DevOps Capstone Team
# ==============================================================================

# Strict error handling
set -euo pipefail

# Configurations
LOGS_DIR="/var/log/devopspulse/logs"
RETENTION_DAYS=7
AUDIT_LOG="/var/log/devopspulse/audit_cleanup.log"

# Colors for terminal styling
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper for formatted timestamps
get_timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

log_info() {
  echo -e "[$(get_timestamp)] [${BLUE}INFO${NC}] $1"
}

log_success() {
  echo -e "[$(get_timestamp)] [${GREEN}SUCCESS${NC}] $1"
}

log_warn() {
  echo -e "[$(get_timestamp)] [${YELLOW}WARN${NC}] $1"
}

# Start process
log_info "Sweeping logs directory: $LOGS_DIR"

# Establish log environment if not present
if [ ! -d "$LOGS_DIR" ]; then
  log_info "Initializing system log path: $LOGS_DIR"
  mkdir -p "$LOGS_DIR"
  
  # Seed some old mock files to test pruning (dated back 10 days)
  log_info "Seeding mock logs for demonstration..."
  touch -d "10 days ago" "$LOGS_DIR/access_2026-05-20.log"
  touch -d "8 days ago" "$LOGS_DIR/error_2026-05-21.log"
  touch -d "6 days ago" "$LOGS_DIR/system_2026-05-22.log"
  touch "$LOGS_DIR/active_access_current.log"
fi

# Audit Logging setup
mkdir -p "$(dirname "$AUDIT_LOG")"

# Scan files
log_info "Scanning files ending in .log older than $RETENTION_DAYS days..."
FILES_TO_REMOVE=$(find "$LOGS_DIR" -name "*.log" -type f -mtime +$RETENTION_DAYS)

if [ -n "$FILES_TO_REMOVE" ]; then
  log_warn "Found outdated logs older than $RETENTION_DAYS days. Purging files..."
  
  # Audit and delete
  echo "--- Cleanup Session [$(get_timestamp)] ---" >> "$AUDIT_LOG"
  while read -r file; do
    log_info "  - $(basename "$file") (pruned)"
    echo "Removed: $file" >> "$AUDIT_LOG"
    rm -f "$file"
  done <<< "$FILES_TO_REMOVE"
  
  log_success "Pruned log records successfully. Log space optimized."
else
  log_info "Sweep complete: No log files older than $RETENTION_DAYS days detected."
fi

# Log current disk usage of log folder
DISK_USAGE=$(du -sh "$LOGS_DIR" | cut -f1)
log_info "Current telemetry log directory size: $DISK_USAGE"

log_success "DevOpsPulse Log cleanup finished. Status: OK"
