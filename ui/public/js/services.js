// services.js

app.factory('config', function($window) {
    
    return new Config();
    // return new $window.feedconfig.FeedConfig();

});

app.factory('JsonService', function($resource) {
    // var data = generateData(10);
    // return data;
});