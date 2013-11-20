function (key, values) {
    
    
    var txt =" ";
    var users=[];
    var tweets=[];
    var diff=[];

    values.forEach(function (value) {        
        txt += " ------ "+value.txt;
        tweets.push(value.tweets);
        diff.push(value.diffusion);
        users.push(value.users);
    });

    return key, {
        users : users,
        txt : txt,
        tweets : tweets,
        diffusion : diff
    }
}