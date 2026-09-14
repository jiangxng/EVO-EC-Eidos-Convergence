from __future__ import annotations
from pathlib import Path
import json, zipfile, hashlib, shutil
from .util import now

def sha256(path:Path):
    h=hashlib.sha256();
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

class FunctionPackManager:
    def backup(self, source_dir, out_file):
        src=Path(source_dir); out=Path(out_file); out.parent.mkdir(parents=True,exist_ok=True)
        manifest=json.loads((src/'manifest.json').read_text(encoding='utf-8'))
        files=[]
        for p in sorted(src.rglob('*')):
            if p.is_file(): files.append({"path":p.relative_to(src).as_posix(),"sha256":sha256(p)})
        envelope={"backupFormat":"ec-function-pack-backup/0.1.0","createdAt":now(),"manifest":manifest,"checksums":files}
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(src.rglob('*')):
                if p.is_file(): z.write(p,arcname='payload/'+p.relative_to(src).as_posix())
            z.writestr('BACKUP.json',json.dumps(envelope,ensure_ascii=False,indent=2))
        return out
    def verify(self, pack_file):
        p=Path(pack_file)
        with zipfile.ZipFile(p) as z:
            env=json.loads(z.read('BACKUP.json'))
            bad=[]
            for item in env['checksums']:
                got=hashlib.sha256(z.read('payload/'+item['path'])).hexdigest()
                if got!=item['sha256']: bad.append(item['path'])
            return {"ok":not bad,"bad":bad,"manifest":env['manifest']}
    def install(self, pack_file, install_root):
        check=self.verify(pack_file)
        if not check['ok']: raise ValueError(f"pack checksum failure: {check['bad']}")
        m=check['manifest']; target=Path(install_root)/m['packId']/m['version']
        if target.exists(): shutil.rmtree(target)
        target.mkdir(parents=True)
        with zipfile.ZipFile(pack_file) as z:
            for n in z.namelist():
                if n.startswith('payload/') and not n.endswith('/'):
                    rel=n[len('payload/'):]; out=target/rel; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(z.read(n))
        current=target.parent/'CURRENT'; previous=current.read_text().strip() if current.exists() else None
        (target.parent/'PREVIOUS').write_text(previous or '',encoding='utf-8')
        current.write_text(m['version'],encoding='utf-8')
        return {"installed":str(target),"previous":previous,"current":m['version']}
    def rollback(self, pack_id, install_root):
        base=Path(install_root)/pack_id; prev=(base/'PREVIOUS').read_text(encoding='utf-8').strip() if (base/'PREVIOUS').exists() else ''
        if not prev: return {"ok":False,"reason":"no previous version"}
        (base/'CURRENT').write_text(prev,encoding='utf-8'); return {"ok":True,"current":prev}
