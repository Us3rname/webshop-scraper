import * as cdk from "@aws-cdk/core";
import { DataOrchestrationStack } from "../dataOrchestrationStack/data-orchestration-stack";
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
        rawZoneBucketName:
          environment +
          "-" +
          application +
          "-" +
          this.node.tryGetContext(environment).rawZoneBucketName,
      }
    );

    const lambdaStack = new LambdaStack(
      this,
      environment + "-" + application + "-LambdaStack",
      {
        env,
        landingZoneBucket: lakehouseStack.landingzoneBucket,
        rawZoneBucket: lakehouseStack.rawzoneBucket,
        jumboScraper: {
          roleDescription:
            "Role that is being used for scraping the jumbo website",
          roleName: environment + "-" + application + "-" + "LambdaRoleJumbo",
        },
      }
    );

    new DataOrchestrationStack(
      this,
      environment + "-" + application + "-DataOrchestrationStack",
      {
        scrapeDirkLambda: lambdaStack.dirkScraperLambda,
        scrapeJumboLambda: lambdaStack.jumboScraperLambda,
      }
    );
  }
}
