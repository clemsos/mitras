// controllers.js

var safename="biaoge";

app.controller('timeCtrl', function($scope,$http,$timeout,socket,config,dataService){
  
  config.setName(safename);

  $http.get("data/"+safename).success(function(data) {

    // console.log(data);
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
      dataService.multilayer
      ;

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

        // multilayer
        d.data.multi_graph.forEach(function(v){  
            dataService.multilayer.push(v);
        });

      };
  }

});


app.controller("dataCtrl", function($scope,$http,socket,config,dataService){
  console.log("dataCtrl");
  console.log(dataService);
})

app.controller('geoCtrl', function($scope,$http,config,mapService,dataService){
  
    var mapFile="../data/"+safename+"/"+safename+"_usermap.json";
  
    // $scope.sort=["gdp","population","meme"]
    $scope.centroidsOnMap=true;

    mapService.mainland.getData(function(data){ $scope.mainland=data })
    mapService.taiwan.getData(function(data){ $scope.taiwan=data })
    mapService.hkmacau.getData(function(data){ $scope.hkmacau=data })
    
    // update geoData
    $scope.$watch(function() { return config.end; }, function(newVal,oldVal){
      $scope.geoEdges=dataService.geo;
    })

    $scope.$watch(function() { return config.start; }, function(newVal,oldVal){
      $scope.geoEdges=dataService.geo;
    })

    
})

app.controller('wordCtrl', function($scope,$http,config){
  var wordFile="../data/"+safename+"/"+safename+"_d3graph.json";
  
  $http.get(wordFile).success(function(data) { 

    $scope.words=data.words;
    $scope.wordForceStarted=true;

  })

})

app.controller('userCtrl', function($scope,$http,config){
  var wordFile="../data/"+safename+"/"+safename+"_d3graph.json";
  
  $http.get(wordFile).success(function(data) { 
    $scope.users=data.users;
  })
})