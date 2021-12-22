import * as cdk from "@aws-cdk/core";
import * as lambda from "@aws-cdk/aws-lambda";
import * as tasks from "@aws-cdk/aws-stepfunctions-tasks";
import * as sfn from "@aws-cdk/aws-stepfunctions";
import { Duration } from "@aws-cdk/core";

export interface DataOrchestrationStackProps extends cdk.StackProps {
  scrapeDirkLambda: lambda.Function;
  scrapeJumboLambda: lambda.Function;
}

export class DataOrchestrationStack extends cdk.Stack {
  constructor(
    scope: cdk.Construct,
    id: string,
    props: DataOrchestrationStackProps
  ) {
    super(scope, id, props);

    const dirkJob = new tasks.LambdaInvoke(this, "Scrape Dirk Webshop", {
      lambdaFunction: props.scrapeDirkLambda,
      // Lambda's result is in the attribute `Payload`
      outputPath: "$.Payload",
    });

    const jumboJob = new tasks.LambdaInvoke(this, "Scrape Jumbo Webshop", {
      lambdaFunction: props.scrapeJumboLambda,
      // Lambda's result is in the attribute `Payload`
      outputPath: "$.Payload",
    });

    const parallel = new sfn.Parallel(this, "Scrape webshops in paralell");
    parallel.branch(dirkJob);
    parallel.branch(jumboJob);

    new sfn.StateMachine(this, "StateMachine", {
      definition: parallel,
      timeout: Duration.minutes(5),
    });
  }
}
