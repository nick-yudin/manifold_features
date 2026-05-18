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
| Part 4 | Manifold-Anchored Fine-Tuning (MAFT) — transfer to Qwen 7B | coming | — |

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
└── four-algorithms/       Part 2 — four-task transformer (P=149)
    ├── index.html         long-form note
    ├── build.py
    ├── data.json, walk_results.json, dictation_results.json, …
    ├── notebooks/         standalone Jupyter notebooks
    └── README.md          per-section guide
```

## Reproduce

Every notebook in this repo is standalone. State dicts that are too large to ship in git live on the Hugging Face Hub at [`NikolayYudin/manifold-features-data`](https://huggingface.co/datasets/NikolayYudin/manifold-features-data).

Quick starts:

- **Part 1** — `pip install torch && python fourier-bloom/verify_handcrafted.py` prints `9216/9216 correct = 100.0000%` in under a minute. No training, no GPU.
- **Part 2** — open [`four-algorithms/notebooks/walk_and_dictation.ipynb`](four-algorithms/notebooks/walk_and_dictation.ipynb) in Colab. It pulls a trained 4-task checkpoint from the Hub and reproduces the steering numbers in a few minutes.

## Headline claims

**Part 1.** A 2-block transformer trained on `c = a · b⁻¹ mod 97` builds a 3D Fourier knot in `W_U`, the same basis appears in FFN1 / residual / V composition, and the model can be steered along that knot at ≥96.7% hit rate. A hand-built version with no training hits 100% on all 9216 input pairs.

**Part 2.** A 4.8M-parameter transformer trained on div + add + max + parity simultaneously grows four different geometric objects in one shared residual stream: each in its own basis, at its own time during training, in its own component of the forward pass. Chord walking on all four manifolds gets ≥97% hit rate across Δ ∈ ±100. Dictation gets 100% on every target class. WD=0.3 is 4.3× faster to grok add than the standard WD=1.0 setup.

**Part 3 (coming).** What the geometry says about grokking as a phenomenon — what the gauge is across seeds, what is and isn't a "true" learned algorithm, how this reframes the memorization/generalization story.

**Part 4 (coming).** **MAFT — Manifold-Anchored Fine-Tuning.** The same dictation operation, applied to a 7B base LLM, lets the model's internal manifold supervise its own fine-tuning. Early result: 47.8% → 88.9% on mult mod 11 with 8-bit AdamW on a single A100.

## Citation

If this work shows up in a paper or thread, a link to the live site or the repo is enough.

Nikolay Yudin. *Manifold Features.* 2026.
https://nick-yudin.github.io/manifold_features/
