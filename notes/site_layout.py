"""Build the Atlas home and consistent chapter modules without rewriting prose."""
from pathlib import Path
import base64
import html
import re
from layout_shell import CSS as DOCKED_NAVIGATION_CSS, apply_docked_navigation
from home_hero import CSS as HOME_HERO_CSS, decorate_home
from stage_cards import CSS as STAGE_CARDS_CSS
from home_case import CSS as HOME_CASE_CSS

NOTES = Path(__file__).resolve().parent
NAME = 'AI Infra Atlas · 智算架构图谱'
SUBTITLE = '从推理原理到异构服务平台'

BRAND_HOME = (
    '<div class="brand"><a class="brand-home" href="#home" '
    'aria-label="AI Infra Atlas · 返回首页" title="返回首页">'
    '<svg class="brand-mark" viewBox="0 0 36 36" fill="none" aria-hidden="true" focusable="false">'
    '<path d="M12 9H23M8 13V26H16M27 16V26H24" stroke="currentColor" stroke-width="1.2"/>'
    '<rect x="3" y="4" width="10" height="10" rx="2" fill="currentColor"/>'
    '<rect x="23" y="7" width="9" height="9" rx="2" fill="#7b9f90"/>'
    '<rect x="15" y="22" width="10" height="10" rx="2" fill="#b7cdc1" stroke="currentColor" stroke-width="1"/>'
    '</svg><span class="brand-copy"><span class="brand-title">AI Infra Atlas</span>'
    '<span class="brand-sub">智算架构图谱</span></span></a></div>'
)


def course_chapters():
    source = (NOTES.parent / 'COURSE.md').read_text()
    chapters = []
    for match in re.finditer(r'^### 第 (\d+) 章｜([^\n]+)\n(.*?)(?=^### |^## |\Z)', source, re.M | re.S):
        number, title, content = match.groups()
        chapters.append(dict(id=f'ch{int(number):02}', number=int(number), title=title,
                             points=re.findall(r'^- (.+)$', content, re.M),
                             goal=re.search(r'本章目标：(.+)', content)[1]))
    assert len(chapters) == 12
    return chapters


def e(value):
    return html.escape(value, quote=True)


def module_heading(number, title):
    number = {'01': '一', '02': '二', '03': '三'}.get(number, number)
    return f'<h2 class="module-heading"><span>{number}</span>{title}</h2>'


