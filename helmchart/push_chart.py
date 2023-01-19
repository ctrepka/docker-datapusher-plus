import subprocess

def run(cmd):
    to_decode = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout
    output = to_decode.read()

    return output.decode()

#################################################################################################################################

docker_tag = input("is there a specific tag you would like to use for this build? (press Enter to use the default, 'latest')\n")

if docker_tag == "":
    docker_tag = "latest"

print("Packaging Helmchart version {}".format(docker_tag))
HELM_PACKAGE_STDOUT = run("helm package . -d ./chart-package/")
print(HELM_PACKAGE_STDOUT)

AWS_ACCOUNT = run(
    "aws sts get-caller-identity --query \"Account\" --output text").strip()
AWS_REGION = run("aws configure get region").strip()
ECR_URI = "{}.dkr.ecr.{}.amazonaws.com".format(AWS_ACCOUNT, AWS_REGION)

LOGIN_STDOUT = run("aws ecr get-login-password --region {} | helm registry login \
    --username AWS --password-stdin {}".format(AWS_REGION, ECR_URI)
                   )
print(LOGIN_STDOUT)

print("\n Pushing Image, please wait... \n")
PUSH_IMAGE_STDOUT = run(
    "helm push ./chart-package/datapusher-plus-helmchart-{}.tgz oci://{}".format(docker_tag, ECR_URI))
print(PUSH_IMAGE_STDOUT)
