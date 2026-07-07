import os
import shutil
import tempfile
from flask import Flask, render_template

class StaticSiteGenerator:
    def __init__(self):
        self.app = Flask(__name__)
        self.output_dir = "_site"
        self.setup_routes()
    
    def setup_routes(self):
        """Настройка маршрутов Flask"""
        @self.app.route('/')
        def index():
            return render_template('base.html')
    
    def clean_output_dir(self):
        """Очистка выходной директории"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
    
    def copy_static_files(self):
        """Копирование статических файлов"""
        if os.path.exists('static'):
            shutil.copytree('static', os.path.join(self.output_dir, 'static'))
            return True
        return False
    
    def fix_urls(self, html_content):
        """Замена Flask url_for на относительные пути"""
        replacements = {
            "{{ url_for('static', filename='": "static/",
            "') }}": "",
        }
        
        for old, new in replacements.items():
            html_content = html_content.replace(old, new)
        
        return html_content
    
    def generate_pages(self):
        """Генерация всех страниц"""
        pages_config = [
            ('index.html', 'base.html', {})
        ]
        
        with self.app.test_request_context():
            for filename, template_name, context in pages_config:
                self.generate_page(filename, template_name, context)
    
    def generate_page(self, filename, template_name, context):
        """Генерация одной страницы"""
        try:
            html = render_template(template_name, **context)
            fixed_html = self.fix_urls(html)
            
            output_path = os.path.join(self.output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(fixed_html)
            
            print(f"✅ {filename}")
            
        except Exception as e:
            print(f"❌ Ошибка в {filename}: {e}")
            self.create_error_page(filename, template_name, str(e))
    
    def create_error_page(self, filename, template_name, error):
        """Создание страницы с ошибкой"""
        error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Ошибка</title>
    <style>
        body {{ font-family: Arial; margin: 40px; }}
        .error {{ background: #ffe6e6; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="error">
        <h1>Ошибка генерации {filename}</h1>
        <p><strong>Шаблон:</strong> {template_name}</p>
        <p><strong>Ошибка:</strong> {error}</p>
    </div>
</body>
</html>
"""
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(error_html)
    
    def create_nojekyll(self):
        """Создание .nojekyll файла"""
        with open(os.path.join(self.output_dir, '.nojekyll'), 'w') as f:
            f.write('')
    
    def copy_to_root(self):
        """Копирование сгенерированных файлов в корень проекта"""
        for item in os.listdir(self.output_dir):
            src = os.path.join(self.output_dir, item)
            dst = os.path.join(os.getcwd(), item)
            
            # Пропускаем скрытые файлы GitHub и сам генератор
            if item in ('.git', '.github'):
                continue
            
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                if os.path.exists(dst):
                    os.remove(dst)
                shutil.copy2(src, dst)
        
        print(f"✅ Файлы скопированы в корень проекта")
    
    def generate(self):
        """Основной метод генерации"""
        print("🚀 Запуск генерации статического сайта...")
        
        # Проверка необходимых папок
        if not all(os.path.exists(folder) for folder in ['templates', 'static']):
            print("❌ Отсутствуют необходимые папки: templates или static")
            return False
        
        # Очистка и подготовка
        self.clean_output_dir()
        print("✅ Выходная директория очищена")
        
        # Копирование статических файлов
        if not self.copy_static_files():
            print("❌ Ошибка копирования статических файлов")
            return False
        print("✅ Статические файлы скопированы")
        
        # Генерация страниц
        print("📄 Генерация HTML страниц:")
        self.generate_pages()
        
        # Создание служебных файлов
        self.create_nojekyll()
        
        # Копирование в корень
        self.copy_to_root()
        
        print(f"🎉 Статический сайт сгенерирован!")
        return True

def main():
    generator = StaticSiteGenerator()
    success = generator.generate()
    exit(0 if success else 1)

if __name__ == '__main__':
    main()
