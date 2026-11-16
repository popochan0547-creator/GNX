/* Shared NPC navigation rules. Metadata uses existing version-2 boolean checks. */
(function(factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else window.GNXNPC=api})(function(){'use strict';
const key=(r,id)=>'npc-plan:'+r.id+':'+id;
function selection(r,state){const selected=r.options.filter(o=>state.checks[key(r,o.id)]===true);return {value:selected.length===1?selected[0].id:null,conflict:selected.length>1}}
function choose(r,state,id){if(id!==null&&!r.options.some(x=>x.id===id))throw Error('Unknown route option');return {...state,checks:{...state.checks,...Object.fromEntries(r.options.map(o=>[key(r,o.id),id===o.id]))}}}
function plan(r,state){const selected=selection(r,state),stages=r.stages.filter(s=>!s.branch||s.branch===selected.value);const done=stages.filter(s=>state.checks[s.taskId]===true).length;const next=r.options.length&&!selected.value&&r.stages[0]?.branch?null:stages.find(s=>state.checks[s.taskId]!==true)||null;return {selection:selected,stages,done,total:stages.length,percent:stages.length?Math.round(done/stages.length*100):0,next,needsChoice:r.options.length>0&&!selected.value,complete:done===stages.length&&!(r.options.length&&!selected.value)}}
function frenzy(state){const receive=state.checks['npc17-hyetta:receive']===true,cure=state.checks['npc17-hyetta:cure']===true;return cure?'recorded-cured':receive?'recorded-active':'unknown'}
function cautions(r,state){return r.id==='hyetta'&&state.checks['npc-plan:hyetta:cure']===true&&state.checks['npc-plan:millicent:oppose']===true?['今周にミケラの針を取得する計画なら、ミリセントは協力側へ。過去周の所持チェックだけで今周の条件は保証されません。']:[]}
return {key,selection,choose,plan,frenzy,cautions};});
