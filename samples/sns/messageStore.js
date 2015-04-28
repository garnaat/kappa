console.log('Loading event');
var aws = require('aws-sdk');
var ddb = new aws.DynamoDB({params: {TableName: 'snslambda'}});
 
exports.handler = function(event, context) {
  var SnsMessageId = event.Records[0].Sns.MessageId;
  var SnsPublishTime = event.Records[0].Sns.Timestamp;
  var SnsTopicArn = event.Records[0].Sns.TopicArn;
  var LambdaReceiveTime = new Date().toString();
  var itemParams = {Item: {SnsTopicArn: {S: SnsTopicArn},
  SnsPublishTime: {S: SnsPublishTime}, SnsMessageId: {S: SnsMessageId},
  LambdaReceiveTime: {S: LambdaReceiveTime}  }};
  ddb.putItem(itemParams, function() {
    context.done(null,'');
  });
};
