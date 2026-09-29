"""Build the Hinayume GitHub Pages site from the text files in content/.

Update flow:
    1. edit content/*.md (page text) or content/parts.tsv (parts list)
    2. py build_site.py
    3. git commit & push
No third-party libraries required.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).parent
CONTENT = ROOT / 'content'
SITE = ROOT / 'docs'
SITE_NAME = 'ミニ四駆ステーション・工房ひなゆめ'
DESCRIPTION = 'ミニ四駆ステーション・工房ひなゆめ。レース情報と、懐古レギュ・アニマルドライバーのレギュレーション。'

# MINI4-LIN9 の公式イベント一覧から、愛知県・工房ひなゆめの開催だけを抜き出したもの。
# 日付やURLを更新すると、同じ一覧UIで次回の予定も表示できます。
RACE_EVENTS = [
    ('2026-09-16', '工房ひなゆめ「ミニ四駆ビギナークラスレース&勉強会」', 'https://www.tamiya.com/japan/event/tamiya_event_26731'),
    ('2026-09-19', 'ミニ四駆ステーション「ストッククラス」レース at 工房ひなゆめ', 'https://www.tamiya.com/japan/event/m4stsc2026_0806_049'),
    ('2026-10-04', '【ダッシュクラス＆チューンクラス開催】ミニ四駆ステーションチャレンジ2026 5th ROUND at 工房ひなゆめ', 'https://www.tamiya.com/japan/event/m4stc2026_5th_0909_027'),
    ('2026-10-04', '工房ひなゆめ「ミニ四駆走行＆交流会vol.83」', 'https://www.tamiya.com/japan/event/tamiya_event_26724'),
    ('2026-10-24', '工房ひなゆめ「ミニ四駆ビギナークラスレース&勉強会」', 'https://www.tamiya.com/japan/event/tamiya_event_26732'),
    ('2026-11-08', '工房ひなゆめ「ミニ四駆走行＆交流会vol.84」', 'https://www.tamiya.com/japan/event/tamiya_event_26725'),
    ('2026-11-21', '工房ひなゆめ「ミニ四駆ビギナークラスレース&勉強会」', 'https://www.tamiya.com/japan/event/tamiya_event_26733'),
    ('2026-12-06', '工房ひなゆめ「ミニ四駆走行＆交流会vol.85」', 'https://www.tamiya.com/japan/event/tamiya_event_26726'),
    ('2026-12-19', '工房ひなゆめ「ミニ四駆ビギナークラスレース&勉強会」', 'https://www.tamiya.com/japan/event/tamiya_event_26734'),
]


def load_parts():
    """content/parts.tsv -> [{file, number, name, category}, ...]"""
    parts = []
    for line in (CONTENT / 'parts.tsv').read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        file, number, name, category = line.split('\t')
        parts.append(dict(file=file, number=number, name=name, category=category))
    return parts


def load_doc(name):
    """content/<name>.md -> (meta dict, markdown body)"""
    raw = (CONTENT / f'{name}.md').read_text(encoding='utf-8')
    head, _, body = raw.partition('\n---\n')
    meta = {}
    for line in head.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            meta[key.strip()] = value.strip()
    return meta, body


def inline(text):
    """Escape, then apply **bold**."""
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html.escape(text))


def markdown(text, slots=None):
    """A deliberately small Markdown subset: ## / ### / - list / > note / {{slot}}."""
    slots = slots or {}
    out = []
    for block in re.split(r'\n\s*\n', text.strip()):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        first = lines[0]
        if first.startswith('{{') and first.endswith('}}'):
            out.append(slots.get(first[2:-2], ''))
        elif first.startswith('### '):
            out.append(f'<h3 class="rule-sub">{inline(first[4:])}</h3>')
        elif first.startswith('## '):
            out.append(f'<h2>{inline(first[3:])}</h2>')
        elif all(l.startswith('- ') for l in lines):
            items = ''.join(f'<li>{inline(l[2:])}</li>' for l in lines)
            out.append(f'<ul class="rule-list">{items}</ul>')
        elif all(l.startswith('> ') for l in lines):
            body = '<br>'.join(inline(l[2:]) for l in lines)
            out.append(f'<p class="note-box">{body}</p>')
        else:
            out.append('<p>' + '<br>'.join(inline(l) for l in lines) + '</p>')
    return '\n'.join(out)


