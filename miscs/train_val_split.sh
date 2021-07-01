#!/usr/bin/zsh
set -e

# rm -rf Images/train Images/val Annotations/train Annotations/val
mkdir Images/train Images/val Annotations/train Annotations/val
cat train.txt | while read line; do cp Images/${line}.jpg Images/train; done
cat train.txt | while read line; do cp Annotations/${line}.xml Annotations/train; done
cat val.txt | while read line; do cp Images/${line}.jpg Images/val; done
cat val.txt | while read line; do cp Annotations/${line}.xml Annotations/val; done
