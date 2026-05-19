"""
Build the four-algorithms site index.html.

Reads the preprocessed bundle from Drive (~/Library/CloudStorage/.../four_algo_v1/)
and emits a single self-contained HTML longform article with seven inline scenes:

  1. Hero + intro
  2. Four blooms — scrubable, 4 panels × 32 frames
  3. Cross-basis 3×3 — each algorithm only readable in its own basis
  4. Multi-location 4×9 — where each algorithm lives along the model
  5. Handcrafted max — 100% accuracy from formula
  6. Steering — chord vs linear vs random vs dictation per task
  7. Cross-seed 5×4 — same algorithms, different gauges

Output: viz/four_algo/index.html (single file, ~1 MB with inline data).
"""

import os, json

# Reads preprocessed JSONs that live next to this build.py and emits index.html.
# To regenerate the JSONs from scratch, run notebooks/train_5seeds.ipynb +
# notebooks/walk_and_dictation.ipynb + notebooks/handcraft_max.ipynb +
# notebooks/multilocation_analysis.ipynb.
SRC = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = SRC
OUT_HTML = os.path.join(OUT_DIR, "index.html")


def main():
    data    = json.load(open(os.path.join(SRC, "data.json")))
    walk    = json.load(open(os.path.join(SRC, "walk_results.json")))
    dictation = json.load(open(os.path.join(SRC, "dictation_results.json")))
    walk_sum = json.load(open(os.path.join(SRC, "walk_summary.json")))
    handcraft = json.load(open(os.path.join(SRC, "handcraft_summary.json")))

    bundle = {
        "data": data,
        "walk": walk,
        "dictation": dictation,
        "walk_summary": walk_sum,
        "handcraft": handcraft,
    }
    payload = json.dumps(bundle, separators=(",", ":"))
    html = HTML_TEMPLATE.replace("__DATA_JSON__", payload)

    with open(OUT_HTML, "w") as f:
        f.write(html)

    size_kb = os.path.getsize(OUT_HTML) / 1024
    print(f"wrote {OUT_HTML}  ({size_kb:.1f} KB)")


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Four algorithms in one tiny brain</title>
<meta name="description" content="A small transformer learns division, addition, max and parity in one shared head — each in its own basis, at its own time, in its own component of the forward pass.">
<meta property="og:type" content="article">
<meta property="og:title" content="Four algorithms in one tiny brain">
<meta property="og:description" content="A small transformer learns division, addition, max and parity in one shared head — each in its own basis, at its own time, in its own component of the forward pass.">
<meta property="og:url" content="https://nick-yudin.github.io/manifold_features/four-algorithms/">
<meta property="og:image" content="https://nick-yudin.github.io/manifold_features/four-algorithms/preview.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Four algorithms in one tiny brain">
<meta name="twitter:description" content="A small transformer learns division, addition, max and parity in one shared head — each in its own basis, at its own time, in its own component of the forward pass.">
<meta name="twitter:image" content="https://nick-yudin.github.io/manifold_features/four-algorithms/preview.png">
<meta name="twitter:creator" content="@Nikolay_Yudin_">
<style>
  :root {
    --bg: #f5f1e8;
    --ink: #1a1a1a;
    --soft-ink: #2c2a23;
    --muted: #6b6657;
    --faint: #aba89a;
    --rule: rgba(0,0,0,0.10);
    --rule-soft: rgba(0,0,0,0.06);
    --accent: #c25540;
    --accent-soft: rgba(194,85,64,0.10);
    --panel: rgba(255,255,253,0.55);

    --c-div:    #d45a2a;
    --c-add:    #3a6e8c;
    --c-max:    #5e9c5c;
    --c-parity: #9c5ebe;
  }
  * { box-sizing: border-box; }
  html { -webkit-text-size-adjust: 100%; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: 'Iowan Old Style', 'Palatino Linotype', 'Palatino', 'P052', 'URW Palladio L', Georgia, serif;
    font-size: 18px;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  ::selection { background: var(--accent-soft); }
  a { color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--rule); }
  a:hover { border-color: var(--ink); }

  article {
    max-width: 720px;
    margin: 0 auto;
    padding: clamp(48px, 7vh, 96px) clamp(20px, 4vw, 40px) 120px;
  }

  /* ---- Title block ---- */
  header.title-block {
    margin-bottom: clamp(40px, 6vh, 64px);
    padding-bottom: 32px;
    border-bottom: 1px solid var(--rule);
  }
  h1.title {
    font-family: 'Iowan Old Style', 'Palatino Linotype', Georgia, serif;
    font-size: clamp(36px, 4.6vw, 52px);
    line-height: 1.12;
    font-weight: 500;
    letter-spacing: -0.01em;
    margin: 0 0 18px;
    color: var(--ink);
  }
  .subtitle {
    font-family: 'Iowan Old Style', 'Palatino Linotype', Georgia, serif;
    font-size: clamp(18px, 2vw, 22px);
    line-height: 1.45;
    color: var(--muted);
    font-style: italic;
    margin: 0 0 22px;
  }
  .meta {
    font-family: ui-monospace, 'SF Mono', Menlo, monospace;
    font-size: 12px;
    color: var(--faint);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin: 0;
  }
  .meta a { color: var(--muted); text-decoration: none; border-bottom: 1px solid var(--rule); }
  .meta a:hover { color: var(--ink); border-color: var(--ink); }
  .meta-sep { margin: 0 8px; color: var(--faint); }

  /* ---- Body ---- */
  h2 {
    font-family: 'Iowan Old Style', 'Palatino Linotype', Georgia, serif;
    font-size: 26px;
    font-weight: 500;
    line-height: 1.25;
    margin: clamp(48px, 6vh, 72px) 0 18px;
    color: var(--ink);
    letter-spacing: -0.005em;
  }
  h3 {
    font-family: 'Iowan Old Style', 'Palatino Linotype', Georgia, serif;
    font-size: 19px;
    font-weight: 500;
    margin: 32px 0 10px;
    color: var(--soft-ink);
  }
  p { margin: 0 0 18px; color: var(--soft-ink); }
  p.lede { font-size: 21px; line-height: 1.55; color: var(--ink); margin-bottom: 28px; }
  em, i { font-style: italic; color: var(--ink); }
  strong, b { font-weight: 600; color: var(--ink); }
  ul { margin: 0 0 18px; padding-left: 22px; color: var(--soft-ink); }
  ul li { margin-bottom: 6px; }
  code {
    font-family: ui-monospace, 'SF Mono', Menlo, monospace;
    font-size: 0.88em;
    background: rgba(0,0,0,0.04);
    padding: 1px 5px;
    border-radius: 3px;
    color: var(--soft-ink);
  }
  .caption { font-size: 13.5px; color: var(--muted); margin-top: 8px; font-style: italic; }
  hr.sep { border: none; border-top: 1px solid var(--rule); margin: 60px 0; }

  /* fig containers can be wider than the article column */
  .figure { margin: 28px -64px; }
  @media (max-width: 920px) { .figure { margin: 28px 0; } }
  .figure-frame {
    background: rgba(255,255,253,0.55);
    border: 1px solid var(--rule);
    border-radius: 10px;
    padding: 20px;
  }

  /* —— Bloom scene —— */
  .bloom-grid { display: grid; grid-template-columns: repeat(4, 1fr);
                gap: 14px; align-items: end; }
  @media (max-width: 720px) { .bloom-grid { grid-template-columns: repeat(2, 1fr); } }
  .bloom-cell { background: var(--bg); border: 1px solid var(--rule);
                border-radius: 6px; padding: 8px; position: relative; }
  .bloom-cell .title { font-size: 12px; letter-spacing: 0.04em;
                        text-transform: uppercase; color: var(--faint);
                        margin-bottom: 6px; }
  .bloom-cell .acc { position: absolute; top: 8px; right: 12px;
                     font-size: 11px; color: var(--muted);
                     font-variant-numeric: tabular-nums; }
  .bloom-cell svg { width: 100%; aspect-ratio: 1/1; display: block; }
  .bloom-controls { display: flex; align-items: center; gap: 14px; margin-top: 18px; }
  .bloom-play { background: var(--accent); border: none; color: white;
                width: 38px; height: 38px; border-radius: 50%; cursor: pointer;
                font-size: 13px; flex-shrink: 0;
                box-shadow: 0 2px 6px rgba(194, 85, 64, 0.30); }
  .bloom-play:hover { background: #a8442f; }
  .bloom-slider { flex: 1; }
  .bloom-step { font-size: 13px; color: var(--muted); font-variant-numeric: tabular-nums;
                white-space: nowrap; min-width: 100px; }
  input[type=range] { -webkit-appearance: none; appearance: none;
                       width: 100%; height: 22px; background: transparent; }
  input[type=range]::-webkit-slider-runnable-track {
    height: 3px; background: rgba(0,0,0,0.18); border-radius: 2px; }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none; width: 14px; height: 14px; margin-top: -6px;
    background: var(--accent); border: 2px solid var(--bg);
    border-radius: 50%; cursor: pointer; }
  input[type=range]::-moz-range-track { height: 3px; background: rgba(0,0,0,0.18); }
  input[type=range]::-moz-range-thumb {
    width: 14px; height: 14px; background: var(--accent);
    border: 2px solid var(--bg); border-radius: 50%; cursor: pointer; }

  /* —— Grid scenes (cross-basis, multi-loc, cross-seed) —— */
  .grid-wrap { overflow-x: auto; }
  .grid-table { display: grid; gap: 6px; }
  .grid-cell { background: var(--bg); border: 1px solid var(--rule);
               border-radius: 4px; aspect-ratio: 1/1; }
  .grid-cell svg { width: 100%; height: 100%; display: block; }
  .grid-cell.diag { border-color: var(--accent); }
  .grid-h-label { font-size: 11px; color: var(--muted); text-align: center;
                  letter-spacing: 0.05em; text-transform: uppercase;
                  padding: 4px 2px; align-self: center; }
  .grid-v-label { font-size: 11px; color: var(--muted); text-align: right;
                  letter-spacing: 0.05em; text-transform: uppercase;
                  padding: 0 8px; align-self: center; font-weight: 600; }

  /* —— Steering charts —— */
  .steer-grid { display: grid; grid-template-columns: repeat(2, 1fr);
                gap: 16px; }
  @media (max-width: 600px) { .steer-grid { grid-template-columns: 1fr; } }
  .steer-cell { background: var(--bg); border: 1px solid var(--rule);
                border-radius: 6px; padding: 14px; }
  .steer-cell h4 { margin: 0 0 8px; font-size: 13px;
                   font-family: ui-monospace, monospace; letter-spacing: 0.02em; }
  .steer-cell svg { width: 100%; height: 130px; display: block; }
  .legend-row { display: flex; gap: 14px; flex-wrap: wrap;
                font-size: 12px; color: var(--muted); margin-top: 14px;
                padding-left: 10px; }
  .legend-row .sw { display: inline-block; width: 16px; height: 2px;
                    background: var(--accent); margin-right: 6px;
                    vertical-align: middle; }

  /* —— Handcraft callout —— */
  .callout {
    background: rgba(194, 85, 64, 0.06);
    border-left: 3px solid var(--accent);
    border-radius: 4px;
    padding: 18px 22px;
    margin: 28px 0;
  }
  .callout .big { font-size: 38px; font-weight: 600;
                   color: var(--accent); letter-spacing: -0.01em;
                   font-variant-numeric: tabular-nums; }
  .callout .label { font-size: 12px; letter-spacing: 0.06em;
                     text-transform: uppercase; color: var(--muted);
                     margin-bottom: 4px; }

  /* —— Task pill —— */
  .pill { display: inline-block; padding: 2px 9px; border-radius: 10px;
          font-size: 13px; font-weight: 600;
          background: rgba(0,0,0,0.05); color: var(--ink); }
  .pill.div    { color: white; background: var(--c-div); }
  .pill.add    { color: white; background: var(--c-add); }
  .pill.max    { color: white; background: var(--c-max); }
  .pill.parity { color: white; background: var(--c-parity); }

  /* —— Stats row —— */
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
           margin: 24px 0; }
  @media (max-width: 600px) { .stats { grid-template-columns: repeat(2, 1fr); } }
  .stat { background: rgba(255,255,253,0.6); border: 1px solid var(--rule);
          border-radius: 6px; padding: 14px; text-align: left; }
  .stat .label { font-size: 11px; color: var(--faint); letter-spacing: 0.06em;
                  text-transform: uppercase; }
  .stat .v { font-size: 22px; font-weight: 600;
              font-variant-numeric: tabular-nums; margin-top: 4px; }
  .stat .sub { font-size: 12px; color: var(--muted); margin-top: 2px; }

  footer { color: var(--muted); font-size: 13px; border-top: 1px solid var(--rule);
           padding-top: 24px; margin-top: 64px; }

  /* —— Series navigation (shared with fourier-bloom) —— */
  .series-nav {
    max-width: 720px; margin: 0 auto;
    padding: 20px clamp(20px, 4vw, 40px) 0;
    display: flex; flex-wrap: wrap; gap: 8px;
    font-family: ui-monospace, 'SF Mono', Menlo, monospace;
    font-size: 11px; letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .series-nav a, .series-nav span {
    padding: 5px 11px; border-radius: 4px; text-decoration: none;
  }
  .series-nav a { color: var(--accent); border: 1px solid var(--rule); }
  .series-nav a:hover { background: rgba(194, 85, 64, 0.10); }
  .series-nav .current { color: var(--ink);
                          background: rgba(194, 85, 64, 0.10);
                          border: 1px solid var(--accent); }
  .series-nav .disabled { color: var(--faint); border: 1px dashed var(--rule); }
</style>
</head>
<body>

<nav class="series-nav">
  <a href="../fourier-bloom/">← Part 1 · Single algorithm</a>
  <span class="current">Part 2 · Four algorithms</span>
  <span class="disabled">Part 3 · Grokking · coming</span>
  <span class="disabled">Part 4 · Transfer to LLMs · coming</span>
</nav>

<article>

  <header class="title-block">
    <h1 class="title">Four algorithms in one tiny brain</h1>
    <p class="subtitle">What happens if you train one small transformer to do four different math operations at the same time? It learns each one in a different shape.</p>
    <p class="meta">
      <a href="https://github.com/nick-yudin">Nikolay Yudin</a>
      <span class="meta-sep">·</span>
      <span>May 2026</span>
      <span class="meta-sep">·</span>
      <span>Mechanistic interpretability — note 2</span>
    </p>
  </header>

<p>
  In the <a href="../fourier-bloom/">previous note</a> I trained a small model on modular
  division. It built a Lissajous knot out of its output projection, and that
  knot was the algorithm.
</p>

<p>
  This time I trained the same architecture on four tasks at once: division,
  addition, max, and parity. All four had to share one 4.8&thinsp;M-parameter
  body and one output head. I ran five seeds at <code>P = 149</code>,
  <code>WD = 0.3</code>.
</p>

<p>
  Every seed grokked all four tasks to at least 98% accuracy. Each task settled
  into its own shape, in its own basis, at its own time during training.
</p>

<div class=stats id=stats-row></div>
<div class=caption>Mean grok step across 5 seeds (± std). Speedup is vs WD=1.0
baseline.</div>

<h2>The four blooms</h2>

<p>
  Below is one seed snapshotted every 200 steps, with one panel per task.
  Each panel shows that task's per-class L2 residual projected onto the top
  two principal directions of its own privileged basis: dlog Fourier for div,
  natural Fourier for add, top SVD for max, Nyquist axis for parity. Drag the
  slider to scrub through training.
</p>

<div class=figure>
<div class=figure-frame>
  <div class=bloom-grid id=bloom-grid></div>
  <div class=bloom-controls>
    <button class=bloom-play id=bloom-play aria-label=play>▶</button>
    <input class=bloom-slider id=bloom-slider type=range min=0 max=31 value=31 step=1>
    <div class=bloom-step id=bloom-step>step 6200</div>
  </div>
</div>
<div class=caption>
  Per-task L2 manifold formation over training. Color = answer class.
  Bases are held fixed from the final state, so motion is real motion in
  R<sup>384</sup>, not a rotation of the projection.
</div>
</div>

<p>
  The four tasks crystallise at very different times.
</p>

<p>
  <span class="pill max">max</span> comes online almost immediately, around
  step 250. There is barely anything to learn: the answer is just
  <code>a</code> or <code>b</code>, and the model uses copy-attention to point
  at whichever is larger.
</p>

<p>
  <span class="pill parity">parity</span>, the bit <code>(a+b) mod 2</code>,
  groks around step 2,800. It needs exactly one Fourier mode, the Nyquist
  frequency <code>k=74</code> on this 149-tooth clock. Once that one
  direction lines up, parity is done.
</p>

<p>
  <span class="pill div">div</span> takes longer, around step 4,200. It needs
  the discrete-logarithm Fourier basis, the same one I used in the previous
  note. Many frequencies have to cooperate.
</p>

<p>
  <span class="pill add">add</span> is the slowest, around step 5,300. Even
  though addition feels simpler than division to a human, it is the model's
  hardest task here. The reason was something I did not expect: add and
  parity share the Nyquist Fourier direction. While parity sits at the 50%
  "always guess the same bit" attractor, that direction is unavailable to
  add. Once parity finally pulls its two answer points apart along Nyquist,
  add can use the same direction to build the rest of its ring. The two grok
  timings move together within a few hundred steps of each other in every
  seed I ran.
</p>

<h2>Each algorithm needs its own glasses</h2>

<p>
  This is the same final model, with each task's residuals projected into
  each task's basis. On the diagonal: each task in its own basis. Off the
  diagonal: the same task viewed through the wrong basis.
</p>

<div class=figure>
<div class=figure-frame>
  <div id=cross-basis class=grid-wrap></div>
</div>
<div class=caption>
  3×3 cross-basis grid. Diagonal cells show each task's privileged geometry,
  off-diagonal cells show it lost.
</div>
</div>

<p>
  Div's ring only exists if you re-index the 148 invertible remainders by
  their discrete logarithm. In natural number order, the same 148 points
  look random.
</p>

<p>
  Add's ring is the opposite: clean in natural order, noise in dlog. Max has
  no Fourier basis at all. It lives along a value-monotonic curve that is
  invisible to a Fourier projection in either order.
</p>

<p>
  The short version: there is no universal coordinate system inside the model.
  Each algorithm picks its own, and looking through the wrong one turns
  geometry into static.
</p>

<h2>Where do the algorithms live?</h2>

<p>
  The residual stream passes through nine recognisable points along the
  forward pass: the two input token embeddings (positions <code>a</code> and
  <code>b</code>), the input to block&nbsp;0 (<code>L0</code>), the output of
  block&nbsp;0's attention (<code>attn0_out</code>), the middle of FFN&nbsp;0
  (<code>ffn0_mid</code>), the input to block&nbsp;1 (<code>L1</code>), the
  same two checkpoints inside block&nbsp;1, and the final residual
  (<code>L2</code>). The grid below shows, per task, what the residual at
  each of those points looks like when projected onto its own top-2 PCs.
</p>

<div class=figure>
<div class=figure-frame>
  <div id=multi-loc class=grid-wrap></div>
</div>
<div class=caption>
  4 × 9 task × location grid. Where each algorithm's structure first appears
  is a fingerprint of how the model computes it.
</div>
</div>

<p>
  <span class="pill add">add</span>'s ring is already present in the token
  embedding for <code>b</code>. The model does not assemble add during
  forward, it bakes it into the input embeddings.
</p>

<p>
  <span class="pill div">div</span>'s dlog ring first appears at
  <code>attn0_out</code>. Block 0's attention is where the
  discrete-logarithm transformation happens. Before that point div is noise.
  After it, div is a clean ring everywhere.
</p>

<p>
  <span class="pill max">max</span>'s value-monotonic structure is present at
  every layer including the bare token embeddings. Copy-attention does not
  need to build geometry, the answer is just one of the inputs.
</p>

<p>
  <span class="pill parity">parity</span> is two points on a single Nyquist
  axis, present from the start and progressively pulled apart by training.
</p>

<p>
  Each algorithm has a different location signature.
</p>

<h2>Rebuilding the algorithms by hand</h2>

<p>
  Once I knew how each of the four worked, the next thing to check was
  whether I could write them from scratch.
</p>

<p>
  Three of the four are trivial.
</p>

<p>
  <span class="pill div">div</span> is the centrepiece of the previous note:
  a 2-block transformer with weights placed directly from the dlog-Fourier
  algorithm — no training — gets 100.00% on every <code>(a, b)</code> pair.
  <code>W_E</code> carries the dlog Fourier of the token id, attention copies
  it to the answer position, FFN1 computes single-frequency products via the
  SiLU linearisation trick, and <code>W_U</code> reads them back out.
</p>

<p>
  <span class="pill add">add</span> is the same construction with natural
  Fourier in place of dlog. Same machinery, simpler basis. I did not bother
  to write it out separately.
</p>

<p>
  <span class="pill parity">parity</span> is rank-1. One Nyquist direction
  in <code>W_U</code> with sign <code>(-1)^c</code>, one bit out. A handful
  of lines of code.
</p>

<p>
  <span class="pill max">max</span> is the only one of the four that needed
  a genuinely different mechanism. It is not Fourier and not algebraic. The
  mechanism is copy-attention: <code>Q·K</code> monotonic in scalar value
  picks the position of the larger token, <code>V</code> copies that token's
  additive Fourier coefficients to the answer slot, and the head decodes via
  a Dirichlet kernel. So I built max by hand on a 4-head 2-block
  architecture matching the trained model.
</p>

<div class=callout>
  <div class=label>Handcrafted max</div>
  <div class=big id=hand-acc>—</div>
  <p style="margin: 6px 0 0; color: var(--muted); font-size: 14px;">
    Accuracy on every <code>(a, b)</code> pair, all 9,409 of them, with
    weights placed by formula. Full recipe in
    <code>plan6c_handcraft_max</code>.
  </p>
</div>

<p>
  The construction is visible directly in the token embeddings. Each value
  token <code>v ∈ {0, …, 96}</code> sits at exactly
  <code>(cos&thinsp;k·v,&thinsp;sin&thinsp;k·v)</code> on a circle of
  frequency <code>k</code>, in a pair of dimensions allocated to that mode.
  The non-value tokens (<code>op</code>, <code>eq</code>) carry zero in those
  dimensions and sit at the centre, off the circle.
</p>

<div class=figure>
<div class=figure-frame>
  <img src="fig_struct1_fourier_circles_tok_emb.png"
       alt="Fourier circles in tok_emb across six frequencies"
       style="width:100%;display:block;border-radius:4px">
</div>
<div class=caption>
  Token embeddings at six different frequencies. The 97 value tokens lie on
  a clean circle by construction; <code>op</code> and <code>eq</code> sit at
  the centre.
</div>
</div>

<p>
  After block 0's attention has picked the larger of <code>a</code> and
  <code>b</code> and copied that token's coefficients into the answer
  position, the residual at <code>=</code> carries the cos Fourier signature
  of <code>max(a, b)</code> exactly. The chart below puts the observed
  coefficients in blue against the closed-form prediction in red. They
  match.
</p>

<div class=figure>
<div class=figure-frame>
  <img src="fig2_residual_fourier.png"
       alt="Cos Fourier coefficients of the post-block-0 residual match the predicted signature for max(a, b)"
       style="width:100%;display:block;border-radius:4px">
</div>
<div class=caption>
  Post-block-0 residual at the <code>=</code> position. Each small panel is
  one <code>(a, b)</code> pair. Predicted cos Fourier coefficients of
  <code>max(a, b)</code> in red, observed in blue.
</div>
</div>

<p>
  This is the strongest claim mechanistic interpretability can make on any
  given mechanism: not a description of what the model does, but a model
  built from understanding alone that does the same thing.
</p>

<h2>Driving the algorithms</h2>

<p>
  Once the geometry is known, the model becomes controllable from outside. I
  tested four interventions, on all four tasks. For each: take the trained
  model, pick an input <code>(a, b)</code> it predicts correctly, capture its
  residual at <code>L2</code>, modify the residual, run the head, see what
  the model now predicts.
</p>

<div class=figure>
<div class=figure-frame>
  <div class=steer-grid id=steer-grid></div>
  <div class=legend-row>
    <span><span class=sw style="background:#1a1a1a"></span>chord walk
      <span style="color:var(--faint)">(use real manifold positions)</span></span>
    <span><span class=sw style="background:#c25540"></span>linear tangent
      <span style="color:var(--faint)">(scale one tangent vector)</span></span>
    <span><span class=sw style="background:#9aa0a6"></span>random
      <span style="color:var(--faint)">(random direction, same magnitude)</span></span>
    <span><span class=sw style="background:#5e9c5c"></span>dictation
      <span style="color:var(--faint)">(inject the answer-centroid)</span></span>
  </div>
</div>
<div class=caption>
  Steering accuracy as a function of requested shift <code>Δ</code>, per task.
  Chord walking and answer dictation succeed at every Δ. Linear tangent fails
  almost immediately for the non-trivial tasks.
</div>
</div>

<p>
  <strong>Chord walk</strong> shifts the residual by the vector between two
  manifold positions: <code>h + (M[step(c, Δ)] − M[c])</code>. Works for
  arbitrary Δ. Accuracy stays 97-100% across all four tasks for Δ from
  -100 to +100.
</p>

<p>
  <strong>Linear tangent</strong> uses a single local tangent vector and
  scales it by Δ. Fails almost immediately for the non-trivial tasks. The
  algorithm curve has curvature, and a single tangent flies off it within
  one step.
</p>

<p>
  <strong>Random</strong> shifts by a random vector of the same magnitude as
  the chord. Accuracy at chance, ~1/P.
</p>

<p>
  <strong>Dictation</strong> replaces the residual with the precomputed
  answer-centroid for the desired class. 100% on all four tasks. This is a
  sanity check that the head reads the answer linearly from L2.
</p>

<p>
  Two of the four interventions work at every shift on every task. That is
  more than a description of the algorithm. It is a working set of geometric
  levers on the model.
</p>

<h2>Multiple seeds</h2>

<p>
  Same architecture, same data, five different random initial seeds. Each
  network grokked all four algorithms in a clean version of its own shape:
  a ring for div, a ring for add, a value cloud for max, two points on the
  Nyquist axis for parity. But the precise orientations of those shapes in
  384-dimensional space differ between seeds.
</p>

<div class=figure>
<div class=figure-frame>
  <div id=cross-seed class=grid-wrap></div>
</div>
<div class=caption>
  Five seeds × four tasks. The geometric content reproduces across seeds.
  The coordinate frames in which each network expresses that content do not.
</div>
</div>

<p>
  The geometry is reproducible up to a gauge; the gauge itself is not. What
  is invariant across seeds is the type of object each task produces, not
  its frame. Part 3 will come back to this.
</p>

<h2>Where this leaves things</h2>

<p>
  A multi-task model is not one geometric object, it is several. They share
  one residual stream, one set of weights, one forward pass. They emerge at
  different times during training. They live in different bases. They occupy
  different parts of the network. They can be coupled, as parity and add are
  through the Nyquist direction, or independent, as div and max are.
</p>

<p>
  Knowing the geometry of one algorithm makes that mechanism auditable.
  Knowing the geometry of all of them makes the model auditable as a system.
</p>

<p>
  Everything in this note happens on a small model on clean algebraic
  tasks, where the right basis is known from number theory. The next
  question is whether the same geometric picture survives in real LLMs —
  and, more importantly, whether the internal manifold can be turned into
  a supervision signal for the model's own training. That is Part 4.
</p>

<hr class=sep>

<footer>
  <p>
    <strong>Architecture.</strong> 2-block transformer, residual dimension 384,
    12 attention heads, SwiGLU FFN, RMSNorm, AdamW (lr 1e-3, WD 0.3, betas
    0.9/0.98). Four tasks share one body and one output head: <i>div</i>
    (a · b<sup>−1</sup> mod 149), <i>add</i> ((a + b) mod 149), <i>max</i>
    (max(a, b)), <i>parity</i> ((a + b) mod 2). 5 seeds. Figures on this
    page are from seed 1000 except where the panel says otherwise.
  </p>
  <p>
    <strong>Everything that produced these visualizations is in the
    repository</strong> (links open the file on GitHub):
  </p>
  <ul>
    <li><a href="https://github.com/nick-yudin/manifold_features/blob/main/four-algorithms/notebooks/train_5seeds.ipynb"><code>notebooks/train_5seeds.ipynb</code></a>
        — trains 5 seeds of the 4-task transformer; saves <code>final.pt</code>
        and per-step snapshots used by every figure below.</li>
    <li><a href="https://github.com/nick-yudin/manifold_features/blob/main/four-algorithms/notebooks/walk_and_dictation.ipynb"><code>notebooks/walk_and_dictation.ipynb</code></a>
        — chord walk, linear tangent, random direction, dictation sweeps.
        Produces the charts in <span style="font-style:italic">Driving the
        algorithms</span>.</li>
    <li><a href="https://github.com/nick-yudin/manifold_features/blob/main/four-algorithms/notebooks/handcraft_max.ipynb"><code>notebooks/handcraft_max.ipynb</code></a>
        — builds a 2-block transformer that solves <i>max(a, b) mod 97</i>
        with weights placed by formula. 100% accuracy on all 9409 pairs.</li>
    <li><a href="https://github.com/nick-yudin/manifold_features/blob/main/four-algorithms/notebooks/multilocation_analysis.ipynb"><code>notebooks/multilocation_analysis.ipynb</code></a>
        — cross-basis 4×4, multi-location 4×9, parity↔add Nyquist coupling.</li>
    <li><a href="https://github.com/nick-yudin/manifold_features/tree/main/four-algorithms"><code>data/</code></a>
        — JSON summaries consumed by this page: training curves, walk hit
        rates, dictation hit rates, handcraft verification.</li>
    <li><a href="https://huggingface.co/datasets/NikolayYudin/manifold-features-data">Hugging Face dataset</a>
        — <code>final.pt</code> for all 5 seeds plus the handcrafted-max
        state dict. The notebooks pull from here if you do not want to
        train from scratch.</li>
  </ul>
  <p>
    Everything in the repository is what produced the figures on this page.
    There are no separate cleaned-up datasets or hand-picked runs.
  </p>
  <p>
    <strong>Author.</strong> Nikolay Yudin —
    <a href="https://twitter.com/Nikolay_Yudin_">@Nikolay_Yudin_</a>.
  </p>
</footer>

</article>

<script>
const BUNDLE = __DATA_JSON__;
const DATA      = BUNDLE.data;
const WALK      = BUNDLE.walk;
const DICTATION = BUNDLE.dictation;
const WALK_SUM  = BUNDLE.walk_summary;
const HANDCRAFT = BUNDLE.handcraft;

const TASKS = DATA.config.tasks;
const TASK_COLORS = DATA.config.task_colors;
const SNAP_STEPS = DATA.config.snapshot_steps;
const N_FRAMES = SNAP_STEPS.length;
const LOCATIONS = DATA.multi_location.locations;

const TASK_LABEL = { div: 'div', add: 'add', max: 'max', parity: 'parity' };
const TASK_FULL  = {
  div: 'c = a · b⁻¹ mod 149',
  add: 'c = (a + b) mod 149',
  max: 'c = max(a, b)',
  parity: 'c = (a + b) mod 2',
};

// ---------- stats row at the top ----------
function renderStats() {
  const stats = DATA.config.stats;
  const order = ['max', 'parity', 'div', 'add'];
  const root = document.getElementById('stats-row');
  for (const t of order) {
    const s = stats[t];
    const speed = s.speedup_vs_wd1;
    const speedTxt = speed >= 0.97 && speed <= 1.05
        ? '≈ 1×' : (speed > 1 ? speed.toFixed(2) + '× faster' : (1/speed).toFixed(2) + '× slower');
    const el = document.createElement('div');
    el.className = 'stat';
    el.innerHTML = `
      <div class="label" style="color:${TASK_COLORS[t]}">${TASK_LABEL[t]}</div>
      <div class="v">${Math.round(s.mean)} <span style="font-size:13px;color:var(--muted);font-weight:400">± ${Math.round(s.std)}</span></div>
      <div class="sub">${speedTxt} vs WD=1.0</div>`;
    root.appendChild(el);
  }
  document.getElementById('hand-acc').textContent =
    (HANDCRAFT.verification.accuracy * 100).toFixed(2) + '%';
}

// ---------- helpers ----------
function hsvToRgb(h, s, v) {
  const i = Math.floor(h * 6), f = h * 6 - i;
  const p = v * (1 - s), q = v * (1 - f * s), t = v * (1 - (1 - f) * s);
  switch (i % 6) {
    case 0: return [v, t, p]; case 1: return [q, v, p]; case 2: return [p, v, t];
    case 3: return [p, q, v]; case 4: return [t, p, v]; default: return [v, p, q];
  }
}
function classColor(i, n) {
  const [r, g, b] = hsvToRgb(i / n, 0.55, 0.75);
  return `rgb(${Math.round(r*255)},${Math.round(g*255)},${Math.round(b*255)})`;
}
function svg(w, h, vbPad) {
  const ns = 'http://www.w3.org/2000/svg';
  const s = document.createElementNS(ns, 'svg');
  s.setAttribute('viewBox', `${-vbPad} ${-vbPad} ${2*vbPad} ${2*vbPad}`);
  s.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  return s;
}

// ---------- §2 Bloom ----------
function renderBloom() {
  const root = document.getElementById('bloom-grid');
  const cells = {};
  for (const t of TASKS) {
    const cell = document.createElement('div');
    cell.className = 'bloom-cell';
    cell.innerHTML = `<div class="title" style="color:${TASK_COLORS[t]}">${TASK_LABEL[t]}</div>
                      <div class="acc" id="acc-${t}">—</div>`;
    const s = svg(0, 0, 1.15);
    cell.appendChild(s);
    root.appendChild(cell);
    cells[t] = { svg: s, accEl: document.getElementById(`acc-${t}`), circles: [] };
    // pre-create circles based on final frame's count
    const nPts = DATA.bloom[t].frames[N_FRAMES - 1].length;
    for (let i = 0; i < nPts; i++) {
      const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      c.setAttribute('r', 0.035);
      c.setAttribute('fill', classColor(i, nPts));
      c.setAttribute('opacity', 0.92);
      s.appendChild(c);
      cells[t].circles.push(c);
    }
  }
  return cells;
}
function applyBloomFrame(cells, idx) {
  for (const t of TASKS) {
    const frame = DATA.bloom[t].frames[idx];
    const acc = DATA.bloom[t].acc[idx];
    cells[t].accEl.textContent = (acc * 100).toFixed(0) + '%';
    for (let i = 0; i < frame.length; i++) {
      cells[t].circles[i].setAttribute('cx', frame[i][0]);
      cells[t].circles[i].setAttribute('cy', -frame[i][1]);
    }
  }
  document.getElementById('bloom-step').textContent = 'step ' + SNAP_STEPS[idx];
  document.getElementById('bloom-slider').value = idx;
}
function initBloomControls(cells) {
  const slider = document.getElementById('bloom-slider');
  const playBtn = document.getElementById('bloom-play');
  slider.max = N_FRAMES - 1;
  slider.addEventListener('input', () => applyBloomFrame(cells, +slider.value));
  let playing = false, t0 = 0;
  function step(now) {
    if (!playing) return;
    if (now - t0 > 200) {
      let idx = +slider.value;
      idx = (idx + 1) % N_FRAMES;
      applyBloomFrame(cells, idx);
      t0 = now;
    }
    requestAnimationFrame(step);
  }
  playBtn.addEventListener('click', () => {
    playing = !playing; playBtn.textContent = playing ? '⏸' : '▶';
    if (playing) { t0 = performance.now(); requestAnimationFrame(step); }
  });
  applyBloomFrame(cells, N_FRAMES - 1);
}

// ---------- §3 Cross-basis 3×3 ----------
function renderCrossBasis() {
  const root = document.getElementById('cross-basis');
  const tasks = DATA.cross_basis.tasks;
  const bases = DATA.cross_basis.bases;
  const tbl = document.createElement('div');
  tbl.className = 'grid-table';
  tbl.style.gridTemplateColumns = `90px repeat(${bases.length}, 1fr)`;
  // header row
  tbl.appendChild(_blank());
  for (const b of bases) tbl.appendChild(_hLabel('basis: ' + b, TASK_COLORS[b]));
  // body
  for (let ri = 0; ri < tasks.length; ri++) {
    tbl.appendChild(_vLabel('residual: ' + tasks[ri], TASK_COLORS[tasks[ri]]));
    for (let ci = 0; ci < bases.length; ci++) {
      const cell = DATA.cross_basis.grid[ri][ci];
      tbl.appendChild(_cellWithPoints(cell.points, ri === ci ? TASK_COLORS[tasks[ri]] : null, ri === ci));
    }
  }
  root.appendChild(tbl);
}
function _blank() { const d = document.createElement('div'); return d; }
function _hLabel(s, c) {
  const d = document.createElement('div');
  d.className = 'grid-h-label';
  if (c) d.style.color = c;
  d.textContent = s; return d;
}
function _vLabel(s, c) {
  const d = document.createElement('div');
  d.className = 'grid-v-label';
  if (c) d.style.color = c;
  d.textContent = s; return d;
}
function _cellWithPoints(points, accentColor, isDiag) {
  const wrap = document.createElement('div');
  wrap.className = 'grid-cell' + (isDiag ? ' diag' : '');
  const s = svg(0, 0, 1.15);
  const n = points.length;
  for (let i = 0; i < n; i++) {
    const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    c.setAttribute('cx', points[i][0]);
    c.setAttribute('cy', -points[i][1]);
    c.setAttribute('r', 0.028);
    c.setAttribute('fill', isDiag ? classColor(i, n) : 'rgba(0,0,0,0.40)');
    c.setAttribute('opacity', isDiag ? 0.9 : 0.55);
    s.appendChild(c);
  }
  wrap.appendChild(s); return wrap;
}

// ---------- §4 Multi-location 4×9 ----------
function renderMultiLoc() {
  const root = document.getElementById('multi-loc');
  const tbl = document.createElement('div');
  tbl.className = 'grid-table';
  tbl.style.gridTemplateColumns = `90px repeat(${LOCATIONS.length}, 1fr)`;
  tbl.appendChild(_blank());
  for (const loc of LOCATIONS) tbl.appendChild(_hLabel(loc));
  for (let ti = 0; ti < TASKS.length; ti++) {
    tbl.appendChild(_vLabel(TASKS[ti], TASK_COLORS[TASKS[ti]]));
    for (let li = 0; li < LOCATIONS.length; li++) {
      const cell = DATA.multi_location.grid[ti][li];
      tbl.appendChild(_cellWithPoints(cell.points, TASK_COLORS[TASKS[ti]], true));
    }
  }
  root.appendChild(tbl);
}

// ---------- §6 Steering charts ----------
function renderSteering() {
  const root = document.getElementById('steer-grid');
  const series = ['chord', 'linear', 'random'];          // dictation is per-class, plotted differently
  const colors = { chord: '#1a1a1a', linear: '#c25540', random: '#9aa0a6' };
  const ks = Object.keys(WALK.chord.div).map(Number).sort((a, b) => a - b);

  for (const t of TASKS) {
    const cell = document.createElement('div');
    cell.className = 'steer-cell';
    cell.innerHTML = `<h4 style="color:${TASK_COLORS[t]}">${t}</h4>`;
    const ns = 'http://www.w3.org/2000/svg';
    const s = document.createElementNS(ns, 'svg');
    s.setAttribute('viewBox', '0 0 300 130');
    s.setAttribute('preserveAspectRatio', 'none');

    // axes
    const axisColor = 'rgba(0,0,0,0.15)';
    const ax = document.createElementNS(ns, 'line');
    ax.setAttribute('x1', 0); ax.setAttribute('y1', 105);
    ax.setAttribute('x2', 300); ax.setAttribute('y2', 105);
    ax.setAttribute('stroke', axisColor); s.appendChild(ax);
    // grid line at 0.5
    const gl = document.createElementNS(ns, 'line');
    gl.setAttribute('x1', 0); gl.setAttribute('y1', 55);
    gl.setAttribute('x2', 300); gl.setAttribute('y2', 55);
    gl.setAttribute('stroke', 'rgba(0,0,0,0.06)'); gl.setAttribute('stroke-dasharray', '2 3');
    s.appendChild(gl);
    // labels
    for (const [y, lbl] of [[5,'1.0'], [55,'0.5'], [105,'0.0']]) {
      const tx = document.createElementNS(ns, 'text');
      tx.setAttribute('x', 4); tx.setAttribute('y', y + 4);
      tx.setAttribute('font-size', 9); tx.setAttribute('fill', 'var(--faint)');
      tx.textContent = lbl; s.appendChild(tx);
    }

    // dictation as a horizontal line at 1.0 (it's per-class, ~100% for all)
    {
      const dl = document.createElementNS(ns, 'line');
      dl.setAttribute('x1', 0); dl.setAttribute('y1', 5);
      dl.setAttribute('x2', 300); dl.setAttribute('y2', 5);
      dl.setAttribute('stroke', '#5e9c5c'); dl.setAttribute('stroke-width', 1.6);
      dl.setAttribute('stroke-dasharray', '4 3');
      s.appendChild(dl);
    }

    // ks → x mapping
    const xMin = 18, xMax = 290;
    const kMin = Math.min(...ks), kMax = Math.max(...ks);
    const xOf = (k) => xMin + (k - kMin) / (kMax - kMin) * (xMax - xMin);
    const yOf = (v) => 105 - v * 100;

    for (const series_name of series) {
      const vals = WALK[series_name][t];
      const pts = ks.map(k => `${xOf(k)},${yOf(vals[String(k)])}`).join(' ');
      const poly = document.createElementNS(ns, 'polyline');
      poly.setAttribute('points', pts);
      poly.setAttribute('fill', 'none');
      poly.setAttribute('stroke', colors[series_name]);
      poly.setAttribute('stroke-width', 1.6);
      s.appendChild(poly);
      // markers
      for (const k of ks) {
        const c = document.createElementNS(ns, 'circle');
        c.setAttribute('cx', xOf(k)); c.setAttribute('cy', yOf(vals[String(k)]));
        c.setAttribute('r', 1.8); c.setAttribute('fill', colors[series_name]);
        s.appendChild(c);
      }
    }
    // x labels (just min/0/max)
    for (const k of [kMin, 0, kMax]) {
      const tx = document.createElementNS(ns, 'text');
      tx.setAttribute('x', xOf(k)); tx.setAttribute('y', 121);
      tx.setAttribute('font-size', 9); tx.setAttribute('text-anchor', 'middle');
      tx.setAttribute('fill', 'var(--faint)');
      tx.textContent = 'Δ=' + k; s.appendChild(tx);
    }

    cell.appendChild(s);
    root.appendChild(cell);
  }
}

// ---------- §7 Cross-seed 5×4 ----------
function renderCrossSeed() {
  const root = document.getElementById('cross-seed');
  const seeds = DATA.cross_seed.seeds;
  const tbl = document.createElement('div');
  tbl.className = 'grid-table';
  tbl.style.gridTemplateColumns = `90px repeat(${TASKS.length}, 1fr)`;
  tbl.appendChild(_blank());
  for (const t of TASKS) tbl.appendChild(_hLabel(t, TASK_COLORS[t]));
  for (let si = 0; si < seeds.length; si++) {
    tbl.appendChild(_vLabel('seed ' + seeds[si]));
    for (let ti = 0; ti < TASKS.length; ti++) {
      const cell = DATA.cross_seed.grid[si][ti];
      tbl.appendChild(_cellWithPoints(cell.points, TASK_COLORS[TASKS[ti]], true));
    }
  }
  root.appendChild(tbl);
}

// ---------- bootstrap ----------
renderStats();
const bloomCells = renderBloom();
initBloomControls(bloomCells);
renderCrossBasis();
renderMultiLoc();
renderSteering();
renderCrossSeed();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
