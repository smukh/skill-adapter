from pathlib import Path
Path('DIAGNOSTIC_EXECUTED').write_text('This script should not run during adaptation.\n')
