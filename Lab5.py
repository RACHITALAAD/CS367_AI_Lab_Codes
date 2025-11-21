import argparse
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler

def download_price(sym: str, start: str, end: str) -> pd.Series:
    df = yf.download(sym, start=start, end=end, progress=False)
    if df.empty:
        raise ValueError(f"No data for {sym} between {start} and {end}")
    if 'Adj Close' in df.columns:
        return df['Adj Close'].rename(sym)
    return df.iloc[:, 4].rename(sym)

def compute_returns(prices: pd.Series) -> pd.Series:
    r = prices.pct_change().dropna()
    r.name = 'returns'
    return r

def fit_hmm(X: np.ndarray, n_states: int, n_init: int = 5, random_state: int = 42, max_iter: int = 200):
    best_model = None
    best_score = -np.inf
    for i in range(n_init):
        model = GaussianHMM(n_components=n_states, covariance_type="diag",
                            n_iter=max_iter, random_state=random_state + i, verbose=False)
        try:
            model.fit(X)
            score = model.score(X)
        except:
            continue
        if score > best_score:
            best_model = model
            best_score = score
    if best_model is None:
        raise RuntimeError("HMM fitting failed")
    return best_model, best_score

def order_states_by_var(means: np.ndarray, covs: np.ndarray):
    vars_ = covs if covs.ndim == 1 else covs.flatten()
    return np.argsort(vars_)

def plot_price(dates, prices, states, labels, out=None):
    plt.figure(figsize=(14,6))
    for s in np.unique(states):
        mask = (states == s)
        plt.plot(dates[mask], prices[mask], linestyle='-', marker='.', linewidth=1, markersize=2, label=f"{labels[s]} (state {s})")
    plt.title("Price colored by HMM states")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc="best")
    plt.tight_layout()
    if out:
        plt.savefig(out, dpi=150)
    plt.show()

def plot_returns(dates, returns, states, out=None):
    fig, (ax1, ax2) = plt.subplots(2,1,figsize=(14,8), sharex=True, gridspec_kw={'height_ratios':[3,1]})
    ax1.plot(dates, returns, linewidth=0.8)
    ax1.set_ylabel("Returns")
    ax1.set_title("Returns (top) and States (bottom)")
    ax2.step(dates, states, where='mid')
    ax2.set_ylabel("State")
    ax2.set_xlabel("Date")
    plt.tight_layout()
    if out:
        plt.savefig(out, dpi=150)
    plt.show()

def run(symbol: str, start: str, end: str, n_states: int, outdir: str, scale: bool):
    os.makedirs(outdir, exist_ok=True)
    prices = download_price(symbol, start, end)
    returns = compute_returns(prices)
    X = returns.values.reshape(-1,1)
    if scale:
        X = StandardScaler().fit_transform(X)
    model, score = fit_hmm(X, n_states, n_init=8)
    means = model.means_.flatten()
    covs = model.covars_.flatten() if model.covariance_type == "diag" else np.array([np.diag(c) for c in model.covars_]).flatten()
    trans = model.transmat_
    order = order_states_by_var(means, covs)
    means_ord = means[order]
    covs_ord = covs[order]
    trans_ord = trans[order][:, order]
    hidden_raw = model.predict(X)
    raw_to_ord = {r: int(np.where(order==r)[0]) for r in range(n_states)}
    hidden = np.array([raw_to_ord[r] for r in hidden_raw])
    highest_var = int(np.argmax(covs_ord))
    labels = ["High Volatility" if s==highest_var else "Low/Moderate Volatility" for s in range(n_states)]
    price_dates = prices.index[1:]
    price_vals = prices.iloc[1:].values
    plot_price(price_dates, price_vals, hidden, labels, out=os.path.join(outdir,f"{symbol}_price_states.png"))
    plot_returns(returns.index, returns.values, hidden, out=os.path.join(outdir,f"{symbol}_returns_states.png"))
    pd.DataFrame({"state":[f"S{i}" for i in range(n_states)], "mean":means_ord, "variance":covs_ord, "std":np.sqrt(covs_ord), "label":labels}).to_csv(os.path.join(outdir,f"{symbol}_hmm_state_params.csv"), index=False)
    pd.DataFrame(trans_ord, index=[f"S{i}" for i in range(n_states)], columns=[f"S{i}" for i in range(n_states)]).to_csv(os.path.join(outdir,f"{symbol}_hmm_transition_matrix.csv"))
    last = int(hidden[-1])
    next_probs = trans_ord[last]
    expected_next = np.dot(next_probs, means_ord)
    print(f"Last state S{last} ({labels[last]})")
    for s in range(n_states):
        print(f"P(next S{s}={labels[s]})={next_probs[s]:.4f}")
    print(f"Expected next return={expected_next:.6f}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, default="AAPL")
    parser.add_argument("--start", type=str, default="2013-01-01")
    parser.add_argument("--end", type=str, default="2023-12-31")
    parser.add_argument("--n_states", type=int, default=2)
    parser.add_argument("--outdir", type=str, default="hmm_outputs")
    parser.add_argument("--scale", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run(symbol=args.symbol, start=args.start, end=args.end, n_states=args.n_states, outdir=args.outdir, scale=args.scale)
