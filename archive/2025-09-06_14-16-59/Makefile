# Dubai Police Dismounted Soldier Project Makefile

# MCP Server Management
MCP_LOG=/tmp/doc-foundry.log
MCP_PID=/tmp/doc-foundry.pid
MCP_CMD=node $(HOME)/Sites/document-foundry/mcp-server/dist/server.js

mcp-start:
	@if [ -f $(MCP_PID) ] && kill -0 $$(cat $(MCP_PID)) 2>/dev/null; then \
		echo "⚡ MCP server already running (PID $$(cat $(MCP_PID)))."; \
	else \
		echo "🚀 Starting MCP server..."; \
		$(MCP_CMD) >> $(MCP_LOG) 2>&1 & echo $$! > $(MCP_PID); \
		echo "✅ MCP server started (PID $$(cat $(MCP_PID))). Log: $(MCP_LOG)"; \
	fi

mcp-stop:
	@if [ -f $(MCP_PID) ] && kill -0 $$(cat $(MCP_PID)) 2>/dev/null; then \
		echo "🛑 Stopping MCP server (PID $$(cat $(MCP_PID)))."; \
		kill $$(cat $(MCP_PID)) && rm -f $(MCP_PID); \
	else \
		echo "⚠️  MCP server not running."; \
		rm -f $(MCP_PID); \
	fi

mcp-restart: mcp-stop mcp-start

mcp-status:
	@if [ -f $(MCP_PID) ] && kill -0 $$(cat $(MCP_PID)) 2>/dev/null; then \
		echo "✅ MCP server is running (PID $$(cat $(MCP_PID)))."; \
	else \
		echo "❌ MCP server is not running."; \
	fi

.PHONY: mcp-start mcp-stop mcp-restart mcp-status