def parts_section(parts, asset_prefix):
    cards = ''
    for part in parts:
        name = html.escape(part['name'])
        key = html.escape(part['name'] + ' ' + part['number'] + ' ' + part['category'])
        src = asset_prefix + 'assets/parts/' + part['file'] + '.png'
        cards += (
            f'<article class="part" data-key="{key}">'
            f'<a class="part-image" href="{src}" target="_blank" rel="noopener"'
            f' aria-label="{name}の画像を拡大（新しいタブ）">'
            f'<img src="{src}" alt="{name}のカタログ画像" loading="lazy" width="750" height="712">'
            f'<span>拡大 ↗</span></a>'
            f'<div class="part-body"><div class="part-meta">'
            f'<span>{html.escape(part["category"])}</span>'
            f'<span>{html.escape(part["number"])}</span></div>'
            f'<h3>{name}</h3></div></article>'
        )
    return f'''<section aria-labelledby="parts-heading">
<div class="section-heading"><h2 id="parts-heading">使用可能パーツ一覧</h2><span>全{len(parts)}点</span></div>
<p class="note">指定カタログで印の付いたパーツを掲載しています。画像をタップすると、商品名・仕様を大きく確認できます。<br>画像内の価格・商品情報は、掲載元カタログ当時のものです。</p>
<div class="part-search"><label for="part-q" class="visually-hidden">パーツを検索</label>
<input id="part-q" type="search" placeholder="パーツ名・品番で絞り込む（例：ローラー / 15161）" autocomplete="off">
<span id="part-count" aria-live="polite">{len(parts)}点</span></div>
<div class="parts-grid" id="parts-grid">{cards}</div>
<p class="parts-empty" id="parts-empty" hidden>該当するパーツがありません。</p>
</section>'''


PARTS_SCRIPT = '''<script>
(function(){
  var q=document.getElementById('part-q'),grid=document.getElementById('parts-grid');
  if(!q||!grid)return;
  var cards=[].slice.call(grid.children),count=document.getElementById('part-count'),empty=document.getElementById('parts-empty');
  q.addEventListener('input',function(){
    var t=q.value.trim().toLowerCase(),hit=0;
    cards.forEach(function(c){
      var on=!t||c.dataset.key.toLowerCase().indexOf(t)>-1;
      c.hidden=!on; if(on)hit++;
    });
    count.textContent=hit+'点';
    empty.hidden=hit>0;
  });
})();
</script>'''


def page(path, title, content, section='', depth=0, extra=''):
    prefix = '../' * depth
    active = lambda key: ' aria-current="page"' if section == key else ''
    text = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | {SITE_NAME}</title><meta name="description" content="{DESCRIPTION}">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}style.css?v=3"></head>
<body><a class="skip" href="#main">本文へ移動</a><header><a class="brand" href="{prefix}index.html"><span class="brand-icon">雛</span><span>{SITE_NAME}<small>HINAYUME · MINI 4WD</small></span></a>
<nav aria-label="メインメニュー"><a href="{prefix}race/index.html"{active('race')}>🏁 レース</a><a href="{prefix}regulations/index.html"{active('regulations')}>レギュレーション</a></nav></header>
<main id="main">{content}</main><footer><a href="{prefix}index.html">{SITE_NAME}</a><span>小さなマシンで、夢中になろう。</span></footer>{extra}</body></html>'''
    dest = SITE / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding='utf-8')


def crumb(trail, parent='../../'):
    return f'<div class="breadcrumb"><a href="{parent}index.html">ホーム</a><span>/</span>{trail}</div>'


def doc_page(path, name, breadcrumb, section, depth, slots=None, extra=''):
    meta, body = load_doc(name)
    badge = f'<span class="status">{html.escape(meta["badge"])}</span>' if meta.get('badge') else ''
    head = ('<div class="page-heading"><div>'
            f'<p class="eyebrow">{html.escape(meta.get("eyebrow", ""))}</p>'
            f'<h1>{html.escape(meta["title"])}</h1>{badge}</div>'
            f'<div class="roundel">{html.escape(meta.get("roundel", ""))}<small>HINAYUME</small></div></div>')
    content = breadcrumb + head + f'<div class="rule">{markdown(body, slots)}</div>'
    page(path, meta['title'], content, section, depth, extra)


def race_page():
    events = json.dumps([
        {'date': date, 'shop': '工房ひなゆめ', 'name': name, 'url': url}
        for date, name, url in RACE_EVENTS
    ], ensure_ascii=False)
    content = crumb('🏁 レース', '../') + f'''<div class="race-heading"><div><p class="eyebrow">RACE CALENDAR</p><h1>🏁 レース開催情報</h1><p class="intro">愛知県「工房ひなゆめ」で開催されるミニ四駆イベント。</p></div><div class="roundel">{len(RACE_EVENTS)}<small>EVENTS</small></div></div>
