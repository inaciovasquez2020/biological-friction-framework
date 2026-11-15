#!/usr/bin/env python3
"""Structural, self-attested cohort preflight. No model scoring or clinical verification."""
import argparse
import csv
import json
from pathlib import Path

REQUIRED = ('study_id', 'patient_id', 'sample_id', 'treatment', 'sampling_time',
            'response', 'malignant_cd36_source', 'macrophage_cd36_source',
            'malignant_cd36_assay', 'macrophage_cd36_assay', 'source_url',
            'patient_identity_verified', 'response_source_verified',
            'treatment_timing_verified', 'cell_type_labels_verified')

def audit(rows):
    rows = list(rows)
    failures = []
    seen_samples, seen_patients = set(), set()
    if not rows:
        failures.append('NO_ROWS')
    for number, row in enumerate(rows, 2):
        missing = [key for key in REQUIRED if not str(row.get(key) or '').strip()]
        for key in missing:
            failures.append(f'ROW_{number}:MISSING_{key}')
        if missing:
            continue
        sample = (row['study_id'], row['sample_id'])
        patient = (row['study_id'], row['patient_id'])
        if sample in seen_samples:
            failures.append(f'ROW_{number}:DUPLICATE_SAMPLE')
        if patient in seen_patients:
            failures.append(f'ROW_{number}:DUPLICATE_PATIENT_REQUIRES_PREDECLARED_SELECTION')
        seen_samples.add(sample)
        seen_patients.add(patient)
        if row['treatment'] != 'anti_PD1_monotherapy':
            failures.append(f'ROW_{number}:INELIGIBLE_TREATMENT')
        if row['sampling_time'] != 'pretreatment':
            failures.append(f'ROW_{number}:NOT_PRETREATMENT')
        if row['response'] not in ('CR', 'PR', 'PD'):
            failures.append(f'ROW_{number}:UNSUPPORTED_FROZEN_ENDPOINT')
        if any(row[key] != 'yes' for key in ('patient_identity_verified',
                 'response_source_verified', 'treatment_timing_verified',
                 'cell_type_labels_verified')):
            failures.append(f'ROW_{number}:UNVERIFIED_SOURCE_LINKAGE')
        if row['malignant_cd36_source'] == row['macrophage_cd36_source']:
            failures.append(f'ROW_{number}:CELL_SOURCES_NOT_DISTINCT')
    return {'status': 'PASS' if not failures else 'BLOCKED',
            'rows': len(rows), 'unique_patients': len(seen_patients),
            'failures': sorted(set(failures)),
            'manifest_claims_independently_authenticated': False,
            'signal_scale_compatibility': 'NOT_ESTABLISHED',
            'clinical_validation': 'NOT_RUN'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('manifest', type=Path)
    args = p.parse_args()
    with args.manifest.open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or any(key not in reader.fieldnames for key in REQUIRED):
            report = {'status':'BLOCKED', 'failures':['MISSING_REQUIRED_COLUMNS'],
                      'manifest_claims_independently_authenticated':False,
                      'signal_scale_compatibility':'NOT_ESTABLISHED',
                      'clinical_validation':'NOT_RUN'}
        else:
            report = audit(reader)
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report['status'] == 'PASS' else 2

if __name__ == '__main__':
    raise SystemExit(main())
