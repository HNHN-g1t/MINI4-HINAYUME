"""Build a dependency-free GitHub Pages site from the approved parts list."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).parent
SITE = ROOT / 'docs'
PARTS = [
('p01_r02_c01','丸穴ボールベアリング 4個セット','15111','ベアリング・ローラー'),
('p01_r02_c06','1.4mm中空軽量プロペラシャフト','15205','シャフト'),
('p01_r03_c01','2.0mm中空軽量プロペラシャフト','15206','シャフト'),
('p01_r03_c02','スーパーXシャーシ 中空軽量プロペラシャフト','15234','シャフト'),
('p01_r03_c04','ローラー用9mm ボールベアリングセット','15344','ベアリング・ローラー'),
('p01_r03_c05','ローラー用11mm ボールベアリングセット','15345','ベアリング・ローラー'),
('p01_r04_c02','17mm アルミベアリングローラー','15161','ベアリング・ローラー'),
('p01_r04_c06','19mm アルミベアリングローラー','15160','ベアリング・ローラー'),
('p01_r05_c01','19mmプラリング付アルミベアリングローラーセット','15125','ベアリング・ローラー'),
('p01_r06_c04','スタビライザーポールセット','15059','ステー・補強パーツ'),
('p02_r02_c05','ステンレス皿ビスセット（10・12・15・20・25・30mm）','15510','ビス・スペーサー'),
('p02_r02_c06','ステンレス皿ビスセット（6・8・15mm）','15527','ビス・スペーサー'),
('p02_r03_c01','ミニ四駆ビスセットA','15322','ビス・スペーサー'),
('p02_r03_c02','ミニ四駆ビスセットB','15323','ビス・スペーサー'),
('p02_r03_c03','ビスセットD（40mmステンレスビス）','15407','ビス・スペーサー'),
('p02_r03_c04','アルミスペーサーセット（12/6.7/6/3/1.5mm）','15473','ビス・スペーサー'),
('p02_r04_c06','スーパーXシャーシ FRPリヤーローラーステー','15243','ステー・補強パーツ'),
('p02_r05_c01','スーパーXシャーシ FRPマルチ強化プレート','15242','ステー・補強パーツ'),
('p02_r05_c02','FRPマルチ補強プレート','15193','ステー・補強パーツ'),
('p02_r05_c06','FRP強化マウントプレートセット','15150','ステー・補強パーツ'),
('p02_r08_c05','トルクチューン2モーター','15484','モーター'),
('p02_r08_c06','レブチューン2モーター','15485','モーター'),
('p02_r09_c01','アトミックチューン2モーター','15486','モーター'),
('p03_r01_c02','アルミモーターサポート','15149','モーター'),
('p03_r01_c03','小径メッキスポークホイールセット（レストンスポンジタイヤ付）','15219','タイヤ・ホイール'),
('p03_r01_c04','中空ゴム小径タイヤ（ホイール付）','15239','タイヤ・ホイール'),
('p03_r03_c03','レーサーミニ四駆 ゴールドターミナルB','15046','ターミナル・ギヤ'),
('p03_r03_c04','スーパーXシャーシ ゴールドターミナル','15237','ターミナル・ギヤ'),
('p03_r05_c06','ハイスピードカウンターギヤ','15236','ターミナル・ギヤ'),
]

def page(path, title, content, section='', depth=0):
    prefix = '../' * depth
    active = lambda key: ' aria-current="page"' if section == key else ''
    text = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | ミニ四駆ステーション・工房ひなゆめ</title><meta name="description" content="ミニ四駆ステーション・工房ひなゆめ。レース情報と、懐古レギュ・アニマルドライバーのレギュレーション。">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}style.css?v=2"></head>
<body><a class="skip" href="#main">本文へ移動</a><header><a class="brand" href="{prefix}index.html"><span class="brand-icon">雛</span><span>ミニ四駆ステーション・工房ひなゆめ<small>HINAYUME · MINI 4WD</small></span></a>
<nav aria-label="メインメニュー"><a href="{prefix}race/index.html"{active('race')}>🏁 レース</a><a href="{prefix}regulations/index.html"{active('regulations')}>レギュレーション</a></nav></header>
<main id="main">{content}</main><footer><a href="{prefix}index.html">ミニ四駆ステーション・工房ひなゆめ</a><span>小さなマシンで、夢中になろう。</span></footer></body></html>'''
    dest = SITE / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding='utf-8')

def crumb(text, parent='../../'):
    return f'<div class="breadcrumb"><a href="{parent}index.html">ホーム</a><span>/</span>{text}</div>'

page('index.html', 'ホーム', '''<h1 class="visually-hidden">ミニ四駆ステーション・工房ひなゆめ</h1>
<section class="entry-grid"><a class="entry" href="race/index.html"><span class="eyebrow">01 / RACE</span><h2>🏁 レース <span>↗</span></h2><p>開催情報・レースのお知らせ</p><small>準備中</small></a><a class="entry" href="regulations/index.html"><span class="eyebrow">02 / REGULATIONS</span><h2>レギュレーション <span>↗</span></h2><p>懐古レギュ / アニマルドライバー</p><small class="live">懐古レギュの使用可能パーツを公開</small></a></section>''')
page('race/index.html', 'レース', crumb('🏁 レース','../') + '<p class="eyebrow">RACE</p><h1>🏁 レース</h1><section class="empty"><span class="status">準備中</span><h2>次のスタートを、お楽しみに。</h2><p>レースの開催情報は、こちらに掲載予定です。</p></section>', 'race',1)
page('regulations/index.html', 'レギュレーション', '''<h1 class="visually-hidden">レギュレーション</h1><section class="entry-grid"><a class="entry" href="kaiko/index.html"><span class="eyebrow">NOSTALGIC CLASS</span><h2>懐古レギュ <span>↗</span></h2><p>使用可能パーツ一覧</p><small class="live">29点のパーツを掲載</small></a><a class="entry" href="animal/index.html"><span class="eyebrow">ANIMAL DRIVER</span><h2>アニマルドライバー <span>↗</span></h2><p>レギュレーションのご案内</p><small>準備中</small></a></section>''','regulations',1)
page('regulations/animal/index.html', 'アニマルドライバー', crumb('<a href="../index.html">レギュレーション</a><span>/</span>アニマルドライバー') + '<p class="eyebrow">ANIMAL DRIVER</p><h1>アニマルドライバー</h1><section class="empty"><span class="status">準備中</span><h2>ルールは、こちらでお知らせします。</h2><p>詳細なレギュレーションは掲載準備中です。</p></section>','regulations',2)
cards = ''
for i,(file,name,number,category) in enumerate(PARTS,1):
    cards += f'''<article class="part"><a class="part-image" href="../../assets/parts/{file}.png" target="_blank" rel="noopener" aria-label="{html.escape(name)}の画像を拡大（新しいタブ）"><img src="../../assets/parts/{file}.png" alt="{html.escape(name)}のカタログ画像" loading="lazy" width="750" height="712"><span>拡大 ↗</span></a><div class="part-body"><div class="part-meta"><span>{category}</span><span>{i:02d}</span></div><h3>{html.escape(name)}</h3></div></article>'''
page('regulations/kaiko/index.html','懐古レギュ｜使用可能パーツ一覧',crumb('<a href="../index.html">レギュレーション</a><span>/</span>懐古レギュ') + f'''<h1 class="visually-hidden">懐古レギュ 使用可能パーツ一覧</h1><section aria-labelledby="parts-heading"><div class="section-heading"><h2 id="parts-heading">使用可能パーツ一覧</h2><span>全29点</span></div><p class="note">指定カタログで印の付いたパーツを掲載しています。画像をタップすると、商品名・仕様を大きく確認できます。<br>画像内の価格・商品情報は、掲載元カタログ当時のものです。</p><div class="parts-grid">{cards}</div></section>''','regulations',2)
(SITE/'parts.json').write_text(json.dumps([dict(image=f'assets/parts/{f}.png',name=n,category=c) for f,n,num,c in PARTS],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Built 5 pages and 29 part entries.')
