"""
Setup script for Hindi AI Assistant
Checks dependencies and creates necessary directories
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False


def create_directories():
    """Create necessary directories"""
    dirs = ['sample_audio', 'output']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✅ Created directory: {dir_name}")
        else:
            print(f"ℹ️  Directory exists: {dir_name}")


def check_dependencies():
    """Check if critical dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    dependencies = [
        'streamlit',
        'speech_recognition',
        'gtts',
        'cv2',
        'pygame',
        'pydub'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            if dep == 'cv2':
                __import__('cv2')
            elif dep == 'gtts':
                __import__('gtts')
            elif dep == 'speech_recognition':
                __import__('speech_recognition')
            elif dep == 'pygame':
                __import__('pygame')
            else:
                __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - not installed")
            missing.append(dep)
    
    return missing


def main():
    """Main setup function"""
    print("=" * 50)
    print("🇮🇳 Hindi AI Assistant - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    install_requirements()
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Some dependencies are missing: {', '.join(missing)}")
        print("Please install them manually:")
        print(f"pip install {' '.join(missing)}")
    else:
        print("\n✅ Setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Run: streamlit run app.py")
        print("2. Open http://localhost:8501 in your browser")
        print("3. Start using the Hindi AI Assistant!")


if __name__ == "__main__":
    main()

