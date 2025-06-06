import os
from zipfile import ZipFile

# Папка проекта
project_root = os.path.abspath(os.path.dirname(__file__))
zip_output = os.path.join(project_root, "noctune_v2_release.zip")

# Упаковка
with ZipFile(zip_output, "w") as zipf:
    for folder in ["frontend", "docs"]:
        folder_path = os.path.join(project_root, folder)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, project_root)
                zipf.write(full_path, arcname)

print(f"✅ Архив создан: {zip_output}")
