# Dieser Script dient dem Installieren von Go auf einem Linux System der Debian Klasse (Ubuntu, Debian, ...)
import subprocess
import os
import tempfile

tdir = tempfile.TemporaryDirectory()

tpir = tdir

# Konvertiere tdir in einen String
tdir = tdir.name

# Wichtiger erster Scritt ist, die Richtige System Architectur zu finden
command = 'uname -m'
command = command.split()
result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = result.communicate()
arch = stdout.strip().lower()

# Wichtig ist Wir definieren nun die Download Urls
urls = {
    "linux-i386": "https://go.dev/dl/go1.22.4.linux-386.tar.gz",
    "linux-amd64": "https://go.dev/dl/go1.22.4.linux-amd64.tar.gz",
    "linux-arm64": "https://go.dev/dl/go1.22.4.linux-arm64.tar.gz",
    "linux-armv6": "https://go.dev/dl/go1.22.4.linux-armv6l.tar.gz"
}

# Jetzt wird es Schwieriger uname -m wirft nicht Standardisierte Namen aus, heisst es wird nie amd64., 386, arm64 oder armv6 kommen
# Daher muessen wir alle moeglichen Bezeichnungen einkesseln damit wir immer die Richtige URL erhalten

amd64 = {
    "codenames": [
        "x86_64",
        "intel64",
        "em64t",
        "amd64"
    ]
}

i386 = {
    "codenames": [
        "ia-32",
        "intel32",
        "80386",
        "x86_32",
        "i386"
    ]
}

arm64 = {
    "codenames": [
        "aarch64",
        "armv8",
        "arm64"
    ]
}

armv6 = {
    "codenames": [
        "arm",
        "armv6"
    ]
}

