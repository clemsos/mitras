// directives.js

app.directive('slider', function ($parse) {
    return {
      restrict: 'E',
      replace: true,
      template: '<input type="text" />',
      link: function ($scope, element, attrs) {

        $scope.$watch('timeMax', function(updatedTimeMax, oldVal) {
            
            if(updatedTimeMax != undefined) {
                
                var model = $parse(attrs.model);
                var slider = $(element[0]).slider({
                    "max": updatedTimeMax,
                    "value": [0,updatedTimeMax]
                });

                slider.on('slide', function(ev) {
                    model.assign($scope, ev.value);

                    $scope.start=$scope.timeSeriesData[ev.value[0]].timestamp;
                    $scope.end=$scope.timeSeriesData[ev.value[1]-1].timestamp;

                    $scope.$apply();

                });

            }
        })
      }
    }
});

app.directive('timeserie', function () {
    // var chart = d3.custom.timeSerie(),
    

    return {
        replace: false,
        scope: { 
            timeData: '=timeData',
            start: '=start',
            end: '=end'

         },
        link: function ($scope, element, attrs) {
            
            console.log("timeline binded");

            var margin = {top: 20, right: 20, bottom: 40, left: 40},
                        width = 900,
                        height = 200,
                        gap = 0,
                        ease = 'cubic-in-out',
                        bars;
            
            var duration = 500;

            var time_width = width - margin.left - margin.right,
                time_height = height - margin.top - margin.bottom;

            // Construct our SVG object.
            var svg = d3.select(element[0])
                .append("svg")
                .attr("width", time_width + margin.left + margin.right)
                .attr("height", time_height + margin.top + margin.bottom)
                    .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            $scope.$watch('timeData', function(updatedTimeData, oldVal) {

                // console.log($scope.start)
                if(updatedTimeData != undefined && $scope.start!= undefined && $scope.end!= undefined) {

                    console.log('draw timeline');

                    var _data=updatedTimeData;

                    // Scales.
                    var x = d3.time.scale().range([time_width/_data.length/2, time_width-time_width/_data.length/2]);
                    // var x = d3.scale.ordinal().rangeRoundBands([0, time_width], .05);
                    var y = d3.scale.linear().range([time_height, 0]);

                    // X-axis.
                    var xAxis = d3.svg.axis()
                        .scale(x)
                        .orient("bottom")
                        // .ticks(d3.time.month, 1)
                        .tickFormat(d3.time.format("%d %B"));

                    var yAxis = d3.svg.axis()
                        .scale(y)
                        .orient("left")
                        .ticks(10);

                    // Set scale domains. 
                    x.domain(d3.extent(_data, function(d) { return d.date; }));
                    y.domain([0, d3.max(_data, function(d) { return d.count; })]);

                    
                    
                    
                    svg.transition().duration(duration).attr({width: width, height: height})
                    
                    // Call x-axis. 
                    d3.select(".x.axis")
                        .transition()
                        .duration(duration)
                        .ease(ease)
                        .call(xAxis);
                    
                    // Draw bars. 
                    bars = svg.append("g")
                        .attr("class","timebar")
                        .selectAll(".timebar")
                        .data( _data, function(d) { return d.date; });

                    bars.transition()
                        .duration(duration)
                        .ease(ease)
                        .attr("x", function(d) { return x(d.date) - time_width/_data.length/2; })
                        .attr("width", time_width / _data.length)
                        .attr("y", function(d) { return y(d.count); })
                        .attr("height", function(d) { return time_height - y(d.count);});

                    bars.enter().append("rect")
                        .attr("class", "count")
                        .attr("width", time_width / _data.length)
                        .attr("x", function(d) { return x(d.date) - (time_width/_data.length)/2; })
                        .attr("y", time_height)
                        .attr("height", 0)
                        .style("fill", function(d){ return (d.selected)?"steelblue":"#CCC"})
                        .transition().duration(1000)
                        .attr("y", function(d) { return y(d.count); })
                        .attr("height", function(d) { return time_height - y(d.count);});

                    svg.append("g")
                        .attr("class", "x axis")
                        .attr("transform", "translate(0," + time_height + ")")
                        .call(xAxis)
                        .selectAll("text")
                            .attr("font-family", "sans-serif")
                            .attr("fill", "#4B4B4B")
                            .attr("font-size", 10)
                            .style("text-anchor", "end")
                            .attr("dx", "-.8em")
                            .attr("dy", ".15em")
                            .attr("transform", function(d) {
                                return "rotate(-65)" 
                                })
                            // .attr("transform", "rotate(-90)" );

                    svg.append("g")
                        .attr("class", "y axis")
                        .attr("transform", "translate(0,0)")
                        .call(yAxis)
                        .selectAll("text")
                            .attr("font-family", "sans-serif")
                            .attr("fill", "#4B4B4B")
                            .attr("font-size", 10)
                    
                    svg.select(".y")
                        .append("text") // caption
                            .attr("transform", "rotate(-90)")
                            .attr("y", 6)
                            .attr("dy", ".71em")
                            .style("text-anchor", "end")
                            .attr("text-anchor", "middle")  
                            .attr("font-family", "sans-serif")
                            .attr("fill", "#4B4B4B")
                            // .style("text-decoration", "bold")  
                            .attr("font-size", 10)
                            .text("Qty per day (tweets)")
                  
                    bars.exit().transition().style({opacity: 0}).remove();

                    duration = 500;

                    function updateChart() {
                        // console.log($scope);
                      bars.data($scope.timeData)
                        .style("fill", function(d){ 
                            return (d.selected)?"steelblue":"#CCC"})
                    }

                    $scope.$watch('start', function(newStart, oldVal) {
                        if (newStart!=undefined) updateChart();
                        
                    })
                    $scope.$watch('end', function(newEnd, oldVal) {
                        if (newEnd!=undefined) updateChart();
                        
                    })
                    
                }
            })
        }
    }
});

