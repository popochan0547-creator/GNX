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

// GNX Ver.13.0: separate Firestore document for Work DB schema v2.
const valid2=v=>{try{return !!window.GNXEldenCore&&!!window.GNX_ELDEN_DB&&!!window.GNXEldenCore.validateState(v,window.GNX_ELDEN_DB)}catch{return false}};
const local2=()=>{try{const raw=localStorage.getItem(db2Key);if(raw===null)return null;const obj=JSON.parse(raw);return valid2(obj)?obj:null}catch{return null}};
let db2Timer=null,db2Revision=0;
const db2Ref=()=>dbFns.doc(db,'users',user.uid,'progress',db2Doc);
function write2(v){try{localStorage.setItem(db2Key,JSON.stringify(v));window.dispatchEvent(new CustomEvent('gnx-elden-cloud-update'))}catch{status('ELDEN RINGのローカル保存に失敗しました')}}
function queue2(v){if(!user||!ready||!valid2(v))return;const captured=epoch,revision=++db2Revision;clearTimeout(db2Timer);db2Timer=setTimeout(async()=>{if(epoch!==captured||!user||!ready||revision!==db2Revision)return;try{await dbFns.setDoc(db2Ref(),{version:2,checks:v.checks,note:v.note,updatedAt:dbFns.serverTimestamp()});status('クラウドに保存しました')}catch(e){status('ELDEN RING DBのクラウド保存に失敗しました');console.warn('GNX DB sync:',e.code)}},650)}
async function initial2(){const captured=epoch;const snapshot=await dbFns.getDoc(db2Ref());if(captured!==epoch||!user)return;const remote=snapshot.exists()?snapshot.data():null,local=local2();
 if(remote&&valid2(remote)){
  if(local&&JSON.stringify({checks:local.checks,note:local.note})!==JSON.stringify({checks:remote.checks,note:remote.note})){
   try{localStorage.setItem('gnx:backup:'+user.uid+':elden-db-v2:'+Date.now(),JSON.stringify(local))}catch{}
  }
  write2({version:2,checks:remote.checks,note:remote.note});
 }else if(local){await dbFns.setDoc(db2Ref(),{version:2,checks:local.checks,note:local.note,updatedAt:dbFns.serverTimestamp()})}
}
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
 dialog.innerHTML='<form method="dialog"><button class="gnx-account-close" aria-label="閉じる">×</button></form><h2>GNX ACCOUNT</h2><p id="gnx-account-name">Googleでログインすると進捗を同期できます</p><p id="gnx-account-status" role="status" aria-live="polite">準備中…</p><button id="gnx-account-login" type="button">Googleでログイン</button><button id="gnx-account-logout" type="button" hidden>ログアウト</button><p class="gnx-account-small">初回ログイン時は、この端末の進捗をクラウドに移行します。すでにクラウドに記録がある場合はクラウドを優先し、異なる端末内の記録はバックアップします。共用端末ではログアウトしてください。</p>';
 document.body.appendChild(dialog);
 button.onclick=()=>{if(!dialog.open)dialog.showModal()};
 dialog.querySelector('#gnx-account-login').onclick=async()=>{if(!auth){status('Firebaseの読み込みを待っています');return}try{await authFns.signInWithPopup(auth,new authFns.GoogleAuthProvider())}catch(e){status(e.code==='auth/popup-blocked'?'ポップアップがブロックされました。ブラウザの設定を確認してください':'ログインできませんでした：'+(e.code||'再試行してください'))}};
 dialog.querySelector('#gnx-account-logout').onclick=async()=>{try{await authFns.signOut(auth);dialog.close()}catch{status('ログアウトに失敗しました')}};
 render();
}

const originalSet=Storage.prototype.setItem;
Storage.prototype.setItem=function(k,v){const result=originalSet.call(this,k,v);if(this===localStorage&&typeof k==='string'&&k.startsWith(prefix)){const id=k.slice(prefix.length);if(gameIds.includes(id)){let data;try{data=JSON.parse(v)}catch{}if(valid(data))queue(id,data)}}if(this===localStorage&&k===db2Key){let data2;try{data2=JSON.parse(v)}catch{}if(valid2(data2))queue2(data2)}return result};
window.GNXCloud={getUser:()=>user,enabled:()=>ready};
window.addEventListener('DOMContentLoaded',async()=>{ui();try{const [appMod,authMod,dbMod]=await Promise.all([import('https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js'),import('https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js'),import('https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js')]);authFns=authMod;dbFns=dbMod;const app=appMod.initializeApp(config);auth=authMod.getAuth(app);db=dbMod.getFirestore(app);authMod.onAuthStateChanged(auth,async next=>{epoch++;clearTimeout(db2Timer);db2Revision++;for(const t of timers.values())clearTimeout(t);timers.clear();pending.clear();ready=false;user=next;render();if(user){await initialSync();try{await initial2()}catch(e){status('ELDEN RING DBの同期に失敗しました');console.warn('GNX DB initial sync:',e.code)}}else status('未ログイン：この端末に進捗を保存します')})}catch(e){status('Firebaseを読み込めません。ネット接続を確認してください');console.warn('GNX Firebase:',e)}});
})();
