import os
import subprocess
import time

# --- НАСТРОЙКИ ---
GITHUB_USER = "da007"
REPO_NAME = "010-CollegeApp"
GITHUB_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}.git"

GITIGNORE_CONTENT = """# Фронтенд (Next.js)
frontend/node_modules/
frontend/.next/
frontend/out/
frontend/.env.local
frontend/.env.*.local
frontend/npm-debug.log*
frontend/yarn-error.log*
frontend/yarn-debug.log*

# Бэкенд (Flask & Python)
backend/venv/
backend/env/
backend/__pycache__/
backend/*.py[cod]
backend/*$py.class
backend/.env
backend/instance/
backend/.pytest_cache/

# Общие системные файлы
.DS_Store
Thumbs.db
.idea/
.vscode/
"""

ENV_EXAMPLE_CONTENT = """# backend/.env.example
# Пример файла переменных окружения. Создайте файл .env на основе этого.

# Настройки базы данных
DATABASE_URL="mysql+mysqlconnector://mysqluser:mysqlpassword@localhost:3306/college_db_mysql"

# Секретные ключи Flask и JWT (в продакшене использовать длинные случайные строки!)
SECRET_KEY="your-very-secret-key-for-dev"
JWT_SECRET_KEY="your-jwt-secret-key"

# API Ключ для AI-помощника (Google Gemini)
GEMINI_API_KEY="your_gemini_api_key_here"
"""

def run_command(command, cwd=None):
    """Выполняет консольную команду и выводит результат"""
    print(f"🚀 Выполняю: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"❌ Ошибка:\n{result.stderr}")
    else:
        print(f"✅ Успешно:\n{result.stdout.strip()}")
    print("-" * 40)

def main():
    root_dir = os.getcwd()
    print(f"Начинаем настройку проекта в папке: {root_dir}\n")

    # 1. Создаем .gitignore
    gitignore_path = os.path.join(root_dir, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(GITIGNORE_CONTENT)
    print("✅ Создан файл .gitignore")

    # 2. Создаем .env.example в папке backend
    backend_dir = os.path.join(root_dir, "backend")
    if os.path.exists(backend_dir):
        env_example_path = os.path.join(backend_dir, ".env.example")
        with open(env_example_path, "w", encoding="utf-8") as f:
            f.write(ENV_EXAMPLE_CONTENT)
        print("✅ Создан шаблон backend/.env.example")
    else:
        print("⚠️ Папка backend не найдена, пропуск .env.example")

    time.sleep(1)

    # 3. Git инициализация и пуш
    run_command("git init")
    run_command("git add .")
    run_command('git commit -m "feat: Initial commit. Full-stack CollegeApp (Flask + Next.js)"')
    run_command("git branch -M main")
    
    # Проверяем, есть ли уже привязанный remote
    check_remote = subprocess.run("git remote -v", shell=True, text=True, capture_output=True)
    if "origin" in check_remote.stdout:
        run_command("git remote remove origin")
    
    run_command(f"git remote add origin {GITHUB_URL}")
    print(f"⏳ Отправляем код на GitHub ({GITHUB_URL})...")
    run_command("git push -u origin main")

    print("\n🎉 ГОТОВО! Проект настроен и (если репозиторий существует) отправлен на GitHub.")
    print("Не забудь удалить файл github_setup.py, он больше не нужен.")

if __name__ == "__main__":
    main()