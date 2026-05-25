# Manifold Features

A series of interactive longform notes on how small transformers grow algorithms inside their residual stream. Every claim has standalone notebooks that reproduce it from scratch.

**Live site:** https://nick-yudin.github.io/manifold_features/

**Author:** Nikolay Yudin — [@Nikolay_Yudin_](https://twitter.com/Nikolay_Yudin_)

## The series

| | Title | Status | Live |
|---|---|---|---|
| Part 1 | [Inside the grokked manifold of mod-97 division](fourier-bloom/) — observe, build, steer | published | [open](https://nick-yudin.github.io/manifold_features/fourier-bloom/) |
| Part 2 | [Four algorithms in one tiny brain](four-algorithms/) — div, add, max, parity in one shared head | published | [open](https://nick-yudin.github.io/manifold_features/four-algorithms/) |
| Part 3 | Grokking, in general | coming | — |
| Part 4 | [Algorithms in a real LLM (Llama 3.1 8B)](algorithms-in-real-LLMs/) | published | [open](https://nick-yudin.github.io/manifold_features/algorithms-in-real-LLMs/) |

## Repository layout

```
manifold_features/
├── README.md              this file
├── fourier-bloom/         Part 1 — single-algorithm work (P=97, division)
│   ├── index.html         long-form note
│   ├── fourier_bloom_chamber.html
│   ├── steering_theater.html
│   ├── verify_handcrafted.py
│   ├── handcrafted_state_dict.pt
│   ├── notebooks/
│   └── data/
├── four-algorithms/       Part 2 — four-task transformer (P=149)
│   ├── index.html         long-form note
│   ├── build.py
│   ├── data.json, walk_results.json, dictation_results.json, …
│   ├── notebooks/         standalone Jupyter notebooks
│   └── README.md          per-section guide
└── algorithms-in-real-LLMs/  Part 4 — Llama 3.1 8B at scale
    ├── index.html         long-form note
    ├── fig0–fig5*.png     inline figures (paper-beige palette)
    ├── algorithms_in_real_llms_hero.gif        manifold-walk hero animation
    ├── anim_six_clocks_addition.gif            six-clock computation animation
    ├── anim_manifold_vs_linear.gif             manifold walk vs linear chord
    ├── anim_multilayer_catastrophe.gif         multi-layer steering catastrophe
    ├── data/              bundled JSON / NPY summaries
    ├── notebooks/         four standalone Jupyter notebooks
    └── README.md          per-section guide
```

## Reproduce

Every notebook in this repo is standalone. State dicts that are too large to ship in git live on the Hugging Face Hub at [`NikolayYudin/manifold-features-data`](https://huggingface.co/datasets/NikolayYudin/manifold-features-data).

Quick starts:

- **Part 1** — `pip install torch && python fourier-bloom/verify_handcrafted.py` prints `9216/9216 correct = 100.0000%` in under a minute. No training, no GPU.
- **Part 2** — open [`four-algorithms/notebooks/walk_and_dictation.ipynb`](four-algorithms/notebooks/walk_and_dictation.ipynb) in Colab. It pulls a trained 4-task checkpoint from the Hub and reproduces the steering numbers in a few minutes.
- **Part 4** — open [`algorithms-in-real-LLMs/notebooks/manifold_walking.ipynb`](algorithms-in-real-LLMs/notebooks/manifold_walking.ipynb) in Colab on an A100. Pulls `meta-llama/Llama-3.1-8B` (gated; needs an HF token with the model agreement accepted) and reproduces the manifold-walk, α-sweep, and multi-layer-catastrophe figures. Set `RECOMPUTE = False` to skip the GPU pass and replot from bundled JSON.

## Headline claims

**Part 1.** A 2-block transformer trained on `c = a · b⁻¹ mod 97` builds a 3D Fourier knot in `W_U`, the same basis appears in FFN1 / residual / V composition, and the model can be steered along that knot at ≥96.7% hit rate. A hand-built version with no training hits 100% on all 9216 input pairs.

**Part 2.** A 4.8M-parameter transformer trained on div + add + max + parity simultaneously grows four different geometric objects in one shared residual stream: each in its own basis, at its own time during training, in its own component of the forward pass. Chord walking on all four manifolds gets ≥97% hit rate across Δ ∈ ±100. Dictation gets 100% on every target class. WD=0.3 is 4.3× faster to grok add than the standard WD=1.0 setup.

**Part 3 (coming).** What the geometry says about grokking as a phenomenon — what the gauge is across seeds, what is and isn't a "true" learned algorithm, how this reframes the memorization/generalization story.

**Part 4.** **Algorithms in a real LLM.** Llama 3.1 8B already runs Goodfire's six-clock base-10 calculator at L=18 and uses it as a *meta-algorithm* serving arithmetic, weekdays, months, and hours through one shared circuit. Three layers of redundancy (within-residual, multi-layer, beyond-Fourier). Single-layer manifold walking through centroids at L=18 reaches 60-65% hit rate on cross-task targets and beats both Goodfire's α=10 default and the linear-chord baseline. The toy's dlog-Fourier circles do *not* transfer — same algorithmic motif, different specific frequencies (task-specific dlog in the toy, base-10 in Llama).

## Citation

If this work shows up in a paper or thread, a link to the live site or the repo is enough.

Nikolay Yudin. *Manifold Features.* 2026.
https://nick-yudin.github.io/manifold_features/
