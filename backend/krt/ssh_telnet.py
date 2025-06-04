import paramiko
import time
import re
from dotenv import load_dotenv
import os
load_dotenv()
def fetch_port_descriptions():

    jump_host = os.getenv("JUMP_HOST")
    jump_user = os.getenv("JUMP_USER")
    jump_pass = os.getenv("JUMP_PASS")

    telnet_host = os.getenv("TELNET_HOST")
    telnet_user = os.getenv("TELNET_USER")
    telnet_pass = os.getenv("TELNET_PASS")

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(jump_host, username=jump_user, password=jump_pass)

        chan = ssh.invoke_shell()
        time.sleep(1)

        # Telnet ke host target
        chan.send(f"telnet {telnet_host}\n")
        time.sleep(2)
        chan.send(f"{telnet_user}\n")
        time.sleep(1)
        chan.send(f"{telnet_pass}\n")
        time.sleep(2)

        chan.send("environment no more\n")
        time.sleep(3)
        
        # Jalankan perintah Nokia
        chan.send("show port description\n")
        time.sleep(3)

        output = ""
        while chan.recv_ready():
            output += chan.recv(9999).decode(errors="ignore")

        ssh.close()
        return parse_ports(output)

    except Exception as e:
        return {"error": str(e)}


def parse_ports(output):

    
    lines = output.splitlines()
    ports = []
    parsing = False
    last_valid = False

    port_id_regex = re.compile(r"^\d+/\d+/\w+(?:/\d+)?$")
    separator_line = re.compile(r"^[=\-]{5,}")

    for line in lines:
        line = line.strip()

        # Stop parsing jika menemukan baris yang mengandung "esat"
        if "esat" in line.lower():
            break

        # Awal bagian parsing tabel
        if re.search(r"Port Id\s+Description", line):
            parsing = True
            continue

        if not parsing or separator_line.match(line) or line == "":
            continue

        # Baris lanjutan dari deskripsi
        if line.startswith(" ") or line.startswith("\t"):
            if last_valid and ports:
                ports[-1]['description'] += " " + line.strip()
            continue

        # Baris utama dengan port_id dan deskripsi
        parts = line.split(None, 1)
        port_id_candidate = parts[0]

        if port_id_regex.match(port_id_candidate):
            description = parts[1].strip() if len(parts) > 1 else ""
            ports.append({
                "port_id": port_id_candidate,
                "description": description
            })
            last_valid = True
        else:
            last_valid = False

    return ports
