import { aws_ecr, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";

export class CdkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const datapusher_plus_repo = new aws_ecr.Repository(
      this,
      "datapusher-plus",
      {
        repositoryName: "datapusher-plus",
      }
    );

    const datapusher_plus_helm_repo = new aws_ecr.Repository(
      this,
      "datapusher-plus-helmchart",
      {
        repositoryName: "datapusher-plus-helmchart",
      }
    );
  }
}
