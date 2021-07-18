# AWS Personalize

## Steps to Follow

- ### Add Datatset Group for which Recommendation is to be performed
- ### Create Campaign
- ### Copy CampaignArn
- ### Replace <campaignArn> in the below script with the campaignArn

- Execute the below script
  <br><br>

## [Reference Link Personalize](https://towardsdatascience.com/build-a-recommender-system-in-less-than-an-hour-using-amazon-personalize-68bee9931c60)

# Lambda Function and API Gateway

## Steps to Follow

- ### Create a new Policy to give full access to Personalize Service as shown in Personalize_permission.json file
- ### Create a new Policy to give full access to Lambda Service as shown in Lambda_permission.json file
- ### Create a new lambda role and attach the above policies
- ### Paste the lambda.py code in the editor
- ### Create a new API Gateway and point it to the lambda function
- ### Keep the method as Any and set the resource path as {proxy+}
- ### Deploy the API Gateway
- ### The Lambda Function is now good to go

### Request Example - https://ccdvwj5y9f.execute-api.us-east-1.amazonaws.com/?name=0

### Change the name to any number to get different recommendations

### [Link to Refer what's captured by the Event Object](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html)
