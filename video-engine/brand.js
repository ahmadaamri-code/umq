/* ================= brand: «عُمق» ================= */
const BR={name:'عُمق',tag:'رياضيات تُفهَم… لا تُحفَظ',navy:'#16222f',navy2:'#22344a',green:'#14905a',mint:'#3fd08c',gold:'#e0a526',blue:'#1f6fd1',red:'#d6453d',paper:'#fbf6ea',ink:'#1d2a3a'};
const bgc=document.createElement('canvas'); bgc.width=W; bgc.height=H; const bx=bgc.getContext('2d');
function blob(ctx,x,y,r,col){ const g=ctx.createRadialGradient(x,y,0,x,y,r); g.addColorStop(0,col); g.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle=g; ctx.fillRect(x-r,y-r,2*r,2*r); }
function paintBG(ctx,T,dark=false){
 const g=ctx.createLinearGradient(0,0,W,H);
 if(dark){ g.addColorStop(0,'#1a2838'); g.addColorStop(1,'#0f1822'); } else { g.addColorStop(0,'#fdf9f0'); g.addColorStop(1,'#f2e8d4'); }
 ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
 const s=Math.sin, q=T*0.25;
 if(dark){ blob(ctx,420+60*s(q),300+40*s(q*1.3),760,'rgba(63,208,140,.16)'); blob(ctx,1560+50*s(q*0.8),820,720,'rgba(31,111,209,.20)'); blob(ctx,1700,120,520,'rgba(224,165,38,.10)'); }
 else { blob(ctx,240+60*s(q),140+40*s(q*1.3),760,'rgba(20,144,90,.10)'); blob(ctx,1760+40*s(q*0.7),1000,760,'rgba(31,111,209,.075)'); blob(ctx,1720+30*s(q*1.1),60,560,'rgba(224,165,38,.10)'); }
 ctx.fillStyle=dark?'rgba(255,255,255,.07)':'rgba(29,42,58,.075)';
 for(let y=18;y<H;y+=36) for(let x=18;x<W;x+=36){ ctx.fillRect(x-1.3,y-1.3,2.6,2.6); }
 // watermark mark (bottom-right, very faint)
 ctx.save(); ctx.globalAlpha=dark?0.06:0.035; ctx.translate(1700,880); ctx.strokeStyle=dark?'#fff':BR.ink; ctx.lineWidth=14; ctx.lineCap='round';
 ctx.beginPath(); ctx.moveTo(-260,170); ctx.lineTo(200,-200); ctx.stroke(); ctx.lineWidth=10; ctx.beginPath(); ctx.moveTo(-90,30); ctx.lineTo(80,30); ctx.lineTo(80,-104); ctx.stroke(); ctx.restore();
 ctx.save(); ctx.strokeStyle=dark?'rgba(255,255,255,.08)':'rgba(29,42,58,.08)'; ctx.lineWidth=2; ctx.beginPath(); ctx.roundRect(18,18,W-36,H-36,28); ctx.stroke(); ctx.restore();
}
function logoMark(ctx,x,y,s,p=1,{dark=false,alpha=1}={}){ if(alpha<=0) return; const sq=backE(cl(p/0.3)); if(sq<=0) return;
 ctx.save(); ctx.globalAlpha*=alpha; ctx.translate(x,y); ctx.scale(sq,sq);
 const r=s*0.24, h=s/2; const g=ctx.createLinearGradient(-h,-h,h,h); g.addColorStop(0,BR.navy2); g.addColorStop(1,BR.navy);
 ctx.shadowColor='rgba(10,20,30,.35)'; ctx.shadowBlur=s*0.18; ctx.shadowOffsetY=s*0.06; ctx.fillStyle=g; ctx.beginPath(); ctx.roundRect(-h,-h,s,s,r); ctx.fill(); ctx.shadowColor='transparent'; ctx.shadowOffsetY=0;
 ctx.strokeStyle='rgba(255,255,255,.10)'; ctx.lineWidth=Math.max(1,s*0.012); ctx.beginPath(); for(let k=1;k<4;k++){ const v=-h+k*s/4; ctx.moveTo(v,-h+s*0.12); ctx.lineTo(v,h-s*0.12); ctx.moveTo(-h+s*0.12,v); ctx.lineTo(h-s*0.12,v); } ctx.stroke();
 const A=[-s*0.26,s*0.20], B=[s*0.24,-s*0.24]; const lp=ease(cl((p-0.25)/0.35));
 const L0=[-s*0.36,s*0.29], L1=[s*0.34,-s*0.33];
 ctx.lineCap='round'; ctx.strokeStyle=BR.mint; ctx.lineWidth=s*0.075; ctx.shadowColor=BR.mint; ctx.shadowBlur=s*0.12;
 ctx.beginPath(); ctx.moveTo(L0[0],L0[1]); ctx.lineTo(L0[0]+(L1[0]-L0[0])*lp,L0[1]+(L1[1]-L0[1])*lp); ctx.stroke(); ctx.shadowBlur=0;
 const tp=ease(cl((p-0.55)/0.25)), up=ease(cl((p-0.72)/0.25));
 if(tp>0){ ctx.strokeStyle='#ff7a6b'; ctx.lineWidth=s*0.05; ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(A[0]+(B[0]-A[0])*tp,A[1]); ctx.stroke(); }
 if(up>0){ ctx.strokeStyle='#66a8ff'; ctx.lineWidth=s*0.05; ctx.beginPath(); ctx.moveTo(B[0],A[1]); ctx.lineTo(B[0],A[1]+(B[1]-A[1])*up); ctx.stroke(); }
 if(lp>0.3){ ctx.fillStyle='#fff'; for(const P0 of [A,B]){ ctx.beginPath(); ctx.arc(P0[0],P0[1],s*0.045,0,7); ctx.fill(); } }
 ctx.restore(); }
