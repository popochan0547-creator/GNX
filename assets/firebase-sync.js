/* GNX 12.0 - Firebase authentication and progress sync. No analytics data sent here. */
(()=>{'use strict';
const config={apiKey:'AIzaSyBOo_fJ-oD7J95mzkV7oMDuksg5jSZ4Kes',authDomain:'gnx-game-nexus.firebaseapp.com',projectId:'gnx-game-nexus',storageBucket:'gnx-game-nexus.firebasestorage.app',messagingSenderId:'273909954850',appId:'1:273909954850:web:cfd790f5bf584b22608d7b',measurementId:'G-W1BV60F8N2'};
const prefix='gnx:guides:v1:';
const db2Key='gnx:elden:progress:v2',db2Doc='elden-db-v2';

const gameIds=['elden-ring','monster-hunter-wilds','apex-legends','valorant'];
let auth,db,authFns,dbFns,user=null,ready=false,epoch=0;
const pending=new Map(),timers=new Map();
const status=(s)=>{const e=document.getElementById('gnx-account-status');if(e)e.textContent=s};
const valid=v=>v&&v.version===1&&v.checks&&typeof v.checks==='object'&&!Array.isArray(v.checks)&&Object.values(v.checks).every(x=>typeof x==='boolean')&&typeof v.note==='string'&&v.note.length<=10000;
const getLocal=id=>{try{const v=JSON.parse(localStorage.getItem(prefix+id));return valid(v)?v:null}catch{return null}};
const setLocal=(id,v)=>{try{localStorage.setItem(prefix+id,JSON.stringify(v));window.dispatchEvent(new CustomEvent('gnx-cloud-progress',{detail:{game:id}}))}catch{status('ブラウザへの保存に失敗しました')}};
const ref=id=>dbFns.doc(db,'users',user.uid,'progress',id);
function queue(id,v){if(!user||!ready||!valid(v))return;pending.set(id,structuredClone(v));clearTimeout(timers.get(id));const captured=epoch;timers.set(id,setTimeout(async()=>{if(captured!==epoch||!user||!ready)return;const val=pending.get(id);pending.delete(id);if(!val)return;try{await dbFns.setDoc(ref(id),{version:1,checks:val.checks,note:val.note,updatedAt:dbFns.serverTimestamp()});status('クラウドに保存しました')}catch(e){status('クラウド保存に失敗しました。ネット接続・Firestoreルールを確認してください');console.warn('GNX sync:',e.code)}},650))}
async function initialSync(){const captured=epoch;ready=false;status('クラウドの記録を確認中…');try{for(const id of gameIds){if(captured!==epoch||!user)return;const snapshot=await dbFns.getDoc(ref(id));if(captured!==epoch||!user)return;const remote=snapshot.exists()?snapshot.data():null;const local=getLocal(id);if(remote&&valid(remote)){
 // Existing cloud data is authoritative on sign-in; never silently overwrite it.
 if(local&&JSON.stringify({checks:local.checks,note:local.note})!==JSON.stringify({checks:remote.checks,note:remote.note})){
   const backupKey='gnx:backup:'+user.uid+':'+id+':'+Date.now();try{localStorage.setItem(backupKey,JSON.stringify(local))}catch{}
 }
 setLocal(id,{version:1,checks:remote.checks,note:remote.note});
}else if(local){await dbFns.setDoc(ref(id),{...local,updatedAt:dbFns.serverTimestamp()})}
}if(captured===epoch){ready=true;status('同期が有効です。保存した進捗は他の端末にも反映されます')}}catch(e){ready=false;status('同期できません。Firestoreのルールと接続を確認してください');console.warn('GNX initial sync:',e.code)}}

// GNX 14.0: retain the existing document; merge only local changes in a transaction.
const S=window.GNXEldenSync;
const valid2=v=>{try{return !!S&&S.state(v)&&!!window.GNXEldenCore.validateState(v,window.GNX_ELDEN_DB)}catch{return false}};
const local2=()=>{try{const v=JSON.parse(localStorage.getItem(db2Key)||'null');return valid2(v)?v:null}catch{return null}};
let db2Timer=null,db2Revision=0,db2Unsubscribe=null,remoteApplying=false,db2Dirty=false,db2Ready=false,db2Observed=null,db2Patch=null,db2Sending=false,db2InFlight=null,db2Conflict=false,db2Flight=0;
const diag={auth:'未確認',firestore:'未確認',dataset:'未確認',remoteChecks:'-',localChecks:'-',ui:'未確認',lastError:'なし'};
const count2=v=>v&&v.checks?Object.values(v.checks).filter(x=>x===true).length:0;
function showDiag(){const e=document.getElementById('gnx-sync-diagnostics');if(e)e.textContent=['ログイン: '+diag.auth,'攻略データ: '+diag.dataset,'Firestore: '+diag.firestore,'クラウド達成数: '+diag.remoteChecks,'端末達成数: '+diag.localChecks,'画面更新: '+diag.ui,'直近エラー: '+diag.lastError].join('\n')}
function recordDiag(k,v){diag[k]=String(v);showDiag()}
const db2Ref=()=>dbFns.doc(db,'users',user.uid,'progress',db2Doc);
const outboxKey=()=>user?'gnx:sync14:'+user.uid+':elden-db-v2:outbox':null;
function protect(v,tag='snapshot'){if(!v)return true;try{originalSet.call(localStorage,'gnx:backup:'+(user?user.uid:'guest')+':elden-db-v2:'+Date.now()+':'+tag,JSON.stringify(v));return true}catch{recordDiag('lastError','バックアップを保存できません');return false}}
function rememberPatch(){if(!user||!db2Patch)return;try{originalSet.call(localStorage,outboxKey(),JSON.stringify(db2InFlight?S.combine(db2InFlight,db2Patch):db2Patch))}catch{recordDiag('lastError','未送信変更を端末に保存できません。JSONを書き出してください')}}
function readPatch(){try{const raw=JSON.parse(localStorage.getItem(outboxKey())||'null');return S.validPatch(raw)?raw:S.emptyPatch()}catch{return S.emptyPatch()}}
function write2(v){try{remoteApplying=true;originalSet.call(localStorage,db2Key,JSON.stringify(v));db2Observed=S.copy(v);recordDiag('localChecks',count2(v));window.dispatchEvent(new CustomEvent('gnx-elden-cloud-update'));recordDiag('ui','更新イベント送信済み')}catch(e){recordDiag('lastError','端末保存: '+(e.code||e.message));status('ELDEN RINGのローカル保存に失敗しました')}finally{remoteApplying=false}}
function queue2(v){if(remoteApplying||!S||!user||!valid2(v))return;const before=db2Observed||S.blank();db2Observed=S.copy(v);db2Patch=S.combine(db2Patch||S.emptyPatch(),S.diff(before,v));db2Dirty=S.hasChanges(db2Patch);recordDiag('localChecks',count2(v));rememberPatch();if(db2Ready&&ready&&!db2Conflict)schedule2();}
function schedule2(){clearTimeout(db2Timer);const captured=epoch;db2Timer=setTimeout(()=>{if(captured===epoch)flush2()},650)}
async function flush2(){if(!user||!ready||!db2Ready||db2Sending||db2Conflict||!S.hasChanges(db2Patch||S.emptyPatch()))return;
 const captured=epoch,owner=user.uid,target=db2Ref(),flight=++db2Flight,patch=structuredClone(db2Patch);db2Patch=S.emptyPatch();db2InFlight=patch;db2Sending=true;
 // Keep the in-flight patch in the durable outbox until the server acknowledges it.
 let result;
 try{result=await dbFns.runTransaction(db,async tx=>{const snap=await tx.get(target);if(captured!==epoch||!user||user.uid!==owner)throw Error('account-changed');const raw=snap.exists()?snap.data():null,remote=raw?{version:raw.version,checks:raw.checks,note:raw.note}:S.blank();if(!valid2(remote))throw Error('invalid-cloud-state');const merged=S.merge(remote,patch);if(merged.conflicts.length)return {conflict:true,remote};tx.set(target,{version:2,checks:merged.value.checks,note:merged.value.note,updatedAt:dbFns.serverTimestamp()},{merge:true});return {conflict:false,value:merged.value};});
 if(captured!==epoch||!user||user.uid!==owner)return;
 if(result.conflict){db2Patch=S.combine(patch,db2Patch);db2Conflict=true;protect(local2(),'local-conflict');protect(result.remote,'cloud-conflict');recordDiag('lastError','メモの同時編集が競合。クラウドは上書きしていません');status('メモが競合しました。JSONで記録を保管し、同期診断から解決してください');conflictUI(result.remote);}
 else{db2Dirty=S.hasChanges(db2Patch);recordDiag('firestore','差分統合保存成功');recordDiag('remoteChecks',count2(result.value));if(!db2Dirty)write2(result.value);status('変更項目をクラウドへ統合しました');}
 }catch(e){if(captured===epoch){db2Patch=S.combine(patch,db2Patch);db2Dirty=true;recordDiag('lastError','差分保存: '+(e.code||e.message));status('クラウドに未送信の変更があります。記録は端末に保持しています');}}
 finally{if(captured===epoch&&flight===db2Flight){db2Sending=false;db2InFlight=null;rememberPatch();if(result&&!result.conflict&&S.hasChanges(db2Patch))schedule2();}}
}
function conflictUI(remote){let e=document.getElementById('gnx-sync-conflict');if(!e){e=document.createElement('div');e.id='gnx-sync-conflict';document.getElementById('gnx-account-dialog')?.appendChild(e)}e.replaceChildren();const p=document.createElement('p');p.textContent='同じメモが別端末で編集されました。両方の記録は端末にバックアップしています。';e.append(p);
 async function resolve(useLocal,button){const captured=epoch,owner=user?.uid;if(!owner)return;button.disabled=true;try{const snap=await dbFns.getDoc(db2Ref());if(captured!==epoch||!user||user.uid!==owner)return;const raw=snap.exists()?snap.data():null,latest=raw?{version:raw.version,checks:raw.checks,note:raw.note}:null,current=local2();if(!valid2(latest)||!current)throw Error('invalid-state');if(!protect(current,'before-note-resolution-local')||!protect(latest,'before-note-resolution-cloud'))return;db2Patch.note=useLocal?{before:latest.note,value:current.note}:null;const merged=S.merge(latest,db2Patch);if(merged.conflicts.length)throw Error('note-conflict');write2(merged.value);db2Conflict=false;db2Dirty=S.hasChanges(db2Patch);e.remove();rememberPatch();schedule2();status('メモの選択を反映しました。変更がある場合はクラウドへ統合します');}catch(err){recordDiag('lastError','競合解決: '+(err.code||err.message));status('競合の解決に失敗しました。記録は保持しています');}finally{button.disabled=false}}
 const useRemote=document.createElement('button');useRemote.type='button';useRemote.textContent='メモはクラウドの内容を使う';useRemote.onclick=()=>resolve(false,useRemote);e.append(useRemote);const useLocal=document.createElement('button');useLocal.type='button';useLocal.textContent='メモはこの端末の内容を使う';useLocal.onclick=()=>resolve(true,useLocal);e.append(useLocal);}
async function initial2(){
 const captured=epoch;db2Ready=false;recordDiag('dataset',S&&window.GNX_ELDEN_DB?'読み込み済み':'未読み込み');if(!S||!window.GNX_ELDEN_DB)return;
 const storedRaw=localStorage.getItem(db2Key);if(storedRaw!==null&&!local2()){recordDiag('lastError','端末の保存形式が不正。元データを保持して同期停止');status('端末の元データを保護中です。JSON退避後に復元してください');return;}
 db2Observed=local2()||S.blank();db2Patch=S.combine(readPatch(),db2Patch||S.emptyPatch());
 const snapshot=await dbFns.getDoc(db2Ref());if(captured!==epoch||!user)return;const raw=snapshot.exists()?snapshot.data():null,remote=raw?{version:raw.version,checks:raw.checks,note:raw.note}:null,local=local2();
 recordDiag('firestore',snapshot.exists()?'elden-db-v2 取得成功':'elden-db-v2 未作成');recordDiag('remoteChecks',count2(remote));recordDiag('localChecks',count2(local));
 if(raw&&!valid2(remote)){recordDiag('lastError','クラウド形式が不正。上書きを停止');status('攻略DBのクラウドを保護しています。データ形式を確認してください');return;}
 if(remote){if(local&&JSON.stringify(local)!==JSON.stringify(remote)&&!protect(local,'before-cloud-load')){status('バックアップ保存に失敗したためクラウド取り込みを停止しました');return;}const merged=S.merge(remote,db2Patch);if(merged.conflicts.length){db2Conflict=true;protect(remote,'cloud-conflict');conflictUI(remote);status('未送信メモとクラウドのメモが競合しています');}else write2(merged.value);}
 else if(local){db2Patch=S.combine(S.diff(S.blank(),local),db2Patch);}
 db2Ready=true;db2Dirty=S.hasChanges(db2Patch);rememberPatch();
 if(db2Unsubscribe)db2Unsubscribe();db2Unsubscribe=dbFns.onSnapshot(db2Ref(),snap=>{if(captured!==epoch||!user||snap.metadata.hasPendingWrites||db2Sending||db2Conflict)return;const raw=snap.exists()?snap.data():null;if(!raw){recordDiag('firestore','クラウド文書なし。端末の記録は保持');return;}const value={version:raw.version,checks:raw.checks,note:raw.note};if(!valid2(value)){recordDiag('lastError','受信形式が不正。端末は保持');return;}recordDiag('remoteChecks',count2(value));const merged=S.merge(value,db2Patch);if(merged.conflicts.length){db2Conflict=true;protect(local2(),'local-conflict');protect(value,'cloud-conflict');conflictUI(value);status('メモが競合しました。同期診断で解決してください');return;}if(JSON.stringify(local2())!==JSON.stringify(merged.value)){if(!protect(local2(),'before-receive'))return;write2(merged.value)}recordDiag('firestore','リアルタイム受信成功');},e=>{recordDiag('lastError','監視: '+(e.code||e.message));status('同期監視が停止しました。端末の記録は保持しています')});
 if(!db2Conflict&&db2Dirty)schedule2();
}
window.addEventListener('online',()=>{if(user&&db2Ready&&!db2Conflict)schedule2()});

function render(){
 const b=document.getElementById('gnx-account-button');if(!b)return;
 const label=user?(user.displayName||user.email||'ログイン中')+' ▾':'ログイン';
 b.textContent=label;b.title=user?(user.email||'アカウント'):'Googleでログイン';
 b.setAttribute('aria-label',user?'アカウント：'+(user.displayName||user.email||'ログイン中'):'ログイン');
 document.getElementById('gnx-account-logout').hidden=!user;
 document.getElementById('gnx-account-login').hidden=!!user;
 document.getElementById('gnx-account-name').textContent=user?'ログイン中：'+(user.displayName||user.email||'Googleアカウント'):'ログインすると進捗をPC・スマホで同期できます';
}
function ui(){
 const button=document.getElementById('gnx-account-button');if(!button)return;
 const dialog=document.createElement('dialog');dialog.id='gnx-account-dialog';dialog.setAttribute('aria-label','GNXアカウント');
 dialog.innerHTML='<form method="dialog"><button class="gnx-account-close" aria-label="閉じる">×</button></form><h2>GNX ACCOUNT</h2><p id="gnx-account-name">Googleでログインすると進捗を同期できます</p><p id="gnx-account-status" role="status" aria-live="polite">準備中…</p><details class="gnx-sync-details"><summary>攻略DBの同期診断</summary><pre id="gnx-sync-diagnostics">確認中…</pre><button id="gnx-sync-refresh" type="button">クラウドから再取得</button></details><button id="gnx-account-login" type="button">Googleでログイン</button><button id="gnx-account-logout" type="button" hidden>ログアウト</button><p class="gnx-account-small">初回ログイン時は、この端末の進捗をクラウドに移行します。すでにクラウドに記録がある場合はクラウドを優先し、異なる端末内の記録はバックアップします。共用端末ではログアウトしてください。</p>';
 document.body.appendChild(dialog);
 button.onclick=()=>{if(!dialog.open)dialog.showModal()};
 dialog.querySelector('#gnx-account-login').onclick=async()=>{if(!auth){status('Firebaseの読み込みを待っています');return}try{await authFns.signInWithPopup(auth,new authFns.GoogleAuthProvider())}catch(e){status(e.code==='auth/popup-blocked'?'ポップアップがブロックされました。ブラウザの設定を確認してください':'ログインできませんでした：'+(e.code||'再試行してください'))}};
 dialog.querySelector('#gnx-account-logout').onclick=async()=>{try{await authFns.signOut(auth);dialog.close()}catch{status('ログアウトに失敗しました')}};
 dialog.querySelector('#gnx-sync-refresh').onclick=async()=>{if(!user||!db){status('ログインしてから実行してください');return}try{if(db2Dirty||db2Sending||db2Conflict){await flush2();status('未送信または競合中の記録を優先して保護しています')}else{await initial2();status('攻略DBのクラウドを再確認しました')}}catch(e){recordDiag('lastError','再取得: '+(e.code||e.message));status('再取得に失敗しました')}};render();showDiag();
}

const originalSet=Storage.prototype.setItem;
Storage.prototype.setItem=function(k,v){const result=originalSet.call(this,k,v);if(this===localStorage&&typeof k==='string'&&k.startsWith(prefix)){const id=k.slice(prefix.length);if(gameIds.includes(id)){let data;try{data=JSON.parse(v)}catch{}if(valid(data))queue(id,data)}}if(this===localStorage&&k===db2Key){let data2;try{data2=JSON.parse(v)}catch{}if(valid2(data2))queue2(data2)}return result};
window.GNXCloud={getUser:()=>user,enabled:()=>ready};
window.addEventListener('DOMContentLoaded',async()=>{ui();try{const [appMod,authMod,dbMod]=await Promise.all([import('https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js'),import('https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js'),import('https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js')]);authFns=authMod;dbFns=dbMod;const app=appMod.initializeApp(config);auth=authMod.getAuth(app);db=dbMod.getFirestore(app);authMod.onAuthStateChanged(auth,async next=>{if(db2Unsubscribe){db2Unsubscribe();db2Unsubscribe=null}db2Dirty=false;db2Ready=false;db2Conflict=false;db2Observed=null;db2Patch=null;db2Sending=false;db2InFlight=null;db2Flight++;document.getElementById('gnx-sync-conflict')?.remove();epoch++;clearTimeout(db2Timer);db2Revision++;for(const t of timers.values())clearTimeout(t);timers.clear();pending.clear();ready=false;user=next;recordDiag('auth',user?'ログイン中':'未ログイン');render();if(user){await initialSync();try{await initial2()}catch(e){recordDiag('lastError','初回取得: '+(e.code||e.message));status('ELDEN RING DBの同期に失敗しました');console.warn('GNX DB initial sync:',e.code)}}else status('未ログイン：この端末に進捗を保存します')})}catch(e){recordDiag('lastError','Firebase: '+(e.code||e.message));status('Firebaseを読み込めません。ネット接続を確認してください');console.warn('GNX Firebase:',e)}});
})();
