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

    for line in lines:
        line = line.rstrip()


        if re.search(r"Port Id\s+Description", line):
            parsing = True
            continue


        if parsing:
            if line == "" or re.match(r"^[-=]+$", line):
                continue

            if re.match(r"^\d+/\d+/(?:[a-zA-Z]?\d+)(?:/\d+)?", line):
                parts = line.split(None, 1)
                if len(parts) == 2:
                    port_id, desc = parts
                    ports.append({
                        "port_id": port_id,
                        "description": desc.strip()
                    })
                else:

                    ports.append({
                        "port_id": parts[0],
                        "description": ""
                    })
            else:
                if ports:
                    if line.startswith(" ") or line.startswith("\t"):
                        ports[-1]['description'] += " " + line.strip()

    return ports
