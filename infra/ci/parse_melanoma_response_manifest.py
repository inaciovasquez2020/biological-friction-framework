import argparse
import csv
import json
import re
from pathlib import Path

REQUIRED_COLUMNS = ("sample_id", "patient_id", "timepoint", "response")

PRE_TREATMENT = {
    "PRE",
    "PRETREATMENT",
    "PRE TREATMENT",
    "BASELINE",
    "BEFORE TREATMENT",
    "BEFORE THERAPY",
}

ON_TREATMENT = {
    "ON",
    "ON TREATMENT",
    "ONTREATMENT",
    "POST",
    "POST TREATMENT",
    "POSTTREATMENT",
    "AFTER TREATMENT",
}

RESPONDER = {
    "CR",
    "COMPLETE RESPONSE",
    "COMPLETE RESPONDER",
    "PR",
    "PARTIAL RESPONSE",
    "PARTIAL RESPONDER",
}

NONRESPONDER = {
    "PD",
    "PROGRESSIVE DISEASE",
    "PROGRESSION",
}

EXCLUDED_RESPONSE = {
    "SD",
    "STABLE DISEASE",
    "MIXED RESPONSE",
    "MIXED",
    "MR",
    "UNEVALUABLE",
    "NOT EVALUABLE",
    "NE",
    "UNKNOWN",
    "NA",
    "N A",
    "MISSING",
    "",
}


def _normalise(token):
    token = str(token).strip().strip('"').upper()
    token = re.sub(r"[_\-/]+", " ", token)
    token = re.sub(r"\s+", " ", token)
    return token


def _classify_timepoint(raw):
    value = _normalise(raw)
    if value in PRE_TREATMENT:
        return "pretreatment"
    if value in ON_TREATMENT:
        return "nonpretreatment"
    raise ValueError(f"unrecognised timepoint: {raw!r}")


def _classify_response(raw):
    value = _normalise(raw)
    if value in RESPONDER:
        return 1, "CR_PR"
    if value in NONRESPONDER:
        return 0, "PD"
    if value in EXCLUDED_RESPONSE:
        return None, "excluded_nonprimary_endpoint"
    raise ValueError(f"unrecognised response: {raw!r}")


def parse_manifest(path):
    """Parse a frozen clinical manifest and fail closed on patient duplication.

    Input columns are exactly semantic fields, not dataset-specific aliases:
    sample_id, patient_id, timepoint, response. Dataset-specific extraction must
    create this manifest before the endpoint parser is invoked.
    """
    with open(Path(path), "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError("manifest has no header")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"manifest missing required columns: {missing}")
        rows = list(reader)

    sample_ids = []
    pretreatment_rows = []
    excluded = []

    for row_number, row in enumerate(rows, start=2):
        sample_id = row["sample_id"].strip()
        patient_id = row["patient_id"].strip()
        if not sample_id or not patient_id:
            raise ValueError(f"row {row_number} has empty sample_id or patient_id")
        sample_ids.append(sample_id)

        timepoint = _classify_timepoint(row["timepoint"])
        if timepoint != "pretreatment":
            excluded.append(
                {
                    "sample_id": sample_id,
                    "patient_id": patient_id,
                    "reason": "nonpretreatment",
                }
            )
            continue

        pretreatment_rows.append((row_number, sample_id, patient_id, row["response"]))

    if len(set(sample_ids)) != len(sample_ids):
        raise ValueError("duplicate sample_id in manifest")

    patient_ids = [patient_id for _, _, patient_id, _ in pretreatment_rows]
    duplicate_patients = sorted(
        patient_id for patient_id in set(patient_ids) if patient_ids.count(patient_id) > 1
    )
    if duplicate_patients:
        raise ValueError(
            "duplicate pretreatment patient_id requires an externally frozen one-sample manifest: "
            f"{duplicate_patients}"
        )

    included = []
    for row_number, sample_id, patient_id, raw_response in pretreatment_rows:
        y, endpoint = _classify_response(raw_response)
        if y is None:
            excluded.append(
                {
                    "sample_id": sample_id,
                    "patient_id": patient_id,
                    "reason": endpoint,
                    "raw_response": raw_response.strip(),
                }
            )
            continue
        included.append(
            {
                "sample_id": sample_id,
                "patient_id": patient_id,
                "y": y,
                "endpoint": endpoint,
                "raw_response": raw_response.strip(),
            }
        )

    return {
        "status": "frozen_primary_endpoint_manifest",
        "unit": "patient",
        "primary_endpoint": "CR_or_PR_vs_PD",
        "included": included,
        "excluded": excluded,
        "n_included": len(included),
        "n_responder": sum(item["y"] == 1 for item in included),
        "n_nonresponder": sum(item["y"] == 0 for item in included),
        "claim_boundary": (
            "This parser only freezes cohort membership and the CR/PR-vs-PD endpoint; "
            "it does not establish predictive validity, treatment selection, efficacy, or cure."
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parse frozen patient-level melanoma pretreatment response manifest."
    )
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    print(json.dumps(parse_manifest(args.manifest), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
