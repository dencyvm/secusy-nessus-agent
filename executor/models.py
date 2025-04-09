from django.db import models

class Scan(models.Model):
    scan_id = models.AutoField(primary_key=True)
    target = models.TextField (blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scan_status = models.IntegerField(default='0') # 0 - Not started,  # 1 - Started, in progress, # 2 - Completed, success, # 3 - Attempted, failure # 4 - deleted
    result_url = models.CharField(blank=True, null=True, max_length=1000)
    errors = models.CharField(blank=True, null=True, max_length=2000)
    nessus_scan_name = models.CharField(blank=True, null=True, max_length=2000)
    resolved_target = models.TextField(blank=True, null=True)
    nessus_scan_id = models.IntegerField(blank=True, null=True) 
    policy_type = models.CharField(blank=True, null=True,max_length=200)
    policy_file = models.TextField(blank=True, null=True)
    scan_scope = models.CharField(blank=True,null=True, max_length=250) # For group-scan and single-scan
    org_ref_id = models.CharField(max_length=350,blank=True,null=True)


#Check if we can use in-memory classes
class ScanX(object):
    _ip = str()
    _ports = str()
    _argmnts = str()

    def set_ip(self, num):
        self._ip = num

    def get_ip(self):
        return self._ip

    def set_ports(self, ports):
        self._ports = ports

    def get_ports(self):
        return self._ports

    def set_argmnts(self, argmnts):
        self._argmnts = argmnts

    def get_argmnts(self):
        return self._argmnts

class S3File(object):
    _bucket = str()
    _key = str()
    _region = str()


