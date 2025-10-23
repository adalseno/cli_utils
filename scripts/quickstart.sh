#!/bin/bash
# Quick start script for CLI Utils development

set -e  # Exit on error

echo "🚀 CLI Utils Quick Start"
echo "======================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo "📦 Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ uv is installed"

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No virtual environment detected"
    echo "🔧 Creating virtual environment..."
    uv venv
    echo "✓ Virtual environment created"
    echo ""
    echo "Please activate it with:"
    echo "  source .venv/bin/activate"
    echo ""
    echo "Then run this script again."
    exit 0
fi

echo "✓ Virtual environment active: $VIRTUAL_ENV"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
make install-dev

# Run tests
echo ""
echo "🧪 Running tests..."
make test ARGS="--no-cov"

# Show version
echo ""
echo "📋 Version info:"
make version

echo ""
echo "✅ Quick start complete!"
echo ""
echo "Next steps:"
echo "  • Run tests:           make test"
echo "  • Format code:         make format"
echo "  • Serve docs:          make docs-serve"
echo "  • Show all commands:   make help"
echo ""
echo "Happy coding! 🎉"
