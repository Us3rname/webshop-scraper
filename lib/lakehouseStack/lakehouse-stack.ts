import * as cdk from "@aws-cdk/core";
import * as s3 from "@aws-cdk/aws-s3";

export interface lakehouseStackProps extends cdk.StackProps {
  landingZoneBucketName: string;
  rawZoneBucketName: string;
}

export class LakehouseStack extends cdk.Stack {
  public readonly landingzoneBucket: s3.IBucket;
  public readonly rawzoneBucket: s3.IBucket;

  constructor(scope: cdk.Construct, id: string, props: lakehouseStackProps) {
    super(scope, id, props);

    this.landingzoneBucket = new s3.Bucket(this, props.landingZoneBucketName, {
      bucketName: props.landingZoneBucketName,
      versioned: true,
      lifecycleRules: [
        {
          abortIncompleteMultipartUploadAfter: cdk.Duration.days(90),
          expiration: cdk.Duration.days(365),
          transitions: [
            {
              storageClass: s3.StorageClass.INTELLIGENT_TIERING,
              transitionAfter: cdk.Duration.days(30),
            },
          ],
        },
      ],
    });

    this.rawzoneBucket = new s3.Bucket(this, props.rawZoneBucketName, {
      bucketName: props.rawZoneBucketName,
      versioned: true,
      lifecycleRules: [
        {
          abortIncompleteMultipartUploadAfter: cdk.Duration.days(90),
          expiration: cdk.Duration.days(365),
          transitions: [
            {
              storageClass: s3.StorageClass.INTELLIGENT_TIERING,
              transitionAfter: cdk.Duration.days(30),
            },
          ],
        },
      ],
    });
  }
}