def home(chapters):
    image = base64.b64encode((NOTES / 'assets/ai-infra-inference-architecture-v3-emerald.png').read_bytes()).decode()
    stages = [('执行基础', '理解一次推理如何发生', '01—03'),
              ('优化机制', '解释计算、状态与引擎如何提效', '04—06'),
              ('平台架构', '连接多卡协同、国产适配与异构服务', '07—09'),
              ('规模化运营', '把性能转化为容量、可靠性与经营结果', '10—12')]
    cards = ''
    for index, (label, description, chapter_range) in enumerate(stages):
        links = ''.join(f'<a href="#{c["id"]}" class="home-chapter"><span>{c["number"]:02}</span><span>{e(c["title"].split("：")[0])}</span><span aria-hidden="true">↗</span></a>' for c in chapters[index*3:index*3+3])
        cards += f'<section class="stage-card"><div class="stage-eyebrow">第 {chapter_range} 章</div><h3>{label}</h3><p>{description}</p>{links}</section>'
    return decorate_home(f'<article id="home" class="chapter home-page" hidden aria-labelledby="home-title">'
            '<header class="home-hero"><div class="home-eyebrow">AI INFRA ATLAS</div>'
            '<h1 id="home-title">智算架构图谱</h1>'
            f'<div class="home-subtitle">{SUBTITLE}</div>'
            '<p class="home-lead">理解一次生成背后的计算，掌握一座推理平台的设计。沿着原理、优化、架构与运营，建立可用于工程判断和产品决策的 AI Infra 知识体系。</p>'
            '<div class="hero-actions"><a class="primary-action" href="#ch01">进入第一章 <span aria-hidden="true">↗</span></a><a class="secondary-action" href="#home-structure">浏览知识结构 <span aria-hidden="true">↓</span></a></div>'
            '<div class="home-facts"><div><strong>12</strong><span>主题章节</span></div><div><strong>4</strong><span>知识层次</span></div><div><strong>1</strong><span>贯穿平台案例</span></div></div></header>'
            '<section class="home-section" id="home-goals"><div class="section-kicker">LEARNING OBJECTIVES</div><h2>从理解机制，到能做出判断</h2>'
            '<div class="goal-grid"><div><span class="goal-no">01</span><h3>看懂执行</h3><p>解释 Token 生成、GPU 执行与数据搬运，建立延迟、吞吐和显存的数量级直觉。</p></div>'
            '<div><span class="goal-no">02</span><h3>判断优化</h3><p>定位瓶颈，识别量化、缓存、合批与并行的收益来源、成立条件和工程边界。</p></div>'
            '<div><span class="goal-no">03</span><h3>设计平台</h3><p>连接异构适配、容量调度与稳定性保障，用质量、性能和成本证据制定产品方案。</p></div></div></section>'
            '<section class="home-section" id="home-map"><div class="section-kicker">INFERENCE ARCHITECTURE</div><div class="home-section-head"><h2>十二章课程，构建完整体系</h2><button class="image-open" type="button" data-image="home-map-image">放大架构图 ↗</button></div>'
            f'<button class="image-frame home-map-frame" type="button" data-image="home-map-image" aria-label="放大推理系统架构图"><img id="home-map-image" src="data:image/png;base64,{image}" alt="推理系统主链为应用入口、推理服务平台、推理引擎实例、设备软件栈、异构算力与互联；左侧为模型制品、实例部署调度与资源纳管，右侧为可观测性、评测与成本治理。" decoding="async"></button>'
            '</section>'
            '<section class="home-section" id="home-structure"><div class="section-kicker">EXPLORE THE ATLAS</div><h2>按知识层次，进入具体问题</h2><div class="stage-grid">'+cards+'</div></section>'
            '<section class="home-case home-section" id="home-case"><div class="section-kicker">ONE CONTINUOUS CASE</div><h2>用统一案例，连接每章内容</h2>'
            '<p>从一条请求开始，逐步构建承载实时对话、长文档和 Agent 请求的推理平台，再扩展到国产与非国产算力共同组成的异构服务平台。</p>'
            '<div class="case-tags"><span>实时对话 · 响应体验</span><span>长文档 · 上下文与状态</span><span>Agent · 多轮与任务成本</span></div>'
            '<p class="reading-guide">每章依次提供章节提纲、全景图解与详细学习。可沿主线阅读，也可从当前问题跳转；相关原理、估算假设与来源随内容展开。</p></section></article>')


