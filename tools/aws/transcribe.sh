#!/bin/sh

# Script including all logic needed to run a aws transcribe job using awscli

# Use:
# transcribe <input_file> <s3_bucket_directory> <output_file> <galaxy_base_directory>

# TODO: shall we use ENV var for <S3_bucket/directory>, <galaxy_base_directory>? 
# The reason for it is to avoid passing parameter to script each time (although since the script is only called by Galaxy not a human, it probably doesn't matter);
# the reason against it is that it makes the tool less flexible and more dependent.

# record transcirbe command parameters
input_file = $1
s3_bucket_directory = $2
output_file = $3
galaxy_base_directory = $4
log_file = ${galaxy_base_directory}/tools/aws/${job_name}.log

#upload media file from local Galaxy source file to S3 directory
aws s3 cp $input_file $s3_bucket_directory

# TODO below can be improved to add a SeqNo to the job directory name so that history is preserved.
# The current SeqNo will be the one more than the last SeqNo, which in turn can be determined from all existing job directories under aws sub directory

# create json file in the job directory, i.e. <galaxy_base_directory>/tools/aws/<job_name>_request.json
job_name = "AmpAwsTransJob"
request_file = ${galaxy_base_directory}/tools/aws/${job_name}_request.json
jq -n '{ "TranscriptionJobName": "${job_name}", "LanguageCode": "en-US", "MediaFormat": "wav", "Media": { "MediaFileUri": "${s3_bucket_directory}/${input_file}" } }' > ${request_file}
 
# submit transcribe job
aws transcribe start-transcription-job --cli-input-json file://${request_file}

# wait while job is running
while [ `aws transcribe get-transcription-job --transcription-job-name "${job_name}" --query "TranscriptionJob"."TranscriptionJobStatus"` = "IN_PROGRESS" ] 
do
    sleep 10s
done

# retrieve job response
response_file = `aws transcribe get-transcription-job --transcription-job-name "${job_name}" > ${job_name}_response.json`
cat $response_file 

# if job succeeded, retrive output file URL and download output file from the URL to galaxy output file location

transcript_file_uri = `jq '.TranscriptionJob.Transcript.TranscriptFileUri' < $response_file`
aws s3 cp $transcript_file_uri $output_file
echo "Job ${job_name} completed in success!" > $log_file


cat $response_file > $log_file



