# SNA for Weibo
Data extraction util from Chinese microblogs services for Social Network Analysis experiments
Written in Python 

## Installation 

    # Install Tencent Weibo lib
    pip install -e git+git://github.com/andelf/pyqqweibo.git
    rm -R src # remove useless install files

    pip install pyqqweibo

Fill in your credentials (tencent weibo, sina weibo, etc.)
    
    cp settings.py.sample settings.py


# Run the tests

    pip install nose pyrg
    ./bin/test-start.sh

## Jobs Queue

    pip install rq rq-scheduler rq-dashboard 
    
You can monitor the jobs with the command ```rq-dashboard``` available on [http://yourhost:9181/](http://localhost:9181/)
