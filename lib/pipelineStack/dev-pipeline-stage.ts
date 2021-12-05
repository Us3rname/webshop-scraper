import * as cdk from "@aws-cdk/core";
import { LakehouseStack } from "../lakehouseStack/lakehouse-stack";
import { LambdaStack } from "../lambdaStack/lambda-stack";

interface devPipelineProps extends cdk.StackProps {}

export class DevPipelineStage extends cdk.Stage {
  constructor(scope: cdk.Construct, id: string, props: devPipelineProps) {
    super(scope, id, props);

    const env: cdk.Environment = this.node.tryGetContext("default").env;
    const application = this.node.tryGetContext("default").application;
    const environment = "develop";

    const lakehouseStack = new LakehouseStack(
      this,
      environment + "-" + application + "-LakehouseStack",
      {
        env,
        landingZoneBucketName:
          environment +
          "-" +
          application +
          "-" +
          this.node.tryGetContext(environment).landingZoneBucketName,
      }
    );

    new LambdaStack(this, environment + "-" + application + "-LambdaStack", {
      env,
      landingZoneBucket: lakehouseStack.landingzoneBucket,
      jumboScraper: {
        roleDescription:
          "Role that is being used for scraping the jumbo website",
        roleName: environment + "-" + application + "-" + "LambdaRoleJumbo",
      },
    });
  }
}
