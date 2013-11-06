#!/bin/sh
scriptdir=`dirname $0`

java -mx700m -cp "$scriptdir/stanford-ner.jar:" edu.stanford.nlp.ie.NERServer -loadClassifier $scriptdir/classifiers/chinese.misc.distsim.crf.ser.gz -port 1234 -outputFormat inlineXML