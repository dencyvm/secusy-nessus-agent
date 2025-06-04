from django_cron import CronJobBase, Schedule
from django.conf import settings
import json
import pathlib
import os
from executor.models import Scan
from executor.s3_util import upload_to_s3,generate_unique_timestamp
from nessus.ext_libraries.nessrest.nessrest import ness6rest
from executor.tasks import update_result_to_core_app



# This will check the scan status of not completed scans and if the status is completed its save the scan results 
class PerformScan(CronJobBase):
    # RUN_EVERY_MINS = 1
    RUN_EVERY_MINS = 10
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'exicutor.run_scans'    # a unique code

    def do(self):
        print("NESSUS Cronjob running")
        try:
            scans = Scan.objects.filter(scan_status__in=[0,1]) # inprogress scans
            print("Scan count >>> ",scans.count())

            result_bucket = settings.S3_BUCKET_NAME
            result_bucket_region = settings.S3_BUCKET_REGION
            SERVER_PORT = settings.SERVER_PORT
            SERVER_HOST = settings.SERVER_HOST
            NESSUS_PWD = settings.NESSUS_PWD
            NESSUS_USERNAME = settings.NESSUS_USERNAME
            IN_PROGRESS = 1
            SUCCESS = 2
            FAILED = 3

            for scope in scans:
                nessscan = ness6rest.Scanner(
                    url="https://{}:{}".format(SERVER_HOST, SERVER_PORT),
                    login=NESSUS_USERNAME,password=NESSUS_PWD, 
                    insecure=True
                )

                try:
                    # Fetching nessus reports
                    report_format="csv"
                    post_data = {"format": report_format}
                    export_url = "scans/{}/export".format(scope.nessus_scan_id)
                    nessscan.action(action=export_url, method="POST", extra=post_data)
                    report_fileid = nessscan.res['file']
                    
                    nessscan.action(
                        action="scans/{}/export/{}/status".format(scope.nessus_scan_id, report_fileid),
                        method="GET"
                    )
                    
                    if nessscan.res['status'] == "ready":
                        nessscan.action(action="scans/"+str(scope.nessus_scan_id), method="GET")
                        report_content = nessscan.download_scan(
                            export_format='csv',
                            scan_id=scope.nessus_scan_id
                        )

                        report_filename = "nessus_{}_{}.csv".format(scope.nessus_scan_id, report_fileid)
                        report_file_path = settings.SITE_ROOT+"/reports/"+report_filename
                        pathlib.Path(report_file_path).parent.mkdir(parents=True, exist_ok=True) 

                        with open(report_file_path, 'wb') as w:
                            w.write(report_content)

                        ######## creating a s3 object #######
                        timestamp = generate_unique_timestamp()
                        s3_result_path = "nessus_scan_results/"+timestamp+'_result.csv'
                        upload_to_s3(result_bucket,s3_result_path,report_file_path,result_bucket_region)

                        # Create a result object and save to instance
                        result_as_object = {"bucket":result_bucket, "key":s3_result_path, "region":result_bucket_region}
                        scope.result_url = json.dumps(result_as_object)
                        scope.scan_status = SUCCESS
                        scope.save()
                        
                        # deleting downloaded file.
                        if os.path.isfile(report_file_path):
                            os.remove(report_file_path)
                    else:
                        # print("scan ststus is not ready")
                        scope.scan_status = IN_PROGRESS
                        scope.save()
                        
                    # Update to core app
                    update_result_to_core_app(scope)
                except Exception as e:
                    print(e,">>> error")
                    # Setting ScanInstance status
                    scope.scan_status = IN_PROGRESS
                    scope.save()
                    # Update to core app
                    update_result_to_core_app(scope) 
        except Exception as e:
            print(e,"Error running scan cronjob")
