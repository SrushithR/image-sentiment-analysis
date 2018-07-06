"""
    Lambda function to perform sentiment analysis of an image uploaded to S3
"""
# boto3 is the AWS python SDK
import boto3

# event is the input to the lambda function and context is an object that interacts with AWS lambda while it is executing
def lambda_handler(event, context):
    """
        This is the entry function in our lambda
        This function's name should be given in the handler part of the lambda configuration
    """
    # all print statements in AWS lambda are logged in CloudWatch by default
    # and it is always advisable to log the input to the lambda function
    print 'input to lambda: {}'.format(event)

    # creating a client object for AWS Rekognition
    client = boto3.client('rekognition')
    # now lets do the sentiment analysis! We use the detect faces method for anylysing the face
    response = client.detect_faces(
        Image={
            # the image uploaded on to S3 is used
            'S3Object' : {
                'Bucket' : 'meetup-image-rekognition',
                'Name' : '{}.jpg'.format(event['name'])
            }
        },
        Attributes=['ALL']
    )
    # extracting only the emotions and age range from the detect face's response
    emotions = response['FaceDetails'][0]['Emotions']
    age_range = response['FaceDetails'][0]['AgeRange']

    # and now lets build the analysis
    analysis = "You must be aged around {} to {} and ".format(age_range['Low'], age_range['High'])
    for emotion in emotions:
        analysis += 'I am {}% sure that you are {}, '.format(round(emotion['Confidence'], 2), emotion['Type'].lower())
    print analysis
    return analysis
