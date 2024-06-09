import os
import subprocess

# Definiere die Pfade, die im Installationsskript verwendet wurden
home = os.getenv('HOME')
GOROOT = os.path.join(home, '.goroot')
GOPATH = os.path.join(home, '.go')
go_env_path = os.path.join(home, '.config', 'go', 'go.env')

# Funktion zum Entfernen von Zeilen aus einer Datei
def remove_line_from_file(file_path, line_content):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
        with open(file_path, "w") as file:
            for line in lines:
                if line_content not in line:
                    file.write(line)

# Entferne die Umgebungsvariablen aus .bashrc und .bash_profile
bashrc = os.path.join(home, '.bashrc')
bash_profile = os.path.join(home, '.bash_profile')
remove_line_from_file(bashrc, f". {go_env_path}")
remove_line_from_file(bash_profile, f". {go_env_path}")

# Lösche die Go-Verzeichnisse
if os.path.exists(GOROOT):
    subprocess.run(['rm', '-rf', GOROOT], check=True)
if os.path.exists(GOPATH):
    subprocess.run(['rm', '-rf', GOPATH], check=True)

# Lösche die go.env Datei und das Verzeichnis, falls leer
if os.path.exists(go_env_path):
    os.remove(go_env_path)
go_env_base_path = os.path.dirname(go_env_path)
if os.path.exists(go_env_base_path) and not os.listdir(go_env_base_path):
    os.rmdir(go_env_base_path)

print("Go deinstallation completed successfully")