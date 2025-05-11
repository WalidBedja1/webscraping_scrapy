import os
from pathlib import Path

def get_path():
    project_dir = Path(__file__).parent.parent.parent
    csv_path = project_dir / "entreprises.csv"

    print(f"✅ Chemin du fichier CSV : {csv_path}")  # Remplace self.logger.info

    return csv_path
