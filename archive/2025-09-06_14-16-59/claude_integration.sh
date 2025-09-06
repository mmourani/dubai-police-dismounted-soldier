#!/bin/bash
# Claude CLI Integration Script
# Displays Multi-AI provider status in this Claude interface

STATUS_FILE="$HOME/.ai_cli_status.json"
DISPLAY_FILE="$HOME/.claude_status_display.txt"

# Function to display current status
show_status() {
    if [ -f "$STATUS_FILE" ]; then
        python3 "$(dirname "$0")/claude_cli_status_monitor.py" current
    else
        echo "🤖 Multi-AI Status: Not Connected (run multi_ai_cli_realtime.py to start)"
    fi
}

# Function to start monitoring in background
start_monitoring() {
    if ! pgrep -f "claude_cli_status_monitor.py start" > /dev/null; then
        python3 "$(dirname "$0")/claude_cli_status_monitor.py" start &
        echo "✅ Status monitoring started in background"
    else
        echo "ℹ️  Status monitoring already running"
    fi
}

# Function to stop monitoring
stop_monitoring() {
    pkill -f "claude_cli_status_monitor.py start"
    echo "⏹️  Status monitoring stopped"
}

# Main command handler
case "${1:-status}" in
    "start")
        start_monitoring
        ;;
    "stop")
        stop_monitoring
        ;;
    "status")
        show_status
        ;;
    "detailed")
        python3 "$(dirname "$0")/claude_cli_status_monitor.py" status
        ;;
    *)
        echo "Usage: $0 [start|stop|status|detailed]"
        echo "  start    - Start background status monitoring"
        echo "  stop     - Stop background status monitoring"
        echo "  status   - Show current provider status"
        echo "  detailed - Show detailed provider information"
        ;;
esac