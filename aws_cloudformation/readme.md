# RHEL 7 RPM Mirror

The script `mirror.template` demonstrates creating an RHEL 7 RPM mirror running on an EC2 instance. The mirror is set up using the commands defined in `configureRepo`. An Apache web server is started to serve the mirror directory at `/var/www/html/rhel-7-server-rhui-rh-common-rpms`. Next, another EC2 instance, `ClientInstance` is provisioned to demonstrate using the custom mirror. The file `/etc/yum.repos.d/my_mirror.repo` is created to point to the mirror. Finally, the commands on that instance are run. `0_disable_other_repos` configures yum to only use the custom mirror. `1_install_from_mirror` installs a package.

## How to run

### Prereqs: 
- Create your aws session
- Create a keypair in the region (image is for us-east-2).
   - Name it "temp-key-pair" to use the default name expected by the script, otherwise you'll have to provide the keyname as an environment variable.

```bash

# Check template
./tasks.sh validate-template

# Variables needed for create-stack
export RHEL_USER=<user> # required
export RHEL_PASSWORD=<password> # required
export KEYNAME=<keyname> # default key is "temp-key-pair"
export SSHLOCATION=<ip/32> # default is your public ip

# Create a non-existing stack
./tasks.sh create-stack

# OR - to delete an existing and recreate
./tasks.sh recreate-stack
```