app.directive("map", function () {
    return {
        replace: false,
        controller: 'geoCtrl',
        scope: { 
         },
        link: function ($scope, element, attrs) {
            
            ////// SETUP
                var centroids,
                    mapFeatures,
                    centroidsSort="gdp";
                    map_width=800,
                    mapY=100,
                    map_height=600,
                    vizWidth=1000;

                var geo = d3.select(element[0]).append("svg")

                    .attr("width", map_width)
                    .attr("height", map_height)
                    .attr("preserveAspectRatio", "xMidYMid")
                    .attr("viewBox", "0 0 " + map_width + " " + map_height);

                var projection = d3.geo.mercator()
                    .center([116,39]) // china long lat 
                    .scale(vizWidth/2);

                var mapPath = d3.geo.path()
                    .projection(projection);


                // projection for HK / Macau
                var projection2 = d3.geo.mercator()
                    .center([126,17])
                    .scale(2000);

                var path2 = d3.geo.path()
                    .projection(projection2);

                var map=geo.append("g").attr("class", "map")
                        // .attr("transform","translate(30,0)") 
                
                $scope.centroids=[]

                var defaultFillColor="#eee",
                    defaultStrokeColor="#404040";

            $scope.$watch('mainland', function(newVal, oldVal) {
                if(newVal!=undefined) {
                    var features=topojson.feature(newVal, newVal.objects.provinces).features;
                    drawProvinces(features);    
                    parseCentroids(features);
                }
            })
            
            $scope.$watch('taiwan', function(newVal, oldVal) {
                if(newVal!=undefined) {
                    var features=topojson.feature(newVal, newVal.objects.layer1).features.filter(function(d) { return d.properties.GU_A3 === 'TWN'; })
                    parseCentroids(features)
                    drawTaiwan(features)
                }
            })

            $scope.$watch('hkmacau', function(newVal, oldVal) {
                if(newVal!=undefined) {
                    var features=topojson.feature(newVal, newVal.objects.layer1).features;
                    parseCentroids(features)
                    drawHkMacau(features)
                }
            })

            // draw edges
            var geoEdges= geo.append("g").attr("class","geo-path")

            $scope.$watch('geoEdges', function(newVal, oldVal) {

                if(newVal==[]) return
                console.log("geoEdges",newVal.length);

                var geoPaths=geoEdges.selectAll(".geoPath")
                    .data(newVal)
                  
                geoPaths.enter() 
                    .append("line")
                    .attr("class", "geoPath")
                        .attr("x1", function(d) { return $scope.centroidsXY[d.source].x; })
                        .attr("y1", function(d) { return $scope.centroidsXY[d.source].y; })
                        .attr("x2", function(d) { return $scope.centroidsXY[d.target].x; })
                        .attr("y2", function(d) { return $scope.centroidsXY[d.target].y; })
                    .style("stroke", function(d) { return "#428bca" })
                    .style("stroke-opacity", function(d) { return 0.3 })
                    .style("stroke-width", function(d) {  return d.weight });

                updateGeoEdges();
                geoPaths.exit().transition().style({opacity: 0}).remove();

                
                function updateGeoEdges() {
                    // console.log($scope.centroidsXY);
                    geoPaths.data(newVal)
                    // userMap.transition()
                    // .duration(500)
                    // .each("end", userMapTick);
                }

                
                
            })
          
            function parseCentroids (features) {
                var vizWidth=900,
                    cnt=0,
                    rgx=d3.scale.linear().domain([0,30]).range([100,vizWidth]);

                features.forEach(function(d, i) {

                    var centroid;
                    cnt=$scope.centroids.length;

                    if (d.properties.name==undefined && (d.properties.NAME=="Hong Kong" || d.properties.NAME=="Macao") ) {
                        centroid = path2.centroid(d);
                        centroid.x = centroid[0]+650;
                        centroid.y = centroid[1]+400;
                        centroid.cx = centroid[0]+650;
                        centroid.cy = centroid[1]+400;
                    } else {
                        centroid = mapPath.centroid(d);
                        centroid.x = centroid[0];
                        centroid.y = centroid[1];
                        centroid.cx = centroid[0];
                        centroid.cy = centroid[1];
                    }

                    // mapCentroids[i].absx= rgx(i)-rgx(i-1);
                    centroid.fixx = rgx(cnt); // fix display
                    centroid.fixy = mapY+100; // fix display

                    if (centroid.some(isNaN)) return;

                    centroid.feature = d;
                    if (d.properties.name != undefined) centroid.name=d.properties.name
                    else if (d.properties.name==undefined && d.properties.NAME=="Taiwan") centroid.name='Taiwan';
                    else if (d.properties.name==undefined && d.properties.NAME=="Macao") centroid.name='Aomen';
                    else centroid.name='Xianggang';

                    centroid.type="province";
                    // centroid.cleanName=provincesInfo[centroid.name].clean_name
                    // centroid.gdp=provincesInfo[centroid.name].gdp
                    // centroid.population=provincesInfo[centroid.name].population

                    $scope.centroids.push(centroid);
                    
                    if($scope.centroids.length==34) drawCentroids();
                });
            }

            // function sortCentroids () {
            // // sort according to selected value
            // if (centroidsSort=="gdp") mapCentroids.sort(function(a,b){ return b.gdp-a.gdp;})
            // else if (centroidsSort=="population") mapCentroids.sort(function(a,b){ return b.population-a.population;})
            // else if (centroidsSort == "meme") mapCentroids.sort(function(a,b){return umap[b.name]-umap[a.name] })
            // }
            
            // Mainland provinces
            function drawProvinces(features) {
                map.append("g")
                    .attr("class", "mainland")
                    .selectAll("path")
                    .data(features)
                    .enter()
                    .append("g")
                    .attr("class", "province")
                    .append("path")
                    .attr("d", mapPath)
                    // .attr("id", function(d) { return d.id; })
                    .attr("class", "province")
                    .attr("class", function(d){ return d.properties.name })
                    .attr("fill", defaultFillColor)
                    .attr("stroke", defaultStrokeColor)
                    .attr("stroke-width", "0.35")
                    .on("click",function(d){
                        
                        console.log(d);
                        // update users mentioned
                        // if(provinceToUsers[d.properties.name]!=undefined) updateSelection(provinceToUsers[d.properties.name]);

                        
                    });
            }

            // Taiwan
            function drawTaiwan(features) {

                map.append('g')
                    .attr("class", "taiwan province")
                    .selectAll("path")
                    .data(features)
                    .enter()
                    .append("path")
                    .attr("d", mapPath)
                    .attr("id", function(d) { return d.id; })
                    .attr("class", "province")
                    .attr("class", function(d){ return "Taiwan" })
                    .attr("fill", defaultFillColor)
                    // .attr("fill", function(d) { return mapColor(umap["Taiwan"]); })
                    .attr("stroke", defaultStrokeColor)
                    .attr("stroke-width", "0.35")
                    .on("click",function(d){
                        
                        console.log(d);
                        // update users mentioned
                        // if(provinceToUsers["Taiwan"]!=undefined) updateSelection(provinceToUsers["Taiwan"]);

                        
                    });
            }

            // HK and Macau
            function drawHkMacau(features) {
                // console.log(error)
                // console.log(topojson.feature(cn, cn.objects.layer1).features.filter(function(d) { return d.properties.GU_A3 === "HKG" }))
              
                geo.select('.map')
                    .append("g")
                    .attr("class", "hk")
                    .attr("transform", "translate("+650+","+400+")")
                    .selectAll("path")
                    .data(features)
                    .enter()
                    .append("path")
                    .attr("d", path2)
                    // .attr("id", function(d) { return d.id; })
                    .attr("class", "province")
                    .attr("class", "Xianggang")
                    .attr("fill", defaultFillColor)
                    // .attr("fill", function(d) { return mapColor(umap["Xianggang"]); })
                    .attr("stroke", defaultStrokeColor)
                    .attr("stroke-width", "0.35");

                geo.select(".hk")
                    .append("text") //add some text
                    .attr("dx", function(d){return 20})
                    .attr("dy", function(d){return 35})
                    .attr("font-family", "sans-serif")
                    .attr("fill", "#aaaaaa")
                    .attr("font-size", 10)
                    .text("Hong Kong & Macau");

                // add demarcation
                geo.select(".hk")
                   .append("svg:line")
                     .attr("x1", 130)
                     .attr("y1", 5)
                     .attr("x2", 0)
                     .attr("y2", 10)
                     .style("stroke", "#cccccc")
                     .style("stroke-width", 1);
                
                geo.select(".hk")
                    .append("svg:line")
                     .attr("x1", 0)
                     .attr("y1", 10)
                     .attr("x2", -10)
                     .attr("y2", 60)
                     .style("stroke", "#cccccc")
                     .style("stroke-width", 1);
            }

            function drawCentroids () {
                
                console.log('test');

                $scope.nodeCentroids=geo.append("g")
                    .attr("class", "centroids")
                    .selectAll(".centroid")
                        .data($scope.centroids)
                    .enter()
                    .append("g")
                    .attr("class", "centroid")
                    .on("click",function(d){
                        console.log(d);
                        if(provinceToUsers[d.name]!=undefined) updateSelection(provinceToUsers[d.name]);
                    })

                $scope.nodeCentroids
                        .data($scope.centroids)
                        .append("circle")
                        .attr("r", 2)
                        .style("fill", function(d) {return "green"})

                $scope.nodeCentroids.append("text")
                        .attr("dx", 2)
                        .attr("dy", "0.35em")
                        .style("fill", "#404040" )
                        .style("fill-opacity", "0.8" )
                        .style("font-size", 11 )
                        .text(function(d) {d.name})

                tickCentroids()
            }

            function tickCentroids () {

                $scope.centroidsXY={}
                $scope.nodeCentroids
                    .each(function (d, i) {
                        var x=($scope.centroidsOnMap)? d.x :d.fixx;
                        var y=($scope.centroidsOnMap)? d.y :d.fixy;

                        $scope.centroidsXY[d.name]={"x":x,"y":y};

                        // console.log(d);
                        var self=d3.select(this);
                        self.transition().attr("transform", "translate(" + x + "," + y + ")")

                        if (!$scope.centroidsOnMap) 
                            self.select("text")
                                .attr("transform", "rotate(60)")
                                .attr("dy","0.45em")
                        else
                            self.select("text")
                                .attr("transform", "rotate(0)")
                })
            }


    
        }
    }
});


