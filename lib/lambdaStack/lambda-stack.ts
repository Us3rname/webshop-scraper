import * as cdk from "@aws-cdk/core";
import * as lambda from "@aws-cdk/aws-lambda";
import * as path from "path";
import { Duration } from "@aws-cdk/core";
import * as s3 from "@aws-cdk/aws-s3";
import * as iam from "@aws-cdk/aws-iam";
import { IFunction } from "@aws-cdk/aws-lambda";
import * as events from "@aws-cdk/aws-events";
import * as targets from "@aws-cdk/aws-events-targets";

export interface lambdaStackProps extends cdk.StackProps {
  landingZoneBucket: s3.IBucket;
  jumboScraper: {
    roleName: string;
    roleDescription: string;
  };
}

export class LambdaStack extends cdk.Stack {
  public readonly jumboScraperLambda: IFunction;

  constructor(scope: cdk.Construct, id: string, props: lambdaStackProps) {
    super(scope, id, props);

    const webshopLayer = new lambda.LayerVersion(this, "webshop-layer", {
      compatibleRuntimes: [
        lambda.Runtime.PYTHON_3_9,
        lambda.Runtime.PYTHON_3_8,
      ],
      code: lambda.Code.fromAsset(path.join(__dirname, "./layers")),
      description: "Layers for webshop scraping",
    });

    const lambdaRole = this._createLambdaRole(props);

    this.jumboScraperLambda = new lambda.Function(
      this,
      "Jumbo mobile webshop scraper",
      {
        runtime: lambda.Runtime.PYTHON_3_9,
        handler: "jumbo_process_products.handler",
        code: lambda.Code.fromAsset(path.join(__dirname, "./src")),
        layers: [webshopLayer],
        timeout: Duration.minutes(1),
        environment: {
          bucket_name: props.landingZoneBucket.bucketName,
        },
        role: lambdaRole,
      }
    );

    const eventRule = new events.Rule(this, "scheduleSuperMarketScrapers", {
      schedule: events.Schedule.rate(Duration.days(1)),
    });
    eventRule.addTarget(new targets.LambdaFunction(this.jumboScraperLambda));
  }

  _createLambdaRole(lambdaStackProps: lambdaStackProps) {
    // Access rights
    const accessToSpecificFolder = new iam.PolicyDocument({
      statements: [
        new iam.PolicyStatement({
          resources: [
            lambdaStackProps.landingZoneBucket.bucketArn,
            lambdaStackProps.landingZoneBucket.bucketArn + "*",
          ],
          actions: ["s3:GetObject", "s3:PutObject"],
          effect: iam.Effect.ALLOW,
        }),
      ],
    });

    const lambdaRole = new iam.Role(
      this,
      lambdaStackProps.jumboScraper.roleName,
      {
        assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
        description: lambdaStackProps.jumboScraper.roleDescription,
        inlinePolicies: { accessToSpecificFolder },
      }
    );

    lambdaRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName("CloudWatchLogsFullAccess")
    );

    return lambdaRole;
  }
}