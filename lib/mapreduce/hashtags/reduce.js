function reduce(key, values) {
    
    var txt =" ";
    var users=[];
    var tweets=[];
    var diff=[];
    var date=[];
    var geo=[];

    values.forEach(function (value) {
        txt += "  "+value.txt;
        
        for (var i = 0; i < value.tweets.length; i++) {
            tweets.push(value.tweets[i]);
        };

        for (var i = 0; i < value.diffusion.length; i++) {
            diff.push(value.diffusion[i]);
        };
        users.push(value.users[0]);
        date.push(value.date[0]);
        if(value.geo.length >1 ) geo.push(value.geo);

    });

    return key, {
        users : users,
        txt : txt,
        tweets : tweets,
        diffusion : diff,
        date : date,
        geo : geo
    }
}