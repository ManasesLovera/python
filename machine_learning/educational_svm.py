# -----------------------------------------------------------
# Educational, step-by-step demo of a Linear SVM for text.
# -----------------------------------------------------------
# Features:
#  - Generates tiny synthetic text for 3 classes (Invoice, Work Letter, ID)
#  - Vectorizes with TF-IDF and reduces to 2D via TruncatedSVD (for plotting)
#  - Trains a linear SVM (SGD hinge loss, one-vs-rest) *one sample at a time*
#  - Press SPACE to step forward, F to fast-forward, R to reset
#  - Shows decision boundaries, margins, and points near margins
#  - Displays the actual text used for the last training update
#
# -----------------------------------------------------------

import numpy as np
import random
import textwrap
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# -----------------------------
# 1. Data Generation
# -----------------------------
random.seed(1)
np.random.seed(1)

invoice_templates = [
    "Invoice #{num} for services rendered. Total amount due is {amt} by {date}. Payment terms net 30.",
    "This invoice includes VAT and line items. Balance: {amt}. Please pay before {date}.",
    "Customer: ACME Corp. Invoice total {amt}. Due date {date}. Subtotal, taxes, and total are listed."
]

workletter_templates = [
    "This letter confirms {name}'s employment as {role} starting on {date}. Monthly salary is {amt}.",
    "To whom it may concern, {name} has been employed full-time as {role} since {date}.",
    "Employment verification: {name}, position {role}, start date {date}. HR confirms current status."
]

id_templates = [
    "Government ID Card. Name: {name}. Date of Birth: {dob}. ID Number: {num}. Expires: {date}.",
    "Passport document. Holder: {name}. Passport No: {num}. Issue date {dob}, expiry {date}.",
    "Driver license of {name}. License number {num}. DOB {dob}. Valid until {date}.",
]

names = ["Ana Morales", "Luis Pérez", "John Smith", "Maria Garcia", "Wei Chen", "Aisha Khan"]
roles = ["Data Analyst", "Engineer", "HR Manager", "Technician", "Developer", "Accountant"]

def rand_num(): return str(np.random.randint(10000, 99999))
def rand_amt(): return f"${np.random.randint(50, 2500)}.{np.random.randint(0,99):02d}"
def rand_date(): return f"{np.random.randint(1,12):02d}/{np.random.randint(1,28):02d}/2025"
def rand_dob(): return f"{np.random.randint(1,12):02d}/{np.random.randint(1,28):02d}/{np.random.randint(1970,2005)}"

def make_samples(templates: list[str], n: int):
    txts: list[str] = []
    for _ in range(n):
        t = random.choice(templates)
        s = t.format(
            num=rand_num(), amt=rand_amt(), date=rand_date(),
            name=random.choice(names), role=random.choice(roles), dob=rand_dob()
        )
        txts.append(s)
    return txts

N_TRAIN_PER_CLASS = 14
N_TEST_PER_CLASS = 6

train_texts: list[str] = []
train_labels: list[str] = []
test_texts: list[str] = []
test_labels: list[str] = []

for label, templates in [("Invoice", invoice_templates),
                         ("Work Letter", workletter_templates),
                         ("Id", id_templates)]:
    train_texts += make_samples(templates, N_TRAIN_PER_CLASS)
    train_labels += [label] * N_TRAIN_PER_CLASS
    test_texts += make_samples(templates, N_TEST_PER_CLASS)
    test_labels += [label] * N_TEST_PER_CLASS

# -----------------------------
# 2. Text → Features → 2D
# -----------------------------
vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=1)
X_train_tfidf = vectorizer.fit_transform(train_texts)
X_test_tfidf = vectorizer.transform(test_texts)

svd = TruncatedSVD(n_components=2, random_state=1)
X_train_2d = svd.fit_transform(X_train_tfidf)
X_test_2d = svd.transform(X_test_tfidf)

le = LabelEncoder()
y_train = np.array(le.fit_transform(train_labels))
y_test = le.transform(test_labels)
class_names = list(le.classes_)

# -----------------------------
# 3. Step-by-Step SVM
# -----------------------------
@dataclass
class TrainerState:
    clf: SGDClassifier
    step: int
    order: np.ndarray
    pos: int
    inited: bool

def make_clf():
    return SGDClassifier(loss="hinge", alpha=1e-4, random_state=1)

def reset_trainer():
    order = np.tile(np.random.permutation(len(y_train)), 15)
    return TrainerState(clf=make_clf(), step=0, order=order, pos=0, inited=False)

state = reset_trainer()

# -----------------------------
# 4. Plotting
# -----------------------------
fig, ax = plt.subplots(figsize=(8, 6))

def _decision_regions(xx, yy):
    grid = np.c_[xx.ravel(), yy.ravel()]
    scores = state.clf.decision_function(grid)
    if scores.ndim == 1:
        Z = (scores > 0).astype(int)
    else:
        Z = np.argmax(scores, axis=1)
    return Z.reshape(xx.shape)

