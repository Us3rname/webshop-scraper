#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "@aws-cdk/core";
import { MyPipelineStack } from "../lib/pipelineStack/my-pipeline-stack";

const app = new cdk.App();

interface EnvProps extends cdk.StackProps {
  env: cdk.Environment;
}

class MyService extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string, props: EnvProps) {
    super(scope, id);

    const pipeline = new MyPipelineStack(
      this,
      this.node.tryGetContext("default").application + "PipelineStack",
      props
    );
  }
}

const env: cdk.Environment = app.node.tryGetContext("default").env;
const props: EnvProps = { env };
new MyService(app, "develop", props);
