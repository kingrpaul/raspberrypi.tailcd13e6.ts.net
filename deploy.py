import subprocess
import os

def deploy_to_pi():
    local_path = 'output/'
    # remote_path = 'pi5@100.67.142.97:/var/www/html'
    # remote_path = 'pi5@raspberrypi.tailcd13e6.ts.net:/var/www/html'
    remote_path = 'pi5@raspberrypi:/var/www/html'
    print(f"Deploying {local_path} to {remote_path}...")
    result = subprocess.run(
        ['rsync', '-avzc', '--delete', '--exclude=stats.html', '--exclude=.*', '--no-times', '--no-perms', '--no-group', '--compress-level=3', local_path, remote_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Deployment failed: {result.stderr}")
    else:
        print("Deployment successful!")

os.system("pelican -s publishconf.py")
deploy_to_pi()
# os.system("pelican --autoreload --listen")


"""
import subprocess
import os


def deploy_to_pi():
    local_path = 'output/'
    remote_path = 'pi5@100.67.142.97:/var/www/html'
    print(f"Deploying {local_path} to {remote_path}...")
    result = subprocess.run(
        ['rsync', '-avz', '--delete', local_path, remote_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Deployment failed: {result.stderr}")
    else:
        print("Deployment successful!")

os.system("pelican -s publishconf.py")

deploy_to_pi()

os.system("pelican --autoreload --listen")
"""