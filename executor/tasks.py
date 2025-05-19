import json
from executor.s3_util import download_from_s3
from django.conf import settings
from django.core.exceptions import *
from urllib.parse import urlparse
from nessus.ext_libraries.nessrest.nessrest import ness6rest,ness6scan,credentials
import time
import pathlib
import os
import requests
from nessusEngine.utils import generate_jwt_service_token
import ipaddress


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def update_result_to_core_app(scanInstance):
    try:
        core_url = settings.CORE_URL.strip("/")
        endpoint = f"{core_url}/scan/refresh-scan/"
        payload = {
            "scan_id": scanInstance.scan_id,
            "agent_type_code": 'nessus',
            "result_url": scanInstance.result_url,
            "errors": scanInstance.errors,
            "scan_status": scanInstance.scan_status,
            "scan_type": scanInstance.scan_type
        }
        service_token = generate_jwt_service_token()
        headers = {
            "org-id": scanInstance.org_ref_id,
            "X-Service-Token": f"Bearer {service_token}"
        }

        res = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        response = res.json()

        if response['status'] == 'success':
            return True
        else:
            return False
    except:
        return False
    

def saveStatus(scanInstance, status, errors=None):
    scanInstance.scan_status = status
    scanInstance.errors = errors
    scanInstance.save()


def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False


def clean_targets(raw_targets):
    target_list = [t.strip() for t in raw_targets.split(',') if t.strip()]
    resolved_target_list = []

    for target in target_list:
        cleaned_target = target

        # If it's a full URL (with http/https), extract the netloc
        if cleaned_target.startswith(('http://', 'https://')):
            cleaned_target = urlparse(cleaned_target).netloc

        # If it's not an IP or CIDR, but contains a path (e.g., domain.com/path)
        if '/' in cleaned_target:
            try:
                # If it's a valid IP or CIDR, keep as-is
                ipaddress.ip_network(cleaned_target, strict=False)
            except ValueError:
                # Not an IP/CIDR, strip trailing path from domain
                cleaned_target = cleaned_target.split('/')[0]

        resolved_target_list.append(cleaned_target)

    return ','.join(resolved_target_list)


def nessusscanner(scanInstance):
    try:
        print("<<< Nessus scan in progress >>>")
        SERVER_PORT = settings.SERVER_PORT
        SERVER_HOST = settings.SERVER_HOST
        NESSUS_PWD = settings.NESSUS_PWD
        NESSUS_USERNAME = settings.NESSUS_USERNAME
        IN_PROGRESS = 1
        SUCCESS = 2
        FAILED = 3
        nessscan = None

        try:
            # Initiating scan
            nessscan = ness6rest.Scanner(
                url="https://{}:{}".format(SERVER_HOST, SERVER_PORT),
                login=NESSUS_USERNAME,password=NESSUS_PWD, 
                insecure=True
            )
            # Default credentials 
            creds = [
                credentials.WindowsPassword(username=NESSUS_USERNAME, password=NESSUS_PWD),
                credentials.SshPassword(username=NESSUS_USERNAME, password=NESSUS_PWD)
            ]

            # Mapping policy
            if scanInstance.policy_type != None and scanInstance.policy_type != '':
                if not nessscan.policy_exists(name=scanInstance.policy_type):
                    print("<<< policy not exists >>>")
                    if scanInstance.policy_file != None and scanInstance.policy_file != '':
                        # Download policy from AWS 
                        data = json.loads(scanInstance.policy_file)
                        filename = time.strftime("%Y%m%d-%H%M%S")+".nessus"
                        local_scope_path = settings.SITE_ROOT+'/policy/'+filename
                        download_from_s3(data['bucket'], data['key'], local_scope_path, data['region'])

                        # Adding policy
                        nessscan.upload(upload_file=local_scope_path)
                        nessscan._policy_add_audit(category="Windows", filename=filename)
                        nessscan.policy_add(name=scanInstance.policy_type,credentials=creds)

                        # Deleting downloaded file after policy settup
                        pathlib.Path(local_scope_path).unlink()
                    else:
                        saveStatus(scanInstance, FAILED, "Given policy is not exists in nessus!.")
                        # Update to core app
                        update_result_to_core_app(scanInstance)
                        return scanInstance
            else:
                if not nessscan.policy_exists(name='DEFAULT'):
                    print("<<< DEFAULT policy not exists >>>")
                    # Adding policy
                    # file_path = BASE_DIR + '/DEFAULT.nessus'
                    file_path = BASE_DIR + '/DEFAULT_NOPING.nessus'
                    nessscan.upload(upload_file=file_path)
                    nessscan._policy_add_audit(category="Windows", filename="DEFAULT.nessus")
                    nessscan.policy_add(name="DEFAULT",credentials=creds)
            
            ##### varifying ip address #########
            try:
                # target_list= scanInstance.target.split(',')
                # resolved_target_list = []
                # for item in target_list:
                #     resolved_target = item
                #     if is_url(resolved_target):
                #         resolved_target = urlparse(resolved_target).netloc
                #     to_check = resolved_target.rsplit('/', 1)
                #     resolved_target_list.append(to_check[0])
                # scanInstance.resolved_target = ','.join(resolved_target_list)


                scanInstance.resolved_target = clean_targets(scanInstance.target)
                print(scanInstance.resolved_target,"<<< resolved target >>>")
            except Exception as e:
                saveStatus(scanInstance, FAILED, e.__class__.__name__)
                # Update to core app
                update_result_to_core_app(scanInstance)
                return scanInstance

            # Create the scan
            nessscan.scan_add(
                targets=scanInstance.resolved_target,
                name="SCAN_00"+ str(scanInstance.scan_id)+"_"+str(scanInstance.resolved_target),
            )
            nessscan_id = nessscan.res["scan"]["id"]

            if nessscan_id is None:
                saveStatus(scanInstance, FAILED, "No scan scheduled")
                # Update to core app
                update_result_to_core_app(scanInstance)
                return scanInstance
            
            nessus_scan_name = str(nessscan.res["scan"]["name"])
            scanInstance.nessus_scan_id = nessscan_id
            scanInstance.nessus_scan_name = nessus_scan_name
            
            # Running scan
            nessscan.scan_run()
            
            # Setting ScanInstance status
            saveStatus(scanInstance, IN_PROGRESS, None)
            print("<<< Scan Successfully Added. >>>")
            # Update to core app
            update_result_to_core_app(scanInstance)
            return scanInstance
        except Exception as e:
            print(e,"Error!.")
            # Add errors and status and Save Instance
            saveStatus(scanInstance, FAILED, str(e))
            # Update to core app
            update_result_to_core_app(scanInstance)
            return scanInstance
    except Exception as e:
        print(str(e)," Error...")
        saveStatus(scanInstance, FAILED, str(e))
        # Update to core app
        update_result_to_core_app(scanInstance)
        return scanInstance

    


    