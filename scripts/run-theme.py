import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"


def run_suite(directory):
    scripts = sorted(directory.glob("*.py"))
    if not scripts:
        raise SystemExit(f"Nenhum script encontrado em {directory.relative_to(ROOT)}")

    for script in scripts:
        print(f"Executando {script.relative_to(ROOT).as_posix()}", flush=True)
        subprocess.run([sys.executable, str(script)], cwd=directory, check=True)


def main():
    parser = argparse.ArgumentParser(description="Executa as suítes de QA de um tema.")
    parser.add_argument("theme", choices=sorted(path.name for path in TESTS.iterdir() if path.is_dir()))
    parser.add_argument("repository", help="Repositório de destino no formato organização/nome")
    args = parser.parse_args()

    repository = args.repository.lower()
    mapping = json.loads((ROOT / "config" / "repositories.json").read_text(encoding="utf-8"))
    theme = TESTS / args.theme
    products = mapping.get(repository, [])
    print(f"Tema: {args.theme} | Repositório: {repository}", flush=True)

    run_suite(theme / "comum")
    selected = [theme / product for product in products if (theme / product).is_dir()]
    if not selected:
        print("Somente a suíte comum se aplica a este repositório neste tema.")
    for suite in selected:
        run_suite(suite)


if __name__ == "__main__":
    main()
