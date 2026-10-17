// A simulated folder for headless tests of Point First.
// Kept in localStorage, so it is shared by every tab in the browser context and survives a reload,
// like a real folder on disk. Handles look paths up on every call, as real handles do.
// window.__fs lets a test act as the outside world: Obsidian edits, deletes, moves, sync touches,
// permission loss, failing writes.
(()=>{
  const KEY='__mockfs';
  const load=()=>{try{return JSON.parse(localStorage.getItem(KEY))||{files:{},dirs:[''],perm:'granted',failWrites:false,clock:0}}catch(_){return{files:{},dirs:[''],perm:'granted',failWrites:false,clock:0}}};
  const save=s=>localStorage.setItem(KEY,JSON.stringify(s));
  // A clock that always moves forward, so two writes never share a timestamp.
  const tick=s=>{const t=Math.max(Date.now(),(s.clock||0)+1);s.clock=t;return t};
  const join=(a,b)=>a?a+'/'+b:b;
  const deny=s=>{if(s.perm!=='granted')throw new DOMException('Permission needed','NotAllowedError')};
  const dirExists=(s,p)=>s.dirs.includes(p);
  class FH{constructor(path){this.kind='file';this.path=path;this.name=path.split('/').pop()}
    async getFile(){const s=load();deny(s);const f=s.files[this.path];if(!f)throw new DOMException('A requested file or directory could not be found','NotFoundError');return new File([f.text],this.name,{lastModified:f.mtime})}
    async createWritable(){const s=load();deny(s);if(!s.files[this.path])throw new DOMException('A requested file or directory could not be found','NotFoundError');
      const self=this;let buf='';
      return{async write(d){if(typeof d==='string')buf+=d;else if(d instanceof Blob)buf+=await d.text();else if(d&&d.type==='write')buf+=typeof d.data==='string'?d.data:await new Blob([d.data]).text();else buf+=await new Blob([d]).text()},
        async truncate(){},async seek(){},
        async close(){const s=load();deny(s);if(s.failWrites)throw new DOMException('The disk is full','QuotaExceededError');
          if(!s.files[self.path])throw new DOMException('A requested file or directory could not be found','NotFoundError');
          s.files[self.path]={text:buf,mtime:tick(s)};save(s)},
        async abort(){}}}
    async isSameEntry(o){return !!o&&o.path===this.path&&o.kind==='file'}
    async queryPermission(){return load().perm}async requestPermission(){const s=load();if(s.perm==='prompt'&&!s.denyRequest){s.perm='granted';save(s)}return load().perm}}
  class DH{constructor(path){this.kind='directory';this.path=path;this.name=path?path.split('/').pop():'Essays'}
    _kids(s){const out=new Map(),pre=this.path?this.path+'/':'';
      for(const p of Object.keys(s.files))if(p.startsWith(pre)){const rest=p.slice(pre.length);if(!rest.includes('/'))out.set(rest,new FH(p))}
      for(const d of s.dirs)if(d&&d.startsWith(pre)){const rest=d.slice(pre.length);if(rest&&!rest.includes('/'))out.set(rest,new DH(d))}
      return out}
    async *entries(){const s=load();deny(s);if(!dirExists(s,this.path))throw new DOMException('A requested file or directory could not be found','NotFoundError');for(const kv of this._kids(s))yield kv}
    async *values(){for await(const [,v] of this.entries())yield v}
    async *keys(){for await(const [k] of this.entries())yield k}
    [Symbol.asyncIterator](){return this.entries()}
    async getDirectoryHandle(n,o){const s=load();deny(s);if(!dirExists(s,this.path))throw new DOMException('nf','NotFoundError');const p=join(this.path,n);
      if(s.files[p])throw new DOMException('t','TypeMismatchError');
      if(!dirExists(s,p)){if(!(o&&o.create))throw new DOMException('A requested file or directory could not be found','NotFoundError');s.dirs.push(p);save(s)}return new DH(p)}
    async getFileHandle(n,o){const s=load();deny(s);if(!dirExists(s,this.path))throw new DOMException('nf','NotFoundError');const p=join(this.path,n);
      if(dirExists(s,p))throw new DOMException('t','TypeMismatchError');
      if(!s.files[p]){if(!(o&&o.create))throw new DOMException('A requested file or directory could not be found','NotFoundError');s.files[p]={text:'',mtime:tick(s)};save(s)}return new FH(p)}
    async removeEntry(n,o){const s=load();deny(s);const p=join(this.path,n);
      if(s.files[p]){delete s.files[p];save(s);return}
      if(dirExists(s,p)){const pre=p+'/';const inside=Object.keys(s.files).some(k=>k.startsWith(pre))||s.dirs.some(d=>d.startsWith(pre));
        if(inside&&!(o&&o.recursive))throw new DOMException('not empty','InvalidModificationError');
        for(const k of Object.keys(s.files))if(k.startsWith(pre))delete s.files[k];s.dirs=s.dirs.filter(d=>d!==p&&!d.startsWith(pre));save(s);return}
      throw new DOMException('nf','NotFoundError')}
    async isSameEntry(o){return !!o&&o.path===this.path&&o.kind==='directory'}
    async resolve(h){return h.path.startsWith(this.path)?h.path.split('/'):null}
    async queryPermission(){return load().perm}async requestPermission(){const s=load();if(s.perm==='prompt'&&!s.denyRequest){s.perm='granted';save(s)}return load().perm}}

  // The folder handle cannot go into IndexedDB as a real handle would. Store a marker, read back a handle.
  const origPut=IDBObjectStore.prototype.put;
  IDBObjectStore.prototype.put=function(v,k){if(v instanceof DH)v='__mockdir__';return origPut.call(this,v,k)};
  const rd=Object.getOwnPropertyDescriptor(IDBRequest.prototype,'result');
  Object.defineProperty(IDBRequest.prototype,'result',{get(){const v=rd.get.call(this);return v==='__mockdir__'?new DH(''):v},configurable:true});

  window.showDirectoryPicker=async()=>{const s=load();if(!s.dirs.includes(''))s.dirs.push('');s.perm='granted';save(s);return new DH('')};
  // The outside world.
  window.__fs={
    reset(){localStorage.removeItem(KEY)},
    write(path,text){const s=load();const parts=path.split('/');for(let i=1;i<parts.length;i++){const d=parts.slice(0,i).join('/');if(!s.dirs.includes(d))s.dirs.push(d)}s.files[path]={text,mtime:tick(s)};save(s)},
    read(path){const f=load().files[path];return f?f.text:null},
    mtime(path){const f=load().files[path];return f?f.mtime:null},
    del(path){const s=load();delete s.files[path];save(s)},
    mv(a,b){const s=load();const f=s.files[a];if(!f)return;delete s.files[a];const parts=b.split('/');for(let i=1;i<parts.length;i++){const d=parts.slice(0,i).join('/');if(!s.dirs.includes(d))s.dirs.push(d)}s.files[b]=f;save(s)},
    touch(path){const s=load();const f=s.files[path];if(f){f.mtime=tick(s);save(s)}},
    rmdir(path){const s=load();const pre=path?path+'/':'';for(const k of Object.keys(s.files))if(!path||k.startsWith(pre))delete s.files[k];s.dirs=path?s.dirs.filter(d=>d!==path&&!d.startsWith(pre)):[];save(s)},
    set perm(v){const s=load();s.perm=v;save(s)},get perm(){return load().perm},
    set denyRequest(v){const s=load();s.denyRequest=v;save(s)},
    set failWrites(v){const s=load();s.failWrites=v;save(s)},
    list(){return Object.keys(load().files).sort()},
  };
  window.__seed=(name,text)=>window.__fs.write(name,text);
})();
