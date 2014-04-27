// MITRAS UI

/////////////////////////// MODULE DEPENDENCIES
    
    var express = require('express');
    var app = module.exports = express();
    var server = require('http').createServer(app);

    var moment = require('moment');

    var config = require("./config/config.json");

    var db = require('monk')('localhost/'+config.MITRAS_MONGO_DB)
    , memes = db.get('memes')

    // dbs
    // var redis = require('redis');
    // var mongoose = require("mongoose");

    // Hook Socket.io into Express
    var io = require('socket.io').listen(server);

/////////////////////////// CONFIGURATION

    // TODO? https://github.com/visionmedia/express/wiki/Migrating-from-3.x-to-4.x
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


/////////////////////////// ROUTES

    app.get('/', function(req, res){
        // res.send("hello world !");
        res.render('index', {layout: false});
    });

    // serve data 
    app.get('/time', function(req, res){

        res.render('timeline', {layout: false});
        
    });

    app.get("/data/:meme",  function(req, res){
        
        console.log(req.params.meme)
        var meme_name=req.params.meme;

        memes.findOne({"name":req.params.meme}).on('success', function (doc) {

            if(doc==null) res.send("meme doesn't exist")
            else res.send(doc.data)
            // for (var i = 0; i < doc.data.length; i++) {
            //     console.log(doc.data[i].time);
            // }
        });
       
    });

    app.get("/times/:meme", function(req, res){
        
        console.log(req.params.meme)
        var meme_name=req.params.meme;

        memes.findOne({"name":req.params.meme}).on('success', function (doc) {

            if(doc==null) res.send("meme doesn't exist")
            else res.send(doc.data.map(function(d){
                return {"count":d.count, "timestamp":d.time}
            }))

        });
       
    });

/////////////////////////// SOCKET IO

    var clientSocket = io
        .sockets
        .on('connection', function (socket) {

            socket.emit('connect', {
                 'hi': 'hello frontend!'
            });

            socket.on("config",function (data){
                var config=JSON.parse(data)
                // console.log(config);
                // updateData(config.start,config.end);
                socket.emit("update");
            })
        });

function updateData (start,end){
    console.log("time changed");
    // console.log(start,end);
}


// Start server
server.listen(config.MITRAS_NODE_PORT, function() {
    console.log("Express server listening on port %d in %s mode", this.address().port, app.settings.env);
});