CSS = '''
/* Atlas site layout — generated by site_layout.py */
/* The brand itself is the home link; keep the resting state quiet. */
.brand{padding:0}
.brand-home{display:flex;align-items:flex-start;gap:12px;padding:26px 20px 24px;color:#365f50;cursor:pointer;transition:background-color .16s ease,color .16s ease}
.brand-mark{display:block;flex:0 0 30px;width:30px;height:30px;margin-top:1px}
.brand-copy{display:block;min-width:0}
.brand-title{display:block;font-family:inherit;font-size:20px;font-weight:650;letter-spacing:.005em;line-height:1.5;color:#284a3d;transition:color .16s ease}
.brand-sub{display:block;font-family:inherit;font-size:12px;font-weight:400;letter-spacing:.1em;margin-top:3px;color:#71897b}
@media(hover:hover){.brand-home:hover{background:#eaf0e8;color:#234d3d}.brand-home:hover .brand-title{color:#173e2e}}
.brand-home:focus-visible{outline:2px solid var(--accent);outline-offset:-5px;border-radius:5px}
@media(prefers-reduced-motion:reduce){.brand-home,.brand-title{transition:none}}
.layout{grid-template-columns:minmax(0,860px) 190px;gap:36px;max-width:1290px}.chapter-header{border-bottom:0;padding-bottom:4px;margin-bottom:22px}.chapter-subtitle{font-size:16px;color:var(--muted)}.module-heading{display:flex;align-items:baseline;gap:13px;font-size:21px;margin:0 0 20px;line-height:1.6}.module-heading>span{font-family:Georgia,serif;font-size:15px;font-weight:400;color:#7c9b8e;letter-spacing:.03em}.chapter-outline{margin-bottom:34px}.outline-card{padding:25px 28px;background:#f2f5ee;border:1px solid #e0e7dd;border-radius:9px}.chapter-outline .module-heading{margin-bottom:16px}.chapter-goal{margin:0 0 18px;font-size:14px;color:#456455;line-height:1.85}.chapter-goal strong{margin-right:9px}.chapter-outline ol{padding-left:21px;margin:0;display:grid;gap:10px}.chapter-outline li{padding-left:5px;font-size:13px;line-height:1.9;color:#56685e}.chapter-outline li::marker{color:#7b9c8a;font-family:Georgia,serif}.panorama{padding-bottom:36px}.panorama .module-heading{font-size:21px;margin:0}.image-frame{background:#f4f5ef;padding:14px;border-radius:9px}.panorama .image-frame img{width:100%;height:auto;max-height:none;object-fit:contain}.learning{border-top:1px solid var(--line);padding-top:26px}.learning>.module-heading{margin-bottom:24px}.learning .topic:first-of-type{margin-top:0;padding-top:0;border-top:0}.learning-empty{border:1px dashed #cfdace;border-radius:8px;padding:18px 22px;background:#fafbf7}.learning-empty p{margin:0;color:#738276;font-size:13px}.outline-label{font-size:11px;letter-spacing:.12em}.toc-link.module-link{font-weight:600;color:#3e6654;margin-top:7px}.home-hero{padding:22px 0 34px;border-bottom:1px solid var(--line)}.home-eyebrow{font-family:Georgia,serif;font-size:12px;letter-spacing:.28em;color:#527a69;margin-bottom:18px}.home-hero h1{font-size:56px;letter-spacing:-.035em;line-height:1.25;margin-bottom:16px}.home-subtitle{font-family:"Songti SC",serif;font-size:23px;color:#476657}.home-lead{font-size:15px;line-height:2.1;color:#718078;margin:23px 0}.hero-actions{display:flex;align-items:center;gap:22px;flex-wrap:wrap;margin:26px 0 33px}.primary-action{display:inline-flex;align-items:center;gap:24px;padding:11px 21px;border-radius:5px;background:#315f50;color:#fffefa;font-size:13px}.primary-action:hover{background:#254d40}.secondary-action{font-size:13px;color:#657c6d}.home-facts{display:flex;gap:45px}.home-facts>div{display:flex;align-items:baseline;gap:9px}.home-facts strong{font-family:Georgia,serif;font-size:29px;font-weight:400;color:#47705c}.home-facts span{font-size:11px;color:#8a958d}.home-section{margin-top:44px;scroll-margin-top:28px}.section-kicker{font-size:10px;letter-spacing:.19em;color:#8a9c90;margin-bottom:9px}.home-section h2{font-family:"Songti SC",serif;font-size:27px;line-height:1.5;margin:0 0 25px}.home-section-head{display:flex;align-items:baseline;justify-content:space-between;gap:15px}.home-section-head h2{margin-bottom:20px}.goal-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:27px}.goal-grid>div{padding-right:12px}.goal-grid>div+div{padding-left:23px;border-left:1px solid var(--line)}.goal-no{font:italic 22px Georgia,serif;color:#87a394}.goal-grid h3{font-family:"Songti SC",serif;font-size:19px;color:var(--ink);margin:11px 0 7px}.goal-grid p{font-size:13px;line-height:1.95;color:#78877d;margin:0}.home-map-frame{padding:8px;background:#f0f7f3;border-color:#cbdcd2;border-radius:12px}.home-map-frame img{max-height:none}.stage-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.stage-card{border:1px solid var(--line);border-radius:8px;padding:23px 24px;background:#fafbf6}.stage-eyebrow{font:11px Georgia,serif;color:#8a9e91;letter-spacing:.05em}.stage-card h3{font-family:"Songti SC",serif;font-size:24px;margin:9px 0 4px;color:#355546}.stage-card p{font-size:12px;line-height:1.8;color:#839084;margin:0 0 19px;min-height:43px}.home-chapter{display:grid;grid-template-columns:23px minmax(0,1fr) 12px;gap:9px;padding:10px 0;border-top:1px solid #e6eae1;font-size:12px;color:#5d7162;align-items:baseline}.home-chapter>span:first-child{font:11px Georgia,serif;color:#8b9e91}.home-chapter>span:last-child{color:#9aaa9e}.home-chapter:hover{color:#244e3d}.home-case{border-top:1px solid var(--line);padding-top:31px}.home-case p{font-size:14px;color:#718078}.case-tags{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 25px}.case-tags span{font-size:11px;padding:5px 10px;background:#eff3eb;border:1px solid #e1e8db;border-radius:4px;color:#66816e}.home-case .reading-guide{font-size:12px;color:#8c988e;line-height:1.9}.home-page .topic{border:0}.module-heading,.home-section,.chapter-outline,.learning{scroll-margin-top:28px}
@media(min-width:1241px){body.is-home .layout{grid-template-columns:minmax(0,860px) 170px}}
@media(max-width:1240px){.layout{grid-template-columns:minmax(0,1fr)}body.is-home .outline-rail{display:none}.toc-link.module-link{margin:0}.home-hero h1{font-size:48px}}
@media(max-width:760px){.layout{padding-top:20px}.mobile-bar>span{font-family:"Songti SC",serif;font-size:15px}.home-hero{padding-top:13px}.home-hero h1{font-size:39px}.home-eyebrow{font-size:10px}.home-subtitle{font-size:18px}.home-lead{font-size:13px;line-height:2}.hero-actions{gap:16px}.primary-action{padding:10px 15px;font-size:12px}.home-facts{gap:22px}.home-facts>div{display:block}.home-facts strong{font-size:27px;display:block}.home-facts span{font-size:10px}.home-section{margin-top:34px}.home-section h2{font-size:24px}.goal-grid{grid-template-columns:1fr;gap:19px}.goal-grid>div,.goal-grid>div+div{border-left:0;padding:0;display:grid;grid-template-columns:30px 1fr;column-gap:13px}.goal-grid h3{margin:0 0 4px}.goal-grid p{grid-column:2;font-size:12px}.goal-no{grid-row:1/3;padding-top:3px}.stage-grid{grid-template-columns:1fr;gap:13px}.stage-card{padding:20px}.stage-card p{min-height:0;margin-bottom:15px}.home-section-head{align-items:flex-start}.home-section-head h2{font-size:22px}.home-section-head .image-open{font-size:10px;white-space:nowrap;padding-top:5px}.chapter-outline{margin-bottom:27px}.outline-card{padding:21px 20px}.chapter-outline li{font-size:12px}.chapter-goal{font-size:13px}.module-heading,.panorama .module-heading{font-size:19px}.learning{padding-top:22px}.chapter-outline,.learning,.home-section{scroll-margin-top:70px}}

'''



