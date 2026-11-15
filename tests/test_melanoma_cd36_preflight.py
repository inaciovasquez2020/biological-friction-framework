"""Synthetic, no-patient-data regression tests for CD36 structural admission."""
import unittest
from infra.ci.melanoma_cd36_preflight import audit

GOOD = {
    'study_id':'synthetic', 'patient_id':'P1', 'sample_id':'S1',
    'treatment':'anti_PD1_monotherapy', 'sampling_time':'pretreatment',
    'response':'CR', 'malignant_cd36_source':'tumor_scRNA',
    'macrophage_cd36_source':'immune_scRNA',
    'malignant_cd36_assay':'counts', 'macrophage_cd36_assay':'counts',
    'endpoint_method':'RECIST_v1.1',
    'malignant_cell_label':'CNV_malignant', 'macrophage_cell_label':'CD68_macrophage',
    'source_url':'https://example.invalid/study',
    'patient_identity_verified':'yes','response_source_verified':'yes',
    'treatment_timing_verified':'yes','cell_type_labels_verified':'yes'
}
class GateTests(unittest.TestCase):
    def test_synthetic_pass_is_only_structural(self):
        result=audit([GOOD])
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['clinical_validation'],'NOT_RUN')
        self.assertEqual(result['signal_scale_compatibility'],'NOT_ESTABLISHED')
        self.assertFalse(result['manifest_claims_independently_authenticated'])
    def test_each_missing_field_blocks(self):
        for field in GOOD:
            with self.subTest(field=field):
                row=GOOD.copy(); row.pop(field)
                self.assertEqual(audit([row])['status'],'BLOCKED')
    def test_timing_treatment_endpoint_and_provenance(self):
        for field,value in [('sampling_time','on_treatment'),('treatment','anti_PD1_CTLA4'),
                            ('response','SD'),('endpoint_method','pathologic_response'),
                            ('patient_identity_verified','unknown'),
                            ('response_source_verified','unknown'),('cell_type_labels_verified','unknown'),
                            ('treatment_timing_verified','unknown'),
                            ('macrophage_cell_label','CNV_malignant')]:
            with self.subTest(field=field):
                row=GOOD.copy(); row[field]=value
                self.assertEqual(audit([row])['status'],'BLOCKED')
    def test_shared_source_is_not_conflation(self):
        row=GOOD.copy()
        row['malignant_cd36_source']='same_biopsy_rna_counts'
        row['macrophage_cd36_source']='same_biopsy_rna_counts'
        self.assertEqual(audit([row])['status'],'PASS')
        row['macrophage_cell_label']=row['malignant_cell_label']
        self.assertEqual(audit([row])['status'],'BLOCKED')
    def test_same_response_label_different_measurement_is_ineligible(self):
        row=GOOD.copy(); row['response']='CR'; row['endpoint_method']='pathologic_response'
        result=audit([row]); self.assertIn('ROW_2:ENDPOINT_METHOD_NOT_RECIST', result['failures'])
    def test_duplicate_sample_and_patient(self):
        row=GOOD.copy()
        self.assertEqual(audit([row,row])['status'],'BLOCKED')
        second=row.copy(); second['sample_id']='S2'
        self.assertEqual(audit([row,second])['status'],'BLOCKED')
    def test_empty_cohort_blocks(self):
        self.assertEqual(audit([])['status'],'BLOCKED')

if __name__ == '__main__':
    unittest.main()