def _highlight_near_margin():
    if not hasattr(state.clf, "coef_"): return
    xs = X_train_2d
    coefs = state.clf.coef_
    intercepts = state.clf.intercept_
    thr = 0.12
    near_idx = set()
    for k in range(coefs.shape[0]):
        w = coefs[k]; b = intercepts[k]
        margins = xs @ w + b
        near = np.where(np.abs(np.abs(margins) - 1.0) < thr)[0]
        for i in near: near_idx.add(i)
    for i in sorted(list(near_idx)):
        ax.scatter(xs[i,0], xs[i,1], s=160, facecolors="none", edgecolors="k", linewidths=1.0)

def _wrap(text, width=48):
    return "\n".join(textwrap.wrap(text, width=width))

def draw_plot(sample_info=None):
    ax.clear()
    if state.inited:
        x_min, x_max = X_train_2d[:,0].min()-0.5, X_train_2d[:,0].max()+0.5
        y_min, y_max = X_train_2d[:,1].min()-0.5, X_train_2d[:,1].max()+0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 250),
                             np.linspace(y_min, y_max, 250))
        Z = _decision_regions(xx, yy)
        ax.contourf(xx, yy, Z, alpha=0.15)

    for k, cname in enumerate(class_names):
        idx_tr = np.where(y_train == k)[0]
        ax.scatter(X_train_2d[idx_tr,0], X_train_2d[idx_tr,1], label=f"Train: {cname}", s=34)
    for k, cname in enumerate(class_names):
        idx_te = np.where(y_test == k)[0]
        ax.scatter(X_test_2d[idx_te,0], X_test_2d[idx_te,1], label=f"Test: {cname}", s=52, marker=MarkerStyle('x'), linewidths=1.3)

    if state.inited and hasattr(state.clf, "coef_"):
        coefs = state.clf.coef_
        intercepts = state.clf.intercept_
        for k in range(coefs.shape[0]):
            w = coefs[k]; b = intercepts[k]
            if abs(w[1]) < 1e-8:
                xs = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 2)
                y_lo, y_hi = ax.get_ylim()
                x0 = -b / (w[0] + 1e-8)
                ax.plot([x0, x0], [y_lo, y_hi])
            else:
                xs = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 220)
                ys = -(w[0]/w[1]) * xs - b / w[1]
                ax.plot(xs, ys, linewidth=1.6)
                ys1 = -(w[0]/w[1]) * xs - (b + 1.0) / w[1]
                ys2 = -(w[0]/w[1]) * xs - (b - 1.0) / w[1]
                ax.plot(xs, ys1, linestyle="--", linewidth=1.0)
                ax.plot(xs, ys2, linestyle="--", linewidth=1.0)
        _highlight_near_margin()

    ax.set_xlabel("LSA Component 1")
    ax.set_ylabel("LSA Component 2")
    ax.set_title("Linear SVM for Text (OvR) — SPACE=step, F=+10, R=reset")
    ax.legend(loc="lower right")

    if state.inited:
        y_pred_tr = state.clf.predict(X_train_2d)
        y_pred_te = state.clf.predict(X_test_2d)
        info = f"Step: {state.step} | Train acc: {accuracy_score(y_train, y_pred_tr):.2f} | Test acc: {accuracy_score(y_test, y_pred_te):.2f}"
    else:
        info = "Step: 0 | Not trained yet"
    ax.text(0.02, 0.98, info, transform=ax.transAxes, va="top", ha="left")

    expl = textwrap.dedent("""\
        Pipeline:
        Text → TF-IDF (1–2 grams) → 2D SVD (LSA) → Linear SVM (OvR)
        Solid lines: decision boundaries
        Dashed lines: ±1 margins
        Hollow circles: points near margins
    """)
    ax.text(1.02, 0.5, expl, transform=ax.transAxes, va="center", ha="left")

    if sample_info is not None:
        txt = _wrap(f"[Last step] {sample_info['label']}: {sample_info['text']}", width=46)
        ax.text(1.02, 0.04, txt, transform=ax.transAxes, va="bottom", ha="left")

    plt.tight_layout()
    fig.canvas.draw_idle()

def do_one_step(n_steps=1):
    global state
    last_sample = None
    for _ in range(n_steps):
        if state.pos >= len(state.order): break
        i = state.order[state.pos]
        Xi = X_train_2d[i].reshape(1, -1)
        yi = np.array([y_train[i]])
        if not state.inited:
            state.clf.partial_fit(Xi, yi, classes=np.unique(y_train))
            state.inited = True
        else:
            state.clf.partial_fit(Xi, yi)
        state.step += 1; state.pos += 1
        last_sample = {"text": train_texts[i], "label": le.inverse_transform([y_train[i]])[0]}
    draw_plot(sample_info=last_sample)

def on_key(event):
    if event.key == " ": do_one_step(1)
    elif event.key in ("f","F"): do_one_step(10)
    elif event.key in ("r","R"):
        global state
        state = reset_trainer()
        draw_plot(sample_info=None)

cid = fig.canvas.mpl_connect('key_press_event', on_key)
draw_plot(sample_info=None)
plt.show()