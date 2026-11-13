const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--autoplay-policy=no-user-gesture-required']});const pg=await b.newPage({viewport:{width:390,height:844}});const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('http://localhost:8765/test.html');await pg.waitForTimeout(2000);await pg.click('#play');await pg.waitForTimeout(4000);
console.log(await pg.evaluate(()=>[vid.currentTime.toFixed(2),!!AC,Object.keys(BUF).length,events().length,document.documentElement.scrollWidth]));
await pg.screenshot({path:'an/b_phone.png'});console.log('errs',errs);await b.close()})();
