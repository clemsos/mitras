function (key, values) {
    
    var txt =" ";
    var users=[];
    var tweets=[];
    var diff=[];

    values.forEach(function (value) {        
        txt += "  "+value.txt;
        for (var i = 0; i < tweets.length; i++) {
            tweets.push(value.tweets[i]);   
        };
        for (var i = 0; i < value.diffusion.length; i++) {
            diff.push(value.diffusion[i]);
        };
        users.push(value.users[0]);
    });

    return key, {
        users : users,
        txt : txt,
        tweets : tweets,
        diffusion : diff
    }
}