import subprocess

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

TAG_IMAGE_STDOUT = run(
    "docker tag datapusher-plus:latest {ECR_URI}/datapusher-plus".format(ECR_URI=ECR_URI))
print(TAG_IMAGE_STDOUT)

print("\n Pushing Image, please wait... \n")
PUSH_IMAGE_STDOUT = run(
    "docker push {ECR_URI}/datapusher-plus:latest".format(ECR_URI=ECR_URI))
print(PUSH_IMAGE_STDOUT)
