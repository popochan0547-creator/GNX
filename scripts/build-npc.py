import pathlib,runpy,json,html,csv,io
R=pathlib.Path(__file__).resolve().parents[1];g=runpy.run_path(str(R/'scripts/build-pages.py'));db=g['db'];H=g['H'];body='<p class="kicker">BASE GAME / NPC JOURNEYS</p><h1>NPCイベントと結末の進行表</h1><p>本編6系統の代表手順。現在のゲーム内状態は自動判定しません。分岐は排他的で、全例外・各ダンジョンの全道順は未収録です。</p><a class="button" href="../../#/elden/npc-events">保存・同期できるNPCナビを開く →</a><p>チェック操作は既存の進捗画面で行います。既存チェックを再利用し、重複して追加しません。</p>'
md='# NPC別イベント進行表\n\n旧IDを再利用。新しいチェックは不足段階だけ。非表示の未来の手順や報酬は、NPCナビの折りたたみで表示できます。資料確認日2026-11-16、実機未検証。\n'
for r in db['npcRoutes']:
 body+='<section><h2>'+H(r['name'])+'</h2><p>'+H(r['warning'])+'</p><details><summary>手順と報酬を開く（ネタバレ）</summary><ol>'
 md+='\n## '+r['name']+'\n\n'+r['warning']+'\n\n|順|段階|場所|条件・必要品|行動・選択|報酬|分岐|チェックID|\n|---:|---|---|---|---|---|---|---|\n'
 for i,s in enumerate(r['stages']):
  body+='<li><h3>'+H(s['label'])+'</h3><p>場所：'+H(s['location'])+' · 条件：'+H(s['condition'])+'</p><p>必要品：'+H(s['items'])+'</p><p>'+H(s['action'])+'</p><p>'+H(s['warning'])+'</p><p>分岐：'+H(next((o['label'] for o in r['options'] if o['id']==s['branch']),'共通'))+' / 報酬：'+H(s['reward'] or 'この段階に指定なし')+'</p><a href="../'+s['entryId']+'/">関連する攻略・出典 →</a></li>'
  md+=f'|{i+1}|{s["label"]}|{s["location"]}|{s["condition"]} / {s["items"]}|{s["action"]}|{s["reward"] or "—"}|{s["branch"] or "共通"}|{s["taskId"]}|\n'
 body+='</ol></details></section>'
(R/'docs/NPC_PROGRESS.md').write_text(md)
body+='<section><h2>本編6結末</h2><p>フィアの対象品は「死王子の修復ルーン」です。結末名はイベント名と区別します。</p>'
md='# エンディング条件一覧\n\n最終戦後の選択前に、狂い火の受領・解除状態をゲーム内で確認。自己チェックは選択可能性の保証ではありません。\n\n|結末|条件|最終選択|注意|\n|---|---|---|---|\n'
for e in db['endingGuide']:
 body+='<details><summary>'+H(e['name'])+'の条件・最終選択</summary><p>'+H(e['condition'])+'</p><p>必要品：'+H(' / '.join(e['requiredItems']) or '指定なし（状態条件を確認）')+'</p><p>'+H(e['choice'])+'</p><p>'+H(e['warning'])+'</p><a href="../'+e['id']+'/">詳細・出典 →</a></details>'
 md+=f'|{e["name"]}|{e["condition"]}|{e["choice"]}|{e["warning"]}|\n'
body+='</section>';out=R/'elden/npc-events';out.mkdir(exist_ok=True);(out/'index.html').write_text(g['page']('NPCイベント・結末の進行表 | GNX','本編NPC6系統の進行、分岐、次の候補と結末条件。','https://popochan0547-creator.github.io/GNX/elden/npc-events/',body,{'@context':'https://schema.org','@type':'CollectionPage','name':'NPCイベントと結末'}));(R/'docs/ENDING_CONDITIONS.md').write_text(md)
