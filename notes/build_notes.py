"""Regenerate a chapter, a panorama, or the Atlas home and module layout.

Usage: python3 notes/build_notes.py --chapter ch02
Use --site to refresh the home and chapter modules from COURSE.md.
Chapter updates preserve other prose; all modes retain the Atlas module layout.
Diagrams are selected by explicit <!-- diagram:NN-name --> references to Archify assets.
"""
from pathlib import Path
import argparse
import base64
import html
import json
import re

NOTES = Path(__file__).resolve().parent

def esc(value):
    return html.escape(value, quote=True)

def inline(value):
    value = esc(value)
    value = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
        lambda m: '<a class="source" href="'+m[2]+'" target="_blank" rel="noopener noreferrer">'+m[1]+'</a>', value)
    value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    return value

def figure(chapter, name, number):
    stem = NOTES / 'diagrams' / chapter / name
    spec = json.loads(stem.with_suffix('.json').read_text())
    title = spec['meta']['title']
    preview = base64.b64encode(stem.with_suffix('.svg').read_bytes()).decode()
    viewer = base64.b64encode(stem.with_suffix('.html').read_bytes()).decode()
    uid = chapter+'-'+name+'-viewer'
    return (f'<figure class="archify-figure" data-archify-source="{name}">'
        f'<figcaption><span>图 {number} · {esc(title)}</span><button type="button" class="diagram-open" data-viewer="{uid}">全屏查看 ↗</button></figcaption>'
        f'<button class="diagram-preview" type="button" data-viewer="{uid}" aria-label="放大查看：{esc(title)}"><img src="data:image/svg+xml;base64,{preview}" alt="{esc(title)}" decoding="async"></button>'
        f'<script type="application/octet-stream" id="{uid}">{viewer}</script></figure>')

