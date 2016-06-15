from fabric.api import local, env, settings


# dev / local commands
def bootstrap():
    run_dev_playbook(extra_vars='bootstrap=yes')

def update():
    run_dev_playbook()

def quickupdate():
    run_dev_playbook(tags='quick')

def freshdb():
    run_dev_playbook(tags='db,quick', extra_vars='bootstrap=yes')

def run_dev_playbook(extra_vars=None, tags=None):
    local('git pull')
    local('ansible-playbook development_vagrant.yml \
            %(tags)s \
            %(extra_vars)s \
            -i dev \
            --private-key=~/.vagrant.d/insecure_private_key \
            -vv' \
            % {
                'tags': '--tags "%s"' % tags if tags else '',
                'extra_vars': '--extra-vars "%s"' % extra_vars if extra_vars else '',
              })


# remote server commands
def staging():
    env.ENV = 'staging'

def launch():
    local('ansible-playbook %(env)s_aws.yml \
            -i %(env)s \
            -vv --ask-vault-pass' \
            % {'env': env.ENV}
        )

# TODO - branch shouldn't have to be required locally
def branchlaunch(branch):
    with settings(warn_only=True):
        result = local('git rev-parse --verify %s' % branch)
        if result.return_code == 128:
            raise Exception('Please specify a branch you have locally. This does not exist')
        if branch == 'staging' or branch == 'prod':
            raise Exception('Cant deploy staging or prod from branch deploy')
        env.ENV = 'branch'
        local('ansible-playbook branch_aws.yml \
                -i branch \
                -vv --ask-vault-pass \
                --extra-vars "branch=%s"' % branch \
                % {'env': 'branch'}
            )


def quicklaunch():
    local('ansible-playbook %(env)s_aws.yml \
            --tags "quick" \
            -i %(env)s \
            -vv --ask-vault-pass' \
            % {'env': env.ENV}
        )

def encrypt_other_vars():
    local('ansible-vault encrypt other_vars/aws.yml')