READING_PRESENTATION_CSS = '''
/* Quiet, staggered highlights for homepage statistics. */
.home-facts{gap:14px;flex-wrap:wrap}
.home-facts>div{position:relative;isolation:isolate;overflow:hidden;padding:15px 21px;min-width:145px;border:1px solid #dce6dc;border-radius:10px;background:linear-gradient(135deg,#f0f5ed,#fafbf7);box-shadow:inset 0 1px 0 #ffffff;transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease}
.home-facts>div::before{content:"";position:absolute;inset:-50% -70%;z-index:-1;pointer-events:none;background:linear-gradient(110deg,transparent 38%,#ffffffb8 48%,#cce6d85c 53%,transparent 64%);transform:translateX(-65%);animation:fact-shimmer 9s ease-in-out infinite}
.home-facts>div:nth-child(2)::before{animation-delay:1.2s}
.home-facts>div:nth-child(3)::before{animation-delay:2.4s}
.home-facts>div:hover{transform:translateY(-2px);border-color:#9dbbac;box-shadow:0 5px 18px #315f5010,inset 0 1px 0 #fff}
.home-facts strong{color:#396451;text-shadow:0 1px 0 #fff;position:relative}
.home-facts span{color:#718579;position:relative}
@keyframes fact-shimmer{0%,10%{transform:translateX(-65%)}35%,100%{transform:translateX(65%)}}
@media(max-width:760px){.home-facts{gap:8px;flex-wrap:nowrap}.home-facts>div{flex:1;min-width:0;padding:12px 10px}.home-facts span{font-size:10px}}
@media(prefers-reduced-motion:reduce){.home-facts>div::before{animation:none;opacity:0}.home-facts>div{transition:none}.home-facts>div:hover{transform:none}}
/* Preview only: hide the original title block; the full image remains intact. */
.chapter .panorama .image-frame{width:100%;max-width:none;margin-inline:auto;padding:14px}
.chapter .panorama-crop{display:block;position:relative;width:min(100%,660px,calc((100vh - 110px) * var(--preview-ratio) * .95));margin-inline:auto;aspect-ratio:var(--preview-ratio);overflow:hidden}
.chapter .panorama .panorama-crop img{position:absolute;left:0;top:0;width:100%;height:auto;max-height:none;transform:translateY(var(--preview-offset))}
.chapter-header h1{font-size:42px;line-height:1.4;font-weight:700;letter-spacing:-.025em;color:#172f29}
.chapter-header .chapter-subtitle{font-size:16px;line-height:1.7;margin-top:12px}
.chapter-header{margin-bottom:36px}
.chapter .module-heading,.chapter .panorama .module-heading{font-size:28px;line-height:1.5;font-weight:700;letter-spacing:0;gap:13px;color:#172f29}
.chapter .module-heading>span{font-size:18px;font-weight:500;color:#426b59;flex-shrink:0}
.chapter-outline .module-heading{margin-bottom:18px}
.learning>.module-heading{margin-bottom:30px}
.learning .topic{margin-top:42px;padding-top:34px}
.learning .topic>.topic-heading{display:flex;align-items:baseline;gap:12px;font-size:24px;line-height:1.6;font-weight:700;letter-spacing:0;color:#203e33;margin:0 0 20px}
.topic-heading .section-no{font:500 21px Georgia,serif;color:#426b59;flex-shrink:0}
.learning .subtopic-heading{display:flex;align-items:baseline;gap:10px;font-size:20px;font-weight:600;line-height:1.7;color:#284f40;letter-spacing:0;margin:32px 0 12px;scroll-margin-top:36px}
.subtopic-heading .subsection-no{font:500 16px Georgia,serif;color:#426b59;flex-shrink:0;white-space:nowrap}
@media(max-width:760px){
 .chapter .panorama .image-frame{width:100%;padding:7px}
 .chapter-header h1{font-size:32px;line-height:1.45}
 .chapter-header .chapter-subtitle{font-size:14px;margin-top:9px}
 .chapter-header{margin-bottom:30px}
 .chapter .module-heading,.chapter .panorama .module-heading{font-size:25px;gap:10px}
 .chapter .module-heading>span{font-size:16px}
 .learning>.module-heading{margin-bottom:25px}
 .learning .topic{margin-top:34px;padding-top:28px}
 .learning .topic>.topic-heading{font-size:22px;gap:10px;margin-bottom:17px}
 .topic-heading .section-no{font-size:19px}
 .learning .subtopic-heading{font-size:18px;gap:9px;margin-top:28px;scroll-margin-top:76px}
 .subtopic-heading .subsection-no{font-size:15px}
}
'''
CSS += READING_PRESENTATION_CSS
CSS += DOCKED_NAVIGATION_CSS
CSS += HOME_HERO_CSS
CSS += STAGE_CARDS_CSS
CSS += HOME_CASE_CSS

