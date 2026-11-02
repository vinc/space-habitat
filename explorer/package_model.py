"""Bundle only the model and pure API, not the repository or server."""
from pathlib import Path
import sys
import zipfile
root=Path(__file__).resolve().parents[1]
with zipfile.ZipFile(sys.argv[1], 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted((root/'habitat_model').glob('*')):
        if path.suffix in ('.py','.toml'):
            archive.write(path,path.relative_to(root))
    archive.write(root/'explorer/model_api.py','explorer/model_api.py')
    archive.writestr('explorer/__init__.py','')
