import argparse
import pandas as pd
import numpy as np
import yaml
import json
import time
import logging
import sys
import os
from io import StringIO


def load_input_file(path):
    """
    Handles two formats:
    1. Plain CSV (.csv)
    2. Excel file saved with .csv extension (Microsoft Excel 2007+)
       where each row is a single cell containing comma-separated text.
    """
    # Try plain CSV first
    try:
        df = pd.read_csv(path, encoding="utf-8", sep=",")
        if df.shape[1] > 1:
            return df
    except Exception:
        pass

    try:
        df = pd.read_csv(path, encoding="latin1", sep=",")
        if df.shape[1] > 1:
            return df
    except Exception:
        pass

    # File might actually be an Excel file with a .csv extension
    # Rename to .xlsx in-memory and parse
    try:
        import openpyxl
        import tempfile, shutil

        # Copy to temp file with .xlsx extension so openpyxl accepts it
        tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        shutil.copy2(path, tmp.name)
        tmp.close()

        wb = openpyxl.load_workbook(tmp.name, read_only=True)
        ws = wb.active
        rows = [r[0] for r in ws.iter_rows(values_only=True) if r[0] is not None]
        wb.close()
        os.unlink(tmp.name)

        csv_text = "\n".join(str(r) for r in rows)
        df = pd.read_csv(StringIO(csv_text))
        return df

    except Exception as e:
        raise ValueError(f"Could not parse input file as CSV or Excel: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",    required=True, help="Path to input CSV/Excel file")
    parser.add_argument("--config",   required=True, help="Path to YAML config file")
    parser.add_argument("--output",   required=True, help="Path to output JSON file")
    parser.add_argument("--log-file", required=True, help="Path to log file")
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Job started")
    start_time = time.time()

    try:
        # ── File validation ──────────────────────────────────────────────
        if not os.path.exists(args.input):
            raise FileNotFoundError(f"Input file not found: {args.input}")

        if not os.path.exists(args.config):
            raise FileNotFoundError(f"Config file not found: {args.config}")

        # ── Load config ──────────────────────────────────────────────────
        with open(args.config) as f:
            config = yaml.safe_load(f)

        required_keys = ["seed", "window", "version"]
        missing = [k for k in required_keys if k not in config]
        if missing:
            raise ValueError(f"Invalid config structure, missing keys: {missing}")

        np.random.seed(config["seed"])
        logging.info(f"Config loaded: {config}")

        # ── Load data ────────────────────────────────────────────────────
        df = load_input_file(args.input)
        logging.info(f"File loaded, raw shape: {df.shape}, columns: {df.columns.tolist()}")

        # ── Validate dataset ─────────────────────────────────────────────
        if df.empty:
            raise ValueError("Input file is empty after parsing")

        if "close" not in df.columns:
            raise ValueError(
                f"Missing 'close' column. Found columns: {df.columns.tolist()}"
            )

        # ── Ensure numeric close ─────────────────────────────────────────
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        before = len(df)
        df = df.dropna(subset=["close"])
        dropped = before - len(df)
        if dropped:
            logging.warning(f"Dropped {dropped} rows with non-numeric 'close' values")

        if df.empty:
            raise ValueError("No valid numeric rows remain after cleaning")

        logging.info(f"Rows after cleaning: {len(df)}")

        # ── Rolling mean & signal ────────────────────────────────────────
        window = int(config["window"])
        df["rolling_mean"] = df["close"].rolling(window).mean()
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

        # ── Metrics ──────────────────────────────────────────────────────
        rows = len(df)
        signal_rate = df["signal"].mean()
        latency = int((time.time() - start_time) * 1000)

        metrics = {
            "version":        config["version"],
            "rows_processed": rows,
            "metric":         "signal_rate",
            "value":          round(float(signal_rate), 4),
            "latency_ms":     latency,
            "seed":           config["seed"],
            "window":         window,
            "status":         "success"
        }

        # ── Write output ─────────────────────────────────────────────────
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics, indent=2))
        sys.exit(0)

    except Exception as e:
        error = {
            "version":       config.get("version", "v1") if "config" in dir() else "v1",
            "status":        "error",
            "error_message": str(e)
        }

        try:
            with open(args.output, "w") as f:
                json.dump(error, f, indent=2)
        except Exception:
            pass

        logging.error(f"Error: {str(e)}", exc_info=True)
        print(json.dumps(error, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()