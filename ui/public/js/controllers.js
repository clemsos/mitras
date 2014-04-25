// controllers.js

app.controller('timeCtrl', function($scope,$http,config){

  var safename="biaoge";
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

