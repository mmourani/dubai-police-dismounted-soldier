#!/usr/bin/env node

import { spawn } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Start MCP server as subprocess
const server = spawn('node', [join(__dirname, 'mcp-server/dist/server.js')], {
  stdio: ['pipe', 'pipe', 'pipe'],
  cwd: __dirname
});

// Handle server output
server.stdout.on('data', (data) => {
  try {
    const response = JSON.parse(data.toString());
    console.log('Response:', JSON.stringify(response, null, 2));
  } catch (e) {
    // Not JSON, just log it
    console.log('Output:', data.toString());
  }
});

server.stderr.on('data', (data) => {
  const msg = data.toString();
  if (!msg.includes('MCP server "doc-foundry" started successfully')) {
    console.error('Error:', msg);
  }
});

// Test commands
const tests = [
  { method: 'tools/list', id: '1', jsonrpc: '2.0' },
  { 
    method: 'tools/call', 
    id: '2', 
    jsonrpc: '2.0',
    params: { name: 'readiness_analyze', arguments: {} }
  },
  {
    method: 'tools/call',
    id: '3', 
    jsonrpc: '2.0',
    params: { name: 'readiness_status', arguments: { verbose: true } }
  }
];

// Send test commands with delay
async function runTests() {
  console.log('Testing MCP server...\n');
  
  for (const test of tests) {
    console.log(`Sending: ${test.method} ${test.params?.name || ''}`);
    server.stdin.write(JSON.stringify(test) + '\n');
    
    // Wait for response
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Clean shutdown
  setTimeout(() => {
    server.kill();
    process.exit(0);
  }, 2000);
}

// Wait for server to start
setTimeout(runTests, 500);