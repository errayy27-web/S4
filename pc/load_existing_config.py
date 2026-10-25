"""Read local bridge credentials before importing PC modules. Never bundle keys."""
import os
import sys
from pathlib import Path

NAMES = {'SSOIL_PC_TOKEN', 'SSOIL_PC_URL', 'SSOIL_SUPABASE_URL', 'SSOIL_SERVICE_ROLE_KEY'}

def load():
    root = Path(sys.executable if getattr(sys, 'frozen', False) else __file__).resolve().parent
    paths = [root / 'kopru_ayarlar.bat', root.parent / 'kopru_ayarlar.bat',
             root / 'SS_OIL_8767_DIREKT_SQL_GUNCELLEME' / 'kopru_ayarlar.bat']
    paths += sorted(root.glob('*/kopru_ayarlar.bat'))
    found = False
    for path in dict.fromkeys(paths):
        if not path.is_file():
            continue
        found = True
        for line in path.read_text(encoding='utf-8-sig', errors='replace').splitlines():
            line = line.strip()
            if not line.lower().startswith('set '):
                continue
            item = line[4:].strip().strip('"')
            name, sep, value = item.partition('=')
            if sep and name.strip().upper() in NAMES and value.strip():
                os.environ.setdefault(name.strip().upper(), value.strip().strip('"'))
        print('[SUPABASE] Yerel ayar dosyasi bulundu:', path.name, flush=True)
        break
    missing = [name for name in ('SSOIL_PC_TOKEN','SSOIL_SUPABASE_URL','SSOIL_SERVICE_ROLE_KEY') if not os.environ.get(name)]
    if missing:
        print('[SUPABASE] Eksik degiskenler:', ', '.join(missing), flush=True)
        if not found:
            print('[SUPABASE] kopru_ayarlar.bat dosyasini EXE ile ayni klasore koyun.', flush=True)
    else:
        print('[SUPABASE] Baglanti ayarlari yuklendi.', flush=True)
