"""
Quick launcher for Hindi AI Assistant
"""

import subprocess
import sys


def main():
    """Launch Streamlit app"""
    print("🚀 Starting Hindi AI Assistant...")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure Streamlit is installed:")
        print("pip install streamlit")


if __name__ == "__main__":
    main()

