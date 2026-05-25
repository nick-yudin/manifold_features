# Algorithms in a real LLM

Part 4 of the *Manifold Features* series. Llama 3.1 8B replicated against Goodfire's two arithmetic-mechinterp papers ([2605.01148](https://arxiv.org/abs/2605.01148), [2605.05115](https://arxiv.org/abs/2605.05115)) plus our own follow-up controls: multi-layer ablation, multi-layer steering catastrophe, manifold walking at L=18, and a direct test of whether the toy from Parts 1–2 transfers up.

**Read the longform**: [`index.html`](index.html) (or open the live page if hosted).

## What's in this folder

- `index.html` — the longform article with six inline figures.
- `fig0_toy_algorithm_absent.png` — Llama baseline accuracy across modular-division problems P ∈ {3, 5, 7, 11, 13, 23, 97}; the toy's dlog-Fourier algorithm doesn't transfer.
- `fig1_goodfire_weekdays_steering.png` — Goodfire's Fourier-rotation steering on weekday Q/A at L=18, replicated.
- `fig2_multilayer_ablation.png` — single-layer ablation of the Fourier subspace, layer-by-layer, on addition + country-capital control.
- `fig3_multilayer_steering_catastrophe.png` — what happens when you stack Goodfire's α=10 rotation across 1, 2, 3, and 5 layers.
- `fig4_manifold_walk.png` — 50-step centroid replacement at L=18 vs linear chord interpolation, P(day) trajectory along Mon→Fri.
- `fig5_alpha_sweep.png` — single-layer α sweep (the optimum is α=5, not Goodfire's α=10) + a distributed-budget control.
- `notebooks/` — four standalone Jupyter notebooks that reproduce every claim in the longform.

## Notebooks

All notebooks are standalone. They install dependencies, pull the Llama 3.1 8B base checkpoint from the Hugging Face Hub, and write outputs into `./out/` next to the notebook. Each one runs end-to-end on a single A100 (40 GB) or L4 (24 GB) in Colab.

| Notebook | What it does | Wall time |
|---|---|---|
| [`toy_algorithms_absence.ipynb`](notebooks/toy_algorithms_absence.ipynb) | For P ∈ {3, 5, 7, 11, 13, 23, 97}, builds (a, b, c=a·b⁻¹ mod P) triples, extracts L=18 residuals, fits Fourier probes in two bases (natural and dlog). Shows the toy's R² > 0.93 dlog-circles do not exist in Llama. | ~10 min on L4 |
| [`goodfire_replication.ipynb`](notebooks/goodfire_replication.ipynb) | Replicates Goodfire's L=18 base-10 calculator: extracts the six clocks T ∈ {2, 5, 10, 20, 50, 100}, applies Fourier rotation steering on weekday and month Q/A. Produces fig1 + the heatmaps + hit-rate numbers reported in §3. | ~15 min on A100 |
| [`multilayer_ablation.ipynb`](notebooks/multilayer_ablation.ipynb) | Single-layer ablation of the Fourier subspace across layers 15–32 on addition. Country-capital control on the same layers. Produces fig2 and the localization claim of §4. | ~20 min on A100 |
| [`manifold_walking.ipynb`](notebooks/manifold_walking.ipynb) | The main positive result. 50-step centroid walk at L=18 from `Mon` to `Fri` vs linear interpolation; α-sweep (single-layer optimum is α=5, not 10); multi-layer steering catastrophe (1, 2, 3, 5 layers at α=10 each). Produces fig3, fig4, fig5. | ~30 min on A100 |

### Quick start

```bash
# Open any notebook in Colab via the "Open in Colab" badge, or locally:
pip install torch transformers matplotlib numpy huggingface_hub
jupyter notebook notebooks/manifold_walking.ipynb
```

The notebook to run first is `goodfire_replication.ipynb` — it caches per-class centroids at L=18 to `./out/`, which the other three notebooks read.

## Headline numbers

- **The toy's algorithm is not in Llama.** Dlog-Fourier probe R² is near zero or negative for all P ∈ {3, 5, 7, 11, 13, 23, 97}. At P=97, toy gets R² > 0.93; Llama gets −0.14.
- **Goodfire's six-clock calculator replicates.** Periods T ∈ {2, 5, 10, 20, 50, 100} are present at L=18. Single-layer Fourier-rotation steering hits 60% on weekdays, 65% on months, 55% on hours.
- **Single-layer ablation localizes the calculator to L=18–20.** Ablating Fourier subspaces of those layers drops addition accuracy by 45–49 pp. Country-capital control unaffected.
- **Multi-layer steering catastrophe at α=10.** Stacking 5 layers at Goodfire's published default drops cross-task (weekdays, months) to ~0%. Addition (probes' native task) is only mildly affected.
- **α=5 single-layer beats α=10.** Sweep peaks at α=5 with hit rate 65% on weekdays, 79% on months — above the published default.
- **Manifold walking ≈ linear teleporting.** 50-step centroid replacement at L=18 produces smooth ordered hand-offs through `Mon → Tue → Wed → Thu → Fri`. Linear interpolation in 4096-d teleports through `Sun` at the midpoint.

## Reproducibility

Llama 3.1 8B base ([`meta-llama/Llama-3.1-8B`](https://huggingface.co/meta-llama/Llama-3.1-8B)) is gated; you need a Hugging Face access token with the model agreement accepted. All other data is in this repo or computed in-notebook. State dicts that are too large for git — per-class L=18 centroids, addition-probe directions — are also published to the [`NikolayYudin/manifold-features-data`](https://huggingface.co/datasets/NikolayYudin/manifold-features-data) Hub dataset under the `algorithms-in-real-LLMs/` prefix.

## Series

- **Part 1** — [single algorithm (div mod 97)](../fourier-bloom/) — the W_U bloom, handcrafted div by formula, steering on the learned model.
- **Part 2** — [four algorithms in one shared head](../four-algorithms/) — div, add, max, parity at P=149.
- **Part 3** — grokking, in general. *Coming.*
- **Part 4** — *this folder* — algorithms in a real LLM.
