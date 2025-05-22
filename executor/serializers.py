from rest_framework import serializers
from executor.models import Scan

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['scan_id', 'created_at', 'target', 'scan_status', 'result_url','errors','resolved_target','policy_type','policy_file','scan_scope', 'org_ref_id', 'scan_type']
