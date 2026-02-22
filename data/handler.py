"""Data import/export handler for StatISO.

Provides file loading (CSV, Excel), manual input parsing,
data validation, and Excel export capabilities.
"""

import io

import numpy as np
import pandas as pd
import streamlit as st
from typing import Optional


class DataHandler:
    """Handles data import, validation, and export for StatISO."""

    @staticmethod
    @st.cache_data
    def load_file(
        file_bytes: bytes,
        filename: str,
        column: Optional[str] = None,
    ) -> np.ndarray:
        """Load numeric data from CSV or Excel bytes.

        Parameters
        ----------
        file_bytes : bytes
            Raw file content.
        filename : str
            Original filename (for extension detection).
        column : str, optional
            Specific column name. If None, first numeric column is used.

        Returns
        -------
        np.ndarray
            1-D float array of values.

        Raises
        ------
        ValueError
            If the format is unsupported, the column is missing,
            no numeric column exists, or the data is empty.
        """
        buf = io.BytesIO(file_bytes)

        if filename.endswith(".csv"):
            df = pd.read_csv(buf)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(buf)
        else:
            raise ValueError("Unsupported format. Use CSV or Excel.")

        if column:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' not found.")
            data = df[column].dropna().values
        else:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                raise ValueError("No numeric column found.")
            data = df[numeric_cols[0]].dropna().values

        if len(data) == 0:
            raise ValueError("No valid data found.")
        return data.astype(float)

    @staticmethod
    def get_columns(file_bytes: bytes, filename: str) -> list[str]:
        """Return list of numeric column names from a file.

        Parameters
        ----------
        file_bytes : bytes
            Raw file content.
        filename : str
            Original filename (for extension detection).

        Returns
        -------
        list[str]
            Names of all numeric columns.
        """
        buf = io.BytesIO(file_bytes)

        if filename.endswith(".csv"):
            df = pd.read_csv(buf)
        else:
            df = pd.read_excel(buf)

        return list(df.select_dtypes(include=[np.number]).columns)

    @staticmethod
    def parse_manual_input(text: str) -> np.ndarray:
        """Parse newline-separated numeric values.

        Parameters
        ----------
        text : str
            Newline-separated values. Commas are replaced by dots
            for decimal separator compatibility.

        Returns
        -------
        np.ndarray
            1-D float array of parsed values.

        Raises
        ------
        ValueError
            If no valid numeric values are found.
        """
        values: list[float] = []
        for line in text.strip().split("\n"):
            line = line.strip().replace(",", ".")
            if line:
                values.append(float(line))
        if not values:
            raise ValueError("No valid values.")
        return np.array(values)

    @staticmethod
    def validate(data: np.ndarray) -> dict:
        """Validate data and return a diagnostic dict.

        Parameters
        ----------
        data : np.ndarray
            1-D numeric array to validate.

        Returns
        -------
        dict
            Keys: ``valid`` (bool), ``errors`` (list[str]),
            ``warnings`` (list[str]).
        """
        result: dict = {"valid": True, "errors": [], "warnings": []}

        n = len(data)
        if n < 2:
            result["errors"].append("min_2_samples")
            result["valid"] = False
            return result

        if np.any(np.isnan(data)):
            result["errors"].append("nan_detected")
            result["valid"] = False

        if np.any(np.isinf(data)):
            result["errors"].append("inf_detected")
            result["valid"] = False

        if n < 10:
            result["warnings"].append("small_sample")

        mean = np.mean(data)
        if mean != 0:
            cv = np.std(data, ddof=1) / abs(mean) * 100
            if cv < 0.1:
                result["warnings"].append("very_low_variability")
            elif cv > 50:
                result["warnings"].append("high_variability")

        return result

    @staticmethod
    def export_to_excel(
        results: dict,
        data: Optional[np.ndarray] = None,
    ) -> io.BytesIO:
        """Export results dict to an Excel file in memory.

        Parameters
        ----------
        results : dict
            Flat dict of parameter -> value pairs.
        data : np.ndarray, optional
            Raw data to include in a separate sheet.

        Returns
        -------
        io.BytesIO
            In-memory Excel workbook ready for download.
        """
        buf = io.BytesIO()

        with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
            # --- Results sheet ---
            rows: list[dict] = []
            for k, v in results.items():
                if not isinstance(v, (dict, list, np.ndarray)):
                    rows.append({"Parameter": k, "Value": v})
            if rows:
                pd.DataFrame(rows).to_excel(
                    writer, sheet_name="Results", index=False
                )

            # --- Data & Statistics sheets ---
            if data is not None:
                pd.DataFrame({"Values": data}).to_excel(
                    writer, sheet_name="Data", index=False
                )
                desc = {
                    "Mean": np.mean(data),
                    "Std": np.std(data, ddof=1),
                    "Min": np.min(data),
                    "Q1": np.percentile(data, 25),
                    "Median": np.median(data),
                    "Q3": np.percentile(data, 75),
                    "Max": np.max(data),
                }
                pd.DataFrame([desc]).to_excel(
                    writer, sheet_name="Statistics", index=False
                )

        buf.seek(0)
        return buf
