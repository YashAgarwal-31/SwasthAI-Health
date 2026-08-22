"""Train reproducible screening models from official UCI datasets.

Run: python -m ml.train_models
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from ucimlrepo import fetch_ucirepo
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

OUT = Path(__file__).resolve().parent / "saved_models"
OUT.mkdir(parents=True, exist_ok=True)

def evaluate(y_true, probability) -> dict[str, float]:
    prediction = (probability >= .5).astype(int)
    return {"accuracy": accuracy_score(y_true,prediction), "precision": precision_score(y_true,prediction,zero_division=0), "recall": recall_score(y_true,prediction,zero_division=0), "f1": f1_score(y_true,prediction,zero_division=0), "roc_auc": roc_auc_score(y_true,probability)}

def train_one(name: str, X: pd.DataFrame, y: pd.Series, source: str) -> dict:
    X = X.apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(y, errors="coerce").fillna(0).astype(int)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1500,class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=40,max_depth=6,min_samples_leaf=5,class_weight="balanced",random_state=42,n_jobs=-1),
    }
    scores={}; fitted={}
    for label, estimator in candidates.items():
        pipeline=Pipeline([("imputer",SimpleImputer(strategy="median")),("scaler",StandardScaler()),("model",estimator)])
        pipeline.fit(X_train,y_train); scores[label]=evaluate(y_test,pipeline.predict_proba(X_test)[:,1]); fitted[label]=pipeline
    best=max(scores,key=lambda label:scores[label]["roc_auc"]); model=fitted[best]
    joblib.dump(model,OUT/f"{name}.joblib",compress=9); joblib.dump(X_train.sample(min(100,len(X_train)),random_state=42),OUT/f"{name}_background.joblib",compress=9)
    metadata={"name":name,"selected_model":best,"source":source,"features":list(X.columns),"metrics":scores}
    (OUT/f"{name}_metrics.json").write_text(json.dumps(metadata,indent=2))
    return metadata

def load_uci(dataset_id: int) -> tuple[pd.DataFrame, pd.Series]:
    """Prefer optional local CSVs, otherwise fetch through the official UCI client."""
    local_dir=os.getenv("SWASTHAI_DATA_DIR")
    if local_dir:
        frame=pd.read_csv(Path(local_dir)/f"{dataset_id}.csv")
        target="Diabetes_binary" if dataset_id==891 else "num"
        return frame.drop(columns=[target,"ID"],errors="ignore"),frame[target]
    dataset=fetch_ucirepo(id=dataset_id)
    return dataset.data.features,dataset.data.targets.squeeze()

def main() -> None:
    dx,dy=load_uci(891)
    dfeatures=[c for c in ["HighBP","HighChol","BMI","Smoker","Stroke","HeartDiseaseorAttack","PhysActivity","GenHlth","Age"] if c in dx]
    train_one("diabetes",dx[dfeatures],(dy>0).astype(int),"UCI CDC Diabetes Health Indicators (ID 891)")
    hx,hy=load_uci(45)
    hfeatures=[c for c in ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"] if c in hx]
    train_one("heart_disease",hx[hfeatures],(pd.to_numeric(hy,errors="coerce")>0).astype(int),"UCI Heart Disease (ID 45)")
    hbp_target=pd.to_numeric(dx["HighBP"],errors="coerce").fillna(0).astype(int)
    bp_features=[c for c in dfeatures if c!="HighBP"]
    train_one("hypertension",dx[bp_features],hbp_target,"UCI CDC Diabetes Health Indicators (ID 891)")
    print(f"Models and evaluation metadata saved to {OUT}")

if __name__ == "__main__": main()
