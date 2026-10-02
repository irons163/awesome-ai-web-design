;!function(){try { var e="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof global?global:"undefined"!=typeof window?window:"undefined"!=typeof self?self:{},n=(new e.Error).stack;n&&((e._debugIds|| (e._debugIds={}))[n]="fa89f67f-6818-b1e0-7127-de5c8edd7185")}catch(e){}}();
(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,91262,193294,e=>{"use strict";var t=e.i(338149),a=e.i(299360),i=e.i(504646),r=e.i(245799),n=e.i(546153),s=e.i(870084);try{var o=window;o._sentryModuleMetadata=o._sentryModuleMetadata||{},o._sentryModuleMetadata[(new o.Error).stack]=Object.assign({},o._sentryModuleMetadata[(new o.Error).stack],{"_sentryBundlerPluginAppKey:website":!0})}catch(e){}let l=null,c=!1,h=1,u=new WeakMap,d=new WeakMap,f=new Map,p=new Set,g=null,m=!1;function b(){return!c&&"u">typeof Worker&&"u">typeof OffscreenCanvas&&"u">typeof HTMLCanvasElement&&"transferControlToOffscreen"in HTMLCanvasElement.prototype}function v(e){c=!0,console.error(`[AgentOrb] worker failed (${e}); remounting orbs on the main thread`);let t=[...f.values()];f.clear();try{l?.terminate()}catch{}for(let e of(l=null,t))e()}function y(){return g||"u"<typeof IntersectionObserver?g:g=new IntersectionObserver(e=>{let t=l;if(t)for(let a of e){let e=d.get(a.target);void 0!==e&&t.postMessage({type:"visible",id:e,visible:a.isIntersecting})}},{threshold:0})}function w(e,t){l?.postMessage({type:"audio",level:e,target:t})}let x={src:e.i(47113).default,width:160,height:160,blurWidth:8,blurHeight:8,blurDataURL:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAA30lEQVR42i2OO07DQABEt4m/67UXe72LnTiJTQEKThEpQqSAAgQSFRVwBwqQ4AQ0nACJY3DDxxJRvGI0T5oR09kpmXSo1OLyHpPPebp65eX2m4/7H8SsG3Gmx5YdR82aWnecb244O77j+fIL0bYnNIc9ru4Y5itkqtGFoa6mXKweELVdorVFygKlSqIo9XN6j6t7RKYsSayYTCJPSBjEPmf+V0GeG0RlBtp2QfAvBF6QUlEUpcf5k8st1g0kSbEv/0iTDJWVmGqBeHv/ZLd9ZDNee0kThpI4zjnQDetxxy94kFXNxe4g8wAAAABJRU5ErkJggg=="};try{var A=window;A._sentryModuleMetadata=A._sentryModuleMetadata||{},A._sentryModuleMetadata[(new A.Error).stack]=Object.assign({},A._sentryModuleMetadata[(new A.Error).stack],{"_sentryBundlerPluginAppKey:website":!0})}catch(e){}let k=n.useLayoutEffect,M={spiral:0,nebula:1,core:2,deep:3},C=["spiral","nebula","core","deep"];function S(e,t,a){let i=t*Math.min(a,1-a),r=t=>{let r=(t+e/30)%12;return a-i*Math.max(-1,Math.min(r-3,9-r,1))};return[r(0),r(8),r(4)]}function R(e,t,a){return`#${S(e,t,a).map(e=>Math.round(255*e).toString(16).padStart(2,"0")).join("")}`}let P=[13,34,125,146,166,187,208,228,249,270,290,311,332,353],T=P.map(function(e){let t=.2*(1-function(e){let[t,a,i]=S(e,1,.5);return .299*t+.587*a+.114*i}(e));return{anchor:R(e,.85,.42+t),accents:[R(e,.95,Math.min(.72,.6+t)),R((e+16)%360,.8,Math.min(.82,.7+t)),R((e+34)%360,.9,Math.min(.9,.8+t))]}}),_=new WeakMap;function E(e,t){let a=Math.min(1,Math.max(0,e));(0,s.setCoreAudioLevel)(a,t),w(a,t)}function L(e){(0,s.setCoreAudioLevel)(null,e),w(null,e)}window.__setAgentOrbAudioLevel=E;let F=null,B=!1,N=!1;function D(){if(F||B)return F;if("u"<typeof document)return null;let e=document.createElement("canvas");e.width=s.MAX_PX,e.height=s.MAX_PX;let t=e.getContext("webgl",s.GL_CONTEXT_OPTS);return t?F=new s.OrbRenderer(e,t):(B=!0,null)}let O=4e3*Math.random(),U=new WeakMap,I=null,z=!1,G=new Set,V=new WeakMap,X=0,j=!1,Y=null,W=!1,q=new Map;function H(){X&&(j?clearTimeout(X):cancelAnimationFrame(X),X=0)}function K(){return Y||"u"<typeof IntersectionObserver?Y:Y=new IntersectionObserver(e=>{for(let t of e){let e=V.get(t.target);e&&(e.visible=t.isIntersecting,e.lastNow=null,t.isIntersecting&&$())}},{threshold:0})}let Q=0;function J(){for(let e of G)if(e.visible&&e.animate)return!0;return!1}function $(){!X&&J()&&(j=!1,X=requestAnimationFrame(Z))}function Z(e){if(X=0,!J()){for(let e of G)e.lastNow=null;return}let t=s.FRAME_MS-(e-Q);if(t>1){j=!0,X=window.setTimeout(()=>{X=0,$()},t);return}Q=e-(e-Q)%s.FRAME_MS;let a=D(),i=function(){if(I||z)return I;if("u"<typeof document)return null;let e=document.createElement("canvas");e.width=s.BATCH_MAX_PX,e.height=s.BATCH_MAX_PX;let t=e.getContext("webgl",s.GL_CONTEXT_OPTS),a=t?.getExtension("ANGLE_instanced_arrays")??null;return t&&a?I=new s.OrbBatchRenderer(e,t,a):(z=!0,null)}();for(let t of(q.clear(),G)){if(!t.visible||!t.animate){t.lastNow=null;continue}if((0,s.advanceAnimT)(t,e),t.spec.lens>0||!i)a?.render(t.spec,t.px,t.animT)&&t.ctx.drawImage(a.canvas,0,0,t.px,t.px,0,0,t.px,t.px);else{let e=q.get(t.px);e?e.push(t):q.set(t.px,[t])}}if(i)for(let[e,t]of q)i.renderGroup(t,e);$()}function ee({size:a=46,seed:o="",palette:w,animate:A=!0,archetype:S,crossfade:R=!1,dpr:_="auto",chrome:E="auto",isDark:L}){let F,B={palette:T[(F=(0,s.hashSeed)(o))%T.length],archetype:C[(F>>>16)%C.length]};w=w??B.palette,S=S??B.archetype;let{resolvedTheme:I}=(0,r.useTheme)(),z=L??"dark"===I?"#000000":"#FFFFFF",X=(0,n.useRef)(null),j=(0,i.useReducedMotion)(),[q,Q]=(0,n.useState)(!1);(0,n.useEffect)(()=>Q(!0),[]);let J=q&&!!j,Z=a>=48,[et,ea]=(0,n.useState)(0),[ei]=(0,n.useState)(()=>!N),er=R&&!J&&ei,en=er?`hue-rotate(${P[(0,s.hashSeed)(o)%P.length]-255}deg)`:void 0,es=A&&!j,eo=(0,n.useRef)(es);return(eo.current=es,k(()=>{let e=X.current;if(!e)return;if(u.has(e)){let t;return void(void 0!==(t=u.get(e))&&l?.postMessage({type:"animate",id:t,animate:es}))}let t=V.get(e);t&&(t.animate=es,t.lastNow=null,es&&$())},[es]),k(()=>{let t=X.current;if(!t)return;let i="full"===_||Z?Math.min(s.MAX_DPR,window.devicePixelRatio||1):1,r=Math.min(s.MAX_PX,Math.round(a*i)),n={bg:(0,s.toRGB)(z),anchor:(0,s.toRGB)(w.anchor),accents:[(0,s.toRGB)(w.accents[0]),(0,s.toRGB)(w.accents[1]),(0,s.toRGB)(w.accents[2])],phase:(0,s.hashSeed)(o)%6283/1e3,arch:void 0!==S?M[S]:-1,seed:o,lens:.4*!!Z,audioSmooth:0,audioFast:0,spinDir:1,spinVel:0,prevA:0,flipQueued:!1,oscSign:1,spin:(0,s.hashSeed)(o)%6283/1e3*3.7,lastT:null};if(!j&&b()||u.has(t)){let a=function(t,a,i,r,n){if(!b()&&!u.has(t))return null;let s=function(){if(l||c)return l;try{l=e.r(655522)(Worker,{type:"module"})}catch(e){return console.error("[AgentOrb] worker unavailable, falling back to main thread:",e),c=!0,null}return l.onerror=e=>{v(`script error: ${e?.message??e}`)},l.onmessage=e=>{if(e.data?.type==="gl-unavailable")v("WebGL unavailable in worker");else if(e.data?.type==="orb-failed"&&void 0!==e.data.id){c=!0;let t=f.get(e.data.id);f.delete(e.data.id),t?.()}},l}();if(!s)return u.has(t)&&queueMicrotask(n),null;let o=u.get(t);if(void 0===o){let e;try{e=t.transferControlToOffscreen()}catch{return null}o=h++,u.set(t,o),s.postMessage({type:"add",id:o,canvas:e,spec:a,px:i,animate:r},[e])}else s.postMessage({type:"update",id:o,spec:a,px:i,animate:r});d.set(t,o),f.set(o,n),p.add(t),!m&&"u">typeof document&&(m=!0,document.addEventListener("visibilitychange",()=>{let e=l;if(!e)return;if("visible"!==document.visibilityState){for(let t of p){let a=u.get(t);void 0!==a&&e.postMessage({type:"visible",id:a,visible:!1})}return}let t=y();for(let e of p)t?.unobserve(e),t?.observe(e)})),y()?.observe(t);let w=o;return()=>{g?.unobserve(t),p.delete(t),f.delete(w),l?.postMessage({type:"visible",id:w,visible:!1}),queueMicrotask(()=>{t.isConnected||l?.postMessage({type:"remove",id:w})})}}(t,n,r,eo.current,()=>ea(e=>e+1));if(a)return N=!0,er&&!t.style.animation&&(t.style.animation="orb-boot-in 460ms cubic-bezier(0.2, 0.8, 0.2, 1) both"),a;if(u.has(t))return}let x=t.getContext("2d");if(!x)return;t.width=r,t.height=r,x.globalCompositeOperation="copy";let A=D(),k=U.get(t)??performance.now()/1e3+O;U.set(t,k);let C=!!A&&!!A.render(n,r,k)&&(x.drawImage(A.canvas,0,0,r,r,0,0,r,r),!0);if(C&&(N=!0),er&&C&&!j&&!t.style.animation&&(t.style.animation="orb-boot-in 460ms cubic-bezier(0.2, 0.8, 0.2, 1) both"),j)return;let R={canvas:t,ctx:x,spec:n,px:r,visible:!0,animate:eo.current,animT:k,lastNow:null};return G.add(R),V.set(R.canvas,R),!W&&"u">typeof document&&(W=!0,document.addEventListener("visibilitychange",()=>{if("visible"!==document.visibilityState){for(let e of G)e.visible=!1,e.lastNow=null;H();return}let e=K();for(let t of G)e?.unobserve(t.canvas),e?.observe(t.canvas)})),K()?.observe(R.canvas),$(),()=>{U.set(R.canvas,R.animT),G.delete(R),V.delete(R.canvas),Y?.unobserve(R.canvas),0===G.size&&H()}},[a,o,w,z,j,S,er,_,Z,et]),Z||"full"===E)?(0,t.jsxs)("div",{"aria-hidden":!0,className:"relative block shrink-0",style:{width:a,height:a},children:[(0,t.jsxs)("div",{style:{position:"absolute",inset:0,borderRadius:"50%",overflow:"hidden",clipPath:"circle(50% at 50% 50%)",WebkitClipPath:"circle(50% at 50% 50%)",maskImage:"radial-gradient(closest-side, #000 calc(100% - 0.5px), transparent)",WebkitMaskImage:"radial-gradient(closest-side, #000 calc(100% - 0.5px), transparent)"},children:[er&&(0,t.jsx)("img",{src:x.src,alt:"",style:{position:"absolute",inset:0,width:a,height:a,display:"block",filter:en}}),(0,t.jsx)("canvas",{ref:X,className:"block",style:{position:"relative",width:a,height:a,clipPath:"circle(50% at 50% 50%)",WebkitClipPath:"circle(50% at 50% 50%)"}},et)]}),(0,t.jsx)("div",{style:{position:"absolute",inset:0,borderRadius:"50%",pointerEvents:"none",opacity:.35,boxShadow:`inset 0 1px 1px rgba(255,255,255,0.7), inset 0 -1px 1px rgba(255,255,255,0.45), inset 0 0 0 1px rgba(255,255,255,0.22), inset 0 0 ${(.06*a).toFixed(1)}px rgba(255,255,255,0.18)`}})]}):(0,t.jsx)("div",{"aria-hidden":!0,className:"relative block shrink-0",style:{width:a,height:a},children:(0,t.jsxs)("div",{style:{position:"absolute",inset:0,borderRadius:"50%",overflow:"hidden",boxShadow:"inset 0 0 0 1px rgba(255,255,255,0.18)"},children:[er&&(0,t.jsx)("img",{src:x.src,alt:"",style:{position:"absolute",inset:0,width:a,height:a,display:"block",filter:en}}),(0,t.jsx)("canvas",{ref:X,className:"block",style:{position:"relative",width:a,height:a}},et)]})})}e.s(["AgentOrb",0,ee,"attachAgentOrbAudio",0,function(e,t){let a;if(e instanceof AnalyserNode)a=e;else if(!function(e){try{if("anonymous"===e.crossOrigin||"use-credentials"===e.crossOrigin)return!0;let t=e.currentSrc||e.src;if(!t)return!1;return new URL(t,location.href).origin===location.origin}catch{return!1}}(e)){let a=0,i=()=>{if(a=requestAnimationFrame(i),e.paused||e.ended)return void E(0,t);let r=performance.now()/1e3;E(Math.max(0,Math.min(1,(.55+.45*Math.sin(.9*r+2*Math.sin(.37*r)))*(.6+.4*Math.sin(6.2*r+3*Math.sin(2.3*r)))*(Math.sin(.7*r+1.7)>-.6?1:.12))),t)};return a=requestAnimationFrame(i),()=>{cancelAnimationFrame(a),E(0,t),void 0!==t&&L(t)}}else{let t=_.get(e);if(!t){let a=new AudioContext,i=a.createMediaElementSource(e),r=a.createAnalyser();r.fftSize=512,i.connect(r),r.connect(a.destination),t={ctx:a,analyser:r},_.set(e,t)}t.ctx.resume(),a=t.analyser}let i=new Uint8Array(a.fftSize),r=0,n=()=>{r=requestAnimationFrame(n),a.getByteTimeDomainData(i);let e=0;for(let t=0;t<i.length;t++){let a=(i[t]-128)/128;e+=a*a}E(Math.min(1,3.2*Math.sqrt(e/i.length)),t)};return r=requestAnimationFrame(n),()=>{cancelAnimationFrame(r),E(0,t),void 0!==t&&L(t)}},"releaseAgentOrbAudio",0,function(e){let t=_.get(e);t&&(_.delete(e),t.ctx.close())}],193294);try{var et=window;et._sentryModuleMetadata=et._sentryModuleMetadata||{},et._sentryModuleMetadata[(new et.Error).stack]=Object.assign({},et._sentryModuleMetadata[(new et.Error).stack],{"_sentryBundlerPluginAppKey:website":!0})}catch(e){}e.s(["AgentOrb",0,function(e){let i=(0,a.useIsDark)();return(0,t.jsx)(ee,{...e,isDark:i,dpr:"full",chrome:"full"})}],91262)},979495,e=>{e.q("/_next/static/media/orb-worker.32jsmosc67nv1.ts")},47113,e=>{e.q("/_next/static/media/placeholder-orb.3vdgr_lx46lxv.png")},870084,e=>{"use strict";try{var t=window;t._sentryModuleMetadata=t._sentryModuleMetadata||{},t._sentryModuleMetadata[(new t.Error).stack]=Object.assign({},t._sentryModuleMetadata[(new t.Error).stack],{"_sentryBundlerPluginAppKey:website":!0})}catch(e){}let a=`
attribute vec2 aPos;
attribute vec2 aUV;
varying vec2 vUV;
void main() {
  vUV = aUV;
  gl_Position = vec4(aPos, 0.0, 1.0);
}`,i=`
float h1(float x) { return fract(sin(x * 127.1) * 43758.5453); }

// ── starfield — a real galaxy in a glass sphere: a tilted galactic band
// of dense star-dust and glowing nebula pockets, dark dust lanes cutting
// through it, three scales of twinkling stars, deep-space black behind.
vec4 starfield(vec3 n, float t) {
  float lon = atan(n.z, n.x);
  float lat = asin(clamp(n.y, -1.0, 1.0));

  // per-orb structural variance, derived from the seed phase: every orb gets
  // its own galaxy — band tilt/undulation/width, star density, pocket hues
  float v1 = fract(uPhase * 7.13);
  float v2 = fract(uPhase * 3.71);
  float v3 = fract(uPhase * 5.37);

  // ── galaxy ARCHETYPE: each orb is one of four different skies
  // 0 spiral (milky-way band) \xb7 1 emission nebula (vivid cloud, few stars)
  // 2 galactic core (warm blazing bulge) \xb7 3 deep field (sparse, crystalline)
  float at = uArch >= 0.0 ? uArch : floor(fract(uPhase * 9.73) * 4.0);
  float isNeb = step(0.5, at) * (1.0 - step(1.5, at));
  float isCore = step(1.5, at) * (1.0 - step(2.5, at));
  float isDeep = step(2.5, at);

  // galactic plane: density concentrates in a band around a tilted equator.
  // lon frequencies MUST be integers: lon wraps at \xb1π, and a non-integer
  // frequency doesn't tile across that seam — it stamps a hard crease that
  // tumbles into view as the sphere spins.
  float gb = lat + (0.15 + 0.4 * v1) * sin(lon * (1.0 + floor(v2 * 2.0)) + 1.3)
           + 0.12 * sin(lon * 3.0 + t * 0.1);
  float band = exp(-gb * gb * (5.0 + 10.0 * v3));
  band = mix(band, max(band, 0.8), isNeb); // nebula: cloud fills the whole sky
  band *= 1.0 - 0.85 * isDeep; // deep field: nearly empty void

  // nebula: two octaves of warped wisps, glowing pockets along the band
  float n1 = sin(lon * 2.0 + sin(lat * 3.0 + t * 0.25) * 1.6 + t * 0.15);
  float n2 = sin(lon * 5.0 - sin(lat * 4.0 - t * 0.2) * 1.2 - t * 0.22 + 2.4);
  float neb = pow(0.5 + 0.5 * n1, 2.0) * (0.45 + 0.55 * pow(0.5 + 0.5 * n2, 2.0));
  // dark dust lanes carved through the bright band
  float lane = pow(0.5 + 0.5 * sin(lon * 4.0 + lat * 7.0 + sin(lon * 2.0) * 2.0), 3.0);
  float galaxy = band * neb * (1.0 - lane * (0.55 + 0.35 * v2));
  float w0g = clamp(galaxy, 0.0, 1.0); // ensure the band registers in alpha
  galaxy = w0g;
  // Milky-Way dust: mostly cool blue-white star haze, the palette only as a
  // faint cast — real galaxies are desaturated except the warm core
  // per-orb color identity: how strongly (and with which accents) the dust is
  // tinted varies orb to orb — some stay silver-blue, others go violet/amber
  vec3 hue = mix(mix(uC0, uC1, v1), mix(uC1, uC2, v3), 0.5 + 0.5 * sin(lon + lat * 2.0 - t * 0.2));
  // saturation push: keep the dust hue vivid even after all the mixing
  vec3 hueGrey = vec3(dot(hue, vec3(0.299, 0.587, 0.114)));
  hue = clamp(hueGrey + (hue - hueGrey) * 1.45, 0.0, 1.0);
  // the palette carries each agent's identity — dust leans firmly into it
  // (different agents on one screen read as different colored skies)
  vec3 dust = mix(vec3(0.72, 0.78, 0.92), hue, 0.45 + 0.3 * v1 + 0.45 * isNeb);
  vec3 col = dust * galaxy * (0.6 + 0.9 * isNeb);
  // rotation streaks: faint orbital shear lines inside the band, drifting —
  // the galaxy visibly *turns*
  float shear = sin(lon * 13.0 + lat * 4.0 - t * 0.35) * sin(lon * 5.0 + t * 0.2);
  col += dust * band * neb * max(shear, 0.0) * 0.14;
  // a second, fainter dust arm crossing the main band — spiral-galaxy depth
  float gb2 = lat - (0.35 + 0.25 * v2) * sin(lon * 2.0 - 1.1) + 0.4;
  float arm = exp(-gb2 * gb2 * 7.0) * neb;
  col += mix(dust, uC1, 0.35) * arm * 0.2;
  // the void itself is never pure black: a whisper of deep indigo that
  // breathes — the "magic" ambient of a long-exposure sky
  // the void itself carries the agent's hue — the strongest identity cue,
  // since it covers the whole sphere
  vec3 voidGlow = mix(vec3(0.04, 0.03, 0.1), mix(uC0, mix(uC1, uC2, v3), v1) * 0.22, 0.75);
  col += voidGlow * (0.5 + 0.22 * sin(t * 0.4 + lon)) * (0.4 + 0.6 * band);
  // warm amber core glow deep in the band
  col += vec3(1.0, 0.88, 0.68) * pow(band, 4.0) * pow(neb, 2.0) * 0.4;
  // galactic-core archetype: a blazing warm bulge with a halo of star-fog,
  // fixed to the rotating sphere so it wheels around as the galaxy turns
  float ca = v2 * 6.28318;
  vec3 Cdir = normalize(vec3(cos(ca) * 0.85, 0.6 * (v3 - 0.5), sin(ca) * 0.85));
  float bulge = max(dot(n, Cdir), 0.0);
  col += mix(vec3(1.0, 0.85, 0.6), uC2, 0.25) * (pow(bulge, 14.0) * 1.6 + pow(bulge, 4.0) * 0.5) * isCore;
  // nebula pockets, two layers in different hues: hot spots of saturated
  // palette color glowing in the dust, slowly breathing
  float pocket = pow(neb, 5.0) * band * (0.7 + 0.3 * sin(t * 0.6 + lon * 3.0));
  col += mix(uC2, uC0, fract(v1 + 0.5 * sin(lon * 2.0) + 0.5)) * pocket * (0.5 + 0.4 * v2 + 0.8 * isNeb);
  float pocket2 = pow(0.5 + 0.5 * sin(lon * 3.0 + lat * 4.0 - t * 0.18 + 2.0), 6.0) * band;
  col += mix(uC1, uC2, v3) * pocket2 * (0.25 + 0.3 * v1 + 0.5 * isNeb);
  // Detail factor by orb size (1 = large): small list orbs keep faded bright stars but drop the grain
  // and most of the dense faint dust — those are what read as granular noise / alias at list sizes.
  float detail = smoothstep(90.0, 200.0, uRes.y);
  // milky grain: ultra-fine star dust packed into the band — the granular
  // texture that says "Milky Way" in long-exposure shots
  vec2 gg = vec2(lon, lat) * 34.0;
  vec2 gc = floor(gg);
  vec2 gf = fract(gg);
  float gh = h1(gc.x * 3.7 + gc.y * 11.3);
  vec2 gp = vec2(0.2 + 0.6 * h1(gh * 91.0), 0.2 + 0.6 * h1(gh * 47.0));
  float gd = length((gf - gp) * vec2(cos(lat), 1.0));
  float grain = exp(-gd * gd * 700.0 * clamp(uRes.y / 420.0, 0.22, 1.0)) * step(0.3, gh) * (0.15 + 0.85 * band);
  col += vec3(0.88, 0.9, 1.0) * grain * 0.4 * detail;
  float w = clamp(galaxy * 0.7 + pow(band, 4.0) * 0.25, 0.0, 1.0);



  // three star scales: a few bright, many mid, dense faint dust (denser in band)
  for (int s = 0; s < 3; s++) {
    float K = s == 0 ? 6.0 : (s == 1 ? 11.0 : 19.0);
    vec2 g = vec2(lon, lat) * K;
    vec2 cell = floor(g);
    vec2 f = fract(g);
    float hx = h1(cell.x * 13.7 + cell.y * 7.3 + float(s) * 91.0);
    float hy = h1(cell.x * 5.1 + cell.y * 17.9 + float(s) * 37.0);
    vec2 sp = vec2(0.15 + 0.7 * hx, 0.15 + 0.7 * hy);
    float d = length((f - sp) * vec2(cos(lat), 1.0));
    // archetype star census: nebulae are star-poor, cores star-rich,
    // deep fields sparse but every star counts
    float census = (v2 - 0.5) * 0.2 + 0.35 * isNeb - 0.2 * isCore + 0.3 * isDeep;
    float keep = step((s == 2 ? 0.3 : 0.55) + census, h1(hx * 89.0 + hy * 31.0) + band * 0.25);
    // small orbs: stars must stay >= ~1px and twinkle gently, or they alias
    // into flicker as the sphere tumbles
    float resFac = clamp(uRes.y / 420.0, 0.22, 1.0);
    float tw = mix(0.92, 0.6 + 0.4 * sin(t * (1.5 + 3.0 * hx) + hx * 40.0), resFac);
    // per-star size: each star draws its own radius from the hash (4x range),
    // and brightness follows size — a real magnitude distribution
    float hz = h1(hx * 53.0 + hy * 71.0 + cell.x);
    float sizeJit = 0.35 + 1.8 * hz * hz; // few big, many small
    float sharp = (s == 0 ? 260.0 : (s == 1 ? 700.0 : 1600.0)) / sizeJit * resFac;
    float star = exp(-d * d * sharp) * keep * tw;
    // near-white stars with the faintest temperature variation, like the sky
    vec3 tint = mix(vec3(1.0), hx < 0.33 ? vec3(0.85, 0.9, 1.0) : (hx < 0.66 ? vec3(1.0, 0.95, 0.85) : mix(vec3(1.0), uC1, 0.3)), 0.6);
    float bright = (s == 0 ? 1.7 : (s == 1 ? 0.9 : 0.5)) * (0.55 + 0.7 * sizeJit);
    // small orbs: keep the bright/mid stars (just faded), but drop most of the dense faint dust (s==2)
    // and the grain — those are what read as granular noise at list sizes.
    float starFade = mix(s == 2 ? 0.14 : 0.45, 1.0, detail);
    col += tint * star * bright * starFade;
    // the biggest stars get a soft halo bloom + diffraction-cross sparkle
    if (s == 0) {
      float big = smoothstep(1.2, 2.0, sizeJit);
      col += tint * exp(-d * d * 60.0) * 0.18 * big * tw * starFade;
      vec2 dd = (f - sp) * vec2(cos(lat), 1.0);
      float spike = exp(-dd.x * dd.x * 1200.0) * exp(-dd.y * dd.y * 26.0)
                  + exp(-dd.y * dd.y * 1200.0) * exp(-dd.x * dd.x * 26.0);
      col += tint * spike * 0.3 * big * tw * starFade;
      w = max(w, spike * 0.3 * big * starFade);
    }
    w = max(w, star * min(bright, 1.5) * starFade);
  }

  // pulsar: one bright star per orb that flashes rhythmically with a halo —
  // audio pushes its beat brighter and faster
  float pa = v1 * 6.28318;
  vec3 P = normalize(vec3(sin(pa) * 0.9, 1.4 * (v2 - 0.5), cos(pa) * 0.9));
  float pd = max(dot(n, P), 0.0);
  float beat = pow(0.5 + 0.5 * sin(t * (1.2 + v3 + 1.5 * uAudio) + v3 * 6.28), 8.0);
  beat = min(1.0, beat + 0.6 * uAudio);
  float pulsarFade = mix(0.45, 1.0, detail);
  col += vec3(0.9, 0.95, 1.0) * (pow(pd, 900.0) * (0.6 + 1.2 * beat) + pow(pd, 110.0) * 0.5 * beat) * pulsarFade;
  w = max(w, pow(pd, 900.0) * (0.5 + 0.5 * beat) * pulsarFade);

  return vec4(min(col, vec3(1.0)), min(w, 1.0));
}

// Sample the rotating sphere at 3D point n (unit sphere). The ball TUMBLES:
// it spins around a tilted axis while that axis itself slowly precesses and
// the whole ball rolls — rotation on multiple axes, like a marble turned in
// the hand, so the pattern travels over the poles too, not just sideways.
vec4 sphereAt(vec3 n, float spin, float t) {
  float roll = t * 0.13; // roll around the view axis
  float cr = cos(roll), sr = sin(roll);
  n = vec3(cr * n.x - sr * n.y, sr * n.x + cr * n.y, n.z);
  float tilt = 0.45 + 0.35 * sin(t * 0.24); // precessing axis
  float cx = cos(tilt), sx = sin(tilt);
  n = vec3(n.x, cx * n.y - sx * n.z, sx * n.y + cx * n.z);
  float cs = cos(spin), ss = sin(spin);
  n = vec3(cs * n.x + ss * n.z, n.y, -ss * n.x + cs * n.z);
  return starfield(n, t);
}

// The whole orb as a pure function of the (pre-lens) screen point p — the
// in-shader lens re-evaluates this at displaced coordinates per RGB channel.
vec3 shade(vec2 p) {
  float r = length(p);
  // No alpha mask: the shader renders edge-to-edge of the square canvas
  // (the limb colors smear outward past r=1 as overscan), so the lens —
  // SVG or in-shader — always has pixels to displace; otherwise it pulls
  // transparent samples and stamps a hard arc inside the sphere. The CSS
  // clip-path on the canvas wrapper cuts the true circular silhouette.
#ifndef DUAL_LAYER
  // Batch (list) orbs have no lens, so the square corners are never used —
  // discard them to skip the whole galaxy compute for ~21% of pixels.
  if (r > 1.0) { discard; }
#endif
  float t = uTime * 0.8 + uPhase;

  // sphere geometry
  float rr = min(r, 0.9995);
  float z = sqrt(1.0 - rr * rr);
  vec3 N = vec3(p.x, p.y, z);
  float fres = pow(1.0 - z, 2.4); // 0 center -> 1 at the limb

  // Front hemisphere point is N itself; the see-through far wall is hit by
  // the refracted ray continuing through the glass to the back of the ball.
  vec3 I = vec3(0.0, 0.0, -1.0);
  vec3 R = refract(I, N, 0.75);
  // exit point of the ray on the back of the unit sphere
  float dHit = -2.0 * dot(N, R);
  vec3 B = normalize(N + R * dHit);

  // both layers live on the SAME rotating sphere — the front face and the
  // far wall seen through the glass — so the whole ball reads as one object
  // spinning, with the back side counter-sliding in true perspective.
  // organic motion: the spin angle is integrated on the CPU (uSpin) so the
  // rotation can accelerate, ease, and reverse smoothly — especially under
  // audio. Pattern time keeps its own gentle warp for non-linear drift.
  float sv = fract(uPhase * 6.31);
  float sw = fract(uPhase * 2.17);
  float tWarp = t
    + (0.9 + 1.3 * sv) * sin(t * (0.09 + 0.07 * sw))
    + (0.5 + 0.8 * sw) * sin(t * (0.21 + 0.09 * sv) + 2.6);
  vec4 front = sphereAt(N, uSpin, tWarp);
  // The back-wall galaxy sample doubles fragment cost; only the hero (single-orb)
  // program keeps it. Batched list orbs skip it (invisible at small sizes).
#ifdef DUAL_LAYER
  vec4 back = sphereAt(B, uSpin, tWarp * 0.8 + 2.7);
#else
  vec4 back = vec4(0.0);
#endif

  // glass body: deep-space glass — near-black void with the anchor color
  // breathing at the rim; just enough page light leaks through the edge
  // to keep it reading as glass rather than a flat black disc
  vec3 voidCol = mix(uAnchor * 0.04, uAnchor * 0.35, fres);
  vec3 col = mix(uBg, voidCol, 0.97 - 0.04 * fres);
  // mix (not add): the band REPLACES the glass color where it lives, so it
  // reads on light pages instead of clipping to white
  float fa = clamp(front.a, 0.0, 1.0);
  float ba = clamp(back.a, 0.0, 1.0);
  col = mix(col, back.rgb, ba * 0.16); // far-wall echo
  col = mix(col, front.rgb, fa * 0.85);
  {
    // ── aurora borealis, voice as light — drawn in VIEW space so the
    // curtains always hang in the visible upper sky (the galaxy tumbles
    // behind them). Amplitude undulates like speech; fine rays shimmer
    // through; classic green at the base climbing into violet.
    float alon = atan(N.x, N.z);
    float speech = pow(0.5 + 0.5 * sin(alon * 3.0 + sin(alon * 7.0 + t * 1.1) * 0.7 + t * 0.5), 3.0)
                 * (0.55 + 0.45 * sin(alon * 5.0 - t * 0.65 + 1.7));
    float sky = -N.y; // canvas blit flips Y: -N.y is the visible upper sky
    float hang = smoothstep(-0.15, 0.5, sky);
    float rays = 0.7 + 0.3 * sin(alon * 24.0 + sin(alon * 9.0 - t * 0.8) * 2.0 + t * 1.6);
    // audio: the voice IS the aurora — curtains surge with live amplitude
    float aur = clamp(speech, 0.0, 1.0) * hang * rays * (1.0 + 2.2 * uAudio);
    // per-orb aurora character: some classic green→violet, others lean into
    // the palette (teal→pink, blue→gold…)
    float av = fract(uPhase * 2.93);
    vec3 aurCol = mix(vec3(0.12, 0.95, 0.55), vec3(0.45, 0.35, 1.0),
                      smoothstep(0.0, 0.95, sky + 0.35 * speech));
    aurCol = mix(aurCol, mix(uC0, uC2, av), 0.15 + 0.4 * av);
    col += aurCol * aur * 0.8;

    // shooting star: every ~6s a meteor streaks across a random trajectory,
    // white-hot head with an exponentially fading tail
    float met = 4.5 + 3.5 * fract(uPhase * 4.91); // per-orb meteor cadence
    float epoch = floor(t / met);
    float ph = fract(t / met);
    vec2 s0 = vec2(-1.1 + 2.2 * h1(epoch * 1.3), 0.85 - 1.4 * h1(epoch * 2.9));
    vec2 sd = normalize(vec2(0.7 + 0.5 * h1(epoch * 4.1), -0.35 - 0.4 * h1(epoch * 5.3)));
    vec2 head = s0 + sd * ph * 2.8;
    vec2 rel = p - head;
    float along = dot(rel, sd);
    float perp = dot(rel, vec2(-sd.y, sd.x));
    float vis = smoothstep(0.0, 0.06, ph) * smoothstep(0.5, 0.32, ph);
    float tail = exp(-perp * perp * 1600.0) * exp(along * 9.0) * step(along, 0.0)
               * smoothstep(-0.5, -0.02, along);
    float headGlow = exp(-dot(rel, rel) * 900.0);
    col += (vec3(1.0) * headGlow * 1.2 + mix(vec3(1.0), uC1, 0.3) * tail * 0.85) * vis;

    // moving illumination: a broad diffuse gradient (a soft terminator)
    // sweeps around the sphere, brightening whole regions of sky and dust in
    // turn — this is what makes the ball feel LIT, not printed
    vec3 LD = normalize(vec3(0.85 * sin(t * 0.42), 0.45 * sin(t * 0.26 + 1.2), 0.5));
    float diffuse = 0.62 + 0.65 * max(dot(N, LD), 0.0);
    // audio: the whole sky brightens and breathes with the voice
    diffuse *= 1.0 + 0.35 * uAudio;
    col *= diffuse;
    // ── voice light: while speaking, a warm core flare wakes deep in the
    // sphere and the rim catches the agent's color — the orb visibly *emits*
    vec3 voiceCol = mix(uC1, vec3(1.0, 0.97, 0.9), 0.45);
    col += voiceCol * pow(1.0 - rr, 1.8) * uAudio * 0.5; // inner flare
    col += (uC1 * 0.7 + vec3(0.12)) * fres * uAudio * 0.65; // rim ignition
    // sparkle excitement: stars glitter harder while the voice is live
    col += col * uAudio * 0.18 * sin(t * 14.0 + rr * 40.0 + uPhase * 7.0);
    // counter-rim: a faint atmospheric glow opposite the moving light
    float counter = max(dot(N.xy, -LD.xy), 0.0) * fres;
    col += mix(uC0, vec3(0.5, 0.6, 0.9), 0.5) * counter * 0.18;
  }

  // 3D lighting off the sphere normal — the key light DRIFTS slowly (like a
  // light source moving in the room) and breathes in intensity, so the glass
  // never feels statically lit
  vec3 L1 = normalize(vec3(-0.45 + 0.3 * sin(t * 0.34), 0.62 + 0.2 * sin(t * 0.27 + 1.7), 0.64));
  float keyAmp = 0.5 * (0.78 + 0.22 * sin(t * 0.45 + 2.2));
  col += vec3(1.0) * pow(max(dot(N, L1), 0.0), 150.0) * keyAmp;
  // broad soft sheen sweeping across the dome on a long period
  vec3 LS = normalize(vec3(sin(t * 0.07) * 0.9, 0.35 + 0.3 * cos(t * 0.05), 0.7));
  col += vec3(1.0) * pow(max(dot(N, LS), 0.0), 7.0) * 0.05;
  vec3 L2 = normalize(vec3(0.52, -0.5 + 0.12 * sin(t * 0.09), 0.69)); // counter glint
  col += vec3(1.0) * pow(max(dot(N, L2), 0.0), 140.0) * 0.25;
  // fresnel rim — a bubble's edge catches a touch of the band's color
  col = mix(col, front.rgb, fa * fres * 0.3);
  // whisper of limb compression
  float limb = smoothstep(0.94, 1.0, rr);
  col = mix(col, col * 0.85, limb * 0.4);

  return col;
}`,r=`
precision highp float;
#define DUAL_LAYER
varying vec2 vUV;
uniform vec2 uRes;
uniform vec3 uBg;
uniform vec3 uAnchor, uC0, uC1, uC2;
uniform float uTime, uPhase;
uniform float uAudio; // live audio level 0..1 — the orb listens
uniform float uSpin; // CPU-integrated spin angle (can accelerate & reverse)
uniform float uArch; // galaxy archetype override; < 0 = derive from seed
uniform float uLens; // in-shader lens displacement (p-units); 0 = lens off
`+i+`
void main() {
  vec2 p = vUV * 2.0 - 1.0;
  if (uLens > 0.0) {
    float r = length(p);
    // erf edge falloff: 0 inside, 1 at the silhouette (erf ≈ tanh(1.7725x),
    // expanded — GLSL ES 1.00 has no tanh); band starts at 1 - depth
    // (depth = 0.1), scale = 1/(depth\xb7√2)
    float ex = exp(2.0 * 1.7724539 * (r - 0.9) / 0.1414214);
    float fall = 0.5 + 0.5 * (ex - 1.0) / (ex + 1.0);
    if (fall > 0.004) {
      // swell: same incommensurate sines the SVG loop animated, so the rim
      // compression re-spikes and the chroma fringe shimmers — free here
      float swell = 1.0 + 0.16 * (0.6 * sin(uTime * 0.9 + uPhase)
                                + 0.4 * sin(uTime * 1.7 + uPhase * 1.3));
      float k = uLens * fall * swell;
      // per-channel displacement (chromaAmount 2 → R \xd71.4, G \xd71.2, B \xd71.0),
      // each with its own slow shimmer (the old per-channel chan factor)
      float cR = 1.4 * (1.0 + 0.06 * sin(uTime * 1.3 + uPhase));
      float cG = 1.2 * (1.0 + 0.06 * sin(uTime * 1.3 + uPhase + 2.1));
      float cB = 1.0 * (1.0 + 0.06 * sin(uTime * 1.3 + uPhase + 4.2));
      vec3 col = vec3(shade(p * (1.0 - k * cR)).r,
                      shade(p * (1.0 - k * cG)).g,
                      shade(p * (1.0 - k * cB)).b);
      // specular pass (the map's B channel): glow lobes at \xb140\xb0 fading in at
      // the rim, plus hard catchlights right at the silhouette edge
      vec2 a2 = min(abs(p), 1.0);
      float lobe = max(abs(a2.x * 0.766 + a2.y * 0.643), abs(a2.x * 0.766 - a2.y * 0.643));
      float glow = 0.65 * pow(clamp((lobe - 0.0707) / 1.3435, 0.0, 1.0), 2.4) * fall;
      glow += 1.02 * clamp(1.0 + (r - 1.0) / 0.15, 0.0, 1.0) * step(r, 1.0) * pow(lobe, 2.0);
      col += vec3(0.25) * min(glow, 1.0);
      gl_FragColor = vec4(col, 1.0);
      return;
    }
  }
  gl_FragColor = vec4(shade(p), 1.0);
}`,n=`
precision highp float;
varying vec2 vUV;
varying vec2 uRes;
varying vec3 uBg, uAnchor, uC0, uC1, uC2;
varying float uPhase, uAudio, uSpin, uArch, uTime;
`+i+`
void main() {
  gl_FragColor = vec4(shade(vUV * 2.0 - 1.0), 1.0);
}`,s=`
attribute vec2 aPos;
attribute vec2 aUV;
attribute vec4 iPos;  // cellX, cellY, sizePx, spin
attribute vec4 iDyn;  // audio, phase, arch, time
attribute vec4 iBg;   // bg.rgb, anchor.r
attribute vec4 iAnc;  // anchor.gb, c0.rg
attribute vec4 iC0b;  // c0.b, c1.rgb
attribute vec4 iC2;   // c2.rgb, _
uniform vec2 uCanvas; // atlas size in device px
varying vec2 vUV;
varying vec2 uRes;
varying vec3 uBg, uAnchor, uC0, uC1, uC2;
varying float uPhase, uAudio, uSpin, uArch, uTime;
void main() {
  vUV = aUV;
  uSpin = iPos.w;
  uAudio = iDyn.x;
  uPhase = iDyn.y;
  uArch = iDyn.z;
  uTime = iDyn.w;
  uRes = vec2(iPos.z);
  uBg = iBg.rgb;
  uAnchor = vec3(iBg.a, iAnc.x, iAnc.y);
  uC0 = vec3(iAnc.z, iAnc.w, iC0b.x);
  uC1 = iC0b.yzw;
  uC2 = iC2.xyz;
  vec2 pPx = iPos.xy + aUV * iPos.z;          // top-down px within the cell
  float ndcX = pPx.x / uCanvas.x * 2.0 - 1.0;
  float ndcY = 1.0 - pPx.y / uCanvas.y * 2.0; // flip to GL y-up
  gl_Position = vec4(ndcX, ndcY, 0.0, 1.0);
}`;function o(e,t,a){let i=e.createShader(t);return i?(e.shaderSource(i,a),e.compileShader(i),e.getShaderParameter(i,e.COMPILE_STATUS))?i:(console.error("[AgentOrb] shader compile failed:",e.getShaderInfoLog(i)),e.deleteShader(i),null):null}let l=["uRes","uBg","uAnchor","uC0","uC1","uC2","uTime","uPhase","uAudio","uSpin","uArch","uLens"],c=0,h=new Map;function u(e,t){let a=null===e.lastT?0:Math.min(.1,Math.max(0,t-e.lastT));e.lastT=t;let i=Math.max(c,h.get(e.seed)??0),r=i>e.audioSmooth?.11:.3;e.audioSmooth+=(i-e.audioSmooth)*(a>0?1-Math.exp(-a/r):0);let n=i>e.audioFast?.04:.18;e.audioFast+=(i-e.audioFast)*(a>0?1-Math.exp(-a/n):0);let s=6.31*e.phase%1,o=.35*Math.sin(t*(.11+.08*(2.17*e.phase%1))+e.phase),l=e.audioFast,u=Math.sin(t*(.45+.2*s)+e.phase);Math.sign(u)!==e.oscSign&&(e.oscSign=Math.sign(u),e.flipQueued=!0),e.flipQueued&&l<.18&&(e.spinDir=-e.spinDir,e.flipQueued=!1);let d=.65*(.65+.7*s)*(1+o)+e.spinDir*l*2.2;e.spinVel+=(d-e.spinVel)*(a>0?1-Math.exp(-a/.35):0);let f=Math.max(0,l-e.prevA);e.prevA=l,e.spinVel+=e.spinDir*Math.min(6*f,1.4)*a*14,e.spin+=e.spinVel*a}class d{canvas;gl;ext;prog=null;ready=!1;uCanvas=null;instBuffer=null;data=new Float32Array(24576);constructor(e,t,a){this.canvas=e,this.gl=t,this.ext=a,this.init()}init(){let e=this.gl,t=o(e,e.VERTEX_SHADER,s),a=o(e,e.FRAGMENT_SHADER,n);if(!t||!a)return;let i=e.createProgram();if(!i)return;if(e.attachShader(i,t),e.attachShader(i,a),e.bindAttribLocation(i,0,"aPos"),e.bindAttribLocation(i,1,"aUV"),e.bindAttribLocation(i,2,"iPos"),e.bindAttribLocation(i,3,"iDyn"),e.bindAttribLocation(i,4,"iBg"),e.bindAttribLocation(i,5,"iAnc"),e.bindAttribLocation(i,6,"iC0b"),e.bindAttribLocation(i,7,"iC2"),e.linkProgram(i),e.deleteShader(t),e.deleteShader(a),!e.getProgramParameter(i,e.LINK_STATUS))return void console.error("[AgentOrb] instanced link failed:",e.getProgramInfoLog(i));this.prog=i,this.uCanvas=e.getUniformLocation(i,"uCanvas");let r=e.createBuffer();e.bindBuffer(e.ARRAY_BUFFER,r),e.bufferData(e.ARRAY_BUFFER,new Float32Array([-1,-1,0,1,1,-1,1,1,-1,1,0,0,1,1,1,0]),e.STATIC_DRAW),e.enableVertexAttribArray(0),e.vertexAttribPointer(0,2,e.FLOAT,!1,16,0),e.enableVertexAttribArray(1),e.vertexAttribPointer(1,2,e.FLOAT,!1,16,8),this.instBuffer=e.createBuffer(),e.bindBuffer(e.ARRAY_BUFFER,this.instBuffer),e.bufferData(e.ARRAY_BUFFER,this.data.byteLength,e.DYNAMIC_DRAW);for(let t=0;t<6;t++){let a=2+t;e.enableVertexAttribArray(a),e.vertexAttribPointer(a,4,e.FLOAT,!1,96,16*t),this.ext.vertexAttribDivisorANGLE(a,1)}e.enable(e.BLEND),e.blendFunc(e.ONE,e.ONE_MINUS_SRC_ALPHA),this.ready=!0}writeInstance(e,t,a,i,r,n){let s=24*e,o=this.data;o[s]=t,o[s+1]=a,o[s+2]=i,o[s+3]=r.spin,o[s+4]=r.audioSmooth,o[s+5]=r.phase,o[s+6]=r.arch,o[s+7]=n,o[s+8]=r.bg[0],o[s+9]=r.bg[1],o[s+10]=r.bg[2],o[s+11]=r.anchor[0],o[s+12]=r.anchor[1],o[s+13]=r.anchor[2],o[s+14]=r.accents[0][0],o[s+15]=r.accents[0][1],o[s+16]=r.accents[0][2],o[s+17]=r.accents[1][0],o[s+18]=r.accents[1][1],o[s+19]=r.accents[1][2],o[s+20]=r.accents[2][0],o[s+21]=r.accents[2][1],o[s+22]=r.accents[2][2],o[s+23]=0}renderGroup(e,t){if(!this.ready||!this.prog)return!1;let a=this.gl,i=Math.max(1,Math.floor(this.canvas.width/t)),r=Math.min(i*Math.max(1,Math.floor(this.canvas.height/t)),1024);a.useProgram(this.prog),a.uniform2f(this.uCanvas,this.canvas.width,this.canvas.height),a.viewport(0,0,this.canvas.width,this.canvas.height),a.bindBuffer(a.ARRAY_BUFFER,this.instBuffer);for(let n=0;n<e.length;n+=r){let s=Math.min(r,e.length-n);for(let a=0;a<s;a++){let r=e[n+a];u(r.spec,r.animT);let s=a%i,o=Math.floor(a/i);this.writeInstance(a,s*t,o*t,t,r.spec,r.animT)}a.bufferSubData(a.ARRAY_BUFFER,0,this.data.subarray(0,24*s)),a.clearColor(0,0,0,0),a.clear(a.COLOR_BUFFER_BIT),this.ext.drawArraysInstancedANGLE(a.TRIANGLE_STRIP,0,4,s);for(let a=0;a<s;a++){let r=e[n+a],s=a%i,o=Math.floor(a/i);r.ctx.drawImage(this.canvas,s*t,o*t,t,t,0,0,t,t)}}return!0}}e.s(["BATCH_MAX_PX",0,512,"FRAME_MS",0,1e3/60,"GL_CONTEXT_OPTS",0,{premultipliedAlpha:!0,alpha:!0,antialias:!0,preserveDrawingBuffer:!0},"MAX_DPR",0,2,"MAX_PX",0,1280,"OrbBatchRenderer",0,d,"OrbRenderer",0,class{gl;prog=null;u=null;ready=!1;canvas;constructor(e,t){this.canvas=e,this.gl=t,e.addEventListener("webglcontextlost",e=>{e.preventDefault(),this.ready=!1}),e.addEventListener("webglcontextrestored",()=>this.init()),this.init()}init(){let e=this.gl,t=o(e,e.VERTEX_SHADER,a),i=o(e,e.FRAGMENT_SHADER,r);if(!t||!i)return;let n=e.createProgram();if(!n||(e.attachShader(n,t),e.attachShader(n,i),e.bindAttribLocation(n,0,"aPos"),e.bindAttribLocation(n,1,"aUV"),e.linkProgram(n),e.deleteShader(t),e.deleteShader(i),!e.getProgramParameter(n,e.LINK_STATUS)))return;this.prog=n;let s={};for(let t of l)s[t]=e.getUniformLocation(n,t);this.u=s;let c=e.createBuffer();e.bindBuffer(e.ARRAY_BUFFER,c),e.bufferData(e.ARRAY_BUFFER,new Float32Array([-1,-1,0,1,1,-1,1,1,-1,1,0,0,1,1,1,0]),e.STATIC_DRAW),e.enableVertexAttribArray(0),e.vertexAttribPointer(0,2,e.FLOAT,!1,16,0),e.enableVertexAttribArray(1),e.vertexAttribPointer(1,2,e.FLOAT,!1,16,8),e.enable(e.BLEND),e.blendFunc(e.ONE,e.ONE_MINUS_SRC_ALPHA),e.enable(e.SCISSOR_TEST),this.ready=!0}render(e,t,a){if(!this.ready||!this.prog||!this.u)return!1;let i=this.gl;i.useProgram(this.prog);let r=this.canvas.height-t;i.viewport(0,r,t,t),i.scissor(0,r,t,t);let n=this.u;return i.uniform2f(n.uRes,t,t),i.uniform3f(n.uBg,e.bg[0],e.bg[1],e.bg[2]),i.uniform3f(n.uAnchor,e.anchor[0],e.anchor[1],e.anchor[2]),i.uniform3f(n.uC0,...e.accents[0]),i.uniform3f(n.uC1,...e.accents[1]),i.uniform3f(n.uC2,...e.accents[2]),i.uniform1f(n.uTime,a),i.uniform1f(n.uPhase,e.phase),i.uniform1f(n.uArch,e.arch),i.uniform1f(n.uLens,e.lens),u(e,a),i.uniform1f(n.uAudio,e.audioSmooth),i.uniform1f(n.uSpin,e.spin),i.clearColor(0,0,0,0),i.clear(i.COLOR_BUFFER_BIT),i.drawArrays(i.TRIANGLE_STRIP,0,4),!0}},"advanceAnimT",0,function(e,t){let a=null===e.lastNow?0:Math.min(100,Math.max(0,t-e.lastNow));e.animT+=a/1e3,e.lastNow=t},"hashSeed",0,function(e){let t=0x811c9dc5;for(let a=0;a<e.length;a++)t^=e.charCodeAt(a),t=Math.imul(t,0x1000193);return t>>>0},"setCoreAudioLevel",0,function(e,t){void 0!==t?null===e?h.delete(t):h.set(t,Math.min(1,Math.max(0,e))):c=null===e?0:Math.min(1,Math.max(0,e))},"toRGB",0,e=>[parseInt(e.slice(1,3),16)/255,parseInt(e.slice(3,5),16)/255,parseInt(e.slice(5,7),16)/255]])},510914,e=>{"use strict";e.s(["default",0,function(t,a){return(i,r)=>(function(t,a,i,r){let n="SharedWorker"===t.name,s=e.b,o=[i.map(t=>e.h("string"==typeof t?t:t.path,s)).reverse(),e.X,s],l=["NEXT_DEPLOYMENT_ID","NEXT_CLIENT_ASSET_SUFFIX"];for(let e=0;e<l.length;e++)o.push(globalThis[l[e]]);let c=new URL(e.h(a,s),location.origin),h=JSON.stringify(o);return n?c.searchParams.set("params",h):c.hash="#params="+encodeURIComponent(h),new t(c,r?{...r,type:void 0}:void 0)})(i,t,a,r)}])},655522,e=>{e.v(e.r(510914).default("static/chunks/turbopack-worker-1r2nq6-dwes2z.js",["static/chunks/28rqz8vogokgu.js","static/chunks/turbopack-2kkiupw9r9-c1.js"]))}]);

//# debugId=fa89f67f-6818-b1e0-7127-de5c8edd7185