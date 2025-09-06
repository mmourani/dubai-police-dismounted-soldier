#!/bin/bash
# Quick test script to trigger Claude rate limits and show fallback

echo "🧪 Testing Claude Rate Limit Fallback"
echo "========================================"
echo "Will send 10 queries to trigger Claude's 8-request limit"
echo

for i in {1..10}; do
    echo "📤 Query $i: Testing message $i"
    python3 multi_ai_cli_realtime.py "Test message $i for rate limit demo"
    echo
    echo "📊 Current Status:"
    ./claude_integration.sh status
    echo
    echo "---"
    sleep 1
done

echo "✅ Rate limit test completed!"
echo "📊 Final Status:"
./claude_integration.sh detailed