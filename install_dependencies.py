import subprocess
import sys

def install_package(package):
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package}: {e}")
        sys.exit(1)

# Install packages in order
packages = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "flask>=2.0.1",
    "flask-cors>=3.0.10",
    "requests>=2.26.0",
    "yfinance>=0.2.0",
    "scikit-learn>=1.0.0",
    "nltk>=3.6.2",
    "python-dotenv>=0.19.0",
    "sqlalchemy>=1.4.23",
    "beautifulsoup4>=4.9.3",
    "newsapi-python>=0.2.6",
    "plotly>=5.3.1"
]

for package in packages:
    install_package(package)

print("\nAll packages installed successfully!") 