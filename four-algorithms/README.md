# Four algorithms in one tiny brain

Part 2 of the *Inside the grokked manifold* series. A small 4.8M-parameter transformer with one shared output head learns four arithmetic tasks at once — division, addition, max, and parity — at P=149, WD=0.3, across 5 random seeds.

**Read the longform**: [`index.html`](index.html) (or open the live page if hosted).

## What's in this folder

- `index.html` — the longform article with seven inline interactive scenes.
- `build.py` — rebuilds `index.html` from the local JSON bundle.
- `data.json`, `walk_results.json`, `dictation_results.json`, `walk_summary.json`, `handcraft_summary.json` — preprocessed bundles consumed by the page.
- `fig_struct1_fourier_circles_tok_emb.png`, `fig2_residual_fourier.png` — handcrafted-max diagnostic figures used inline.
- `notebooks/` — four self-contained Jupyter notebooks that reproduce every claim in the longform.

## Notebooks

All notebooks are standalone. They install dependencies, pull state dicts from the [Hugging Face Hub dataset](https://huggingface.co/datasets/NikolayYudin/manifold-features-data) when needed, and write outputs into `./out/` next to the notebook.

| Notebook | What it does | Wall time |
|---|---|---|
| [`train_5seeds.ipynb`](notebooks/train_5seeds.ipynb) | Trains 5 seeds of the 4-task transformer; saves `out/seed_{N}/final.pt` and snapshots. | ~10–20 min/seed on A100 |
| [`walk_and_dictation.ipynb`](notebooks/walk_and_dictation.ipynb) | Loads seed 1000, computes per-class L2 manifolds, runs chord walk / linear tangent / random direction / dictation sweeps. Saves `walk_results.json`, `dictation_results.json`. | ~3 min |
| [`handcraft_max.ipynb`](notebooks/handcraft_max.ipynb) | Builds a 2-block transformer that solves `max(a, b) mod 97` by formula (no training); verifies 100% on all 9409 pairs; visualises Fourier circles in `tok_emb` and a weight-norm map. | <1 min on CPU |
| [`multilocation_analysis.ipynb`](notebooks/multilocation_analysis.ipynb) | Generates the cross-basis 4×4 grid, the multi-location 4×9 grid, and the parity↔add Nyquist coupling trace. | ~5 min |

### Quick start

```bash
# Open any notebook in Colab via the "Open in Colab" badge, or locally:
pip install torch matplotlib numpy huggingface_hub
jupyter notebook notebooks/walk_and_dictation.ipynb
```

The first notebook to run end-to-end should be `walk_and_dictation.ipynb`, since it pulls the trained checkpoint from the Hub and lets you immediately verify the steering numbers without training anything yourself.

## Headline numbers

- **Five seeds, four tasks, all grokked.** Mean grok step (WD=0.3): max 258, parity 2840, div 4168, add 5294. Baseline WD=1.0 takes 22780 steps to grok add — WD=0.3 makes it 4.3× faster.
- **Chord walk on the 4 manifolds.** ≥ 97% across Δ ∈ ±100 on all four tasks.
- **Dictation.** 100% on every target class for every task.
- **Handcrafted max.** 9409 / 9409 input pairs correct, weights placed entirely by formula.

## Reproducibility

State dicts: [`NikolayYudin/manifold-features-data`](https://huggingface.co/datasets/NikolayYudin/manifold-features-data) (`four-algorithms/seed_{1000..1004}_final.pt`, `four-algorithms/handcraft_max.pt`).

If you'd rather train from scratch, run `train_5seeds.ipynb` first; the other notebooks will pick up local `./out/seed_{N}/final.pt` files before falling back to the Hub.

## Series

- **Part 1** — [single algorithm (div mod 97)](../fourier-bloom/) — the W_U bloom, handcrafted div by formula, steering on the learned model.
- **Part 2** — *this folder* — four algorithms in one shared head.
- **Part 3** — grokking, in general. *Coming.*
- **Part 4** — manifold transfer to a real LLM + MAFT (Manifold-Anchored Fine-Tuning). *Coming.*
