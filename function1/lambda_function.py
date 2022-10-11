# from git.repo import Repo
# from git import RemoteProgress
import json
import os
import re
import subprocess
import tempfile

message_id_cache = {}
prefix_destination = os.getenv('prefix_destination') or ''
prefix_source = os.getenv('prefix_source')
repo_path = os.getenv('repo_path')
# repos to ignore
deny = {}
# if assigned repositories to allow

# just pigini

conversions = {"fdh-source": "bitgdi-source",
               "fdh-fdh-s3lab_ap-consumer": "bitgdi-fdh-s3lab_ap-consumer",
               "fdh-fdh-tracking-api": "bitgdi-fdh-tracking-api",
               "fdh-s3lab_garpe-ap-producer": "bitgdi-s3lab_garpe-ap-producer",
               "fdh-s3lab_tiger-ap-producer": "bitgdi-s3lab_tiger-ap-producer",
               "fdh-fdh-pigini_elastic_tracking-consumer": "bitgdi-fdh-pigini_elastic_tracking-consumer",
               "fdh-fdh-pigini_recovery_tracking-consumer": "bitgdi-fdh-pigini_recovery_tracking-consumer",
               "fdh-fdh-pigini_tracking-consumer": "bitgdi-fdh-pigini_tracking-consumer",
               "fdh-gps-s3lab_pigini_gpseof-consumer": "bitgdi-gps-s3lab_pigini_gpseof-consumer",
               "fdh-gps-s3lab_pigini_workorder_prop_fb-consumer": "bitgdi-gps-s3lab_pigini_workorder_prop_fb-consumer",
               "fdh-gps_pigini-trigger-producer": "bitgdi-pigini-gps-api",
               "fdh-gps_pigini_to_s3lab-simulatedhq-flow": "bitgdi-gps_pigini_to_s3lab-simulatedhq-flow",
               "fdh-gps_pigini_to_s3lab-suggestion_prod-flow": "bitgdi-gps_pigini_to_s3lab-suggestion_prod-flow",
               "fdh-gps_pigini_to_s3lab-suggestion_transf-flow": "bitgdi-gps_pigini_to_s3lab-suggestion_transf-flow",
               "fdh-gps_pigini_to_s3lab-workorder_ope-flow": "bitgdi-gps_pigini_to_s3lab-workorder_ope-flow",
               "fdh-gps_pigini_to_s3lab-workorder_prop-flow": "bitgdi-gps_pigini_to_s3lab-workorder_prop-flow",
               "fdh-jde_pigini-s3lab_pigini_data-consumer": "bitgdi-jde_pigini-s3lab_pigini_data-consumer",
               "fdh-jde_pigini_to_s3lab_pigini-anagrafiche-flow": "bitgdi-jde_pigini_to_s3lab_pigini-anagrafiche-flow",
               "fdh-jde_pigini_to_s3lab_pigini-cambi-flow": "bitgdi-jde_pigini_to_s3lab_pigini-cambi-flow",
               "fdh-mes_pigini-data-producer": "bitgdi-pigini-mes-api",
               "fdh-mes_pigini-s3lab_pigini_data-consumer": "bitgdi-mes_pigini-s3lab_pigini_data-consumer",
               "fdh-s3lab_pigini-ap-producer": "bitgdi-s3lab_pigini-ap-producer",
               "fdh-s3lab_pigini-data-producer": "bitgdi-s3lab_pigini-data-producer",
               "fdh-s3lab_pigini-gpstrigger-consumer": "bitgdi-s3lab_pigini-gpstrigger-consumer",
               "fdh-s3lab_pigini-mes_pigini_data-consumer": "bitgdi-s3lab_pigini-mes_pigini_data-consumer",
               "fdh-s3lab_pigini-trigger-producer": "bitgdi-pigini-s3lab-api",
               "fdh-s3lab_pigini_to_fdh_gps-cci-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cci-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cci_tgl-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cci_tgl-flow",
               "fdh-s3lab_pigini_to_fdh_gps-ccl-flow": "bitgdi-s3lab_pigini_to_fdh_gps-ccl-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cdb-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cdb-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cil-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cil-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cir-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cir-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cpr-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cpr-flow",
               "fdh-s3lab_pigini_to_fdh_gps-cprtgl-flow": "bitgdi-s3lab_pigini_to_fdh_gps-cprtgl-flow",
               "fdh-s3lab_pigini_to_fdh_gps-dbr-flow": "bitgdi-s3lab_pigini_to_fdh_gps-dbr-flow",
               "fdh-s3lab_pigini_to_fdh_gps-fab-flow": "bitgdi-s3lab_pigini_to_fdh_gps-fab-flow",
               "fdh-s3lab_pigini_to_fdh_gps-giaexp-flow": "bitgdi-s3lab_pigini_to_fdh_gps-giaexp-flow",
               "fdh-s3lab_pigini_to_fdh_gps-item-flow": "bitgdi-s3lab_pigini_to_fdh_gps-item-flow",
               "fdh-s3lab_pigini_to_fdh_gps-orfexp-flow": "bitgdi-s3lab_pigini_to_fdh_gps-orfexp-flow",
               "fdh-s3lab_pigini_to_fdh_gps-polexp-flow": "bitgdi-s3lab_pigini_to_fdh_gps-polexp-flow",
               "fdh-s3lab_pigini_to_fdh_gps-supplier-flow": "bitgdi-s3lab_pigini_to_fdh_gps-supplier-flow",
               "fdh-s3lab_pigini_to_fdh_gps-warehouse-flow": "bitgdi-s3lab_pigini_to_fdh_gps-warehouse-flow",
               "fdh-spc_ddc-s3lab_pigini_data-consumer": "bitgdi-spc_ddc-s3lab_pigini_data-consumer",
               "fdh-spc_to_s3lab_pigini-dcfo-flow": "bitgdi-spc_to_s3lab_pigini-dcfo-flow",
               "fdh-supplier_tag-s3lab_pigini_data-consumer": "bitgdi-supplier_tag-s3lab_pigini_data-consumer",
               "fdh-temera_rfid-s3lab_pigini_data-consumer": "bitgdi-rfid-s3lab_pigini_data-consumer",
               "fdh-digital-label-producer": "bitgdi-digital-label-producer",
               "fdh-fdh-digital-api": "bitgdi-digital-api",
               "fdh-dp_atlante_to_fdh-all-flow": "bitgdi-dp_atlante_to_fdh-all-flow",
               "fdh-enginenow_to_fdh-all-flow": "bitgdi-enginenow_to_fdh-all-flow",
               "fdh-fdh-hq_elastic_tracking-consumer": "bitgdi-fdh-hq_elastic_tracking-consumer",
               "fdh-fdh-hq_tracking-consumer": "bitgdi-fdh-hq_tracking-consumer",
               "fdh-gps_hq-trigger-producer": "bitgdi-hq-gps-api",
               "fdh-gps_hq_to_s3hq-suggestion_prod-flow": "bitgdi-gps_hq_to_s3hq-suggestion_prod-flow",
               "fdh-gps_hq_to_s3hq-workorder_prop-flow": "bitgdi-gps_hq_to_s3hq-workorder_prop-flow",
               "fdh-serpico_atlante_to_fdh-consumi-flow": "bitgdi-serpico_atlante_to_fdh-consumi-flow"}

