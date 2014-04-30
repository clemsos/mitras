// controllers.js

app.controller('navCtrl', function($scope,config,memeService){

  memeService.list.getData(function(memeList){ 
    $scope.memeList=[];
    memeList.memes.forEach(function(meme){
       // exclude some memes from the list
        if (meme.safename != "diaosi" && meme.safename != "iphone5" && meme.safename != "tuhao" && meme.safename != "cgc" && meme.rank == 1 && meme.name != "") $scope.memeList.push(meme)
    });

  })

})

app.controller('dataCtrl', function($scope,$http,$location,$timeout,config,dataService){


  console.log($location.$$absUrl);
  var url=getLocation($location.$$absUrl); // default
  
  var safename=url.pathname.slice(1,url.pathname.length);
  console.log(safename);

  if(safename == undefined) safename="biaoge"
  console.log(safename);


  function getLocation(href) {
    var match = href.match(/^(https?\:)\/\/(([^:\/?#]*)(?:\:([0-9]+))?)(\/[^?#]*)(\?[^#]*|)(#.*|)$/);
    return match && {
        protocol: match[1],
        host: match[2],
        hostname: match[3],
        port: match[4],
        pathname: match[5],
        search: match[6],
        hash: match[7]
    }
  }
    
  

  config.setName(safename);   //default


  $http.get("data/"+safename).success(function(data) {

    console.log(data);
    $scope.rawdata=data;
    $scope.data=data;

    // TIME
    $scope.timeSeriesData=data.map(function(d){
      return {"count":d.count, "timestamp":d.time}
    });

    // sort time frames
    $scope.timeSeriesData.sort(function(a,b){ return a.timestamp-b.timestamp});

    $scope.timeSeriesData.map(function(d){ d.timestamp=d.timestamp*1000});

    // init scope values
    $scope.timeMax=$scope.timeSeriesData.length;
    $scope.start=$scope.timeSeriesData[0].timestamp;
    $scope.end=$scope.timeSeriesData[data.length-1].timestamp;
    config.setStart($scope.start)
    config.setEnd($scope.end)    
    // socket.emit('config', config.toJSON());
    
    $scope.updateTimeData();

    $scope.updateData();
  });


  $scope.stop = function(){
    $timeout.cancel(playAll);
  }

  var i,step,frames;

  $scope.playAll=function (){
    step=10,
    i=step, 
    frames=$scope.timeSeriesData.length/step;
    $timeout($scope.playFrame,100);
  }

  $scope.playFrame=function() {

    var t0=$scope.timeSeriesData[i-step].timestamp,
        t1=$scope.timeSeriesData[i].timestamp;

        // $scope.start=t0;
        $scope.end=t1;
        console.log(t0,t1);

        i+=step;
        $timeout($scope.playFrame,100)
  }

  // // monitor time changes
  $scope.$watch('start', function(newStart, oldVal) {
    // console.log(updatedStart);
    if (newStart!=undefined) {
      $scope.start=newStart; 
      $scope.updateTimeData();
      config.setStart(newStart)
      // socket.emit('config', config.toJSON());

      $scope.updateData();
    }
  })

  $scope.$watch('end', function(newEnd, oldVal) {
    if (newEnd!=undefined) {
      $scope.end=newEnd; 
      $scope.updateTimeData();
      config.setEnd(newEnd);
      // socket.emit('config', config.toJSON());
      $scope.updateData();
    }  
  })

  var color = d3.scale.category20c();

  $scope.updateTimeData=function () {
    $scope.timeSeriesData.forEach(function(d) {
        if(d.timestamp>$scope.start && d.timestamp<$scope.end) d.selected=true
        else d.selected=false
        d.date=new Date(d.timestamp);
    });
  }

  $scope.updateData=function () {
      
      
      $scope.data=$scope.rawdata.map(function(d) {
        if(d.time>(config.start/1000) && d.time<(config.end/1000)) return d
      })


      // console.log("updateData");
      // console.log($scope.rawdata);
      
      
      // init
      dataService.users.nodes=[], 
      dataService.users.edges=[],
      dataService.users.index=[],
      dataService.words.nodes=[], 
      dataService.words.edges=[],
      dataService.words.index=[],
      dataService.geo=[],
      dataService.wordsProvince={};


      // update data
      for (var i = 0; i < $scope.data.length; i++) {
        var d=$scope.data[i];
        if(d==undefined) return;
        
        // user nodes
        d.data.user_nodes.forEach(function(v){  
          if(dataService.users.index.indexOf(v.name) == -1 ) {
            dataService.users.nodes.push(v);
            dataService.users.index.push(v.name);
          }
        });

        // user edges
        d.data.user_edges.forEach(function(v){  
          if(dataService.users.index.indexOf(v.source) !=-1 && dataService.users.index.indexOf(v.target) != -1 
            ) {
              // check if already exists
              var index=-1;
              for (var j = 0; j < dataService.users.edges.length; j++) {
                var e=dataService.users.edges[j];
                if (v.source===e.source && v.target ===e.target) {
                  index=j;
                  break;
                } 
              }   
              if(index!=-1) dataService.users.edges[index].weight+=v.weight;
              else dataService.users.edges.push(v);
          }
        });

        // word nodes
        d.data.words_nodes.forEach(function(v){  
          if(dataService.words.index.indexOf(v.name) == -1 ) {
            dataService.words.nodes.push(v);
            dataService.words.index.push(v.name);
          }
        });

        // words edges
        d.data.words_edges.forEach(function(v){  
          
          // check if in scope
          if(dataService.words.index.indexOf(v.source) !=-1 && dataService.words.index.indexOf(v.target) != -1) {
              
              // check if already exists
              var index=-1;
              for (var j = 0; j < dataService.words.edges.length; j++) {
                var e=dataService.words.edges[j];
                if (v.source===e.source && v.target ===e.target) {
                  index=j;
                  break;
                } 
              }   

              if(index!=-1) dataService.words.edges[index].weight+=v.weight;
              else dataService.words.edges.push(v);
          }
        });

        // geo (provinces edges)
        d.data.provinces_edges.forEach(function(v){  
            
            if (v.source == "Qita" || v.source == 0 || v.source =="Haiwai") return 
            if (v.target == "Qita" || v.target == 0 || v.target =="Haiwai") return 

            var index=-1;
            for (var j = 0; j < dataService.geo.length; j++) {
              var e=dataService.geo[j];
              if (v.source===e.source && v.target ===e.target) {
                index=j;
                break;
              } 
            }   
            if(index!=-1) dataService.geo[index].weight+=v.weight;
            else dataService.geo.push(v);
              // dataService.geo.push(v);
        });

        // provinces_words
        d.data.words_provinces.forEach(function(v){

          // init word
          if(dataService.wordsProvince[v.word]==undefined) dataService.wordsProvince[v.word]=[]

          //check if province already exists
          var index=-1;
          for (var j = 0; j < dataService.wordsProvince[v.word].length; j++) {
            var e=dataService.wordsProvince[v.word][j];
            if (v.province===e.label) {
              index=j;
              break;
            } 
          }
          if(index==-1) dataService.wordsProvince[v.word].push({"label":v.province,"value":v.weight, "color":color(v.province)});
          else dataService.wordsProvince[v.word][index]["value"]+=v.weight;
        })
      };
    }

});


// app.controller("dataCtrl", function($scope,$http,socket,config,dataService){
//   console.log("dataCtrl");
//   console.log(dataService);
// })

app.controller('geoCtrl', function($scope,$http,config,geoService,dataService){
  
    // var mapFile="../data/"+safename+"/"+safename+"_usermap.json";
  
    // $scope.sort=["gdp","population","meme"]
    $scope.centroidsOnMap=true;

    geoService.mainland.getData(function(data){ $scope.mainland=data })
    geoService.taiwan.getData(function(data){ $scope.taiwan=data })
    geoService.hkmacau.getData(function(data){ $scope.hkmacau=data })

    geoService.ratio.getData(function(data){ 
      var provinceUsersRatio={}
      data.nb_of_users_by_provinces.forEach(function(d){
        provinceUsersRatio[d.name]=d.percent;
      })

      $scope.ratio=provinceUsersRatio;
    })

    
    // update geoData
    $scope.$watch(function() { return config.end; }, function(newVal,oldVal){
      $scope.geoEdges=dataService.geo;
    })

    $scope.$watch(function() { return config.start; }, function(newVal,oldVal){
      $scope.geoEdges=dataService.geo;
    })

    $scope.saveGeo=function(){
      var sv=new Simg($(".geo-container svg")[0]);
      sv.download();
    }

})

app.controller('wordCtrl', function($scope,$http,config,dataService){

  $scope.wordForceStarted=true;

  $scope.$watch(function() { return config.end; }, function(newVal,oldVal){
    $scope.words=dataService.words;
    if(dataService.words.index!=undefined) $scope.wordsLength=dataService.words.index.length;
    $scope.wordProvinces=dataService.wordsProvince;

  })

  $scope.$watch(function() { return config.start; }, function(newVal,oldVal){
    $scope.words=dataService.words;
    if(dataService.words.index!=undefined) $scope.wordsLength=dataService.words.index.length;
    $scope.wordProvinces=dataService.wordsProvince;
  })

  $scope.saveWords=function(){
    var sv=new Simg($(".word-container svg")[0]);
    sv.download();
  }

})

app.controller('userCtrl', function($scope,$http,config,dataService){

  $scope.userForceStarted=true;

  $scope.$watch(function() { return config.end; }, function(newVal,oldVal){
    $scope.users=dataService.users;
    if(dataService.users.index!=undefined) $scope.usersLength=dataService.users.index.length;

  })

  $scope.$watch(function() { return config.start; }, function(newVal,oldVal){
    $scope.users=dataService.users;
    if(dataService.users.index!=undefined) $scope.usersLength=dataService.users.index.length;
  })

  $scope.saveUsers=function(){
    var sv=new Simg($(".user-container svg")[0]);
    sv.download();
  }

})