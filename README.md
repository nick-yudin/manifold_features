# Fourier Bloom

A small transformer learns modular division by growing a 3D Fourier knot inside itself. This repository contains the interactive visualizations, the standalone notebooks that produced them, a hand-built version of the model that reaches 100% accuracy with no training, and a verify script anyone can run in under a minute.

**Live site:** https://nick-yudin.github.io/fourier-bloom/

## What's here

### Interactive

- [`index.html`](index.html) — landing page served at the URL above. Long-form writeup with two embedded interactive scenes.
- [`fourier_bloom_chamber.html`](fourier_bloom_chamber.html) — scrub through training and watch the 96 invertible remainders settle into a Lissajous knot.
- [`steering_theater.html`](steering_theater.html) — pick a shift Δ and compare the manifold walk against the linear chord.

### Reproduce

- [`verify_handcrafted.py`](verify_handcrafted.py) — 90 lines. Loads the hand-built weights, runs the model on all 9216 (a, b) input pairs, prints accuracy. Expected output: `9216/9216 correct = 100.0000%`.
- [`handcrafted_state_dict.pt`](handcrafted_state_dict.pt) — the hand-built weights. No training. Every entry set from the recipe in `notebooks/handcrafted_construction.ipynb`.

```
git clone https://github.com/nick-yudin/fourier-bloom
cd fourier-bloom
pip install torch
python verify_handcrafted.py
```

Runs in under a minute on CPU. No GPU required.

### Notebooks

All four notebooks are standalone. They write to `./outputs/<name>/` and do not require Google Drive.

- [`notebooks/training_slowmo.ipynb`](notebooks/training_slowmo.ipynb) — the per-step training run that produces the bloom in Fig. 1. Saves snapshots at every gradient step.
- [`notebooks/handcrafted_construction.ipynb`](notebooks/handcrafted_construction.ipynb) — builds every weight in the hand-built model from scratch and writes out `handcrafted_state_dict.pt`.
- [`notebooks/multi_location_bloom.ipynb`](notebooks/multi_location_bloom.ipynb) — measures the Fourier-circle structure at five different locations inside the trained network. Produces Fig. 2 (`multiloc_diffusion.png`).
- [`notebooks/steering_methods.ipynb`](notebooks/steering_methods.ipynb) — six steering methods compared head-to-head: dictation, walking, the linear chord baseline, and three controls.

`multi_location_bloom.ipynb` and `steering_methods.ipynb` both read the snapshot file produced by `training_slowmo.ipynb`. Run that notebook first.

### Data

JSON files containing the raw numbers behind each panel of the writeup. Re-plotting or re-analyzing without re-running the notebooks is one read away.

- `data/slowmo_training.json` — per-step training and test accuracy.
- `data/handcrafted_verification.json` — accuracy of the hand-built model on the full input set.
- `data/multiloc_bloom.json` — Fourier-circle quality (CV) per training step, per location.
- `data/steering2_hit_rates.json` — hit rates for six steering methods, per Δ.
- `data/steering3_per_seed.json` — per-seed hit rates across ten independently trained models.

## The setup

A 2-block transformer with residual dimension 384, SwiGLU FFN, RMSNorm, AdamW. Task: c = a · b⁻¹ mod 97 over the multiplicative group of order 96. The visualizations project the unembedding matrix `W_U` onto three of its own Fourier directions. No t-SNE, no PCA. Each axis is a column-projection of `W_U` onto a real cosine or sine basis vector.

## What this is, in one paragraph

A trained transformer solving mod-97 division does not memorize a lookup table. The 96 invertible remainders arrange themselves on a precise 3D Fourier knot inside the residual stream, and the network reads its predictions off that knot. Once you can see this, two things follow. First, you can write the model by hand from the same recipe, with no training, and get 100% accuracy. Second, you can shift the model's predictions from outside, by walking along the knot rather than pushing sideways through it. Walking hits 96.7%. Direct manifold replacement hits 100%. The standard linear activation-steering vector caps at about 50%, because the algorithmic direction is curved.

## Citation

If this work shows up in a paper or thread, a link to the site or the repo is enough.

Nikolay Yudin. *Fourier Bloom: How a small transformer learns modular division.* 2026.
https://nick-yudin.github.io/fourier-bloom/