<section class="race-panel" aria-labelledby="race-list-heading"><div class="race-toolbar"><div><h2 id="race-list-heading">工房ひなゆめの予定</h2><p class="note">タミヤ公式イベント情報をもとに掲載しています。詳細・受付状況は各イベントページでご確認ください。</p></div><span id="race-count" class="race-count"></span></div><div id="race-months" class="race-months" role="group" aria-label="月で絞り込む"></div><label class="race-search"><span class="visually-hidden">イベント名で検索</span><input id="race-q" type="search" placeholder="イベント名で検索" autocomplete="off"></label><div id="race-list" class="race-list"></div><p id="race-empty" class="parts-empty" hidden>該当するイベントがありません。</p></section>'''
    script = f'''<script>
(function(){{
  var events={events}, list=document.getElementById('race-list'), months=document.getElementById('race-months'), q=document.getElementById('race-q'), count=document.getElementById('race-count'), empty=document.getElementById('race-empty'), active='all';
  var labels={{'09':'9月','10':'10月','11':'11月','12':'12月'}};
  function dateText(value){{var p=value.split('-'), d=new Date(value+'T00:00:00'); return p[1]+'月'+p[2]+'日（'+['日','月','火','水','木','金','土'][d.getDay()]+'）';}}
  function renderMonths(){{var keys=[]; events.forEach(function(e){{var m=e.date.slice(5,7); if(keys.indexOf(m)<0)keys.push(m);}}); months.innerHTML='<button class="race-chip on" data-month="all">すべて</button>'+keys.map(function(m){{return '<button class="race-chip" data-month="'+m+'">'+labels[m]+'</button>';}}).join(''); [].forEach.call(months.children,function(b){{b.addEventListener('click',function(){{active=b.dataset.month; [].forEach.call(months.children,function(x){{x.classList.toggle('on',x===b);}}); render();}});}});}}
  function render(){{var term=q.value.trim().toLowerCase(), hit=events.filter(function(e){{return (active==='all'||e.date.slice(5,7)===active)&&(!term||e.name.toLowerCase().indexOf(term)>-1);}}); list.innerHTML=hit.map(function(e){{return '<article class="race-card"><div class="race-date">'+dateText(e.date)+'</div><div class="race-info"><span class="race-shop">'+e.shop+'</span><h3>'+e.name+'</h3></div><a class="race-detail" href="'+e.url+'" target="_blank" rel="noopener">公式詳細 ↗</a></article>';}}).join(''); count.textContent=hit.length+'件'; empty.hidden=hit.length>0;}}
  q.addEventListener('input',render); renderMonths(); render();
}})();
</script>'''
    page('race/index.html', '🏁 レース', content, 'race', 1, script)


parts = load_parts()

page('index.html', 'ホーム', f'''<h1 class="visually-hidden">{SITE_NAME}</h1>
<section class="entry-grid"><a class="entry" href="race/index.html"><span class="eyebrow">01 / RACE</span><h2>🏁 レース <span>↗</span></h2><p>開催情報・レースのお知らせ</p><small>準備中</small></a><a class="entry" href="regulations/index.html"><span class="eyebrow">02 / REGULATIONS</span><h2>レギュレーション <span>↗</span></h2><p>懐古レギュ / アニマルドライバー</p><small class="live">懐古レギュ 2023年度を公開中</small></a></section>''')

race_page()

page('regulations/index.html', 'レギュレーション', f'''<h1 class="visually-hidden">レギュレーション</h1><section class="entry-grid"><a class="entry" href="kaiko/index.html"><span class="eyebrow">NOSTALGIC CLASS</span><h2>懐古レギュ <span>↗</span></h2><p>2023年度レギュレーション / 使用可能パーツ一覧</p><small class="live">{len(parts)}点のパーツを掲載</small></a><a class="entry" href="animal/index.html"><span class="eyebrow">ANIMAL DRIVER</span><h2>アニマルドライバー <span>↗</span></h2><p>レギュレーションのご案内</p><small>準備中</small></a></section>''', 'regulations', 1)

doc_page('regulations/animal/index.html', 'animal',
         crumb('<a href="../index.html">レギュレーション</a><span>/</span>アニマルドライバー'), 'regulations', 2)

doc_page('regulations/kaiko/index.html', 'kaiko',
         crumb('<a href="../index.html">レギュレーション</a><span>/</span>懐古レギュ'), 'regulations', 2,
         slots={'parts': parts_section(parts, '../../')}, extra=PARTS_SCRIPT)

(SITE / 'parts.json').write_text(
    json.dumps([dict(image='assets/parts/' + p['file'] + '.png', number=p['number'], name=p['name'],
                     category=p['category']) for p in parts], ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8')

print(f'Built 5 pages and {len(parts)} part entries.')
