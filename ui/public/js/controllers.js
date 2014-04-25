// controllers.js

var safename="biaoge";

app.controller('timeCtrl', function($scope,$http,config){

  var timeFile="../data/"+safename+"/"+safename+"_time_series.json";

  $http.get(timeFile).success(function(data) {
    
    // TIME
    $scope.timeSeriesData=data;

    // sort time frames
    $scope.timeSeriesData.sort(function(a,b){ return a.timestamp-b.timestamp})

    $scope.timeSeriesData.map(function(d){ d.timestamp=d.timestamp*1000});

    // init scope values
    $scope.timeMax=data.length;
    $scope.start=data[0].timestamp;
    $scope.end=data[data.length-1].timestamp;

    $scope.updateTimeData()

  });

  // // monitor time changes
  $scope.$watch('start', function(newStart, oldVal) {
    // console.log(updatedStart);
    if (newStart!=undefined) {
      $scope.start=newStart; 
      $scope.updateTimeData();
    }
  })

  $scope.$watch('end', function(newEnd, oldVal) {
    if (newEnd!=undefined) {
      $scope.end=newEnd; 
      $scope.updateTimeData();
    }
    // config.setEnd(new Date(newEnd))
    // console.log(config.toJSON());
  })

  $scope.updateTimeData=function () {
    $scope.timeSeriesData.forEach(function(d) {
        if(d.timestamp>$scope.start && d.timestamp<$scope.end) d.selected=true
        else d.selected=false
        d.date=new Date(d.timestamp);
    });
  }

});

app.controller('geoCtrl', function($scope,$http,config){
  
    var mapFile="../data/"+safename+"/"+safename+"_usermap.json";
  
    // $scope.sort=["gdp","population","meme"]
    $scope.centroidsOnMap=true;

    $http.get("../public/maps/zh-mainland-provinces.topo.json").success(function(data) { $scope.mainland=data; })
    
    $http.get("../public/maps/zh-chn-twn.topo.json").success(function(data) { $scope.taiwan=data; })

    $http.get("../public/maps/zh-hkg-mac.topo.json").success(function(data) { $scope.hkmacau=data; })
            
  $http.get(mapFile).success(function(data) {
    // console.log(data);
    $scope.geoData=data.provinces;
  })
})