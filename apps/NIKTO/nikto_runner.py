import subprocess
import json
import os
import tempfile
from datetime import datetime

# ============================================================
# CHEMINS VERS NIKTO
# ============================================================
PERL_PATH = r"C:\Strawberry\perl\bin\perl.exe"
NIKTO_PATH = r"C:\Strawberry\perl\bin\nikto.bat"
# ============================================================


def run_nikto(target_url, extra_options=None):
    """
    Lance un scan Nikto sur l'URL cible et retourne les résultats.
    """

    with tempfile.NamedTemporaryFile(
        suffix='.json', delete=False, mode='w'
    ) as tmp_file:
        tmp_path = tmp_file.name

    started_at = datetime.now().isoformat()

    try:
        cmd = [
            NIKTO_PATH,
            '-h', target_url,
            '-Format', 'json',
            '-output', tmp_path,
            '-nointeractive',
            '-Tuning', '123456789abc',
            '-timeout', '3',
            '-maxtime', '600',
        ]

        if extra_options:
            cmd.extend(extra_options)

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=660,
        )

        finished_at = datetime.now().isoformat()

        findings = []
        raw_output = process.stdout + process.stderr

        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
            with open(tmp_path, 'r', encoding='utf-8') as f:
                try:
                    nikto_data = json.load(f)
                    findings = parse_nikto_json(nikto_data)
                except json.JSONDecodeError:
                    findings = parse_nikto_text(raw_output)
        else:
            findings = parse_nikto_text(raw_output)

        return {
            'success': True,
            'output': raw_output,
            'findings': findings,
            'started_at': started_at,
            'finished_at': finished_at,
            'error': None,
        }

    except subprocess.TimeoutExpired:
        finished_at = datetime.now().isoformat()
        return {
            'success': False,
            'output': '',
            'findings': [],
            'started_at': started_at,
            'finished_at': finished_at,
            'error': 'Le scan a dépassé le délai de 5 minutes.',
        }

    except FileNotFoundError as e:
        finished_at = datetime.now().isoformat()
        return {
            'success': False,
            'output': '',
            'findings': [],
            'started_at': started_at,
            'finished_at': finished_at,
            'error': (
                f'Fichier introuvable : {str(e)}. '
                f'Vérifiez NIKTO_PATH="{NIKTO_PATH}"'
            ),
        }

    except Exception as e:
        finished_at = datetime.now().isoformat()
        return {
            'success': False,
            'output': '',
            'findings': [],
            'started_at': started_at,
            'finished_at': finished_at,
            'error': f'Erreur inattendue : {str(e)}',
        }

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def parse_nikto_json(data):
    findings = []
    vulnerabilities = []

    if isinstance(data, list):
        vulnerabilities = data
    elif 'vulnerabilities' in data:
        vulnerabilities = data['vulnerabilities']
    elif 'host' in data:
        host_data = data['host']
        if isinstance(host_data, list):
            for host in host_data:
                vulnerabilities.extend(host.get('vulnerabilities', []))
        else:
            vulnerabilities = host_data.get('vulnerabilities', [])

    for vuln in vulnerabilities:
        findings.append({
            'id': vuln.get('id', 'N/A'),
            'osvdb': vuln.get('OSVDB', vuln.get('osvdb', 'N/A')),
            'method': vuln.get('method', 'GET'),
            'url': vuln.get('url', '/'),
            'msg': vuln.get('msg', vuln.get('message', 'Aucun détail')),
        })

    return findings


def parse_nikto_text(output):
    import re
    findings = []

    for line in output.splitlines():
        line = line.strip()
        if line.startswith('+ '):
            msg = line[2:]

            # Extraire l'URL si présente
            url = '/'
            if ': /' in msg:
                parts = msg.split(': ', 1)
                if parts[0].startswith('/'):
                    url = parts[0]
                    msg = parts[1] if len(parts) > 1 else msg

            # Extraire OSVDB si présent
            osvdb = 'N/A'
            match = re.search(r'OSVDB-(\d+)', msg)
            if match:
                osvdb = match.group(1)

            findings.append({
                'id': 'N/A',
                'osvdb': osvdb,
                'method': 'GET',
                'url': url,
                'msg': msg,
            })

    return findings


def is_nikto_installed():
    try:
        result = subprocess.run(
            [NIKTO_PATH, '-Version'],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0 or 'nikto' in result.stdout.lower()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False