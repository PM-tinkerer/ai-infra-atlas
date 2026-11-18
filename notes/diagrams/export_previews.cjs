// Derive portable SVG previews from the exact delivered Archify documents.
const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})});
 const page=await browser.newPage({viewport:{width:1440,height:900},colorScheme:'light'});
 const chapter=process.argv[2]||'ch01';
 if(!/^ch\d{2}$/.test(chapter))throw new Error('Expected chapter chNN');
 const dir=path.join(__dirname,chapter);
 for(const name of fs.readdirSync(dir).filter(n=>/^\d{2}-.*\.json$/.test(n)&&!n.endsWith('.visual-check.json')).sort().map(n=>n.slice(0,-5))){
  await page.goto(pathToFileURL(path.join(dir,name+'.html')).href+'?theme=light');
  await page.evaluate(()=>document.fonts.ready);
  const svg=await page.locator('.diagram-container > svg').evaluate(root=>{
   const copy=root.cloneNode(true);
   const originals=[root,...root.querySelectorAll('*')];
   const copies=[copy,...copy.querySelectorAll('*')];
   const props=['fill','fill-opacity','stroke','stroke-width','stroke-opacity','stroke-dasharray','stroke-linecap','stroke-linejoin','opacity','font-family','font-size','font-weight','letter-spacing','text-anchor','dominant-baseline','visibility','display'];
   originals.forEach((el,i)=>{const css=getComputedStyle(el);props.forEach(p=>copies[i].style.setProperty(p,css.getPropertyValue(p)));});
   copy.setAttribute('xmlns','http://www.w3.org/2000/svg');
   const vb=root.viewBox.baseVal;copy.setAttribute('width',vb.width);copy.setAttribute('height',vb.height);
   copy.style.width='100%';copy.style.height='auto';copy.style.background='#fff';
   return new XMLSerializer().serializeToString(copy);
  });
  fs.writeFileSync(path.join(dir,name+'.svg'),svg);
 }
 await browser.close();
 console.log('Exported chapter vector previews. Original delivered HTML retained unchanged.');
})().catch(e=>{console.error(e);process.exit(1)});
