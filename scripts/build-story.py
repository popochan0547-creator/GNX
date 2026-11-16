# Run build-pages.py first. This chart is an editorial route, not a mandatory order.
import runpy,pathlib,json,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1];g=runpy.run_path(str(R/'scripts/build-pages.py'));db=g['db'];H=g['H'];page=g['page'];BASE=g['BASE']
chapters=[
('出発と探索','一本道で進めず、祝福と装備の準備を優先する。',['area-limgrave','collect-whetstone','collect-physick'],['area-weeping','dungeon-stormfoot','dungeon-deathtouched'],'入手するだけの収集とボス撃破は別のチェック。'),
('ストームヴィル城','マルギットからゴドリックへ進む一例。',['boss-margit','area-stormveil','boss-godrick'],['npc-nepheli-early','npc-roderika'],'ネフェリとの序盤会話など、NPCの掲載段階を確認する。'),
('リエーニエと学院','学院の鍵を取り、赤狼からレナラへ。',['collect-academy-key','boss-red-wolf','boss-rennala'],['npc-ranni-intro','npc-thops','weapon-carian-regal'],'学院外の鍵と、トープスに渡す2本目は区別。'),
('アルター高原と王都','大昇降機または古遺跡断崖から高原へ進む。',['area-altus','area-leyndell','boss-godfrey-shade','boss-morgott'],['weapon-gransax','area-volcano'],'王都の入場条件を確認。グランサクスの雷は灰都化前に回収する。'),
('巨人たちの山嶺','モーゴット後の進行を経て火の巨人へ。',['boss-fire-giant'],['weapon-rivers-blood'],'火の釜でのイベント・エンディングの全分岐条件は未収録。'),
('ファルムアズラ','火の釜のイベント後に探索する。',['area-farum','boss-godskin-duo','boss-maliketh'],['talisman-alexander'],'マリケス撃破で王都が変化。王都の取り逃しを先に点検する。'),
('灰都から最終戦','ギデオン、ホーラ・ルーを越えてラダゴン／エルデの獣へ。',['boss-gideon','boss-hoarah','boss-final-pair'],[],'エンディングの全解除条件は未収録。最後の選択前に目的の分岐条件を確認する。'),
('任意の長期探索','本筋と並行できる寄り道。順序固定ではない。',['boss-radahn','area-nokron','npc-ranni-late'],['area-haligtree','boss-malenia'],'指殺しの刃を渡す前にセルブス側を確認。DLCへの入口は本編クリアと別条件。')]
lookup={e['id']:e for e in db['entries']}
body='<p class="kicker">BASE GAME / ROUTE PLANNER</p><h1>本編ストーリー攻略チャート</h1><p class="lead">準備から最終戦へ。GNXが提案する探索順の一例です。</p><p>必須の唯一の順序ではありません。全エンディング・NPC分岐の保証は未完了。DLCの章は含みません。</p><a class="button" href="../../#/elden">検索・既存進捗へ戻る →</a>'
for i,(name,summary,main,side,warn) in enumerate(chapters):
 side=side+[x['entryId'] for x in db['collections']['items'] if x['entryId'].startswith(('v18-','v19-','v20-','v21-')) and x['chartChapter']==i+1]
 body+=f'<section id="chapter-{i+1}"><p class="kicker">CHAPTER {i+1:02}</p><h2>{H(name)}</h2><p>{H(summary)}</p><h3>進行・重要アイテム</h3><ol>'+''.join(f'<li><a href="../../#/elden/{id}">{H(lookup[id]["name"])}</a> <a href="../{id}/">資料ページ ↗</a></li>' for id in main)+'</ol><h3>寄り道</h3><div class="related">'+(''.join(f'<a href="../{id}/">{H(lookup[id]["name"])}</a>' for id in side) or 'この章の寄り道は未収録。')+f'</div><aside class="warning">{H(warn)}</aside></section>'
body+='<section><h2>主要な追加攻略と結末</h2><p>火山館：<a href="../boss-rykard/">ライカード</a>。ファルムアズラの寄り道：<a href="../boss-placidusax/">プラキドサクス</a>。地下の寄り道：<a href="../npc-fia-late/">フィアとフォルサクス</a>。</p><p>進行前に<a href="../ending-frenzy/">狂い火の注意</a>、<a href="../ending-order/">律の時代の条件</a>を確認。<a href="../coverage/">未収録台帳</a>には未確認の前提も記録。</p></section>'
body+='<section><h2>出典・確認範囲</h2><a href="https://game8.jp/eldenring/422141" target="_blank" rel="noopener noreferrer">Game8 ストーリー攻略チャート</a><p>進行の前後関係を資料確認（2026-11-16）。推奨順はGNXの編集提案。重要アイテム・注意点の個別出典は各項目へ。文章と地図は転載していません。</p></section>'
out=R/'elden/story';out.mkdir(exist_ok=True);(out/'index.html').write_text(page('本編ストーリー攻略チャート | GNX','本編の探索順、寄り道、重要アイテムと取り逃し注意。',BASE+'elden/story/',body,{'@context':'https://schema.org','@type':'Article','headline':'本編ストーリー攻略チャート','inLanguage':'ja-JP'}))
ns='{http://www.sitemaps.org/schemas/sitemap/0.9}';tree=ET.parse(R/'sitemap.xml');u=ET.SubElement(tree.getroot(),ns+'url');ET.SubElement(u,ns+'loc').text=BASE+'elden/story/';ET.indent(tree);tree.write(R/'sitemap.xml',encoding='utf-8',xml_declaration=True)
