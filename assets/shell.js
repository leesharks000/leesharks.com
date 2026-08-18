/* shell.js — the building's behaviors. First: THE INK RAMP.
   The ground darkens down the page; the ink lightens in inverse sync, so
   legibility is constant through the descent. Each text element samples its
   document position against the depth's gradient stops and takes the
   inverse shade. Elements that carry their own ground (cards, plaques,
   captions, the fleet box, the colophon) are exempt. Opt out: .ink-skip. */
(function () {
  var depth = document.body.getAttribute('data-depth') || '0';

  /* GROUND STOPS — keep in sync with the gradients in gallery-type.css and
     main's own descent. The ink rule is not positional: for each element we
     compute the ground color beneath it, take its luminance, and pick dark
     or pale ink discretely. No blend, no band, no per-page tuning. */
  var GROUNDS = {
    '0': [[0,'#f1eadb'],[0.28,'#ece3cd'],[0.50,'#e2d5b6'],[0.68,'#cfbd97'],
          [0.80,'#9a835c'],[0.88,'#57432b'],[0.95,'#221709'],[1,'#0a0603']],
    '1': [[0,'#eee4c9'],[0.38,'#e2d3ae'],[0.68,'#c4ab7e'],[0.88,'#8a6f47'],[1,'#5e4830']],
    '2': [[0,'#d8c7a2'],[0.40,'#b59a6c'],[0.72,'#7a5f3d'],[0.92,'#3a2c1c'],[1,'#221709']]
  };
  var INK = { dark:'#211a0d', pale:'#f9f1dc', linkDark:'#4a3608', linkPale:'#f0d98c' };
  var stops = GROUNDS[depth] || GROUNDS['1'];

  function hex(c){ return parseInt(c,16); }
  function rgbAt(f){
    for (var i=1;i<stops.length;i++){
      if (f<=stops[i][0]){
        var lo=stops[i-1], hi=stops[i];
        var t=(f-lo[0])/((hi[0]-lo[0])||1);
        var a=lo[1], b=hi[1];
        return [hex(a.slice(1,3))+(hex(b.slice(1,3))-hex(a.slice(1,3)))*t,
                hex(a.slice(3,5))+(hex(b.slice(3,5))-hex(a.slice(3,5)))*t,
                hex(a.slice(5,7))+(hex(b.slice(5,7))-hex(a.slice(5,7)))*t];
      }
    }
    var z=stops[stops.length-1][1];
    return [hex(z.slice(1,3)),hex(z.slice(3,5)),hex(z.slice(5,7))];
  }
  function lum(rgb){ return (0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2])/255; }
  function at(f, idx){
    var L = lum(rgbAt(f));
    if (idx===2) return L > 0.45 ? INK.linkDark : INK.linkPale;
    return L > 0.45 ? INK.dark : INK.pale;
  }
  function at(f, idx){ /* idx 1 = ink, 2 = link ink */
    for (var i=1;i<ramp.length;i++){
      if (f<=ramp[i][0]){
        var lo=ramp[i-1], hi=ramp[i];
        var t=(f-lo[0])/((hi[0]-lo[0])||1);
        return mix(lo[idx],hi[idx],t);
      }
    }
    return ramp[ramp.length-1][idx];
  }

  function paint(){
    var H = document.documentElement.scrollHeight || 1;
    /* block-level carriers only; inline children inherit their ink */
    var els = document.body.querySelectorAll(
      'h1,h2,h3,h4,p,li,blockquote,figcaption,a,div');
    var jobs = [];
    /* READ PHASE: no writes, no thrash */
    for (var i=0;i<els.length;i++){
      var el=els[i];
      if (el.closest(SKIP)) continue;
      if (el.tagName!=='A'){
        var hasText=false;
        for (var n=el.firstChild;n;n=n.nextSibling){
          if (n.nodeType===3 && /\S/.test(n.nodeValue)) { hasText=true; break; }
        }
        if (!hasText) continue;
      }
      var r=el.getBoundingClientRect();
      jobs.push([el, (r.top + r.height/2 + window.scrollY)/H]);
    }
    /* WRITE PHASE */
    for (var k=0;k<jobs.length;k++){
      var el2=jobs[k][0];
      var ink = at(jobs[k][1], el2.tagName==='A' ? 2 : 1);
      el2.style.color = ink;
      if (ink===INK.pale || ink===INK.linkPale)
        el2.style.textShadow='0 1px 2px rgba(10,6,2,.6)';
      else el2.style.removeProperty('text-shadow');
    }
  }

  function paintSVGs(){
    var H = document.documentElement.scrollHeight || 1;
    var svgs = document.body.querySelectorAll('svg');
    for (var i=0;i<svgs.length;i++){
      var el=svgs[i];
      var p=el.parentElement;
      if (p && p.closest('.shell-plaque,.shell-nav,.shell-foot,.fleetbox,footer,.ink-skip')) continue;
      var r=el.getBoundingClientRect();
      var f=(r.top + r.height/2 + window.scrollY)/H;
      el.style.color = at(f, 1);
    }
  }
  var t=null;
  function schedule(){ clearTimeout(t); t=setTimeout(function(){paint();paintSVGs();}, 120); }
  if (document.readyState==='loading')
    document.addEventListener('DOMContentLoaded', function(){ paint(); paintSVGs(); setTimeout(function(){paint();paintSVGs();}, 600); });
  else { paint(); paintSVGs(); setTimeout(function(){paint();paintSVGs();}, 600); }
    var lastW = window.innerWidth;
  window.addEventListener('resize', function(){
    if (window.innerWidth !== lastW){ lastW = window.innerWidth; schedule(); }
  });
  window.addEventListener('load', function(){paint();paintSVGs();});
})();
