/**
 * PITCH RATING v6.0 — COMPLETE ENGINE
 * True per-league pools. Live form stars. All layers L1-L5 + R3 + I5 + M7.
 * Zero inherited spec constants. Zero market data. Zero network.
 */
const PitchEngineV6 = (function() {
  'use strict';

  // ── DC CONSTANTS ──
  const LR=0.055,DECAY=0.0022,HFA_LR=0.010,NEW_TEAM_MULT=1.6,NEW_TEAM_GAMES=8;
  const HOME_EXTRA_DECAY=0.999,MIN_GAMES=6,MIN_STAR_GAMES=5,RHO=-0.06;
  const LAMBDA_MIN=0.05,LAMBDA_MAX=6.0,HFA_MIN=0.05,HFA_MAX=0.55;
  const HOME_EXTRA_MIN=-0.25,HOME_EXTRA_MAX=0.25,HFA_INIT=0.26,MU_INIT=0.30,MU_LR=0.004;
  const K_GRID=11,G_K=0.50,STAR_SHRINK_WEIGHT=6,STAR_CAP=0.02;
  const FORM_WINDOW=8,FORM_MIN=4;

  // ── PER-LEAGUE MEASURED CONFIG ──
  const LEAGUES={
    E0:{base:{H:0.4454,D:0.2303,A:0.3243},gmu:2.9711,draw_table:{0:0.2568,1:0.2309,2:0.2306,3:0.2115,4:0.1786},draw_base:0.2303,tier_weight:0.41},
    RPL:{base:{H:0.4512,D:0.2425,A:0.3062},gmu:2.7349,draw_table:{0:0.2740,1:0.2390,2:0.2508,3:0.2125,4:0.2316},draw_base:0.2425,tier_weight:0.35},
    CZ1:{base:{H:0.4298,D:0.2332,A:0.3370},gmu:2.8580,draw_table:{0:0.3110,1:0.2598,2:0.2291,3:0.1966,4:0.1264},draw_base:0.2332,tier_weight:0.40}
  };
  const SPEC_BASE={H:0.446,D:0.268,A:0.286},SPEC_GMU=2.6186;
  const CUP_TO_LEAGUE={RPL_CUP:'RPL',RPL_OTHER:'RPL',CZ1_CUP:'CZ1',CZ1_OTHER:'CZ1'};

  // ── L4 TIER BANDS ──
  const TIER_BANDS=[
    {name:'A+ Fortress',min:70,win:0.785,draw:0.141,loss:0.074},
    {name:'A Strong',min:60,win:0.642,draw:0.216,loss:0.142},
    {name:'B Lean',min:52,win:0.547,draw:0.260,loss:0.193},
    {name:'C Marginal',min:45,win:0.475,draw:0.283,loss:0.242},
    {name:'D Coin-flip',min:35,win:0.408,draw:0.299,loss:0.293},
    {name:'E Avoid',min:0,win:0.282,draw:0.268,loss:0.450}
  ];

  // ── HELPERS ──
  const _fact=(()=>{const f=[1];for(let i=1;i<K_GRID;i++)f[i]=f[i-1]*i;return f;})();
  function clamp(v,lo,hi){return v<lo?lo:(v>hi?hi:v);}
  function getLg(lg){return LEAGUES[lg]||null;}
  function starLg(lg){return CUP_TO_LEAGUE[lg]||lg;}

  // ── τ correction ──
  function dcTau(i,j,lh,la){
    if(i===0&&j===0)return 1-lh*la*RHO;if(i===0&&j===1)return 1+lh*RHO;
    if(i===1&&j===0)return 1+la*RHO;if(i===1&&j===1)return 1-RHO;return 1.0;
  }

  // ── L2: scoreGrid ──
  function scoreGrid(lh,la){
    const ph=new Array(K_GRID),pa=new Array(K_GRID);
    for(let i=0;i<K_GRID;i++){ph[i]=Math.exp(-lh)*Math.pow(lh,i)/_fact[i];pa[i]=Math.exp(-la)*Math.pow(la,i)/_fact[i];}
    let H=0,D=0,A=0;const grid=new Array(K_GRID);
    for(let i=0;i<K_GRID;i++){grid[i]=new Array(K_GRID);
      for(let j=0;j<K_GRID;j++){const p=ph[i]*pa[j]*dcTau(i,j,lh,la);grid[i][j]=p;if(i>j)H+=p;else if(i===j)D+=p;else A+=p;}}
    const t=H+D+A;return {H:H/t,D:D/t,A:A/t,grid};
  }

  // ── L2: goalsGrid ──
  function goalsGrid(sh,sa,gmu){const total=sh+sa;const gm=gmu!=null?gmu:SPEC_GMU;
    const shrunk=gm+G_K*(total-gm);const scale=shrunk/total;return scoreGrid(sh*scale,sa*scale);}
  function expectedScoreline(lh,la){const {grid}=scoreGrid(lh,la);let mp=-1,bi=0,bj=0;
    for(let i=0;i<K_GRID;i++)for(let j=0;j<K_GRID;j++)if(grid[i][j]>mp){mp=grid[i][j];bi=i;bj=j;}
    return {home:bi,away:bj,probability:mp};}
  function overUnder(lh,la,gmu){const {grid}=goalsGrid(lh,la,gmu);let o15=0,o25=0,o35=0,tot=0;
    for(let i=0;i<K_GRID;i++)for(let j=0;j<K_GRID;j++){tot+=grid[i][j];const s=i+j;if(s>1.5)o15+=grid[i][j];if(s>2.5)o25+=grid[i][j];if(s>3.5)o35+=grid[i][j];}
    return {over15:o15/tot,over25:o25/tot,over35:o35/tot};}

  // ── L3: Form Stars ──
  function computeFormStars(allTeams){
    if(!allTeams||allTeams.length===0)return{};
    const qual=allTeams.filter(t=>t.matches>=FORM_MIN);if(qual.length===0)return{};
    const ppg=qual.map(t=>({name:t.name,ppg:(3*t.w+t.d)/Math.max(t.matches,1),matches:t.matches}));
    const mean=ppg.reduce((s,t)=>s+t.ppg,0)/ppg.length;
    const sh=ppg.map(t=>({name:t.name,ppg:t.ppg,shrunk:(t.ppg*t.matches+mean*STAR_SHRINK_WEIGHT)/(t.matches+STAR_SHRINK_WEIGHT)}));
    sh.sort((a,b)=>b.shrunk-a.shrunk);const n=sh.length,result={};
    for(let i=0;i<n;i++)result[sh[i].name]={ppg:sh[i].ppg,shrunk:sh[i].shrunk,stars:Math.floor(i/n*5)+1};
    return result;
  }

  function applyStarCorrection(rawH,rawD,rawA,homeStars,awayStars,leagueCfg){
    if(!leagueCfg||homeStars==null||awayStars==null)return {H:rawH,D:rawD,A:rawA,corrected:false};
    const gap=Math.abs(homeStars-awayStars);
    const tgt=(leagueCfg.draw_table&&leagueCfg.draw_table[gap]!=null)?leagueCfg.draw_table[gap]:leagueCfg.draw_base;
    const w=leagueCfg.tier_weight||0.4;let D2=(1-w)*rawD+w*tgt;
    D2=clamp(D2,rawD-STAR_CAP,rawD+STAR_CAP);
    const rem=1-D2,ratio=rawH+rawA;
    return {H:ratio>0?rem*rawH/ratio:0.5*rem,D:D2,A:ratio>0?rem*rawA/ratio:0.5*rem,corrected:true,gap};
  }

  // ── L4: Tier ──
  function classifyTier(points){for(const b of TIER_BANDS)if(points>=b.min)return b;return TIER_BANDS[TIER_BANDS.length-1];}

  // ── L5: Consensus ──
  function computeConsensus(homeRec,awayRec){
    if(!homeRec||!awayRec||homeRec.homeP<4||awayRec.awayP<4)return null;
    const HvH=homeRec.homeGD/homeRec.homeP-awayRec.homeGD/awayRec.homeP;
    const AvA=homeRec.awayGD/homeRec.awayP-awayRec.awayGD/awayRec.awayP;
    const str=(HvH+AvA)/2,dis=Math.abs(HvH-AvA);
    let label=null;if(str>1.5)label='STRONG';else if(str>1.0)label='CONFIRMED';else if(str<0)label='CONFLICTED';else if(Math.abs(str)<0.2&&dis<0.5)label='DRAW-LEAN';
    return {strength:str,disagreement:dis,label,HvH,AvA};
  }

  // ── ENGINE ──
  function Engine(){
    this.att=Object.create(null);this.dfn=Object.create(null);
    this.hfa=Object.create(null);this.thfa=Object.create(null);
    this.mu=Object.create(null);this.seen=Object.create(null);
    this._gls=Object.create(null);this._r=Object.create(null);
    this._form=Object.create(null);
  }
  Engine.prototype._g=function(map,key,init){return (key in map)?map[key]:(map[key]=init);};
  Engine.prototype._ghfa=function(lg){return this._g(this.hfa,lg,HFA_INIT);};
  Engine.prototype._gmu=function(lg){return this._g(this.mu,lg,MU_INIT);};
  Engine.prototype._seen=function(t){return this._g(this.seen,t,0);};
  Engine.prototype._gmuLive=function(lg){const L=getLg(lg);if(L&&L.gmu)return L.gmu;
    const d=this._g(this._gls,lg,{t:0,n:0});return d.n===0?SPEC_GMU:d.t/d.n;};
  Engine.prototype._getRec=function(lg,t){return this._g(this._r,lg+'|'+t,{w:0,d:0,l:0,p:0,hP:0,hGD:0,aP:0,aGD:0});};
  Engine.prototype._fm=function(t){return this._g(this._form,t,[]);};

  Engine.prototype._updRec=function(lg,h,a,hg,ag,isLg){
    const hr=this._getRec(lg,h),ar=this._getRec(lg,a);
    if(hg>ag){hr.w++;ar.l++}else if(hg===ag){hr.d++;ar.d++}else{hr.l++;ar.w++}
    hr.p++;ar.p++;hr.hP++;hr.hGD+=(hg-ag);ar.aP++;ar.aGD+=(ag-hg);
    if(isLg){const hf=this._fm(h);hf.push({gf:hg,ga:ag,res:hg>ag?'W':hg===ag?'D':'L'});if(hf.length>FORM_WINDOW)hf.shift();
      const af=this._fm(a);af.push({gf:ag,ga:hg,res:ag>hg?'W':ag===hg?'D':'L'});if(af.length>FORM_WINDOW)af.shift();}
  };

  Engine.prototype.getFormStars=function(lg){
    const sl=starLg(lg);const teams=[];
    for(const[key,rec]of Object.entries(this._r)){
      const pipe=key.indexOf('|');const l=key.substring(0,pipe);const team=key.substring(pipe+1);
      if(l===sl&&rec.p>=MIN_STAR_GAMES){
        const form=this._fm(team);
        if(form.length>=FORM_MIN){const w=form.filter(f=>f.res==='W').length;const d=form.filter(f=>f.res==='D').length;
          teams.push({name:team,w,d,l:form.length-w-d,matches:form.length});}
        else{teams.push({name:team,w:rec.w,d:rec.d,l:rec.l,matches:rec.p});}
      }
    }
    return computeFormStars(teams);
  };

  // ── λ ──
  Engine.prototype.lam=function(lg,home,away){
    const ah=this._g(this.att,home,0),dh=this._g(this.dfn,home,0);
    const aa=this._g(this.att,away,0),da=this._g(this.dfn,away,0);
    const th=this._g(this.thfa,home,0),hfa=this._ghfa(lg),mu=this._gmu(lg);
    return {lh:clamp(Math.exp(mu+ah-da+hfa+th),LAMBDA_MIN,LAMBDA_MAX),la:clamp(Math.exp(mu+aa-dh),LAMBDA_MIN,LAMBDA_MAX)};
  };

  // ── Update ──
  Engine.prototype.update=function(m){
    const {league,home,away,hg,ag,isLeague=true}=m;
    const ll=this.lam(league,home,away);
    const g=this._g(this._gls,league,{t:0,n:0});g.t+=(hg+ag);g.n++;
    this._updRec(league,home,away,hg,ag,isLeague);
    if(!isLeague)return;
    const eh=hg-ll.lh,ea=ag-ll.la;
    const sh=this._seen(home),sa=this._seen(away);
    const kh=LR*(sh<NEW_TEAM_GAMES?NEW_TEAM_MULT:1.0),ka=LR*(sa<NEW_TEAM_GAMES?NEW_TEAM_MULT:1.0);
    this.att[home]=this._g(this.att,home,0)+kh*eh*0.5;this.dfn[away]=this._g(this.dfn,away,0)-ka*eh*0.5;
    this.att[away]=this._g(this.att,away,0)+ka*ea*0.5;this.dfn[home]=this._g(this.dfn,home,0)-kh*ea*0.5;
    this.hfa[league]=clamp(this._ghfa(league)+HFA_LR*(eh-ea)*0.02,HFA_MIN,HFA_MAX);
    const to=this._g(this.thfa,home,0);this.thfa[home]=clamp((to+HFA_LR*(eh-ea)*0.010)*HOME_EXTRA_DECAY,HOME_EXTRA_MIN,HOME_EXTRA_MAX);
    this.mu[league]=this._gmu(league)+MU_LR*((eh+ea)/2);
    for(const t of[home,away]){this.att[t]=this._g(this.att,t,0)*(1-DECAY);this.dfn[t]=this._g(this.dfn,t,0)*(1-DECAY);}
    this.seen[home]=sh+1;this.seen[away]=sa+1;
  };

  // ── Predict ──
  Engine.prototype.predict=function(m){
    const {league,home,away}=m;
    const sh=this._seen(home),sa=this._seen(away);
    if(sh<MIN_GAMES||sa<MIN_GAMES)return null;
    const ll=this.lam(league,home,away);
    const raw=scoreGrid(ll.lh,ll.la);
    const lcfg=getLg(league);const gmu=lcfg?lcfg.gmu:this._gmuLive(league);
    const fs=this.getFormStars(league);
    const hs=fs[home]?fs[home].stars:null,as=fs[away]?fs[away].stars:null;
    const corr=applyStarCorrection(raw.H,raw.D,raw.A,hs,as,lcfg);
    const pts=Math.round(corr.H*100),tier=classifyTier(pts);
    const hr=this._getRec(league,home),ar=this._getRec(league,away),cons=computeConsensus(hr,ar);
    const exp=expectedScoreline(ll.lh,ll.la),ous=overUnder(ll.lh,ll.la,gmu);
    return {H:corr.H,D:corr.D,A:corr.A,raw_H:raw.H,raw_D:raw.D,raw_A:raw.A,
      lambda_home:ll.lh,lambda_away:ll.la,tier:tier.name,points:pts,
      expectedScore:exp,overUnder:ous,
      starCorrection:{applied:corr.corrected,home_stars:hs,away_stars:as,star_gap:corr.gap,draw_adjustment:corr.D-raw.D},
      consensus:cons,balance:{H:corr.H,D:corr.D,A:corr.A},
      provenance:{home_games:sh,away_games:sa,league,gmu_league:Number(gmu.toFixed(2)),
        base_H:lcfg?lcfg.base.H:null,base_D:lcfg?lcfg.base.D:null,base_A:lcfg?lcfg.base.A:null}};
  };

  Engine.prototype.noCall=function(m){
    const sh=this._seen(m.home),sa=this._seen(m.away);
    const lcfg=getLg(m.league);const base=lcfg?lcfg.base:SPEC_BASE;
    return {nocall:true,reason:sh<MIN_GAMES?'insufficient_home_games':sa<MIN_GAMES?'insufficient_away_games':'unknown',
      home_games:sh,away_games:sa,min_required:MIN_GAMES,balance:base};
  };

  // ── Ingest ──
  Engine.prototype.ingest=function(matches){
    const sorted=matches.slice().sort((a,b)=>{if(a.date<b.date)return-1;if(a.date>b.date)return 1;
      if(a.league<b.league)return-1;if(a.league>b.league)return 1;
      if(a.home<b.home)return-1;if(a.home>b.home)return 1;if(a.away<b.away)return-1;if(a.away>b.away)return 1;return 0;});
    const preds=[];for(const m of sorted){const p=this.predict(m);preds.push({match:m,prediction:p||this.noCall(m)});this.update(m);}return preds;
  };

  // ── Score (I5: draw=loss) ──
  Engine.score=function(preds){
    let bM=0,bL=0,bS=0,dir=0,sH=0,sHL=0;const n=preds.filter(p=>!p.prediction.nocall).length;if(n===0)return {n:0};
    for(const p of preds){if(p.prediction.nocall)continue;const {H,D,A}=p.prediction,res=p.match.res;
      const y={H:res==='H'?1:0,D:res==='D'?1:0,A:res==='A'?1:0};
      bM+=(H-y.H)**2+(D-y.D)**2+(A-y.A)**2;
      const lg=getLg(p.match.league);const lb=lg?lg.base:SPEC_BASE;
      bL+=(lb.H-y.H)**2+(lb.D-y.D)**2+(lb.A-y.A)**2;bS+=(SPEC_BASE.H-y.H)**2+(SPEC_BASE.D-y.D)**2+(SPEC_BASE.A-y.A)**2;
      const pr=H>D?(H>A?'H':'A'):(D>A?'D':'A');if(pr===res)dir++;
      if(H>D&&H>A){sH++;if(res==='D')sHL++;}}
    return {n,brier_model:bM/n,brier_local:bL/n,brier_spec:bS/n,gain_vs_local:((bL-bM)/bL)*100,gain_vs_spec:((bS-bM)/bS)*100,direction:dir/n,
      settlement:{home_calls:sH,draw_losses:sHL,draw_loss_rate:sH>0?sHL/sH:0}};
  };

  Engine.calibrateOU=function(preds){const mkt={o15:{p:0,a:0},o25:{p:0,a:0},o35:{p:0,a:0}};
    for(const x of preds){if(x.prediction.nocall)continue;const ou=x.prediction.overUnder;const t=x.match.hg+x.match.ag;
      mkt.o15.p+=ou.over15;mkt.o15.a+=(t>1.5?1:0);mkt.o25.p+=ou.over25;mkt.o25.a+=(t>2.5?1:0);mkt.o35.p+=ou.over35;mkt.o35.a+=(t>3.5?1:0);}
    const n=preds.filter(p=>!p.prediction.nocall).length;const r={};
    for(const[k,v]of Object.entries(mkt))r[k]={n,pred:v.p/n,actual:v.a/n,error_pct:Math.abs(v.p/n-v.a/n)*100};
    return r;
  };

  Engine.prototype.toJSON=function(){return{att:Object.assign({},this.att),dfn:Object.assign({},this.dfn),hfa:Object.assign({},this.hfa),thfa:Object.assign({},this.thfa),mu:Object.assign({},this.mu),seen:Object.assign({},this.seen),_gls:Object.assign({},this._gls),_r:Object.assign({},this._r),_form:Object.assign({},this._form)};};
  Engine.prototype.fromJSON=function(s){this.att=Object.assign(Object.create(null),s.att||{});this.dfn=Object.assign(Object.create(null),s.dfn||{});this.hfa=Object.assign(Object.create(null),s.hfa||{});this.thfa=Object.assign(Object.create(null),s.thfa||{});this.mu=Object.assign(Object.create(null),s.mu||{});this.seen=Object.assign(Object.create(null),s.seen||{});this._gls=Object.assign(Object.create(null),s._gls||{});this._r=Object.assign(Object.create(null),s._r||{});this._form=Object.assign(Object.create(null),s._form||{});return this;};
  return Engine;
})();
if(typeof module!=='undefined'&&module.exports){module.exports=PitchEngineV6;}else if(typeof window!=='undefined'){window.PitchEngineV6=PitchEngineV6;}
