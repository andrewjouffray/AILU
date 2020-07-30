#!/bin/bash

# sysinfo_page - A script to produce a neural network trained or data from the AILU robot

cat ./cute.txt 

WORK_DIR="/media/andrew/70C2E801236FA6FA/Supermodel"
DATASET_NAME=$1
INPUT_DIR=$2

echo dataset name: $DATASET_NAME
echo input dir: $INPUT_DIR

python /home/andrew/Projects/AILU/tools/augment.py -d $DATASET_NAME -a $INPUT_DIR -w $WORK_DIR

echo Data successfully augmented...
echo Bytes Generated:
du -sh $WORK_DIR/datasets/$DATASET_NAME

echo Preprocessing data

python $WORK_DIR/Tensorflow/Workspace/preprocessing/new_generate_tfrecord.py -x $WORK_DIR/datasets/$DATASET_NAME/training/xml -l $WORK_DIR/datasets/$DATASET_NAME/annotation/label_map.pbtxt -o $WORK_DIR/datasets/$DATASET_NAME/annotaion/train.record -i $WORK_DIR/datasets/$DATASET_NAME/training/images

python $WORK_DIR/Tensorflow/Workspace/preprocessing/new_generate_tfrecord.py -x $WORK_DIR/datasets/$DATASET_NAME/validation/xml -l $WORK_DIR/datasets/$DATASET_NAME/annotation/label_map.pbtxt -o $WORK_DIR/datasets/$DATASET_NAME/annotaion/validation.record -i $WORK_DIR/datasets/$DATASET_NAME/validation/images


echo Training and Validation datasets successfully preprocessed

