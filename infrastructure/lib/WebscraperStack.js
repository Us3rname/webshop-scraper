import { CfnOutput, Duration } from "@aws-cdk/core";
import * as dynamodb from "@aws-cdk/aws-dynamodb";
import * as s3 from "@aws-cdk/aws-s3";
import * as sst from "@serverless-stack/resources";
import * as sqs from "@aws-cdk/aws-sqs";

export default class WebscraperStack extends sst.Stack {
  constructor(scope, id, props) {
    super(scope, id, props);

    const app = this.node.root;

    this.bucket = new s3.Bucket(this, "WebshopResponse", {
    });

    // Export values
    new CfnOutput(this, "ResponseBucketName", {
      value: this.bucket.bucketName,
      exportName: app.logicalPrefixedName("s3ResponseBucketName"),
    });
    new CfnOutput(this, "ResponseBucketARN", {
      value: this.bucket.bucketArn,
      exportName: app.logicalPrefixedName("s3ResponseBucketARN"),
    });
    
    const table = new dynamodb.Table(this, "product", {
      billingMode: dynamodb.BillingMode.PROVISIONED, // Is cheaper for now
      partitionKey: { name: "productId", type: dynamodb.AttributeType.STRING },
      sortKey: { name: "productType", type: dynamodb.AttributeType.STRING },      
    });

    // Output values
    new CfnOutput(this, "TableName", {
      value: table.tableName,
      exportName: app.logicalPrefixedName("TableName"),
    });

    new CfnOutput(this, "TableArn", {
      value: table.tableArn,
      exportName: app.logicalPrefixedName("TableArn"),
    });

    const sqsBijenkorfProductSpecifications = new sqs.Queue(this, 'Save Bijenkorf Product Specifications Queue', {
      visibilityTimeout: Duration.seconds(60),
      receiveMessageWaitTime: Duration.seconds(20)
    });
   
    // Output values
    new CfnOutput(this, "BijenkorfProductSpecificationSQSTopicName", {
      value: sqsBijenkorfProductSpecifications.queueName,
      exportName: app.logicalPrefixedName("BijenkorfProductSpecificationSQSTopicName"),
    });

    new CfnOutput(this, "BijenkorfProductSpecificationSQSTopicArn", {
      value: sqsBijenkorfProductSpecifications.queueArn,
      exportName: app.logicalPrefixedName("BijenkorfProductSpecificationSQSTopicArn"),
    });

    const sqsZalandoProductSpecification = new sqs.Queue(this, 'Save Zalando Product specifications Queue', {
      visibilityTimeout: Duration.seconds(60),
      receiveMessageWaitTime: Duration.seconds(20)
    });
   
    // Output values
    new CfnOutput(this, "ZalandoProductSpecificationsSQSTopicName", {
      value: sqsZalandoProductSpecification.queueName,
      exportName: app.logicalPrefixedName("ZalandoProductSpecificationsSQSTopicName"),
    });

    new CfnOutput(this, "ZalandoProductSpecificationsSQSTopicArn", {
      value: sqsZalandoProductSpecification.queueArn,
      exportName: app.logicalPrefixedName("ZalandoProductSpecificationsSQSTopicArn"),
    });
  
  }
}