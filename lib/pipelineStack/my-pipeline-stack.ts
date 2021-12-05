import * as cdk from "@aws-cdk/core";

import {
  CodePipeline,
  CodePipelineSource,
  ShellStep,
} from "@aws-cdk/pipelines";
import { DevPipelineStage } from "./dev-pipeline-stage";

interface pipelineProps extends cdk.StackProps {}

export class MyPipelineStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: pipelineProps) {
    super(scope, id, props);

    const pipeline = new CodePipeline(this, "Pipeline", {
      ...props,
      pipelineName: "Pipeline",
      synth: new ShellStep("Synth", {
        input: CodePipelineSource.gitHub(
          "Us3rname/webshop-scraper",
          "cdk-init"
        ),
        commands: ["npm ci", "npm run build", "npx cdk synth"],
      }),
    });

    // pipeline.addStage(
    //   new DevPipelineStage(this, "development", {
    //     ...props,
    //   })
    // );
  }
}
