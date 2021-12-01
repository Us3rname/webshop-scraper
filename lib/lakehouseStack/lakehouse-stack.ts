import * as cdk from "@aws-cdk/core";
import * as s3 from "@aws-cdk/aws-s3";

export interface lakehouseStackProps extends cdk.StackProps {
  landingZoneBucketName: string;
}

export class LakehouseStack extends cdk.Stack {
  public readonly landingzoneBucket: s3.IBucket;

  constructor(scope: cdk.Construct, id: string, props: lakehouseStackProps) {
    super(scope, id, props);

    const landingzoneBucket = new s3.Bucket(this, props.landingZoneBucketName, {
      bucketName: props.landingZoneBucketName,
      versioned: true, // a Bucket used as a source in CodePipeline must be versioned
    });

    this.landingzoneBucket = landingzoneBucket;
  }
}
