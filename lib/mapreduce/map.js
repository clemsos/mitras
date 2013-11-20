function map(){

    //compute graph
    var diff=[];
    for (var i = 0; i < this.mentions.length; i++) {
        diff.push(this.mentions[i])
    };

    if(this.retweetFromUserId != "") diff.push(this.retweetFromUserId)
    
    // compute dico as string with blank space
    var txt=""
    for (var i = 0; i < this.dico.length; i++) {
        txt+=this.dico[i]+" ";
    };

    var users = [this.userId];

    var tweets = [this.mid];

    this.hashtags.forEach(function(h) {

        emit(h,{
            users : users,
            txt : txt,
            tweets : tweets,
            diffusion : diff
        });

    });

}

