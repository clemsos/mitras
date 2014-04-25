// MITRAS UI

/////////////////////////// MODULE DEPENDENCIES
    
    var express = require('express');
    var app = module.exports = express();
    var server = require('http').createServer(app);

    var moment = require('moment');

    // dbs
    // var redis = require('redis');
    var mongoose = require("mongoose");

    // Hook Socket.io into Express
    // var io = require('socket.io').listen(server);

/////////////////////////// CONFIGURATION

    // https://github.com/visionmedia/express/wiki/Migrating-from-3.x-to-4.x

    var config = require("./config/config.json");

    
    app.use(function(err, req, res, next){
      console.error(err.stack);
      res.send(500, 'Something broke!');
    });

    app.configure( function(){
        app.set('views', __dirname + '/views');
        app.engine('.html', require('ejs').renderFile);
        app.set('view engine', 'html');
        app.set('view options', {
                layout: false
        });
        
        app.use(express.bodyParser());
        app.use(express.methodOverride());
        app.use(express.static(__dirname + '/public'));

        app.use(app.router);
    });

    app.configure('development', function(){
        app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
    });

    app.configure('production', function(){
        app.use(express.errorHandler());
    });

/////////////////////////// MONGO

    mongoose.connect('mongodb://localhost/'+config.ETHER_MONGO_DB, function(err) {
      if (err) { throw err; }
    });

    var db = mongoose.connection;
    db.on('error', console.error.bind(console, 'connection error:'));

    // model 

/////////////////////////// ROUTES

    app.get('/', function(req, res){
        // res.send("hello world !");
        res.render('index', {layout: false});
    });

    // serve data 
    app.get('/time', function(req, res){

        res.render('timeline', {layout: false});
        
    });

/////////////////////////// SOCKET IO
/*

    // var redisSocketClient= redis.createClient()
    // // redisSocketClient.subscribe(config.ETHER_REDIS_Q);

    var clientSocket = io
        .sockets
        // .of('/device')
        .on('connection', function (socket) {

            socket.emit('connect', {
                 'hi': 'hello device!'
            });

        });
*/

// Start server
server.listen(config.MITRAS_NODE_PORT, function() {
    console.log("Express server listening on port %d in %s mode", this.address().port, app.settings.env);
});