allow = [x for x in conversions.keys()]


def handler(event, context):
    print("incoming event:" + json.dumps(event))
    common = event['Records'][0]['Sns']
    message_id = common['MessageId']
    # avoid processing duplicated request (sns can send duplicated
    # https://cloudonaut.io/your-lambda-function-might-execute-twice-deal-with-it/)
    # global variables in python are maintained between invocations if
    # lambda is not recreated by AWS (so it's not accurately unique)
    if message_id_cache.get(message_id, None):
        print("event with MessageId: {} already processed".format(message_id))
        return
    else:
        message_id_cache[message_id] = '1'
    m = json.loads(common['Message'])
    repo_source = m["detail"]["repositoryName"]
    if repo_source in deny:
        print("{} is present in ignore list, skipping".format(repo_source))
        return event
    if allow is None:
        print("allow list is empty, continuing")
    elif repo_source in allow:
        print("{} is present in allow list, continuing".format(repo_source))
    else:
        print("{} is not on allow list, exiting".format(repo_source))
        return event
    # check if special conversion exists
    repo_destination = None
    repo_converted = conversions.get(repo_source, repo_source)
    if repo_converted != repo_source:
        print("converted from dict {}->{}".format(repo_source, repo_converted))
        repo_destination = repo_converted
    else:
        repo_destination = re.sub(re.compile("^{}".format(prefix_source)),
                                  prefix_destination, repo_source)
        print("converted from sub {}->{}".format(repo_source,
                                                 repo_destination))

    with tempfile.TemporaryDirectory() as clone_dir:
        os.environ['HOME'] = "/tmp"
        os.environ['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no -i $HOME/.ssh/id_rsa'
        print(os.getenv('HOME'))
        print(os.getenv('GIT_SSH_COMMAND'))
        clone = """
        mkdir -p $HOME/.ssh;
        cp id_rsa $HOME/.ssh;
        chmod 600 $HOME/.ssh/id_rsa;
        git clone --mirror {source} {clone_dir};
        cd {clone_dir};
        git remote add dest {destination};
        git push dest --mirror
        """.format(source="{}/{}".format(repo_path, repo_source),
                   clone_dir=clone_dir,
                   destination="{}/{}".format(repo_path, repo_destination),
                   path="/tmp/usr/bin")
        print(clone)
        ret = subprocess.run(clone,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        print(ret.stdout.decode('utf-8'))
        if ret.returncode > 0:
            print("[ERROR] {clone} gave {result} with {error}".format(
                clone=clone,
                result=ret.stdout.decode('utf-8'),
                error=ret.stderr.decode('utf-8')).replace("\n", "\\n"))
    return event
