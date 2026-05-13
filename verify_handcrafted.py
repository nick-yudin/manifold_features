#!/usr/bin/env python3
"""
Verify the hand-built transformer reproduces mod-97 division at 100% accuracy.

Loads handcrafted_state_dict.pt — weights written by hand, no training —
runs it through all 9216 (a, b) input pairs, and prints the accuracy.

Runs in under a minute on CPU. No GPU required, no training involved.

Usage:
    python verify_handcrafted.py
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

P = 97          # modulus
D_MODEL = 384   # residual dimension
N_HEADS = 4
HC_PATH = 'handcrafted_state_dict.pt'


class RMSNorm(nn.Module):
    def __init__(self, d, eps=1e-8):
        super().__init__()
        self.scale = nn.Parameter(torch.ones(d))
        self.eps = eps

    def forward(self, x):
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * self.scale


class GrokBlock(nn.Module):
    def __init__(self, d, nh):
        super().__init__()
        self.norm1 = RMSNorm(d)
        self.attn = nn.MultiheadAttention(d, nh, dropout=0.0, batch_first=True)
        self.norm2 = RMSNorm(d)
        self.w1 = nn.Linear(d, 4 * d, bias=False)
        self.w2 = nn.Linear(4 * d, d, bias=False)
        self.w3 = nn.Linear(d, 4 * d, bias=False)

    def forward(self, x):
        h = self.norm1(x)
        o, _ = self.attn(h, h, h, need_weights=False)
        x = x + o
        h2 = self.norm2(x)
        gate = F.silu(self.w1(h2))
        return x + self.w2(gate * self.w3(h2))


class GrokModel(nn.Module):
    def __init__(self, p=P, d=D_MODEL, nh=N_HEADS):
        super().__init__()
        self.tok_emb = nn.Embedding(p + 2, d)
        self.pos_emb = nn.Embedding(4, d)
        self.blocks = nn.ModuleList([GrokBlock(d, nh) for _ in range(2)])
        self.norm_f = RMSNorm(d)
        self.head = nn.Linear(d, p, bias=False)
        self.p = p

    def forward(self, a, b):
        B = a.size(0)
        op = torch.full((B,), self.p, dtype=torch.long)
        eq = torch.full((B,), self.p + 1, dtype=torch.long)
        tok = torch.stack([a, op, b, eq], dim=1)
        pos = torch.arange(4).unsqueeze(0).expand(B, -1)
        x = self.tok_emb(tok) + self.pos_emb(pos)
        for bl in self.blocks:
            x = bl(x)
        return self.head(self.norm_f(x)[:, -1, :])


def main():
    print(f'Loading hand-built weights from {HC_PATH}')
    sd = torch.load(HC_PATH, map_location='cpu', weights_only=True)
    m = GrokModel()
    m.load_state_dict({k: v.float() for k, v in sd.items()}, strict=False)
    m.eval()

    # Build all 9216 (a, b) input pairs and their correct outputs
    # c = a * b^(-1) mod P  (Fermat's little theorem for the inverse)
    all_a, all_b, all_c = [], [], []
    for a in range(1, P):
        for b in range(1, P):
            all_a.append(a)
            all_b.append(b)
            all_c.append((a * pow(b, P - 2, P)) % P)
    a_t = torch.tensor(all_a, dtype=torch.long)
    b_t = torch.tensor(all_b, dtype=torch.long)
    c_t = torch.tensor(all_c, dtype=torch.long)

    print(f'Running through {len(all_a)} (a, b) pairs...')
    with torch.no_grad():
        correct = 0
        BS = 256
        for i in range(0, len(all_a), BS):
            preds = m(a_t[i:i+BS], b_t[i:i+BS]).argmax(-1)
            correct += int((preds == c_t[i:i+BS]).sum())

    print()
    print(f'  {correct}/{len(all_a)} correct = {100 * correct / len(all_a):.4f}%')
    print()
    if correct == len(all_a):
        print('  No training. Just the algorithm written into the weights.')
    else:
        print('  Something is off — expected 100%.')


if __name__ == '__main__':
    main()
