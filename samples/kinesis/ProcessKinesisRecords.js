console.log('Loading event');
exports.handler = function(event, context) {
   console.log(JSON.stringify(event, null, '  '));
   for(i = 0; i < event.Records.length; ++i) {
      encodedPayload = event.Records[i].kinesis.data;
      payload = new Buffer(encodedPayload, 'base64').toString('ascii');
      console.log("Decoded payload: " + payload);
   }
   context.done(null, "Hello World");  // SUCCESS with message
};
