"""Responsive reading layout with chapter navigation docked to the right edge."""
import re

CSS = '''
/* The outer rails follow the viewport; the reading column uses the space between. */
:root{--course-rail:258px;--section-rail:232px}
.layout,body.is-home .layout{display:block;margin-left:var(--course-rail);margin-right:var(--section-rail);max-width:none;padding:40px clamp(28px,2.4vw,56px) 96px}
.reader{width:100%;max-width:960px;margin-inline:auto;min-width:0}
.panorama .image-frame{width:100%;max-width:none;margin-inline:auto}.panorama .image-frame img{max-width:830px;margin-inline:auto}
.outline-rail{position:fixed;inset:0 0 0 auto;width:var(--section-rail);height:100vh;max-height:none;overflow-y:auto;overscroll-behavior:contain;padding:35px 20px 30px;border-left:1px solid #e0e6dc;background:#f8faf5;z-index:12;scrollbar-width:thin}
.outline-disclosure>summary{display:none}
.outline-content{min-width:0}
.outline-rail .outline{display:block}
.outline-rail .outline-label{display:block;font-size:11px;letter-spacing:.1em;padding:0 0 16px;color:#8a998d}
.outline-rail .toc-link{display:block;border:0;border-left:1px solid #dce4d9;border-radius:0;margin:0;padding:7px 0 7px 13px;font-size:12px;line-height:1.7;color:#718578;background:none}
.outline-rail .toc-link.level-2{font-size:13px;padding:10px 0 8px 13px;color:#365747}
.outline-rail .toc-link.level-3{display:block;font-size:12px;padding:6px 0 6px 21px;color:#526d5e}
.outline-rail .toc-link.level-2:not(.module-link){padding-left:21px}
.outline-rail .toc-link.level-3{padding-left:29px}
.outline-rail .toc-link.module-link{font-size:14px;font-weight:650;margin:0 0 3px;padding-top:10px;padding-bottom:10px;color:#284f40}
.outline-rail .toc-link:hover{color:#2e654b;background:#eef3e9}
.outline-rail .toc-link.current{border-left:2px solid #3d6b54;color:#173e2b;font-weight:650;background:linear-gradient(90deg,#e9f0e3,transparent)}
@media(min-width:1180px){body.is-home .outline-rail{display:block}}
@media(max-width:1179px){
 .layout,body.is-home .layout{display:flex;flex-direction:column;margin-left:var(--course-rail);margin-right:0;max-width:none;padding:30px 30px 80px;gap:0}
 .reader{order:0;max-width:960px}
 .outline-rail{order:-1;position:static;inset:auto;width:100%;height:auto;max-height:none;padding:0;margin:0 0 22px;border:0;background:none;overflow:visible;z-index:auto}
 .outline-disclosure{border:1px solid #dfe6d9;border-radius:6px;background:#f5f7f0}
 .outline-disclosure>summary{display:flex;align-items:center;justify-content:space-between;list-style:none;cursor:pointer;padding:10px 14px;color:#52725f;font-size:12px;line-height:1.8}
 .outline-disclosure>summary::-webkit-details-marker{display:none}
 .outline-disclosure>summary::after{content:'展开 ＋';color:#91a18e;font-size:10px}
 .outline-disclosure[open]>summary::after{content:'收起 −'}
 .outline-disclosure>summary:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
 .outline-content{padding:0 14px 13px;max-height:48vh;overflow-y:auto;overscroll-behavior:contain;scrollbar-width:thin}
 .outline-rail .outline-label{display:none}
 body.is-home .outline-rail{display:none}
}
@media(max-width:760px){
 .layout,body.is-home .layout{margin-left:0;margin-right:0;padding:20px 20px 60px}
 .reader{max-width:none}
 .outline-rail{margin-bottom:22px}
 .outline-content{max-height:46vh}
}
'''

SCRIPT = '''<script id="docked-navigation-runtime">
(()=>{
 const rail=document.querySelector('.outline-rail');
 const disclosure=rail.querySelector('.outline-disclosure');
 const desktop=matchMedia('(min-width:1180px)');
 const sync=()=>{disclosure.open=desktop.matches;};
 sync();desktop.addEventListener('change',sync);
 rail.addEventListener('click',event=>{
  if(!desktop.matches&&event.target.closest('.toc-link'))disclosure.open=false;
 });
 document.querySelectorAll('.chapter-link,.brand-home').forEach(link=>link.addEventListener('click',()=>{
  if(!desktop.matches)disclosure.open=false;
 }));
})();
</script>'''


def apply_docked_navigation(document):
    pattern = r'(<aside class="outline-rail">)(.*?)(</aside>)'
    match = re.search(pattern, document, re.S)
    if not match:
        raise ValueError('Existing chapter navigation rail required')
    content = match[2]
    content = re.sub(r'<details class="outline-disclosure"[^>]*><summary[^>]*>.*?</summary><div class="outline-content">', '', content, count=1, flags=re.S)
    content = content.replace('</div></details>', '', 1)
    replacement = (match[1]+'<details class="outline-disclosure" open><summary>本章导航</summary>'+
                   '<div class="outline-content">'+content+'</div></details>'+match[3])
    document = document.replace(match[0], replacement, 1)
    document = re.sub(r'<script id="docked-navigation-runtime">.*?</script>', '', document, flags=re.S)
    return document.replace('</body>', SCRIPT+'</body>', 1)