# Pixel boundaries reviewed against each original 1055 × 1491 panorama.
# These affect the embedded preview only; the zoom viewer uses the untouched PNG.
PANORAMA_PREVIEW_TOP = {
    'ch01': 170, 'ch02': 170, 'ch03': 150, 'ch04': 180,
    'ch05': 170, 'ch06': 170, 'ch07': 170, 'ch08': 170,
    'ch09': 170, 'ch10': 170, 'ch11': 170, 'ch12': 180,
}


def compact_panorama(chapter, panorama):
    panorama = re.sub(r'<span class="panorama-crop"[^>]*>(<img\b[^>]*>)</span>', r'\1', panorama)
    top = PANORAMA_PREVIEW_TOP[chapter]
    ratio = 1055 / (1491 - top)
    offset = -100 * top / 1491
    wrapper = (f'<span class="panorama-crop" style="--preview-ratio:{ratio:.12f};'
               f'--preview-offset:{offset:.12f}%">')
    return re.sub(rf'(<img\b[^>]*\bid="{chapter}-image"[^>]*>)',
                  lambda m: wrapper+m[1]+'</span>', panorama, count=1)


def normalize_learning_headings(body):
    """Nest prose headings beneath the module without changing text or anchors."""
    body = re.sub(r'<h2><span class="section-no">(.*?)</h2>',
                  r'<h3 class="topic-heading"><span class="section-no">\1</h3>', body, flags=re.S)
    body = re.sub(r'<h3 id="([^"]+)"><span class="subsection-no">(.*?)</h3>',
                  r'<h4 class="subtopic-heading" id="\1"><span class="subsection-no">\2</h4>', body, flags=re.S)
    return body


