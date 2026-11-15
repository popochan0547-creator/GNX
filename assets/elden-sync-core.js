/* GNX 14: pure three-way field merge. No Firebase dependency. */
(function(f){const a=f();if(typeof module==='object'&&module.exports)module.exports=a;else window.GNXEldenSync=a;})(function(){'use strict';
const safeId=k=>typeof k==='string'&&/^[a-zA-Z0-9][a-zA-Z0-9:_-]{0,159}$/.test(k)&&!['constructor','prototype','__proto__'].includes(k);
const state=v=>v&&v.version===2&&v.checks&&typeof v.checks==='object'&&!Array.isArray(v.checks)&&Object.keys(v.checks).length<=4096&&Object.entries(v.checks).every(([k,x])=>safeId(k)&&typeof x==='boolean')&&typeof v.note==='string'&&v.note.length<=10000;
const copy=v=>({version:2,checks:{...v.checks},note:v.note});
const blank=()=>({version:2,checks:{},note:''});
function diff(before,after){if(!state(before)||!state(after))throw Error('invalid state');const checks={};for(const k of new Set([...Object.keys(before.checks),...Object.keys(after.checks)])){const a=before.checks[k]===true,b=after.checks[k]===true;if(a!==b)checks[k]={before:a,value:b};}return {version:1,checks,note:before.note!==after.note?{before:before.note,value:after.note}:null};}
function validPatch(p){return p&&p.version===1&&p.checks&&typeof p.checks==='object'&&!Array.isArray(p.checks)&&Object.keys(p.checks).length<=4096&&Object.entries(p.checks).every(([k,v])=>safeId(k)&&v&&typeof v.before==='boolean'&&typeof v.value==='boolean')&&(p.note===null||p.note&&typeof p.note.before==='string'&&typeof p.note.value==='string'&&p.note.before.length<=10000&&p.note.value.length<=10000);}
function combine(a,b){if(!validPatch(a)||!validPatch(b))throw Error('invalid patch');const checks={...a.checks};for(const [k,v]of Object.entries(b.checks)){checks[k]={before:checks[k]?checks[k].before:v.before,value:v.value};if(checks[k].before===checks[k].value)delete checks[k];}let note=b.note?{before:a.note?a.note.before:b.note.before,value:b.note.value}:a.note;if(note&&note.before===note.value)note=null;return {version:1,checks,note};}
function merge(remote,patch){if(!state(remote)||!validPatch(patch))throw Error('invalid merge');const value=copy(remote),conflicts=[];for(const [k,v]of Object.entries(patch.checks)){const current=value.checks[k]===true;if(current!==v.before&&current!==v.value)conflicts.push(k);else value.checks[k]=v.value;}if(patch.note){if(value.note!==patch.note.before&&value.note!==patch.note.value)conflicts.push('note');else value.note=patch.note.value;}return {value,conflicts};}
const emptyPatch=()=>({version:1,checks:{},note:null});
const hasChanges=p=>Object.keys(p.checks).length>0||p.note!==null;
return {safeId,state,copy,blank,diff,validPatch,combine,merge,emptyPatch,hasChanges};
});
