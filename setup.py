#!/usr/bin/env python3
"""
Setup script for RAG Knowledge Base repository.

This script helps set up the development environment and installs
all necessary dependencies for the RAG examples.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    if not os.path.exists("venv"):
        return run_command("python -m venv venv", "Creating virtual environment")
    else:
        print("✅ Virtual environment already exists")
        return True

def activate_and_install():
    """Activate virtual environment and install dependencies."""
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    commands = [
        f"{pip_cmd} install --upgrade pip",
        f"{pip_cmd} install -r examples/requirements.txt"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Running: {cmd}"):
            return False
    
    return True

def create_env_file():
    """Create a .env file template."""
    env_content = """# RAG Knowledge Base Environment Variables
# Copy this file to .env and fill in your API keys

# OpenAI API Key (for text generation)
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone API Key (optional - for Pinecone vector database)
PINECONE_API_KEY=your_pinecone_api_key_here

# Weaviate URL (optional - for Weaviate vector database)
WEAVIATE_URL=http://localhost:8080

# Other configuration
LOG_LEVEL=INFO
DEBUG=False
"""
    
    env_file = Path(".env.example")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env.example file")
    else:
        print("✅ .env.example file already exists")
    
    return True

def create_directories():
    """Create necessary directories."""
    directories = [
        "data",
        "logs",
        "temp",
        "chroma_db",
        "vector_db"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up RAG Knowledge Base...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not activate_and_install():
        sys.exit(1)
    
    # Create .env file template
    if not create_env_file():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and add your API keys")
    print("2. Activate the virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Run the basic RAG example:")
    print("   python examples/basic-rag-setup.py")
    print("\nFor more information, see the README.md file.")

if __name__ == "__main__":
    main()