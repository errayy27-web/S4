"""Load legacy local bridge settings without publishing secrets in GitHub."""
import os,re,sys
from pathlib import Path
def load():
    root=Path(sys.executable).resolve().parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parent
    candidates=[root/'kopru_ayarlar.bat',root.parent/'kopru_ayarlar.bat',root/'SS_OIL_8767_DIREKT_SQL_GUNCELLEME'/'kopru_ayarlar.bat']
    for path in candidates:
        if not path.is_file():continue
        try:
            raw=path.read_text(encoding='utf-8-sig',errors='replace')
            for line in raw.splitlines():
                m=re.match(r'^\\s*set\\s+"?(SSOIL_(?:PC_TOKEN|SUPABASE_URL|SERVICE_ROLE_KEY))=(.*?)"?\\s*$',line,re.I)
                if m:
                    value=m.group(2).strip().rstrip('"')
                    if value:os.environ.setdefault(m.group(1).upper(),value)
            print('[SUPABASE] Yerel kopru_ayarlar.bat okundu',flush=True)
            return
        except OSError as e:print('[SUPABASE] Ayar okunamadi:',e,flush=True)
    print('[SUPABASE] kopru_ayarlar.bat EXE yaninda bulunamadi',flush=True)
