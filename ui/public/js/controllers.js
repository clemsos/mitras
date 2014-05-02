// controllers.js

app.controller('navCtrl', function($scope,config,memeService){

  memeService.list.getData(function(memeList){ 
    $scope.memeList=[];
    memeList.memes.forEach(function(meme){
       // limit list to some of the memes only
       var memelist=['biaoge','thevoice','moyan','hougong', 'gangnam','sextape','dufu','ccp','yuanfang','qiegao']
        if (memelist.indexOf(meme.safename)!=-1) $scope.memeList.push(meme)
    });

  })

})

app.controller('dataCtrl', function($scope,$http,$location,$timeout,config,dataService){


  // get location and name
  // console.log($location.$$absUrl);
  var url=getLocation($location.$$absUrl); // default
  
  var safename=url.pathname.slice(1,url.pathname.length);
  console.log(safename);

  if(safename == undefined) safename="biaoge"
  // console.log(safename);

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


  $http.get("times/"+safename).success(function(_time_data) {

    // TIME
    $scope.timeSeriesData=_time_data

    // sort time frames
    $scope.timeSeriesData.sort(function(a,b){ return a.timestamp-b.timestamp});

    $scope.timeSeriesData.map(function(d){ d.timestamp=d.timestamp*1000});

    // init scope values
    $scope.timeMax=$scope.timeSeriesData.length;
    $scope.start=$scope.timeSeriesData[0].timestamp;
    $scope.end=$scope.timeSeriesData[_time_data.length-1].timestamp;
    config.setStart($scope.start)
    config.setEnd($scope.end)    
    // socket.emit('config', config.toJSON());
    
    $scope.updateTimeData();

    // $scope.updateData();
  });


  $scope.stop = function(){
    $timeout.cancel($scope.playFrame);
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

    
    if($scope.start!=undefined && $scope.end!=undefined && ($scope.prevStart!=$scope.start || $scope.prevEnd!=$scope.end)) {

      var url="datatime/"+safename+"/"+$scope.start+"/"+$scope.end
      // console.log(url);

      $http.get(url).success(function(_data) {

        // $scope.data=_data;
        dataService.users.nodes=_data.users.nodes 
        dataService.users.edges=_data.users.edges,
        dataService.users.index=_data.users.index,
        dataService.words.nodes=_data.words.nodes 
        dataService.words.edges=_data.words.edges,
        dataService.words.index=_data.words.index,
        dataService.geo=_data.geo,
        dataService.wordsProvince=_data.wordsProvince
        dataService.trigger++;
        // console.log(dataService);
      })
    
      $scope.prevStart=$scope.start
      $scope.prevEnd=$scope.end;
    }

  }

});




app.controller('geoCtrl', function($scope,$http,config,geoService,dataService){
  
    // var mapFile="../data/"+safename+"/"+safename+"_usermap.json";
  
    // $scope.sort=["gdp","population","meme"]
    $scope.centroidsOnMap=true;
    $scope.memeName=config.name

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
    $scope.$watch(function() { return dataService.trigger }, function(newVal,oldVal){
      if(newVal!=oldVal && newVal!=0) $scope.geoEdges=dataService.geo;
    })


    $scope.saveGeo=function(){
      var sv=new Simg($(".geo-container svg")[0]);
      sv.download();
    }

})

app.controller('wordCtrl', function($scope,$http,config,dataService){

  $scope.wordForceStarted=true;
  $scope.memeName=config.name

  $scope.$watch(function() { return dataService.trigger }, function(newVal,oldVal){
    if(newVal!=oldVal && newVal!=0) {
      $scope.words=dataService.words;
      if(dataService.words.index!=undefined) $scope.wordsLength=dataService.words.index.length;
      $scope.wordProvinces=dataService.wordsProvince;
    }

  })

  $scope.saveWords=function(){
    var sv=new Simg($(".word-container svg")[0]);
    sv.download();
  }

})

app.controller('userCtrl', function($scope,$http,config,dataService){

  $scope.userForceStarted=true;
  $scope.memeName=config.name

  $scope.$watch(function() { return dataService.trigger }, function(newVal,oldVal){
    if(newVal!=oldVal && newVal!=0) {
      $scope.users=dataService.users;
      if(dataService.users.index!=undefined) $scope.usersLength=dataService.users.index.length;      
    }

  })


  $scope.saveUsers=function(){
    var sv=new Simg($(".user-container svg")[0]);
    sv.download();
  }

})