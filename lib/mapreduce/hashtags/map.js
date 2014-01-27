function map(){

    var txt =" ";
    var users=[];
    var tweets=[];
    var diff=[];
    var date=[];
    var geo=[];
    

    //compute diffusion graph
    for (var i = 0; i < this.mentions.length; i++) {
        // diff.push(this.mentions[i]);
        if(this.uid != this.mentions[i]) diff.push({"from":this.uid,"to":this.mentions[i]})
    };

    // add RT info to diffusion graph
    if(!isNaN(this.retweeted_uid)) diff.push({"from":this.retweeted_uid,"to":this.uid});
    
    // compute dico as string with blank space
    for (var i = 0; i < this.dico.length; i++) {
        txt+=this.dico[i]+" ";
    };

    // collect users
    users.push(this.uid);

    // collect all tweets
    tweets.push(this.mid);
    if(!isNaN(this.retweeted_status_mid)) tweets.push(this.retweeted_status_mid)


    // collect all geo info
    if (!isNaN(this.geo)) geo.push(this.geo)
    
    // collect all dates   
    function roundDate(_date) {

        _date.setHours(_date.getHours() + Math.round(_date.getMinutes()/60));
        _date.setMinutes(0);
        _date.setSeconds(0);

        return _date.getTime()/1000;
    }

    date.push(roundDate( new Date(this.created_at) ));

    // should be hashtags or mentions
    this.hashtags.forEach(function(h) {
        // print
        emit(h,{
            users : users,
            txt : txt,
            tweets : tweets,
            diffusion : diff,
            date : date,
            geo: geo
        });
    });
}