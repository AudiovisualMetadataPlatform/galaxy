#!/bin/sh

# Script to run a aws transcribe job using aws-cli.

# Usage:
# transcribe.sh <input_file> <s3_bucket_directory> <output_file> <galaxy_root_directory> <audio_format> 

# TODO: shall we use ENV var for <S3_bucket/directory>, <galaxy_root_directory>? 
# The reason for it is to avoid passing parameter to script each time (although since the script is only called by Galaxy not a human, it probably doesn't matter);
# the reason against it is that it makes the tool less flexible and more dependent.

# record transcirbe command parameters
input_file=$1
s3_bucket_directory=$2
output_file=$3
galaxy_root_directory=$4
audio_format=$5

job_name="AWS_Transcribe"
log_file=${galaxy_root_directory}/tools/aws/${job_name}.log
echo ${input_file} ${s3_bucket_directory} ${output_file} ${galaxy_root_directory} ${audio_format} > $log_file

# upload media file from local Galaxy source file to S3 directory
aws s3 cp $input_file $s3_bucket_directory > $log_file

# TODO aws job related files probably should go to a designated directory called jobs under galaxy root, and each job has a sub-directory after job name
# for now all job files are under the tools/aws directory.

# TODO below can be improved to add a SeqNo to the job directory name so that history is preserved.
# The current SeqNo will be the one more than the last SeqNo, which in turn can be determined from all existing job directories under aws sub directory

# create json file in the aws directory, i.e. <galaxy_root_directory>/tools/aws/<job_name>_request.json
request_file=${galaxy_root_directory}/tools/aws/${job_name}_request.json
input_file_name=$(basename ${input_file})

# TODO can we use input file extension as the AWS audio format, or does this info need to come from media info which can be done in pre-processing?
# for now we can let user specify it via parameter
### use the last extention as the file format
### input_file_format=${input_file_name##*.}

jq -n '{ "TranscriptionJobName": "${job_name}", "LanguageCode": "en-US", "MediaFormat": "${audio_format}", "Media": { "MediaFileUri": "${s3_bucket_directory}/${input_file_name}" } }' > ${request_file}
 
# submit transcribe job
aws transcribe start-transcription-job --cli-input-json file://${request_file} > $log_file

# wait while job is running
while [ `aws transcribe get-transcription-job --transcription-job-name "${job_name}" --query "TranscriptionJob"."TranscriptionJobStatus"` = "IN_PROGRESS" ] 
do
    sleep 10s
done

# retrieve job response
response_file= ${galaxy_root_directory}/tools/aws/${job_name}_response.json
aws transcribe get-transcription-job --transcription-job-name "${job_name}" > ${response_file}
cat $response_file > $log_file
job_status=`jq '.TranscriptionJob.TranscriptionJobStatus' < $response_file`

# if job succeeded, retrieve output file URL and download output file from the URL to galaxy output file location
if [ ${job_status} = 'COMPLETED' ]
    transcript_file_uri=`jq '.TranscriptionJob.Transcript.TranscriptFileUri' < $response_file`
    aws s3 cp $transcript_file_uri $output_file > $log_file
    echo "Job ${job_name} completed in success!" > $log_file
# otherwise print error message to the log and exit with error code
elif [ ${job_status} = 'FAILED' ]
    echo "Job ${job_name} failed!" > $log_file
    exit 1
else
    echo "Job ${job_name} ended in unexpected status: ${job_status}" > $log_file
    exit 2
fi




