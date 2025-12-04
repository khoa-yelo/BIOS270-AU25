### **1. Project Overview**

**Goal:**
Build a machine-learning model to **predict post-operative complications** in orthopedic surgery patients using both structured EHR data and text from operative reports.

**Why it matters:**
Complications after surgery are costly and can extend recovery. Doctors currently find risk factors by reading patient charts manually. A predictive model could help flag high-risk cases earlier and support clinical decisions.

**Aims:**

1. Use structured data (e.g., age, BMI, labs) to train a simple classifier.
2. Add text features from operative notes using BioClinicalBERT to improve predictions.

---

### **2. Data**

* **Source:** Stanford STARR database (Orthopedic Surgery EHR data).
* **Size:** ≈ 3 000 patients, ~200 features + operative notes.
* **Format:** CSV (for numbers) and plain text (for notes).

**Preprocessing:**

* Normalize numerical features and encode categorical ones.
* Tokenize text and truncate to 512 tokens.
* Merge modalities by patient ID and split into train / validation / test sets.

**Storage:** Data stored on Stanford Farmshare (`~/project2/data`) with secure backup.

---

### **3. Environment**

* **Platform:** Stanford Farmshare HPC with GPU.
* **Language:** Python 3.10 (Jupyter Notebook or VS Code Remote SSH).
* **Libraries:** `pandas`, `numpy`, `scikit-learn`, `xgboost`, `transformers`, `torch`.
* **Reproducibility:** Code under GitHub with `requirements.txt` for environment setup.

---

### **4. Pipeline**

1. Load and clean data.
2. Engineer features (structured + text embeddings).
3. Train baseline XGBoost model.
4. Fine-tune BioClinicalBERT and combine outputs.
5. Evaluate and plot results (ROC curve, confusion matrix).

---

### **5. Machine Learning**

* **Task:** Binary classification (Complication = 1, No Complication = 0).
* **Features:** Tabular variables + text embeddings (768-D).
* **Models:** XGBoost → Hybrid (BERT + MLP).
* **Evaluation:** AUROC, F1, precision, recall.
* **Generalization:** 5-fold cross-validation to prevent data leakage.

---

### **Expected Outcome**

A working ML pipeline that predicts surgical complications and shows that combining text and structured data improves accuracy over using either alone.
This could help build future AI tools for clinical decision support in orthopedic surgery.

---

Would you like me to make this a nicely formatted `.md` file (with headers, spacing, and bullet alignment ready to copy-paste into GitHub)?


