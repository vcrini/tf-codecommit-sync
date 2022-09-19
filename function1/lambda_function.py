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
# special conversions
conversions = {}
# repos to ignore
deny = {}
# if assigned repositories to allow
allow = {}
c = os.getenv('conversions')
i = os.getenv('deny')
a = os.getenv('allow')
if c is not None:
    conversions = json.loads(c)
if i is not None:
    deny = json.loads(i)
if a is not None:
    allow = json.loads(a)


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
            print("ERROR: {clone} gave {result} with {error}".format(
                clone=clone,
                result=ret.stdout.decode('utf-8'),
                error=ret.stderr.decode('utf-8')))
    return event
