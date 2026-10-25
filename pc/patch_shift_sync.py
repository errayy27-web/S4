from pathlib import Path
p=Path("pc/vardiya_entegre.py")
s=p.read_text(encoding="utf-8")
old="INSERT INTO vardiya_local(table_name,row_key,payload,pending) VALUES(?,?,?,0) ON CONFLICT(table_name,row_key) DO UPDATE SET payload=excluded.payload WHERE vardiya_local.pending=0"
new="""INSERT INTO vardiya_local(table_name,row_key,payload,pending) VALUES(?,?,?,0)
ON CONFLICT(table_name,row_key) DO UPDATE SET
payload=excluded.payload,
pending=CASE WHEN COALESCE(CAST(json_extract(excluded.payload,'$.revision') AS INTEGER),0)>COALESCE(CAST(json_extract(vardiya_local.payload,'$.revision') AS INTEGER),0) THEN 0 ELSE vardiya_local.pending END
WHERE vardiya_local.pending=0
OR COALESCE(CAST(json_extract(excluded.payload,'$.revision') AS INTEGER),0)>COALESCE(CAST(json_extract(vardiya_local.payload,'$.revision') AS INTEGER),0)"""
assert s.count(old)==1, "Expected shift cloud-pull SQL not found; refusing unsafe build"
s=s.replace("'"+old+"'", "'''"+new+"'''")
import ast
ast.parse(s, filename=str(p))
p.write_text(s,encoding="utf-8")
print("Cloud pull accepts newer phone revisions even if stale local pending flag remains")
