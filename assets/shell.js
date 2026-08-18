/* shell.js — the building's behaviors. First: THE INK RAMP.
   The ground darkens down the page; the ink lightens in inverse sync, so
   legibility is constant through the descent. Each text element samples its
   document position against the depth's gradient stops and takes the
   inverse shade. Elements that carry their own ground (cards, plaques,
   captions, the fleet box, the colophon) are exempt. Opt out: .ink-skip. */
(function () {
  var depth = document.body.getAttribute('data-depth') || '0';

  /* ink stops per depth: [document-fraction, ink, link-ink] — tuned to the
     ground gradients in gallery-type.css and main's own descent */
  var RAMPS = {
    '0': [[0.00,'#4a3a1c','#7d5e1a'],[0.55,'#4a3a1c','#7d5e1a'],
          [0.66,'#5e4c2c','#8a6a20'],[0.74,'#a8946a','#c9a13b'],
          [0.82,'#dcCBa0','#e0c268'],[1.00,'#f0e2c0','#f0d98c']],
    '1': [[0.00,'#4a3a1c','#7d5e1a'],[0.42,'#4a3a1c','#7d5e1a'],
          [0.62,'#6a5836','#9a7c2a'],[0.78,'#c4b088','#d0b055'],
          [1.00,'#f0e2c0','#f0d98c']],
    '2': [[0.00,'#3a2c14','#7d5e1a'],[0.30,'#4a3a1c','#8a6a20'],
          [0.52,'#8a7850','#b08c2e'],[0.70,'#d5c49c','#dcbe60'],
          [1.00,'#f5e9c8','#f0d98c']]
  };
  var ramp = RAMPS[depth] || RAMPS['1'];

  var SKIP = ['.shell-plaque','.shell-nav','.shell-foot','.colophon-mini',
    '.plaque','.caption','.fleetbox','footer','.door','.board','.stairslot',
    '.ink-skip','svg','button','.bar'].join(',');

  function hex(c){ return parseInt(c,16); }
  function mix(a,b,t){
    var r1=hex(a.slice(1,3)),g1=hex(a.slice(3,5)),b1=hex(a.slice(5,7));
    var r2=hex(b.slice(1,3)),g2=hex(b.slice(3,5)),b2=hex(b.slice(5,7));
    return 'rgb('+Math.round(r1+(r2-r1)*t)+','+Math.round(g1+(g2-g1)*t)+','+Math.round(b1+(b2-b1)*t)+')';
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
    var els = document.body.querySelectorAll(
      'h1,h2,h3,h4,p,li,blockquote,figcaption,span,i,b,em,strong,a,div');
    for (var i=0;i<els.length;i++){
      var el=els[i];
      if (el.closest(SKIP)) { el.style.removeProperty('color'); continue; }
      /* only ink elements that directly hold text */
      var hasText=false;
      for (var n=el.firstChild;n;n=n.nextSibling){
        if (n.nodeType===3 && /\S/.test(n.nodeValue)) { hasText=true; break; }
      }
      if (!hasText) continue;
      var r=el.getBoundingClientRect();
      var f=(r.top + r.height/2 + window.scrollY)/H;
      el.style.color = at(f, el.tagName==='A' ? 2 : 1);
    }
  }

  var t=null;
  function schedule(){ clearTimeout(t); t=setTimeout(paint, 120); }
  if (document.readyState==='loading')
    document.addEventListener('DOMContentLoaded', function(){ paint(); setTimeout(paint, 600); });
  else { paint(); setTimeout(paint, 600); }
  window.addEventListener('resize', schedule);
  window.addEventListener('load', paint);
})();
