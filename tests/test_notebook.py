import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import nbformat
import numpy as np
import pandas as pd
from nbclient import NotebookClient

class NotebookTest(unittest.TestCase):
    def test_notebook_depuis_les_deux_dossiers(self):
        repo = Path(__file__).resolve().parents[1]
        notebook = (repo / "notebooks/final_model.ipynb").read_bytes()
        official = (repo / "submissions/submission_xgb_glm.csv").read_bytes()
        with TemporaryDirectory(prefix="assurprime-") as tmp:
            root = Path(tmp)
            for name in ("notebooks", "data", "submissions"):
                (root / name).mkdir()
            (root / "notebooks/final_model.ipynb").write_bytes(notebook)
            (root / "submissions/submission_xgb_glm.csv").write_bytes(official)
            rng = np.random.default_rng(42)
            features = pd.DataFrame({
                "ID": np.arange(240),
                "ANNEE_ASSURANCE": rng.uniform(0.5, 4, 240),
                "CAPITAL": rng.uniform(0.1, 3, 240),
                "REGION": rng.choice(["A", "B", "C"], 240),
            })
            freq = rng.poisson(0.45, 200)
            target = pd.DataFrame({
                "ANNEE_ASSURANCE": features["ANNEE_ASSURANCE"].iloc[:200],
                "FREQ": freq,
                "CHARGE": freq * rng.uniform(10, 200, 200),
            })
            features.iloc[:200].to_csv(root / "data/xtrain_input_Z61KlZo.csv", index=False)
            features.iloc[200:].to_csv(root / "data/test_input_5qJzHrr.csv", index=False)
            target.to_csv(root / "data/ytrain_output_DzPxaPY.csv", index=False)
            # Execute the complete notebook with working directories used by Jupyter and CLI tools.
            for cwd in (root, root / "notebooks"):
                nb = nbformat.reads(notebook.decode(), as_version=4)
                nbformat.validate(nb)
                NotebookClient(nb, timeout=90, resources={"metadata": {"path": str(cwd)}}).execute()
                result_path = root / "outputs/submission_xgb_glm.csv"
                result = pd.read_csv(result_path)
                assert result.columns.tolist() == ["ID", "FREQ", "CM", "ANNEE_ASSURANCE", "CHARGE"]
                assert result.ID.tolist() == list(range(200, 240))
                assert np.isfinite(result.to_numpy()).all()
                assert (result[["FREQ", "CM", "CHARGE"]] >= 0).all().all()
                assert (root / "submissions/submission_xgb_glm.csv").read_bytes() == official
                assert not (root / "submission_xgb_glm.csv").exists()
                assert not (root / "notebooks/submission_xgb_glm.csv").exists()
                result_path.unlink()
                print(f"Notebook OK depuis {cwd.name} : {len(result)} prédictions, format officiel.")
