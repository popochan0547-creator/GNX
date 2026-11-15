/* Pure domain logic, shared by the UI and Node tests. No browser dependencies. */
(function(factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else window.GNXEldenCore=api;})(function(){'use strict';
const normalize=s=>String(s).normalize('NFKC').toLowerCase().replace(/[ァ-ヶ]/g,c=>String.fromCharCode(c.charCodeAt(0)-96)).trim();
const tasks=db=>db.entries.flatMap(e=>e.tasks.map(t=>({...t,entryId:e.id,category:e.category})));
const empty=()=>({version:2,checks:{},note:''});
const plain=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
function validateState(v,db){if(!plain(v)||v.version!==2||Object.keys(v).some(k=>!['version','checks','note'].includes(k))||!plain(v.checks)||typeof v.note!=='string'||v.note.length>10000)throw Error('保存データの形式が正しくありません。');const ids=new Set(tasks(db).map(x=>x.id));for(const [id,val]of Object.entries(v.checks)){if(!ids.has(id)||typeof val!=='boolean')throw Error('未対応の項目IDまたは値が含まれています。');}return {version:2,checks:{...v.checks},note:v.note};}
function progress(entries,state){const a=entries.flatMap(x=>x.tasks),done=a.filter(x=>state.checks[x.id]===true).length;return {done,total:a.length,percent:a.length?Math.round(done/a.length*100):0};}
function entryStatus(e,s){const p=progress([e],s);return p.done===0?'todo':p.done===p.total?'done':'partial';}
function search(db,filters,state){const terms=normalize(filters.q||'').split(/\s+/).filter(Boolean);return db.entries.filter(e=>(!filters.category||filters.category==='all'||e.category===filters.category)&&(!filters.region||filters.region==='all'||e.regions.includes(filters.region))&&(!filters.status||filters.status==='all'||entryStatus(e,state)===filters.status)&&terms.every(t=>normalize([e.name,...e.aliases,e.location,e.summary,...e.regions.map(id=>db.regions.find(r=>r.id===id)?.name||''),...e.facts.map(x=>x.value)].join(' ')).includes(t)));}
function backup(state,db){return {format:'gnx-elden-progress',game:'elden-ring',schemaVersion:2,datasetVersion:db.datasetVersion,createdAt:new Date().toISOString(),state:validateState(state,db)};}
function restore(raw,db){if(typeof raw!=='string'||raw.length>200000)throw Error('ファイルのサイズが上限を超えています。');let v;try{v=JSON.parse(raw)}catch{throw Error('JSONとして読み込めません。');}if(!plain(v)||v.format!=='gnx-elden-progress'||v.game!=='elden-ring'||v.schemaVersion!==2||typeof v.datasetVersion!=='string')throw Error('ELDEN RING DB用のバックアップではありません。Ver.11.0の仮チェック用JSONは旧画面で読み込めます。');return validateState(v.state,db);}
return {normalize,tasks,empty,validateState,progress,entryStatus,search,backup,restore};
});
