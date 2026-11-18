"""Visual treatment for the homepage course cards; no content changes."""

CSS = '''
#home-structure .stage-grid{gap:20px}
#home-structure .stage-card{--stage-rgb:63,112,87;--stage-ink:#29543e;position:relative;isolation:isolate;overflow:hidden;padding:29px 28px 21px;border:1px solid rgba(var(--stage-rgb),.22);border-radius:12px;background:linear-gradient(140deg,rgba(var(--stage-rgb),.085),transparent 65%),#fcfdf9;box-shadow:0 8px 25px -20px rgba(var(--stage-rgb),.4),inset 0 1px 0 #fff;transition:transform .3s ease,border-color .3s ease,box-shadow .3s ease}
#home-structure .stage-card:nth-child(2){--stage-rgb:63,106,132;--stage-ink:#30566d}
#home-structure .stage-card:nth-child(3){--stage-rgb:84,99,141;--stage-ink:#4b577a}
#home-structure .stage-card:nth-child(4){--stage-rgb:150,116,65;--stage-ink:#7b603b}
#home-structure .stage-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,rgba(var(--stage-rgb),.95),rgba(var(--stage-rgb),.12));pointer-events:none}
#home-structure .stage-card::after{content:'';position:absolute;z-index:-1;width:144px;height:144px;right:-22px;top:-22px;border:1px solid rgba(var(--stage-rgb),.11);border-radius:25px;transform:rotate(30deg);background:repeating-linear-gradient(0deg,transparent 0 17px,rgba(var(--stage-rgb),.07) 17px 18px),repeating-linear-gradient(90deg,transparent 0 17px,rgba(var(--stage-rgb),.07) 17px 18px);box-shadow:0 0 0 13px rgba(var(--stage-rgb),.025),0 0 0 28px rgba(var(--stage-rgb),.018);transition:transform .6s ease,opacity .6s ease;pointer-events:none}
#home-structure .stage-card:nth-child(2)::after{border-radius:50%;transform:rotate(-20deg);background:repeating-radial-gradient(circle at center,transparent 0 18px,rgba(var(--stage-rgb),.10) 18px 19px)}
#home-structure .stage-card:nth-child(3)::after{transform:rotate(45deg);border-radius:8px;background:repeating-linear-gradient(0deg,transparent 0 25px,rgba(var(--stage-rgb),.10) 25px 26px),repeating-linear-gradient(90deg,transparent 0 25px,rgba(var(--stage-rgb),.10) 25px 26px)}
#home-structure .stage-card:nth-child(4)::after{border-radius:50%;background:conic-gradient(from 20deg,transparent,rgba(var(--stage-rgb),.10),transparent 60%,rgba(var(--stage-rgb),.07),transparent);box-shadow:inset 0 0 0 14px #fcfdf9,0 0 0 12px rgba(var(--stage-rgb),.035),0 0 0 25px rgba(var(--stage-rgb),.025)}
#home-structure .stage-eyebrow{display:inline-block;padding:5px 9px;border:1px solid rgba(var(--stage-rgb),.16);border-radius:4px;background:#ffffffe0;color:rgba(var(--stage-rgb),.95);font-size:10px;letter-spacing:.06em}
#home-structure .stage-card h3{position:relative;color:var(--stage-ink);font-size:27px;margin:17px 0 9px;line-height:1.4}
#home-structure .stage-card p{position:relative;color:#718073;min-height:37px;font-size:12px;margin-bottom:23px;max-width:85%}
#home-structure .home-chapter{position:relative;border-top-color:rgba(var(--stage-rgb),.15);padding:13px 8px 13px 0;font-size:12px;line-height:1.7;color:#4f6257;transition:color .2s ease,background .2s ease,padding .2s ease;border-radius:3px}
#home-structure .home-chapter>span:first-child{font-size:11px;color:rgba(var(--stage-rgb),.75)}
#home-structure .home-chapter>span:last-child{display:flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:50%;background:rgba(var(--stage-rgb),.075);color:rgba(var(--stage-rgb),.8);transition:background .2s ease,color .2s ease,transform .2s ease}
#home-structure .home-chapter:hover,#home-structure .home-chapter:focus-visible{padding-left:8px;background:rgba(var(--stage-rgb),.065);color:var(--stage-ink)}
#home-structure .home-chapter:hover>span:last-child{background:rgba(var(--stage-rgb),.9);color:#fff;transform:translate(1px,-1px)}
#home-structure .stage-card:hover{transform:translateY(-3px);border-color:rgba(var(--stage-rgb),.45);box-shadow:0 16px 32px -20px rgba(var(--stage-rgb),.38),inset 0 1px 0 #fff}
#home-structure .stage-card:hover::after{transform:rotate(12deg) scale(1.08);opacity:.8}
#home-structure .home-chapter:focus-visible{outline:2px solid var(--stage-ink);outline-offset:3px}
@media(max-width:760px){#home-structure .stage-grid{gap:15px}#home-structure .stage-card{padding:24px 21px 16px}#home-structure .stage-card h3{font-size:26px}#home-structure .stage-card p{max-width:90%;min-height:0;margin-bottom:20px}#home-structure .home-chapter{font-size:12px;padding-block:13px}#home-structure .stage-card::after{width:130px;height:130px}}
@media(prefers-reduced-motion:reduce){#home-structure .stage-card,#home-structure .stage-card::after,#home-structure .home-chapter,#home-structure .home-chapter>span:last-child{transition:none}#home-structure .stage-card:hover{transform:none}}
'''