# Erstellen einer Eigenen Exception Klasse
class GoInstallerError(Exception):
    """
    Diese Exception kommt bei Fehlern
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

# Nun finden wir raus welche URL am besten zu unserem System Passt

amd64_exist = False
i386_exist = False
arm64_exist = False
armv6_exist = False

if arch in amd64["codenames"]:
    amd64_exist = True
elif arch in i386["codenames"]:
    i386_exist = True
elif arch in arm64["codenames"]:
    arm64_exist = True
elif arch in armv6["codenames"]:
    armv6_exist = True

if amd64_exist:
    url = urls["linux-amd64"]
elif i386_exist:
    url = urls["linux-i386"]
elif arm64_exist:
    url = urls["linux-arm64"]
elif armv6_exist:
    url = urls["linux-armv6"]

# Nun haben wir erfolgreich alle benoetigten Informationen fuer das Installieren von GO erhalten
# Jetzt erstellen wir eine Kleine Klasse damit wir noch einfacher commands handhaben koennen

class command:
    """
    Diese Klasse dient dazu, Commands einfacher zu Handhaben als mit subprocess oder os
    """
    def __init__(self, programm: str, safe_output=False):
        """
        Hier waehlst du deinen Main Programm und ob der Output gesaft werden soll oder nicht
        """
        self.command = []
        self.command.append(programm)
        self.arguments = []
        self.safe_output = safe_output
        self.stdout = None
        self.stderr = None
        self.programm = programm
        self.executed = False

    def arg(self, argument: str):
        """
        Fuege einen Argument dem Command hinzu
        """
        if self.executed:
            raise GoInstallerError(f"Command {self.command} already executed")
        self.command.append(argument)
        self.arguments.append(argument)

    def args(self, arguments: list):
        if self.executed:
            raise GoInstallerError(f"Command {self.command} already executed")
        """
        Fuege eine Liste von Argumenten dem Command hinzu
        """
        self.command.extend(arguments)
        self.arguments.extend(arguments)

    def get_command(self):
        """
        Gib den Command zurueck
        """
        return self.command
    
    def get_arguments(self):
        """
        Gebe die Argumente zurueck
        """
        return self.arguments
    
    def get_programm(self):
        """
        Gebe das Gewaehlte Haupt Programm zurueck
        """
        return self.programm
    
    def run(self):
        """
        Fuehre den Command aus
        Wenn die Klasse mit safe_output initialisiert wurde erhaelst du Keinen Output
        Auch wird der Output nicht sofort wieder gegeben heisst, es kommen 2 weiter funktionen dazu
        """
        if self.executed:
            raise GoInstallerError(f"Command {self.command} already executed")
        self.executed = True
        if self.safe_output:
            result = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout_raw, stderr_raw = result.communicate()
            self.stdout = stdout_raw.strip()
            self.stderr = stderr_raw.strip()
        else:
            subprocess.run(self.command)

    def get_stdout(self):
        """
        Gebe den stdout zurueck
        """
        if not self.executed:
            raise GoInstallerError(f"Command {self.command} not executed")
        return self.stdout
    
    def get_stderr(self):
        """
        Gebe den stderr zurueck
        """
        if not self.executed:
            raise GoInstallerError(f"Command {self.command} not executed")
        return self.stderr


# wir definieren nun GOROOT und GOPATH

home = os.getenv('HOME')
GOROOT = os.path.join(home, '.goroot')
GOPATH = os.path.join(home, '.go')

os.makedirs(GOROOT, exist_ok=True)
os.makedirs(GOPATH, exist_ok=True)

# Wir erstellen eine neue Datei mit dem Namen go.env
go_env_base_path = os.path.join(home, '.config', 'go')
os.makedirs(go_env_base_path, exist_ok=True)
go_env_path = os.path.join(go_env_base_path, 'go.env')
with open(go_env_path, 'w') as f:
    f.write(f"export GOROOT={GOROOT}\n")
    f.write(f"export GOPATH={GOPATH}\n")
    f.write(f"export PATH=$PATH:$GOROOT/bin\n")
    f.write(f"export PATH=$PATH:$GOPATH/bin\n")

# Nun muessen wir sicherstellen dass die .bashrc oder die .bash_profile, je nachdem welche existiert automatisvh die go.env sourcen tut
bashrc = os.path.join(home, '.bashrc')
bash_profile = os.path.join(home, '.bash_profile')

if os.path.exists(bashrc):
    # nun muessen wir aufpassen, die bashrc darf NICHT ueberschireben werden
    # Vielmehr muss '. {bash_env_path}' angehangen werden in der LETZTEN ZEILE
    with open(bashrc, 'a') as f:
        f.write(f"\n. {go_env_path}\n")
elif os.path.exists(bash_profile):
    # nun muessen wir aufpassen, die bash_profile darf NICHT ueberschireben werden
    # Vielmehr muss '. {bash_env_path}' angehangen werden in der LETZTEN ZEILE
    with open(bash_profile, 'a') as f:
        f.write(f"\n. {go_env_path}\n")
else:
    raise GoInstallerError("No .bashrc or .bash_profile found")

# Nun wechseln wir in das GOROOT und laden go runter
os.chdir(tdir)

archive_path = os.path.join(tdir, os.path.basename(url))

cmd = command(programm='curl', safe_output=False)
cmd.arg('-o')
cmd.arg(archive_path)
cmd.arg('-L')
cmd.arg(url)
cmd.run()

# Jetzt haben wir erfolgreich die richtige datei runtergeladen und werden die entpacken auch hier verwenden wir wieder die Klasse Command, da diese am Besten arbeitet
cmd = command(programm='tar', safe_output=False)
cmd.arg('-x')
cmd.arg('-z')
cmd.arg('-f')
cmd.arg(archive_path)
cmd.run()

cmd = command(programm='rm', safe_output=False)
cmd.arg('-f')
cmd.arg(archive_path)
cmd.run()

folder = os.listdir(tdir)

# Kovertiere folder in einen String
folder = " ".join(folder)

# Jetzt werden wir alle Dateien im Folder go* in das GOROOT verschieben
cmd = command(programm='mv', safe_output=False)
cmd.arg(folder)
cmd.arg(GOROOT)
cmd.run()

cmd = command(programm='rm', safe_output=False)
cmd.arg('-rf')
cmd.arg(archive_path)
cmd.run()

tpir.cleanup()
print("Go installed successfully")