function wordmark(ctx,x,y,size,col,align='center',a=1){ if(a<=0) return; ctx.save(); ctx.globalAlpha*=a; ctx.direction='rtl'; ctx.textAlign=align; ctx.textBaseline='middle'; ctx.font=`800 ${size}px Cairo`; ctx.fillStyle=col; ctx.fillText(BR.name,x,y); ctx.restore(); }
// ---- intro / outro ----
function sIntro(lt){
 c.drawImage(bgc,0,0); // already dark (see draw)
 logoMark(c,960,380,230,cl(lt/1.6),{dark:true});
 wordmark(c,960,590,120,'#ffffff','center',P(lt,1.2,1.8));
 ar(BR.tag,960,690,40,'#a9d8c1',{a:P(lt,1.6,2.2),w:600,align:'center'});
 const ea=P(lt,2.2,2.8); if(ea>0){ c.save(); c.globalAlpha=ea; c.font='800 46px Cairo'; c.direction='rtl'; const w=c.measureText(EP.title).width+80; c.fillStyle=BR.gold; c.beginPath(); c.roundRect(960-w/2,780,w,84,42); c.fill(); c.restore();
  ar(EP.title,960,823,46,BR.navy,{a:ea,w:800,align:'center'}); ar(EP.sub,960,915,30,'rgba(255,255,255,.7)',{a:P(lt,2.5,3),w:600,align:'center'}); }
}
function sOutro(lt){
 logoMark(c,960,360,190,cl(lt/1.4));
 wordmark(c,960,540,104,BR.ink,'center',P(lt,1,1.5));
 ar(BR.tag,960,630,40,BR.green,{a:P(lt,1.4,1.9),w:700,align:'center'});
 c.save(); c.globalAlpha=P(lt,1.8,2.3); c.fillStyle='rgba(29,42,58,.12)'; c.fillRect(760,700,400,3); c.restore();
 ar(EP.next,960,770,34,K.muted,{a:P(lt,2.1,2.6),w:600,align:'center'});
}
const SCX=[[sIntro,3.6],...SC_CORE,[sOutro,4.5]];
const SC=SCX;
const START=[]; {let s=0; for(const x of SC){ START.push(s); s+=x[1]; } }
const TOTAL=START[START.length-1]+SC[SC.length-1][1];
function brandChrome(si,lt,dur){
 logoMark(c,74,70,56,1); wordmark(c,116,72,38,BR.ink,'left');
 ar(EP.title+' · '+EP.sub,1820,1042,24,K.muted,{w:600});
 const core=SC.length-2; for(let i=1;i<=core;i++){ const x=110+(i-1)*58; const f= i<si?1: i>si?0: cl(lt/dur);
  c.fillStyle='rgba(29,42,58,.09)'; c.beginPath(); c.roundRect(x,1036,46,8,4); c.fill();
  if(f>0){ const gr=c.createLinearGradient(x,0,x+46,0); gr.addColorStop(0,BR.green); gr.addColorStop(1,BR.mint); c.fillStyle=gr; c.beginPath(); c.roundRect(x,1036,46*f,8,4); c.fill(); } }
}
window.draw=function(T){ let si=SC.length-1; for(let i=0;i<SC.length;i++){ if(T<START[i]+SC[i][1]){ si=i; break; } } const lt=T-START[si], dur=SC[si][1];
 const dark = si===0; paintBG(bx,T,dark);
 c.setTransform(1,0,0,1,0,0); c.globalAlpha=1; c.drawImage(bgc,0,0); SC[si][0](lt);
 const fade=Math.min(1,cl(lt/0.4), cl((dur-lt)/0.4));
 if(si===0){ const f2=cl((dur-lt)/0.5); if(f2<1){ paintBG(bx,T,false); c.globalAlpha=1-f2; c.drawImage(bgc,0,0); c.globalAlpha=1; } }
 else if(fade<1 && !(si===SC.length-1 && lt>dur-0.4)){ c.globalAlpha=1-fade; c.drawImage(bgc,0,0); c.globalAlpha=1; }
 if(si>0 && si<SC.length-1) brandChrome(si,lt,dur);
 if(si===SC.length-1 && lt>dur-0.6){ c.fillStyle='#fbf6ea'; c.globalAlpha=cl((lt-(dur-0.6))/0.6); c.fillRect(0,0,W,H); c.globalAlpha=1; }
};
// ---- identity board & exports ----
window.board=function(){ paintBG(bx,0,false); c.setTransform(1,0,0,1,0,0); c.globalAlpha=1; c.drawImage(bgc,0,0);
 card(90,90,1740,900,1);
 // left: logo block (dark panel)
 c.save(); const g=c.createLinearGradient(130,130,800,950); g.addColorStop(0,'#1d2d40'); g.addColorStop(1,'#101a25'); c.fillStyle=g; c.beginPath(); c.roundRect(130,130,700,820,26); c.fill(); c.restore();
 c.save(); c.beginPath(); c.roundRect(130,130,700,820,26); c.clip(); blob(c,300,260,500,'rgba(63,208,140,.18)'); blob(c,760,900,500,'rgba(31,111,209,.22)'); c.restore();
 logoMark(c,480,390,250,1,{dark:true}); wordmark(c,480,620,130,'#fff'); ar(BR.tag,480,720,38,'#a9d8c1',{w:600,align:'center'});
 ar('هوية بصرية لمقاطع الرياضيات',480,880,28,'rgba(255,255,255,.55)',{w:600,align:'center'});
 // right: palette
 ar('الهوية البصرية',1780,180,56,BR.ink,{w:800});
 ar('الألوان',1780,270,32,K.muted,{w:700});
 const sw=[['حبر',BR.ink],['أخضر الميل',BR.green],['نعناع',BR.mint],['أزرق رأسي',BR.blue],['أحمر أفقي',BR.red],['ذهبي',BR.gold],['ورق',BR.paper]];
 sw.forEach(([nm,col],i)=>{ const x=1780-i*128-110, y=300; c.save(); c.fillStyle=col; c.strokeStyle='rgba(0,0,0,.08)'; c.lineWidth=2; c.beginPath(); c.roundRect(x,y,110,110,20); c.fill(); c.stroke(); c.restore();
  ar(nm,x+55,y+136,20,BR.ink,{w:700,align:'center'}); c.save(); c.font='400 18px "STIX Two Text"'; c.fillStyle=K.muted; c.textAlign='center'; c.fillText(col.toUpperCase(),x+55,y+164); c.restore(); });
 ar('الخطوط',1780,520,32,K.muted,{w:700});
 ar('Cairo — للنصوص العربية',1780,580,40,BR.ink,{w:800});
 c.save(); c.font='italic 400 40px "STIX Two Text"'; c.fillStyle=BR.ink; c.textAlign='right'; c.direction='ltr'; c.fillText('y = mx + b',1780,650); c.restore(); ar('STIX Two — للرموز الرياضية',1500,646,26,K.muted,{w:600});
 ar('قاعدة الألوان: الأزرق للتغير الرأسي، والأحمر للأفقي، والأخضر للميل',1780,740,28,BR.ink,{w:600});
 ar('الخلفية: ورق دافئ، شبكة نقاط، وهج أخضر وأزرق وذهبي',1780,790,28,BR.ink,{w:600});
 // mini lower bar sample
 c.save(); c.fillStyle='rgba(29,42,58,.05)'; c.beginPath(); c.roundRect(880,850,900,90,20); c.fill(); c.restore();
 logoMark(c,930,895,50,1); wordmark(c,970,897,34,BR.ink,'left'); ar('ميل المستقيم · الحلقة 1',1750,897,26,K.muted,{w:600});
};
window.bgOnly=function(){ paintBG(bx,0,false); c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,W,H); c.drawImage(bgc,0,0); logoMark(c,74,70,56,1); wordmark(c,116,72,38,BR.ink,'left'); };
window.logoOnly=function(){ c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,W,H); logoMark(c,640,540,520,1); wordmark(c,1300,560,300,BR.ink); ar(BR.tag,1300,760,60,BR.green,{w:700,align:'center'}); };
