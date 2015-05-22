from fabric.api import local, task, quiet


@task
def release():
    with quiet():
        version_row = local("grep 'VERSION = ' setup.py", capture=True)
        version = version_row.split(' = ')[1].strip()
        version = version[1:-1].split('.')
        version[-1] = str(int(version[-1]) + 1)
        new_version = '.'.join(version)
        local("sed -isetup.py 's/VERSION =.*/VERSION = \"{}\"/g' setup.py".format(new_version))
        local('git commit -am "new version {}"'.format(new_version))
        local('git tag -a v{0} -m \'new version {0}\''.format(new_version))
        local('git push origin master --tags')
    local("python setup.py register")
    local("python setup.py sdist upload -r pypi")
