#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "@aws-cdk/core";
import { LambdaStack } from "../lib/lambdaStack/lambda-stack";
import { LakehouseStack } from "../lib/lakehouseStack/lakehouse-stack";

const app = new cdk.App();
const env: cdk.Environment = app.node.tryGetContext("default").env;
const application = app.node.tryGetContext("default").application;
const environment = "develop";

const lakehouseStack = new LakehouseStack(
  app,
  environment + "-" + application + "-LakehouseStack",
  {
    env,
    landingZoneBucketName:
      environment +
      "-" +
      application +
      "-" +
      app.node.tryGetContext(environment).landingZoneBucketName,
  }
);

new LambdaStack(app, environment + "-" + application + "-LambdaStack", {
  env,
  landingZoneBucket: lakehouseStack.landingzoneBucket,
  jumboScraper: {
    roleDescription: "Role that is being used for scraping the jumbo website",
    roleName: environment + "-" + application + "-" + "LambdaRoleJumbo",
  },
});
