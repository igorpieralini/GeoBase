import os
import importlib.util
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
ENV_PATH = ROOT_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    print("⚠️ No .env file found — defaults will be used.\n")

class Config:
    """ Environment configuration class """

    PROJECT_NAME = os.getenv("PROJECT_NAME", "TraderIA")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

def check_folder_structure():
    """ Verify project folder structure """
    print("📁 Checking folder structure...\n")

    base_path = ROOT_DIR / "app" / "src"
    required_folders = [
        "analysis",
        "assets/images",
        "assets/media",
        "assets/videos",
        "config",
        "connections",
        "data",
        "indicators",
        "queries",
        "search",
    ]

    missing = []
    for folder in required_folders:
        folder_path = base_path / folder
        if folder_path.exists():
            print(f"   ✅  {folder}")
        else:
            print(f"   ❌  Missing: {folder}")
            missing.append(folder)

    if missing:
        print("\n⚠️ Some folders are missing — please review your project structure.\n")
        return False
    else:
        print("\n🎯 All required folders are correctly structured.\n")
        return True

def check_requirements():
    """ Verify that all packages from requirements.txt are installed """
    print("📦 Checking Python dependencies...\n")

    req_path = ROOT_DIR / "requirements.txt"
    if not req_path.exists():
        print("⚠️ requirements.txt not found in project root.\n")
        return False

    with open(req_path, "r", encoding="utf-8") as req_file:
        requirements = [line.strip() for line in req_file if line.strip()]

    missing = []
    for package in requirements:
        pkg_name = package.split("==")[0] if "==" in package else package
        if importlib.util.find_spec(pkg_name.replace("-", "_")) is None:
            missing.append(pkg_name)

    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("💡 Tip: Run → pip install -r requirements.txt\n")
        return False
    else:
        print("✅ All dependencies are installed!\n")
        return True

def system_check():
    """ Run full environment verification """
    print(f"\n🚀 Starting {Config.PROJECT_NAME} environment check...\n")

    folders_ok = check_folder_structure()
    deps_ok = check_requirements()

    print(f"🧩 Environment variables loaded successfully (PROJECT_NAME={Config.PROJECT_NAME}, ENVIRONMENT={Config.ENVIRONMENT})\n")

    if folders_ok and deps_ok:
        print("✅ System check completed successfully!\n")
    else:
        print("⚠️ Some checks failed — please fix the issues above.\n")

if __name__ == "__main__":
    system_check()