app.directive("words", function () {
     return {
        replace: false,
        controller: 'wordCtrl',
        scope: { 
         },
        link: function ($scope, element, attrs) {
            
            var w=900,
                h=500;

            var viz=d3.select(element[0]).append("svg")
                .attr("class","svg-viz")
                .attr("width", w)
                .attr("height", h)
                .attr("preserveAspectRatio", "xMidYMid")
                .attr("viewBox", "0 0 " + w + " " + h);

            $scope.$watch("words", function(newVal,oldVal){

                if(newVal==undefined) return

                

                var wordsX={},
                    wordsY={};

                updateWordXY= function updateWordXY() {

                    var margin=30,
                        rgx=d3.scale.linear().domain([0,wordNodes.length]).range([margin,w-margin-200]),
                        s=d3.shuffle(wordNodes),
                        rgy=d3.scale.linear().domain(fontScale).range([margin,communityTopY-150]);

                    for (var i = 0; i < wordNodes.length; i++) {
                        var d=s[i];
                        wordsX[d.name]=rgx(i);
                        wordsY[d.name]=rgy(wordScaleFont(d.count));
                    };
                }

                //SVG Setup
                var divWords=viz.append("g").attr("class","wordzone")

                var wordForce=d3.layout.force()
                    .nodes(newVal.nodes)
                    .links(newVal.edges)
                    .size([w,h])
                    .linkDistance(150)
                    .charge(-1000)
                    .gravity(.4)
                    .on("tick", tickWord);

                
                
                var myWordNodes={}

                for (var i = 0; i < newVal.length; i++) {
                    myWordNodes[data.words[i]["name"]]=newVal[i];
                    newVal[i].words=null;
                };

                newVal.edges.forEach(function(link) {
                    // console.log(link.weight);
                    link.source = myWordNodes[link.source] || 
                        (myWordNodes[link.source] = {name: link.source});
                    link.target = myWordNodes[link.target] || 
                        (myWordNodes[link.target] = {name: link.target});
                    link.value = link.weight;
                });
                

                var wordPath = divWords.append("g")
                    .attr("class", "wordgraph")
                    .selectAll("path")
                        .data(newVal.edges)
                    .enter() //.append("svg:path")
                    .append("line")
                    .attr("class", "word-link")

                var words = divWords.append("g")
                    .attr("class", "words")
                    .selectAll("path")
                    .data(newVal.nodes)
                    .enter()
                    .append("g")
                    .attr("class", "word")
                    .call(wordForce.drag);

                
                // scales
                var fontScale=[15,60],
                    wordScale=newVal.nodes.map(function(d){return d.count}),
                    maxMinWordScale=[Math.min.apply(Math,wordScale), Math.max.apply(Math,wordScale)],
                    wordScaleFont=d3.scale.linear().domain(maxMinWordScale).range(fontScale),
                    userPathColor=d3.scale.category20b(),
                    mapColor;
                
                

                function drawWords() {

                    words.each(function (d, i) {

                        var self = d3.select(this);
                        
                        // var ext;
                        // if(selectedCommunity) ext=communitiesIndex[selectedCommunity].words.map(function(d) {return d.weight})
                        // else  
                        var ext=words.data().map(function(d){ return d.count })
                        // console.log(d3.extent(ext))
                        var wordScaleSize=d3.scale.linear().domain(d3.extent(ext)).range([15, 35]);
                        var wordScaleOpacity=d3.scale.linear().domain(d3.extent(ext)).range([.8,1]);
                        var wordColor = d3.scale.linear().domain(d3.extent(ext)).range(["#a1d99b","#006d2c"]);
                        self.append("rect")
                            .attr("width", function(d) { return wordScaleSize(d.count) })
                            .attr("height", function(d) { return 20 })
                            .style("fill", function(d) {  return "transparent"; })
                            .style("stroke", function(d) { return "transparent" });

                        self.append("text")
                            .attr("dx", 12)
                            .attr("dy", 8)
                            .style("font-size", function(d) { return wordScaleSize(d.count) })//scale_size(d.btw_cent) })
                            .style("fill", function(d) {  return wordColor(d.count) })
                            .style("fill-opacity", function(d) {  return wordScaleOpacity(d.count) })
                            .attr("text-anchor", "middle") // text-align: right
                            .text(function(d) { return d.name });

                        var x=i*20;
                        var y=80;

                        wordsX[d.name]=x;
                        wordsY[d.name]=y;
                        // self.attr("transform", function(d) { return "translate(" + x + "," + y + ")"; });

                    })
                }

                function drawWordPath() {
                    
                    // console.log(newVal.edges[0].source);

                    wordPath.each(function (d, i) {
                        var self = d3.select(this);
                        // console.log(d);
                        
                        self.style("stroke", function(d) { return "red" })
                            .style("stroke-width", function(d) {  return 1 });

                        if(!$scope.wordForceStarted) self.style("stroke-opacity", function(d) { return 0 })
                        else self.style("stroke-opacity", function(d) { return 0.3 })
                    })

                }

                
                

                function tickWord() {
                    // remove transition for force
                    var ww = ($scope.wordForceStarted)? words : words.transition();

                    ww.attr("transform", function(d) { 
                        
                        // console.log(w,h)
                        var r=wordScaleFont(d.count),
                            x=(d.x==undefined || !$scope.wordForceStarted)? wordsX[d.name] : Math.max(r, Math.min(w - r, d.x)),
                            y=(d.y==undefined || !$scope.wordForceStarted)? wordsY[d.name] : Math.max(r, Math.min(h - r, d.y));
                        // console.log(x,y);

                        // console.log(d.x,x,d.y,y,r,w,h);
                        wordsX[d.name]=x;
                        wordsY[d.name]=y;

                        return "translate(" + x + "," + y + ")"; 

                    });

                    // if(displayWordForce) 
                    tickWordPath();
                }

                function tickWordPath() {
                    // console.log(wordForce.links());
                    wordPath.each(function (d, i) {

                        var self=d3.select(this);

                        if(!$scope.wordForceStarted) self.style("stroke-opacity", function(d) { return 0 })
                        else self.style("stroke-opacity", function(d) { return 0.3 })

                        console.log(d.source);

                        
                        self.attr("fill", function(d){
                            console.log(d);
                            var r=wordScaleFont(d.source.count),
                                w=wordForce.size()[0],
                                x=Math.max(r, Math.min(w, d.source.x));
                                console.log(d.source.x)
                                return d.source.x=x;
                            })
                            /*
                            .attr("y1", function(d){
                                var r=wordScaleFont(d.source.count),
                                    h=wordForce.size()[1],
                                    y=Math.max(r, Math.min(h, d.source.y));
                                    // console.log(r,h)
                                    return d.source.y=y;
                                })
                            .attr("x2", function(d) { 
                                
                                var r=wordScaleFont(d.target.count),
                                    w=wordForce.size()[0],
                                    x=Math.max(r, Math.min(w, d.target.x));
                                    // console.log(x>w)
                                    return d.target.x=x;
                                     })
                            .attr("y2", function(d) { 
                                var r=wordScaleFont(d.target.count),
                                    h=wordForce.size()[1],
                                    y=Math.max(r, Math.min(h, d.target.y));
                                    // console.log(r,h)
                                    return d.target.y=y;
                            });*/

                        });
                }

                
                // tickWordPath();
                drawWords();

                wordForce.stop()
                wordForce.start()
                
                

            });
        }
    }
})


app.directive("users", function () {
     return {
        replace: false,
        controller: 'userCtrl',
        scope: { 
         },
        link: function ($scope, element, attrs) {
            
            var w=900,
                h=500;

            var viz=d3.select(element[0]).append("svg")
                .attr("class","svg-viz")
                .attr("width", w)
                .attr("height", h)
                .attr("preserveAspectRatio", "xMidYMid")
                .attr("viewBox", "0 0 " + w + " " + h);

            $scope.$watch("users", function(newVal,oldVal){

                if(newVal==undefined) return
                console.log(newVal);

            })
        }
    }
})