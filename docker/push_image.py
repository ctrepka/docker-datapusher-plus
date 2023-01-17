import subprocess

docker_tag = input("is there a specific tag you would like to use for this build? (press Enter to use the default, 'latest')\n")

if docker_tag == "":
    docker_tag = "latest"


def run(cmd):
    to_decode = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout
    output = to_decode.read()

    return output.decode()


AWS_ACCOUNT = run(
    "aws sts get-caller-identity --query \"Account\" --output text").strip()
AWS_REGION = run("aws configure get region").strip()
ECR_URI = "{A}.dkr.ecr.{R}.amazonaws.com".format(R=AWS_REGION, A=AWS_ACCOUNT)

LOGIN_STDOUT = run("aws ecr get-login-password --region {R} | docker login \
    --username AWS --password-stdin {ECR_URI}".format(R=AWS_REGION, ECR_URI=ECR_URI)
                   )
print(LOGIN_STDOUT)

BUILD_IMAGE_STDOUT = run (
    "docker build ./1-datapusher-plus/{TAG} -t datapusher-plus:{TAG}".format(TAG=docker_tag)
)
print(BUILD_IMAGE_STDOUT)

TAG_IMAGE_STDOUT = run(
    "docker tag datapusher-plus:{TAG} {ECR_URI}/datapusher-plus:{TAG}".format(ECR_URI=ECR_URI, TAG=docker_tag))
print(TAG_IMAGE_STDOUT)

print("\n Pushing Image, please wait... \n")
PUSH_IMAGE_STDOUT = run(
    "docker push {ECR_URI}/datapusher-plus:{TAG}".format(ECR_URI=ECR_URI, TAG=docker_tag))
print(PUSH_IMAGE_STDOUT)