def render(chapter, source):
    lines = source.splitlines()
    out, toc = [], []
    section = sub = figures = 0
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        i += 1
        if not s or s.startswith('# '):
            continue
        match = re.fullmatch(r'<!-- diagram:([0-9]{2}-[a-z0-9-]+) -->', s)
        if match:
            figures += 1
            out.append(figure(chapter, match[1], figures))
        elif s.startswith('## '):
            if section:
                out.append('</section>')
            section += 1
            sub = 0
            title = re.sub(r'^\d+\s+', '', s[3:])
            anchor = f'{chapter}-s{section:02}'
            out.append(f'<section class="topic" id="{anchor}"><h3 class="topic-heading"><span class="section-no">{section}</span>{esc(title)}</h3>')
            toc.append((2, f'{section} {title}', anchor))
        elif s.startswith('### '):
            sub += 1
            title = s[4:]
            anchor = f'{chapter}-s{section:02}-t{sub}'
            out.append(f'<h4 class="subtopic-heading" id="{anchor}"><span class="subsection-no">{section}.{sub}</span> {esc(title)}</h4>')
            toc.append((3, f'{section}.{sub} {title}', anchor))
        elif s.startswith('```'):
            if s[3:] not in ('text', ''):
                raise ValueError('Use explicit Archify diagram markers for flowcharts')
            block = []
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i += 1
            if i == len(lines):
                raise ValueError('Unclosed code block')
            i += 1
            out.append('<div class="formula">'+'<br>'.join(inline(v) for v in block)+'</div>')
        elif s.startswith('|'):
            rows = [s]
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip()); i += 1
            cells = [[c.strip() for c in row.strip('|').split('|')] for row in rows]
            cells = [row for row in cells if not all(re.fullmatch(r'[:\- ]+', c) for c in row)]
            out.append('<div class="table-scroll" tabindex="0"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in cells[0])+'</tr></thead><tbody>')
            for row in cells[1:]:
                out.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>')
            out.append('</tbody></table></div>')
        elif s.startswith('<!--'):
            continue
        else:
            out.append('<p>'+inline(s)+'</p>')
    if section:
        out.append('</section>')
    return ''.join(out), toc, section, figures

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chapter', default='ch02')
    parser.add_argument('--site', action='store_true', help='Refresh Atlas home and chapter module layout while preserving prose')
    parser.add_argument('--panoramas', nargs='+', metavar='chNN',
                        help='Update selected panorama images from panorama-manifest.json; preserve existing prose')
    args = parser.parse_args()
    if args.site:
        from site_layout import refresh_site
        refresh_site()
        return
    if args.panoramas:
        update_panoramas(args.panoramas)
        from site_layout import refresh_site
        refresh_site()
        return
    chapter = args.chapter
    if not re.fullmatch(r'ch\d{2}', chapter):
        parser.error('chapter must be chNN')
    target = NOTES / 'index.html'
    before = target.read_text()
    article_pattern = rf'<article id="{chapter}"\s[^>]*>.*?</article>'
    nav_pattern = rf'<nav class="outline" data-for="{chapter}"[^>]*>.*?</nav>'
    article = re.search(article_pattern, before, re.S)
    nav = re.search(nav_pattern, before, re.S)
    if not article or not nav:
        raise ValueError('Existing chapter article and outline required')
    boundary = re.search(r'<!-- learning-body:start -->|<section class="(?:topic|outline-only)"', article[0])
    if not boundary:
        raise ValueError('Existing prose or outline boundary required')
    prefix = article[0][:boundary.start()]
    body, toc, sections, figures = render(chapter, (NOTES / (chapter+'.md')).read_text())
    if '<!-- learning-body:start -->' in article[0]:
        article_new = prefix+'<!-- learning-body:start -->'+body+'<!-- learning-body:end --></section></article>'
    else:
        article_new = prefix+body+'</article>'
    has_panorama = f'id="{chapter}-overview"' in prefix
    entries = ([(2, '全景图解', chapter+'-overview')] if has_panorama else [])+toc
    nav_start = nav[0].split('>', 1)[0]+'>'
    nav_new = nav_start+'<div class="outline-label">本章内容</div>'+''.join(
        f'<a href="#{anchor}" class="toc-link level-{level}">{esc(title)}</a>'
        for level, title, anchor in entries)+'</nav>'
    after = before.replace(article[0], article_new, 1).replace(nav[0], nav_new, 1)
    def mask(document):
        document = re.sub(article_pattern, '[chapter]', document, flags=re.S)
        return re.sub(nav_pattern, '[outline]', document, flags=re.S)
    assert mask(before) == mask(after)
    assert after.count(f'id="{chapter}-image"') == before.count(f'id="{chapter}-image"')
    if target.read_text() != before:
        raise RuntimeError('HTML changed during build; rerun to preserve concurrent edits')
    target.write_text(after)
    from site_layout import refresh_site
    refresh_site()
    print(f'Updated {chapter}: {sections} sections, {len(toc)-sections} subheadings, {figures} explicit Archify diagrams. Other HTML preserved.')

def update_panoramas(chapters):
    """Replace only requested overview blocks, preserving unrelated HTML bytes."""
    manifest = json.loads((NOTES / 'panorama-manifest.json').read_text())
    target = NOTES / 'index.html'
    before = target.read_text()
    after = before
    for chapter in chapters:
        if not re.fullmatch(r'ch\d{2}', chapter):
            raise ValueError('chapter must be chNN')
        item = manifest[chapter]
        asset = (NOTES / item['asset']).resolve()
        if not asset.is_relative_to(NOTES / 'assets'):
            raise ValueError('Panorama asset must be in notes/assets')
        encoded = base64.b64encode(asset.read_bytes()).decode()
        mime = {'.png': 'image/png', '.svg': 'image/svg+xml', '.webp': 'image/webp'}.get(asset.suffix.lower())
        if not mime:
            raise ValueError('Unsupported panorama format')
        source_links = '、'.join(
            f'<a class="source" href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["label"])}</a>'
            for s in item.get('sources', []))
        evidence = ''  # Sources stay in adjacent prose and the review manifest.
        overview = (f'<section class="panorama" id="{chapter}-overview">'
            f'<div class="panorama-heading"><h2>全景图解</h2><button class="image-open" type="button" data-image="{chapter}-image">放大图解 ↗</button></div>'
            f'<button class="image-frame" type="button" data-image="{chapter}-image" aria-label="放大查看第 {int(chapter[2:])} 章全景图">'
            f'<img id="{chapter}-image" src="data:{mime};base64,{encoded}" alt="{esc(item["title"])}" decoding="async"></button>{evidence}</section>')
        pattern = rf'<article id="{chapter}"\s[^>]*>.*?</article>'
        match = re.search(pattern, after, re.S)
        if not match:
            raise ValueError(f'Missing existing chapter {chapter}')
        old = match[0]
        overview_pattern = rf'<section class="panorama(?: [^"]*)?" id="{chapter}-overview">.*?</section>'
        if re.search(overview_pattern, old, re.S):
            new = re.sub(overview_pattern, lambda _: overview, old, count=1, flags=re.S)
        else:
            new = old.replace('</header>', '</header>'+overview, 1)
        new = new.replace('<section class="outline-only">', f'<section class="outline-only" id="{chapter}-outline">', 1)
        after = after.replace(old, new, 1)
        nav_pattern = rf'<nav class="outline" data-for="{chapter}"[^>]*>.*?</nav>'
        nav = re.search(nav_pattern, after, re.S)
        entry = f'<a href="#{chapter}-overview" class="toc-link level-2">全景图解</a>'
        if nav:
            if f'#{chapter}-overview' not in nav[0]:
                updated = nav[0].replace('<div class="outline-label">本章内容</div>', '<div class="outline-label">本章内容</div>'+entry, 1)
                after = after.replace(nav[0], updated, 1)
        else:
            new_nav = (f'<nav class="outline" data-for="{chapter}" aria-label="本章小标题" hidden>'
                       f'<div class="outline-label">本章内容</div>{entry}'
                       f'<a href="#{chapter}-outline" class="toc-link level-2">章节提纲</a></nav>')
            after = after.replace('</aside></div><dialog', new_nav+'</aside></div><dialog', 1)
    # Check that only the requested articles and their navigation changed.
    def masked(document):
        for chapter in chapters:
            document = re.sub(rf'<article id="{chapter}"\s[^>]*>.*?</article>', '', document, flags=re.S)
            document = re.sub(rf'<nav class="outline" data-for="{chapter}"[^>]*>.*?</nav>', '', document, flags=re.S)
        return document
    assert masked(before) == masked(after), 'Unrelated HTML changed'
    # Refuse to overwrite concurrent edits made while the build was running.
    if target.read_text() != before:
        raise RuntimeError('HTML changed during build; rerun to preserve concurrent edits')
    target.write_text(after)
    print('Updated panoramas: '+', '.join(chapters)+'; existing prose and unrelated HTML preserved.')

if __name__ == '__main__':
    main()

