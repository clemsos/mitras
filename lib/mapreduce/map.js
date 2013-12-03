function map(){

    //compute diffusion graph
    var diff=[];
    for (var i = 0; i < this.mentions.length; i++) {
        diff.push(this.mentions[i])
    };

    // add RT info to diffusion graph
    if(this.retweetFromUserId != "") diff.push(this.retweetFromUserId)
    
    // compute dico as string with blank space
    var txt=""
    for (var i = 0; i < this.dico.length; i++) {
        txt+=this.dico[i]+" ";
    };

    // collect users
    var users = [this.userId];

    // collect all tweets
    var tweets = [this.mid];
    if(this.retweetFromPostId != "") tweets.push(this.retweetFromPostId)

    // TO_BE_CHANGED is changed by a replace in python script
    // should be hashtags or mentions
    this.TO_BE_CHANGED.forEach(function(h) {

        emit(h,{
            type: "TO_BE_CHANGED",
            users : users,
            txt : txt,
            tweets : tweets,
            diffusion : diff
        });

    });

}

