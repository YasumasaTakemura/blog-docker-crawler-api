#!/usr/bin/env bash
set -e

flg=$#
ENV=latest

usage_exit() {
        if [  $flg -eq  0 ] || [ -z $SOURCE_IMAGE ];then
            echo "Usage: bash $0 -s <SOURCE_IMAGE> [-p <PROJECT_ID> ] ..." 1>&2
            exit 1
        fi
}

set_env(){
    export `cat ./env/.env | grep -v ^# | xargs`
}


# validation
#usage_exit

set_env

# check args
while getopts p:s:e:h OPT
do
    case $OPT in
        p)  PROJECT_ID=$OPTARG
            ;;
        s)  SOURCE_IMAGE=$OPTARG
            ;;
        e)  ENV=$OPTARG
            ;;
        h)  usage_exit
            ;;
        \?) usage_exit
            ;;
    esac
done

echo "============Start Pushing Docker Image To GCR============"
echo $SOURCE_IMAGE:$ENV

#docker build --no-cache=true -t gcr.io/$PROJECT_ID/$SOURCE_IMAGE:$ENV .
docker build -t gcr.io/$PROJECT_ID/$SOURCE_IMAGE:$ENV .
#docker tag $SOURCE_IMAGE gcr.io/$PROJECT_ID/$SOURCE_IMAGE:$ENV
gcloud docker -- push gcr.io/$PROJECT_ID/$SOURCE_IMAGE:$ENV