"""Load trained pipelines, predict probabilities and calculate local SHAP evidence."""
from __future__ import annotations
import json
from pathlib import Path
import joblib
import pandas as pd

ROOT=Path(__file__).resolve().parent/"saved_models"

def available_models() -> list[str]: return [p.stem for p in ROOT.glob("*.joblib") if not p.stem.endswith("_background")]

def metadata(name: str) -> dict:
    path=ROOT/f"{name}_metrics.json"
    return json.loads(path.read_text()) if path.exists() else {}

def predict(name: str, values: dict[str,float]) -> tuple[float,str]:
    model=joblib.load(ROOT/f"{name}.joblib"); frame=pd.DataFrame([{f:values.get(f,0) for f in metadata(name)["features"]}])
    probability=float(model.predict_proba(frame)[0,1]); risk="High" if probability>=.65 else "Medium" if probability>=.35 else "Low"
    return probability,risk

def shap_factors(name: str, values: dict[str,float], top_k: int=6) -> list[dict]:
    import shap
    model=joblib.load(ROOT/f"{name}.joblib"); background=joblib.load(ROOT/f"{name}_background.joblib"); frame=pd.DataFrame([{f:values.get(f,0) for f in metadata(name)["features"]}])
    explainer=shap.Explainer(model.predict_proba,background); explanation=explainer(frame)
    raw=explanation.values[0]; contributions=raw[:,1] if raw.ndim==2 else raw
    ranked=sorted(zip(frame.columns,contributions,frame.iloc[0]),key=lambda x:abs(float(x[1])),reverse=True)[:top_k]
    return [{"feature":f,"impact":float(impact),"value":float(value)} for f,impact,value in ranked]
