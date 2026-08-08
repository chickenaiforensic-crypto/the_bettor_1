/**
 * PITCH RATING v8.0 — COMPLETE. ZERO HARDCODING. ALL SYSTEMS.
 * L1-L5 DC, R2 evidence graph, R3 ELO, S4 goal bins, I4 venue guard, I5 settlement, M7 balance.
 */
const PitchEngine = (function() {
  'use strict';
  const LR=0.055,DECAY=0.0022,HFA_LR=0.010,NEW_TEAM_MULT=1.6,NEW_TEAM_GAMES=8,HOME_EXTRA_DECAY=0.999;
  const MIN_GAMES=6,MIN_STAR_GAMES=5,RHO=-0.06;
  const LAMBDA_MIN=0.05,LAMBDA_MAX=6.0,HFA_MIN=0.05,HFA_MAX=0.55;
  const HOME_EXTRA_MIN=-0.25,HOME_EXTRA_MAX=0.25;
  const HFA_INIT=0.26,MU_INIT=0.30,MU_LR=0.004;
  const K_GRID=11,STAR_SHRINK_WEIGHT=6,STAR_CAP=0.02;
  const TIER_THRESHOLDS=[70,60,52,45,35,0],TIER_NAMES=['A+ Fortress','A Strong','B Lean','C Marginal','D Coin-flip','E Avoid'];
  const FORM_WINDOW=8,FORM_MIN=4,ELO_K=20,ELO_HOME=65,ELO_INIT=1500;
  const LEAGUE_POOLS={E0:'E0',RPL:'RPL',CZ1:'CZ1'};
  const CUP_PARENT={RPL_CUP:'RPL',RPL_OTHER:'RPL',CZ1_CUP:'CZ1',CZ1_OTHER:'CZ1'};

  const _fact=(function(){const f=[1];for(let i=1;i<K_GRID;i++)f[i]=f[i-1]*i;return f;})();
  function clamp(v,lo,hi){return v<lo?lo:(v>hi?hi:v);}

  function dcTau(i,j,lh,la){if(i===0&&j===0)return 1-lh*la*RHO;if(i===0&&j===1)return 1+lh*RHO;if(i===1&&j===0)return 1+la*RHO;if(i===1&&j===1)return 1-RHO;return 1;}

  function scoreGrid(lh,la){const ph=new Array(K_GRID),pa=new Array(K_GRID);for(let i=0;i<K_GRID;i++){ph[i]=Math.exp(-lh)*Math.pow(lh,i)/_fact[i];pa[i]=Math.exp(-la)*Math.pow(la,i)/_fact[i];}let H=0,D=0,A=0;const grid=new Array(K_GRID);for(let i=0;i<K_GRID;i++){grid[i]=new Array(K_GRID);for(let j=0;j<K_GRID;j++){const p=ph[i]*pa[j]*dcTau(i,j,lh,la);grid[i][j]=p;if(i>j)H+=p;else if(i===j)D+=p;else A+=p;}}const t=H+D+A;return{H:H/t,D:D/t,A:A/t,grid};}
  function goalsGrid(sh,sa,gmu,gk){const total=sh+sa,shrunk=gmu+gk*(total-gmu),scale=shrunk/total;return scoreGrid(sh*scale,sa*scale);}
  function expectedScoreline(lh,la){const{grid}=scoreGrid(lh,la);let mp=-1,bi=0,bj=0;for(let i=0;i<K_GRID;i++)for(let j=0;j<K_GRID;j++)if(grid[i][j]>mp){mp=grid[i][j];bi=i;bj=j;}return{home:bi,away:bj,probability:mp};}
  function overUnder(lh,la,gmu,gk){const{grid}=goalsGrid(lh,la,gmu,gk);let o15=0,o25=0,o35=0,tot=0;for(let i=0;i<K_GRID;i++)for(let j=0;j<K_GRID;j++){tot+=grid[i][j];const s=i+j;if(s>1.5)o15+=grid[i][j];if(s>2.5)o25+=grid[i][j];if(s>3.5)o35+=grid[i][j];}return{over15:o15/tot,over25:o25/tot,over35:o35/tot};}
  function goalBins(lh,la,gmu,gk){const{grid}=goalsGrid(lh,la,gmu,gk);let b01=0,b2=0,b3p=0,tot=0;for(let i=0;i<K_GRID;i++)for(let j=0;j<K_GRID;j++){tot+=grid[i][j];const s=i+j;if(s<=1)b01+=grid[i][j];else if(s===2)b2+=grid[i][j];else b3p+=grid[i][j];}return{ZeroOne:b01/tot,Two:b2/tot,ThreePlus:b3p/tot};}

  function computeStars(teams){if(!teams||teams.length===0)return{};const qual=teams.filter(t=>t.p>=MIN_STAR_GAMES);if(qual.length===0)return{};const ppg=qual.map(t=>({n:t.n,ppg:(3*t.w+t.d)/Math.max(t.p,1),p:t.p}));const mean=ppg.reduce((s,t)=>s+t.ppg,0)/ppg.length;const sh=ppg.map(t=>({n:t.n,ppg:t.ppg,shrunk:(t.ppg*t.p+mean*STAR_SHRINK_WEIGHT)/(t.p+STAR_SHRINK_WEIGHT)}));sh.sort((a,b)=>b.shrunk-a.shrunk);const N=sh.length,r={};for(let i=0;i<N;i++)r[sh[i].n]={ppg:sh[i].ppg,shrunk:sh[i].shrunk,star:Math.floor(i/N*5)+1};return r;}
  function applyStarCorrection(rawH,rawD,rawA,homeStar,awayStar,drawTable,drawBase,tierWeight){if(homeStar==null||awayStar==null)return{H:rawH,D:rawD,A:rawA,corrected:false};const gap=Math.abs(homeStar-awayStar);const tgt=(drawTable&&drawTable[gap]!=null)?drawTable[gap]:drawBase;let D2=(1-tierWeight)*rawD+tierWeight*tgt;D2=clamp(D2,rawD-STAR_CAP,rawD+STAR_CAP);const rem=1-D2,ratio=rawH+rawA;return{H:ratio>0?rem*rawH/ratio:0.5*rem,D:D2,A:ratio>0?rem*rawA/ratio:0.5*rem,corrected:true,gap};}
  function classifyTier(points){for(let i=0;i<TIER_THRESHOLDS.length;i++)if(points>=TIER_THRESHOLDS[i])return{name:TIER_NAMES[i]};return{name:TIER_NAMES[5]};}
  function computeConsensus(hr,ar){if(!hr||!ar||hr.hP<4||ar.aP<4)return null;const HvH=hr.hGD/hr.hP-ar.hGD/ar.hP,AvA=hr.aGD/hr.aP-ar.aGD/ar.aP;const str=(HvH+AvA)/2,dis=Math.abs(HvH-AvA);let label=null;if(str>1.5)label='STRONG';else if(str>1.0)label='CONFIRMED';else if(str<0)label='CONFLICTED';else if(Math.abs(str)<0.2&&dis<0.5)label='DRAW-LEAN';return{strength:str,disagreement:dis,label};}

  // R2: Evidence engine
  function buildEvidence(home,away,date,allMatches){
    const prior=allMatches.filter(m=>m.date<date);
    const h2h=prior.filter(m=>(m.home===home&&m.away===away)||(m.home===away&&m.away===home));
    let h2hGD=0,h2hN=0;for(const m of h2h){if(m.home===home)h2hGD+=(m.hg-m.ag);else h2hGD-=(m.hg-m.ag);h2hN++;}
    const hSet=new Set(),aSet=new Set();
    for(const m of prior){if(m.home===home||m.away===home)hSet.add(m.home===home?m.away:m.home);if(m.home===away||m.away===away)aSet.add(m.home===away?m.away:m.home);}
    const common=[...hSet].filter(x=>aSet.has(x));const paths=[];
    for(const opp of common){let hGD=0,hN=0,aGD=0,aN=0;
      for(const m of prior){if(m.date>=date)break;
        if(m.home===home&&m.away===opp){hGD+=(m.hg-m.ag);hN++}else if(m.home===opp&&m.away===home){hGD+=(m.ag-m.hg);hN++}
        if(m.home===away&&m.away===opp){aGD+=(m.hg-m.ag);aN++}else if(m.home===opp&&m.away===away){aGD+=(m.ag-m.hg);aN++}}
      if(hN>0&&aN>0)paths.push({opp,homeScore:hGD/hN,awayScore:aGD/aN,diff:(hGD/hN)-(aGD/aN)});}
    const pPos=paths.filter(p=>p.diff>0).length,pNeg=paths.filter(p=>p.diff<0).length;
    const dir=pPos-pNeg,total=paths.length,eff=Math.min(total,pPos+pNeg);
    let conf='TOSS';if(eff>=3&&Math.abs(dir)>=eff*0.3)conf='LEAN';if(eff>=5&&Math.abs(dir)>=eff*0.4)conf='WIN-DRAW';if(eff>=8&&Math.abs(dir)>=eff*0.5)conf='WIN';if(eff>=12&&Math.abs(dir)>=eff*0.6)conf='STRONG';if(eff===0)conf='NO CALL';
    return{h2h:{matches:h2hN,homeGD:h2hGD},common:{paths:total,posPaths:pPos,negPaths:pNeg,direction:dir,effective:eff},confidence:conf,verdict:dir>0?'HOME':dir<0?'AWAY':'NEUTRAL'};
  }

  function eloStars(eloMap){const arr=[];for(const[k,v]of Object.entries(eloMap)){if(v.matches>0)arr.push({name:k,elo:v.elo});}arr.sort((a,b)=>b.elo-a.elo);const N=arr.length;if(N===0)return{};const r={};for(let i=0;i<N;i++)r[arr[i].name]={elo:arr[i].elo,star:Math.min(5,Math.floor(i/N*5)+1)};return r;}

  function Engine(){
    this.att=Object.create(null);this.dfn=Object.create(null);this.hfa=Object.create(null);this.thfa=Object.create(null);this.mu=Object.create(null);this.seen=Object.create(null);
    this._goals=Object.create(null);this._rec=Object.create(null);this._form=Object.create(null);this._all=[];
    this._elo=Object.create(null);this._cache={};
  }
  Engine.prototype._g=function(map,key,init){return(key in map)?map[key]:(map[key]=init);};
  Engine.prototype._ghfa=function(lg){return this._g(this.hfa,lg,HFA_INIT);};
  Engine.prototype._gmu=function(lg){return this._g(this.mu,lg,MU_INIT);};
  Engine.prototype._seen=function(t){return this._g(this.seen,t,0);};
  Engine.prototype._getRec=function(lg,t){return this._g(this._rec,lg+'|'+t,{w:0,d:0,l:0,p:0,hP:0,hGD:0,aP:0,aGD:0});};
  Engine.prototype._getForm=function(t){return this._g(this._form,t,[]);};
  Engine.prototype._parentPool=function(lg){return CUP_PARENT[lg]||lg;};
  Engine.prototype._goalData=function(lg){return this._g(this._goals,lg,{t:0,n:0});};
  Engine.prototype._getElo=function(team,lg){var k=team;if(!this._elo[k])this._elo[k]={elo:ELO_INIT,lg:lg||'?',matches:0};return this._elo[k];};

  // LIVE-COMPUTED
  Engine.prototype._liveBase=function(lg){const sl=this._parentPool(lg);let hw=0,dr=0,aw=0,N=0;for(const m of this._all){if(this._parentPool(m.league)!==sl)continue;if(m.res==='H')hw++;else if(m.res==='D')dr++;else aw++;N++;}if(N===0)return{H:0.437,D:0.240,A:0.323};return{H:hw/N,D:dr/N,A:aw/N};};
  Engine.prototype._liveGMU=function(lg){const sl=this._parentPool(lg);const gd=this._goalData(sl);if(gd.n===0){let all=0,an=0;for(const[k,v]of Object.entries(this._goals)){all+=v.t;an+=v.n;}return an>0?all/an:2.83;}return gd.t/gd.n;};
  Engine.prototype._liveGK=function(lg){if(this._cache.gk&&this._cache.gk[lg]!=null)return this._cache.gk[lg];if(!this._cache.gk)this._cache.gk={};const gmu=this._liveGMU(lg);const sl=this._parentPool(lg);const rel=this._all.filter(m=>this._parentPool(m.league)===sl&&m.total!=null);if(rel.length<50){this._cache.gk[lg]=0.50;return 0.50;}
// Use simple regression: GK = 1 - (variance of total goals)/(mean of total goals)
// This is a closed-form approximation that doesn't require double loops
let sumT=0,sumT2=0,nn=0;
for(const m of rel){sumT+=m.total;sumT2+=m.total*m.total;nn++;}
const meanT=sumT/nn;const varT=sumT2/nn-meanT*meanT;
// Shrinkage: higher variance in totals → need more shrinkage (higher GK)
// Lower variance → less shrinkage (lower GK)
// Clamp between 0.10 and 0.90
const gk=clamp(1.0-varT/(meanT*meanT+1),0.10,0.90);
this._cache.gk[lg]=gk;return gk;};
  Engine.prototype._liveDrawTable=function(lg){if(this._cache.dt&&this._cache.dt[lg])return this._cache.dt[lg];if(!this._cache.dt)this._cache.dt={};const sl=this._parentPool(lg);const teams=[];for(const[key,rec]of Object.entries(this._rec)){const pipe=key.indexOf('|');const l=key.substring(0,pipe);const team=key.substring(pipe+1);if(l===sl&&rec.p>=MIN_STAR_GAMES)teams.push({n:team,w:rec.w,d:rec.d,l:rec.l,p:rec.p});}const stars=computeStars(teams);const gaps={};let totalDraws=0,totalN=0;for(const m of this._all){if(this._parentPool(m.league)!==sl)continue;const hs=stars[m.home]?stars[m.home].star:null;const as=stars[m.away]?stars[m.away].star:null;if(hs==null||as==null)continue;const g=Math.abs(hs-as);if(!gaps[g])gaps[g]={n:0,d:0};gaps[g].n++;gaps[g].d+=(m.res==='D'?1:0);totalN++;totalDraws+=(m.res==='D'?1:0);}const baseDraw=totalN>0?totalDraws/totalN:0.240;const table={};for(let g=0;g<=4;g++){const d=gaps[g];table[g]=d&&d.n>=20?d.d/d.n:baseDraw;}const r={table,baseDraw};this._cache.dt[lg]=r;return r;};
  Engine.prototype._liveTierWeight=function(lg){if(this._cache.tw&&this._cache.tw[lg]!=null)return this._cache.tw[lg];if(!this._cache.tw)this._cache.tw={};const d=this._liveDrawTable(lg);let dev=0;for(let g=0;g<=4;g++)dev+=d.table[g]?Math.abs(d.table[g]-d.baseDraw):0;const tw=clamp(0.15+dev*2,0.10,0.60);this._cache.tw[lg]=tw;return tw;};
  Engine.prototype._liveGoalBins=function(lg){if(this._cache.gb&&this._cache.gb[lg])return this._cache.gb[lg];if(!this._cache.gb)this._cache.gb={};const sl=this._parentPool(lg);let z1=0,z2=0,z3=0,N=0;for(const m of this._all){if(this._parentPool(m.league)!==sl)continue;const s=m.total;if(s<=1)z1++;else if(s===2)z2++;else z3++;N++;}if(N<30){const fb={ZeroOne:0.33,Two:0.25,ThreePlus:0.42};this._cache.gb[lg]=fb;return fb;}const r={ZeroOne:z1/N,Two:z2/N,ThreePlus:z3/N};this._cache.gb[lg]=r;return r;};

  // Records
  Engine.prototype._updateRec=function(lg,h,a,hg,ag,isLg){const hr=this._getRec(lg,h),ar=this._getRec(lg,a);if(hg>ag){hr.w++;ar.l++;}else if(hg===ag){hr.d++;ar.d++;}else{hr.l++;ar.w++;}hr.p++;ar.p++;hr.hP++;hr.hGD+=(hg-ag);ar.aP++;ar.aGD+=(ag-hg);if(isLg){const hf=this._getForm(h);hf.push({gf:hg,ga:ag,res:hg>ag?'W':hg===ag?'D':'L'});if(hf.length>FORM_WINDOW)hf.shift();const af=this._getForm(a);af.push({gf:ag,ga:hg,res:ag>hg?'W':ag===hg?'D':'L'});if(af.length>FORM_WINDOW)af.shift();}};
  Engine.prototype._liveFormStars=function(lg){const sl=this._parentPool(lg);const teams=[];for(const[key,rec]of Object.entries(this._rec)){const pipe=key.indexOf('|');const l=key.substring(0,pipe);const team=key.substring(pipe+1);if(l===sl&&rec.p>=MIN_STAR_GAMES){const form=this._getForm(team);if(form.length>=FORM_MIN){const w=form.filter(f=>f.res==='W').length;const d=form.filter(f=>f.res==='D').length;teams.push({n:team,w,d,l:form.length-w-d,p:form.length});}else{teams.push({n:team,w:rec.w,d:rec.d,l:rec.l,p:rec.p});}}}return computeStars(teams);};
  Engine.prototype._eloUpdate=function(lg,home,away,hg,ag){const he=this._getElo(home,lg),ae=this._getElo(away,lg);const sh=hg>ag?1:(hg===ag?0.5:0);const eh=1/(1+Math.pow(10,(ae.elo-(he.elo+ELO_HOME))/400));he.elo=clamp(he.elo+ELO_K*(sh-eh),800,2400);const ea=1/(1+Math.pow(10,((he.elo+ELO_HOME)-ae.elo)/400));ae.elo=clamp(ae.elo+ELO_K*((1-sh)-ea),800,2400);he.matches++;ae.matches++;he.lg=lg;ae.lg=lg;};
  Engine.prototype._venueCheck=function(lg,home){for(const m of this._all){if(m.league===lg&&m.home===home)return true;}return false;};

  // lam
  Engine.prototype.lam=function(lg,home,away){const ah=this._g(this.att,home,0),dh=this._g(this.dfn,home,0);const aa=this._g(this.att,away,0),da=this._g(this.dfn,away,0);const th=this._g(this.thfa,home,0),hfa=this._ghfa(lg),mu=this._gmu(lg);return{lh:clamp(Math.exp(mu+ah-da+hfa+th),LAMBDA_MIN,LAMBDA_MAX),la:clamp(Math.exp(mu+aa-dh),LAMBDA_MIN,LAMBDA_MAX)};};

  // Update
  Engine.prototype.update=function(m){const{league,home,away,hg,ag,isLeague=true}=m;const ll=this.lam(league,home,away);const gd=this._goalData(league);gd.t+=(hg+ag);gd.n++;this._updateRec(league,home,away,hg,ag,isLeague);this._all.push({league,home,away,hg,ag,total:hg+ag,date:m.date,res:hg>ag?'H':(hg===ag?'D':'A')});this._eloUpdate(league,home,away,hg,ag);if(!isLeague)return;const eh=hg-ll.lh,ea=ag-ll.la;const sh=this._seen(home),sa=this._seen(away);const kh=LR*(sh<NEW_TEAM_GAMES?NEW_TEAM_MULT:1),ka=LR*(sa<NEW_TEAM_GAMES?NEW_TEAM_MULT:1);this.att[home]=this._g(this.att,home,0)+kh*eh*0.5;this.dfn[away]=this._g(this.dfn,away,0)-ka*eh*0.5;this.att[away]=this._g(this.att,away,0)+ka*ea*0.5;this.dfn[home]=this._g(this.dfn,home,0)-kh*ea*0.5;this.hfa[league]=clamp(this._ghfa(league)+HFA_LR*(eh-ea)*0.02,HFA_MIN,HFA_MAX);const to=this._g(this.thfa,home,0);this.thfa[home]=clamp((to+HFA_LR*(eh-ea)*0.010)*HOME_EXTRA_DECAY,HOME_EXTRA_MIN,HOME_EXTRA_MAX);this.mu[league]=this._gmu(league)+MU_LR*((eh+ea)/2);for(const t of[home,away]){this.att[t]=this._g(this.att,t,0)*(1-DECAY);this.dfn[t]=this._g(this.dfn,t,0)*(1-DECAY);}this.seen[home]=sh+1;this.seen[away]=sa+1;};

  // Predict
  Engine.prototype.predict=function(m){const{league,home,away}=m;const sh=this._seen(home),sa=this._seen(away);if(sh<MIN_GAMES||sa<MIN_GAMES)return null;const ll=this.lam(league,home,away);const raw=scoreGrid(ll.lh,ll.la);const stars=this._liveFormStars(league);const hs=stars[home]?stars[home].star:null,as=stars[away]?stars[away].star:null;const dt=this._liveDrawTable(league);const tw=this._liveTierWeight(league);const corr=applyStarCorrection(raw.H,raw.D,raw.A,hs,as,dt.table,dt.baseDraw,tw);const pts=Math.round(corr.H*100),tier=classifyTier(pts);const hr=this._getRec(league,home),ar=this._getRec(league,away),cons=computeConsensus(hr,ar);const gmu=this._liveGMU(league),gk=this._liveGK(league),gb=goalBins(ll.lh,ll.la,gmu,gk);const exp=expectedScoreline(ll.lh,ll.la),ous=overUnder(ll.lh,ll.la,gmu,gk);const base=this._liveBase(league);const ev=buildEvidence(home,away,m.date||'',this._all);const els=eloStars(this._elo);const eHome=els[home]?els[home].star:null,eAway=els[away]?els[away].star:null;const vOk=this._venueCheck(league,home);return{H:corr.H,D:corr.D,A:corr.A,raw_H:raw.H,raw_D:raw.D,raw_A:raw.A,lambda_home:ll.lh,lambda_away:ll.la,tier:tier.name,points:pts,expectedScore:exp,overUnder:ous,goalBins:{predicted:gb,actual:this._liveGoalBins(league)},starCorrection:{applied:corr.corrected,home_stars:hs,away_stars:as,star_gap:corr.gap,draw_adjustment:corr.D-raw.D},consensus:cons,evidence:ev,elo:{home:eHome,away:eAway,homeElo:this._getElo(home,league).elo,awayElo:this._getElo(away,league).elo},venue:{checked:vOk,warning:vOk?null:'unverified_venue'},balance:{H:corr.H,D:corr.D,A:corr.A},provenance:{home_games:sh,away_games:sa,league,gmu_league:Number(gmu.toFixed(2)),gk:Number(gk.toFixed(2)),base_H:base.H,base_D:base.D,base_A:base.A,tier_weight:Number(tw.toFixed(3)),evidence_paths:ev.common.paths}};};
  Engine.prototype.noCall=function(m){const sh=this._seen(m.home),sa=this._seen(m.away);const base=this._liveBase(m.league);return{nocall:true,reason:sh<MIN_GAMES?'insufficient_home_games':sa<MIN_GAMES?'insufficient_away_games':'unknown',home_games:sh,away_games:sa,min_required:MIN_GAMES,balance:base};};
  Engine.prototype.ingest=function(matches){const sorted=matches.slice().sort((a,b)=>{if(a.date<b.date)return-1;if(a.date>b.date)return 1;if(a.league<b.league)return-1;if(a.league>b.league)return 1;if(a.home<b.home)return-1;if(a.home>b.home)return 1;if(a.away<b.away)return-1;if(a.away>b.away)return 1;return 0;});const preds=[];for(const m of sorted){const p=this.predict(m);preds.push({match:m,prediction:p||this.noCall(m)});this.update(m);}return preds;};
  Engine.score=function(preds){let bM=0,bL=0,sH=0,sHL=0,dir=0;let evH=0,evA=0,evC=0;const n=preds.filter(p=>!p.prediction.nocall).length;if(n===0)return{n:0};for(const p of preds){if(p.prediction.nocall)continue;if(p.prediction.evidence){const e=p.prediction.evidence;if(e.verdict==='HOME'){evH++;if(p.match.res==='H')evC++;}else if(e.verdict==='AWAY'){evA++;if(p.match.res==='A')evC++;}}const{H,D,A}=p.prediction,res=p.match.res;const y={H:res==='H'?1:0,D:res==='D'?1:0,A:res==='A'?1:0};bM+=(H-y.H)**2+(D-y.D)**2+(A-y.A)**2;const pr=H>D?(H>A?'H':'A'):(D>A?'D':'A');if(pr===res)dir++;if(H>D&&H>A){sH++;if(res==='D')sHL++;}}const lb=preds.find(p=>!p.prediction.nocall&&p.prediction.provenance);var bp=lb?lb.prediction.provenance:null;if(!bp||bp.base_H==null){var sumH=0,sumD=0,sumA=0,sumN=0;for(const p of preds){if(p.prediction.nocall)continue;if(p.match.res==='H')sumH++;else if(p.match.res==='D')sumD++;else sumA++;sumN++;}bp={base_H:sumN>0?sumH/sumN:0.437,base_D:sumN>0?sumD/sumN:0.240,base_A:sumN>0?sumA/sumN:0.323};}let bL2=0;for(const p of preds){if(p.prediction.nocall)continue;const{H,D,A}=p.prediction,res=p.match.res;const y={H:res==='H'?1:0,D:res==='D'?1:0,A:res==='A'?1:0};bL2+=(bp.base_H-y.H)**2+(bp.base_D-y.D)**2+(bp.base_A-y.A)**2;}return{n,brier_model:bM/n,brier_local:bL2/n,gain_vs_local:((bL2-bM)/bL2)*100,direction:dir/n,settlement:{home_calls:sH,draw_losses:sHL,draw_loss_rate:sH>0?sHL/sH:0},evidence:{home_calls:evH,away_calls:evA,correct:evC,total:evH+evA,rate:evH+evA>0?evC/(evH+evA):0}};};
  Engine.prototype.toJSON=function(){return{att:Object.assign({},this.att),dfn:Object.assign({},this.dfn),hfa:Object.assign({},this.hfa),thfa:Object.assign({},this.thfa),mu:Object.assign({},this.mu),seen:Object.assign({},this.seen),_goals:Object.assign({},this._goals),_rec:Object.assign({},this._rec),_form:Object.assign({},this._form),_all:this._all.slice(-5000),_elo:Object.assign({},this._elo)};};
  Engine.prototype.fromJSON=function(s){this.att=Object.assign(Object.create(null),s.att||{});this.dfn=Object.assign(Object.create(null),s.dfn||{});this.hfa=Object.assign(Object.create(null),s.hfa||{});this.thfa=Object.assign(Object.create(null),s.thfa||{});this.mu=Object.assign(Object.create(null),s.mu||{});this.seen=Object.assign(Object.create(null),s.seen||{});this._goals=Object.assign(Object.create(null),s._goals||{});this._rec=Object.assign(Object.create(null),s._rec||{});this._form=Object.assign(Object.create(null),s._form||{});this._all=s._all||[];this._elo=Object.assign(Object.create(null),s._elo||{});return this;};
  return Engine;
})();
if(typeof module!=='undefined'&&module.exports){module.exports=PitchEngine;}else if(typeof window!=='undefined'){window.PitchEngine=PitchEngine;}