def refresh_site():
    target = NOTES / 'index.html'
    before = target.read_text()
    result = before
    chapters = course_chapters()
    for c in chapters:
        chapter = c['id']
        pattern = rf'<article id="{chapter}"\s[^>]*>.*?</article>'
        old = re.search(pattern, result, re.S)[0]
        header = re.search(r'<header class="chapter-header">.*?</header>', old, re.S)[0]
        header = re.sub(r'<nav class="chapter-modules".*?</nav>', '', header, flags=re.S)
        panorama = re.search(r'<section class="panorama(?: [^"]*)?".*?</section>', old, re.S)[0]
        panorama = re.sub(r'<p class="panorama-evidence">.*?</p>', '', panorama, flags=re.S)
        panorama = re.sub(r'<h2[^>]*>.*?</h2>', module_heading('02', '全景图解'), panorama, count=1, flags=re.S)
        panorama = compact_panorama(chapter, panorama)
        if '<!-- learning-body:start -->' in old:
            body = old.split('<!-- learning-body:start -->', 1)[1].split('<!-- learning-body:end -->', 1)[0]
        else:
            boundary = re.search(r'<section class="topic"', old)
            body = old[boundary.start():-len('</article>')] if boundary else ''
        body = normalize_learning_headings(body)
        outline = (f'<section class="chapter-outline" id="{chapter}-outline">'+module_heading('01','章节提纲')+
                   f'<div class="outline-card"><p class="chapter-goal"><strong>本章目标</strong>{e(c["goal"])}</p><ol>'+''.join('<li>'+e(p)+'</li>' for p in c['points'])+'</ol></div></section>')
        learning = (f'<section class="learning" id="{chapter}-learning">'+module_heading('03','详细学习')+
                    '<!-- learning-body:start -->'+body+'<!-- learning-body:end -->'+
                    ('' if body else '<div class="learning-empty"><p>本章正文尚未整理，可先结合章节提纲与全景图阅读。</p></div>')+'</section>')
        opening = old.split('>',1)[0]+'>'
        guide = outline+panorama
        new = opening+header+guide+learning+'</article>'
        result = result.replace(old, new, 1)
        nav_pattern = rf'<nav class="outline" data-for="{chapter}"[^>]*>.*?</nav>'
        old_nav = re.search(nav_pattern, result, re.S)
        toc = []
        if old_nav:
            toc = re.findall(r'<a href="#[^"]+-s\d+[^"]*".*?</a>',old_nav[0],re.S)
        entries = ''.join(f'<a href="#{chapter}-{anchor}" class="toc-link level-2 module-link">{label}</a>' for anchor,label in [('outline','章节提纲'),('overview','全景图解'),('learning','详细学习')])
        new_nav = f'<nav class="outline" data-for="{chapter}" aria-label="本章导航" hidden><div class="outline-label">章节导航</div>{entries}'+''.join(toc)+'</nav>'
        if old_nav:
            result = result.replace(old_nav[0],new_nav,1)
    result = re.sub(r'<article id="home"\s[^>]*>.*?</article>', '', result, flags=re.S)
    result = result.replace('<main class="reader">','<main class="reader">'+home(chapters),1)
    result = re.sub(r'<nav class="outline" data-for="home"[^>]*>.*?</nav>', '',result,flags=re.S)
    home_nav = '<nav class="outline" data-for="home" aria-label="首页导航" hidden><div class="outline-label">图谱导览</div>'+''.join(f'<a class="toc-link level-2" href="#home-{a}">{b}</a>' for a,b in [('goals','学习目标'),('map','推理架构'),('structure','章节总览'),('case','贯穿案例')])+'</nav>'
    result = result.replace('<aside class="outline-rail">','<aside class="outline-rail">'+home_nav,1)
    result = re.sub(r'<div class="brand">.*?(?=<nav class="chapter-nav")', BRAND_HOME,result,count=1,flags=re.S)
    result = re.sub(r'<a class="chapter-link home-link".*?</a>', '',result,flags=re.S)
    result = result.replace('>单卡与引擎</div>','>优化机制</div>').replace('>多卡与异构</div>','>平台架构</div>')
    result = re.sub(r'<div class="mobile-bar"><span>.*?</span>', '<div class="mobile-bar"><span>智算架构图谱</span>',result,count=1,flags=re.S)
    result = re.sub(r'<title>.*?</title>', f'<title>{NAME}</title>',result,count=1)
    result = re.sub(r'<style id="atlas-style">.*?</style>','',result,flags=re.S)
    result = result.replace('</head>','<style id="atlas-style">'+CSS+'</style></head>',1)
    result = result.replace("decodeURIComponent(location.hash.slice(1))||'ch01'", "decodeURIComponent(location.hash.slice(1))||'home'")
    result = result.replace("let chapter=match?match[0]:'ch01'", "let chapter=match?match[0]:'home'")
    result = result.replace("chapter='ch01';", "chapter='home';")
    result = result.replace("document.title=document.querySelector('#'+chapter+' h1').textContent+' · AI Infra';", "document.title=chapter==='home'?'"+NAME+"':document.querySelector('#'+chapter+' h1').textContent+' · AI Infra Atlas';\n document.body.classList.toggle('is-home',chapter==='home');")
    result = result.replace("'#'+activeChapter+' .topic, #'+activeChapter+' h3, #'+activeChapter+' .panorama'", "'#'+activeChapter+' .topic, #'+activeChapter+' h3, #'+activeChapter+' .panorama, #'+activeChapter+' .chapter-outline, #'+activeChapter+' .learning, #'+activeChapter+' .home-section'")
    result = result.replace("activeChapter+' h3, #'+activeChapter", "activeChapter+' .subtopic-heading, #'+activeChapter")
    result = result.replace("?'知识架构':'全景图解'", "?'推理系统架构':'全景图解'")
    result = result.replace('largeImage.alt=original.alt;setZoom(100);', "largeImage.alt=original.alt;dialog.querySelector('.dialog-bar>span').textContent=original.id==='home-map-image'?'推理系统架构':'全景图解';setZoom(100);")
    result = apply_docked_navigation(result)
    if target.read_text() != before:
        raise RuntimeError('HTML changed during build; rerun')
    target.write_text(result)
    print('Updated Atlas home and 12 chapter modules; existing detailed learning HTML preserved.')


if __name__ == '__main__':
    refresh_site()
