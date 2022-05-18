import subprocess

def run(cmd):
    to_decode = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout
    output = to_decode.read()

    return output.decode()


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
    "helm push ./chart-package/datapusher-plus-helmchart-0.1.0.tgz oci://{}".format(ECR_URI))
print(PUSH_IMAGE_STDOUT)
