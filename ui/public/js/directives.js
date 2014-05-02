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
            
            // console.log("timeline binded");

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

                    // console.log('draw timeline');

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
                    mapY=100,
                    map_width=800,
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

                var mapLegend=geo.append("g").attr("class","map-legend")
                                .attr("transform", "translate("+(100)+","+(map_height-200)+")");
                                // console.log($scope);
                    
                $scope.$watch('memeName', function(newVal, oldVal) {
                    console.log(newVal);
                    if(newVal!=undefined) {                           
                        mapLegend.append("text")
                            .attr("dx",1)
                            .attr("dy",12)
                            .text("Users interactions by provinces for '"+newVal+"'")
                            .style("fill","#404040")
                            .style("margin-left",5)
                            .style("font-size",10)
                            .call(wrap, 135);
                    }

                    
                })

                function wrap(text, width) {
                        text.each(function() {
                            var text = d3.select(this),
                                words = text.text().split(/\s+/).reverse(),
                                word,
                                line = [],
                                lineNumber = 0,
                                lineHeight = 0.7, // ems
                                y = text.attr("y"),
                                dy = parseFloat(text.attr("dy")),
                                tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy );
                            while (word = words.pop()) {
                              line.push(word);
                              tspan.text(line.join(" "));
                              if (tspan.node().getComputedTextLength() > width) {
                                line.pop();
                                tspan.text(line.join(" "));
                                line = [word];
                                tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy ).text(word);
                              }
                            }
                        });
                }

                // projection for HK / Macau
                var projection2 = d3.geo.mercator()
                    .center([126,17])
                    .scale(2000);

                var path2 = d3.geo.path()
                    .projection(projection2);

                var map=geo.append("g").attr("class", "map")
                            .style("fill",'#fff')
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

            var geoDefs=geo.append("defs").attr("class","geo-arrows")

            var geoStrokeColor="#428bca"

            $scope.$watch('geoEdges', function(newVal, oldVal) {

                if(newVal==undefined || newVal==[] && $scope.centroidsXY==undefined) return

                var geoPaths=geoEdges.selectAll(".geoPath")
                    .data(newVal)

                var geoMarkers=geoDefs.selectAll("marker")
                   .data(["medium"])

                geoMarkers.enter()
                    .append("marker")
                    .attr("id", String)
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", 20)
                    .attr("refY", -1.5)
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .attr("orient", "auto")
                    .append("svg:path")
                    .attr("d", "M0,-5L10,0L0,5");

                geoPaths.enter() 
                    .append("line")
                    .attr("class", "geoPath")
                    .style("stroke", function(d) { return geoStrokeColor })
                    .style("stroke-opacity", function(d) { return 0.3 })
                    .attr("marker-mid", "url(#end)")                
                
                if($scope.centroidsXY!=undefined) {
                    geoPaths.attr("x1", function(d) { return $scope.centroidsXY[d.source].x; })
                            .attr("y1", function(d) { return $scope.centroidsXY[d.source].y; })
                            .attr("x2", function(d) { return $scope.centroidsXY[d.target].x; })
                            .attr("y2", function(d) { return $scope.centroidsXY[d.target].y; })

                }

                if($scope.ratio!=undefined) {
                    
                    // poids de l'échange pondéré par la population totale de Weibo
                    var geoExt=newVal.map(function(d){
                            return (d.weight*$scope.ratio[d.source])/100;
                        }),
                        geoPathStrokeWidth=d3.scale.linear().domain(d3.extent(geoExt)).range([1, 10]),
                        legendExt=d3.scale.linear().domain([0,4]).range(d3.extent(geoExt));
                    

                    geoPaths.style("stroke-width", function(d) {  
                        return geoPathStrokeWidth(d.weight *($scope.ratio[d.source]/100));
                    });

                    //legend

                    
                    d3.select(".legend-rates").remove()

                    var mapRates=mapLegend.append("g")
                            .attr("class","legend-rates")

                    mapRates.append("text")
                        .attr("transform","translate(0,30)")
                        .attr("dx",1)
                        .attr("dy",10)
                        .text("User interactions rates (%) (weighted by population by province)")
                        .style("fill","#aaa")
                        .style("margin-left",5)
                        .style("font-size",10)
                        .call(wrap, 150);

                    for (var i = 0; i < 4; i++) {
                        var strokeWidth=geoPathStrokeWidth(legendExt(i)),
                            y=80+i*12+strokeWidth,
                            percent=Math.round(legendExt(i)/d3.sum(geoExt)*100);

                        mapRate=mapRates.append("g")

                        mapRate.append("text")
                            .attr("dx",1)
                            .attr("dy",y+3)
                            .text( percent+"%" )
                            .style("fill","#aaa")
                            .style("margin-left",5)
                            .style("font-size",9);

                        mapRate.append("line")
                                 .attr("x1", 30)
                                 .attr("y1", y)
                                 .attr("x2", 60)
                                 .attr("y2", y)
                                 .style("stroke", geoStrokeColor)
                                 .style("stroke-width", strokeWidth);

                    }
                    
                }

                geoPaths.exit().remove();
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

                tickCentroids()
            }

            function tickCentroids () {

                 $scope.nodeCentroids
                    .each(function (d, i) {
                        
                        var x=($scope.centroidsOnMap)? d.x :d.fixx;
                        var y=($scope.centroidsOnMap)? d.y :d.fixy;

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
            
            //SVG Setup
            var w=900,
                h=500;

            var viz=d3.select(element[0]).append("svg")
                .attr("class","svg-viz")
                .attr("width", w)
                .attr("height", h)
                .attr("preserveAspectRatio", "xMidYMid")
                .attr("viewBox", "0 0 " + w + " " + h);

            var divWords=viz.append("g").attr("class","wordzone")

            var wordEdges = divWords.append("g")
                        .attr("class", "wordgraph")

            var words = divWords.append("g")
                        .attr("class", "words")

            var wordsLegend=divWords.append("g")
                        .attr("class", "words-legend")
                        .attr("transform", "translate("+(100)+","+(h-200)+")");
                    
            $scope.$watch('memeName', function(newVal, oldVal) {
                // console.log(newVal);
                if(newVal!=undefined) {                           
                    wordsLegend.append("text")
                        .attr("dx",1)
                        .attr("dy",12)
                        .text("Words correlation for '"+newVal+"'")
                        .style("fill","#404040")
                        .style("margin-left",5)
                        .style("font-size",10)
                        .call(wrap, 135);

                    wordsLegend.append("text")
                        .attr("transform","translate(0,30)")
                        .attr("dx",1)
                        .attr("dy",10)
                        .text("Weighted co-occurences in tweets for 500 most used words")
                        .style("fill","#aaa")
                        .style("margin-left",5)
                        .style("font-size",10)
                        .call(wrap, 150);
                }
            });



            function wrap(text, width) {
                text.each(function() {
                    var text = d3.select(this),
                        words = text.text().split(/\s+/).reverse(),
                        word,
                        line = [],
                        lineNumber = 0,
                        lineHeight = 0.7, // ems
                        y = text.attr("y"),
                        dy = parseFloat(text.attr("dy")),
                        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy );
                    while (word = words.pop()) {
                      line.push(word);
                      tspan.text(line.join(" "));
                      if (tspan.node().getComputedTextLength() > width) {
                        line.pop();
                        tspan.text(line.join(" "));
                        line = [word];
                        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy ).text(word);
                      }
                    }
                });
            }
            
            // data 
            $scope.$watch("wordsLength", function(newVal,oldVal){

                if(newVal==undefined) return
                var wordsData=$scope.words;

                d3.selectAll(".word-link").remove();
                d3.selectAll(".word").remove();

                var wordsX={},
                    wordsY={};

                updateWordXY= function updateWordXY() {

                    var margin=30,
                        rgx=d3.scale.linear().domain([0,wordNodes.length]).range([margin,w-margin-200]),
                        s=d3.shuffle(wordNodes),
                        rgy=d3.scale.linear().domain(fontScale).range([margin,h-150]);

                    for (var i = 0; i < wordNodes.length; i++) {
                        var d=s[i];
                        wordsX[d.name]=rgx(i);
                        wordsY[d.name]=rgy(wordScaleFont(d.count));
                    };
                }

                // parse data properly                     
                var myWordNodes={},
                    myWordEdges={};

                for (var i = 0; i < wordsData.nodes.length; i++) {
                    myWordNodes[wordsData.nodes[i]["name"]]=wordsData.nodes[i];
                    wordsData.nodes[i].children=[];
                    wordsData.nodes[i].selected=false;
                };

                wordsData.edges.forEach(function(link) {
                    // console.log(link.weight);
                     myWordNodes[link.source].children.push(myWordNodes[link.target]);
                     myWordNodes[link.target].children.push(myWordNodes[link.source]);

                    link.source = myWordNodes[link.source] || 
                        (myWordNodes[link.source] = {name: link.source});
                    link.target = myWordNodes[link.target] || 
                        (myWordNodes[link.target] = {name: link.target});
                    link.value = link.weight;
                });


                var wordForce=d3.layout.force()
                        .nodes(wordsData.nodes)
                        .links(wordsData.edges)
                        .size([w,h])
                        .linkDistance(150)
                        .charge(-1000)
                        .gravity(.4)
                        .on("tick", tickWord);

                var wordPath=wordEdges.selectAll(".word-link")
                        .data(wordForce.links())
                
                wordPath.enter()
                    .append("line")
                    .attr("class", "word-link")

                var wordNodes=words.selectAll(".word")
                        .data(wordForce.nodes())

                wordNodes.enter()
                    .append("g")
                    .attr("class", "word")
                    
                if($scope.wordForceStarted) {
                    wordForce.start();
                    wordNodes.call(wordForce.drag);
                }

                drawWords();

                // scales
                var fontScale=[15,60],
                    wordScale=wordsData.nodes.map(function(d){return d.count}),
                    maxMinWordScale=[Math.min.apply(Math,wordScale), Math.max.apply(Math,wordScale)],
                    wordScaleFont=d3.scale.linear().domain(maxMinWordScale).range(fontScale),
                    userPathColor=d3.scale.category20b(),
                    mapColor;
                
                $scope.selection=false;

                function drawWords() {

                    var ext=wordsData.nodes.map(function(d){ return d.children.length }), 
                        wordScaleSize=d3.scale.linear().domain(d3.extent(ext)).range([15, 35]),
                        wordScaleOpacity=d3.scale.linear().domain(d3.extent(ext)).range([.5,1]),
                        wordColor = d3.scale.linear().domain(d3.extent(ext)).range(["#a1d99b","#006d2c"]);

                    wordNodes.each(function (d, i) {

                        var self = d3.select(this);
                    
                        self.append("rect")
                            .attr("width", function(d) { return wordScaleSize(d.children.length) })
                            .attr("height", function(d) { return 20 })
                            .style("fill", function(d) {  return "transparent"; })
                            .style("stroke", function(d) { return "transparent" });

                        self.append("text")
                            .attr("dx", 12)
                            .attr("dy", 8)
                            .style("font-size", function(d) { return wordScaleSize(d.children.length) })//scale_size(d.btw_cent) })
                            .style("fill", function(d) {  return "#006d2c" })
                            // .style("fill-opacity", function(d) {  return "#006d2c" })
                            // .style("fill-opacity", function(d) {  return wordScaleOpacity(d.count) })
                            .attr("text-anchor", "middle") // text-align: right
                            .text(function(d) { return d.name });

                        var x=i*20;
                        var y=80;

                        wordsX[d.name]=x;
                        wordsY[d.name]=y;
                    }).on("mouseover",function(d,i){
                        
                        $scope.selection=true;
                        d.selected=true;
                        d.children.forEach(function(e){
                            e.selected=true;
                        })
                        
                        drawWordPie(d3.select(".wordpie-container"),$scope.wordProvinces[d.name])

                    }).on("mouseout",function(d,i){
                        $scope.selection=false;
                        d.selected=false;
                        d.children.forEach(function(e){
                            e.selected=false;
                        })
                        d3.select(".wordpie-chart").remove()

                    });

                    drawWordPath();
                }

                function drawWordPie(element, data) {

                  d3.select(".wordpie-chart").remove()
                  data.map(function(d){
                    if(d.label != 0) return d
                  })

                  var width = 200,
                    height = 200,
                    radius = Math.min(width, height) / 2;

                  var arc = d3.svg.arc()
                      .outerRadius(radius - 10)
                      .innerRadius(0);

                  var pie = d3.layout.pie()
                      .sort(null)
                      .value(function(d) { return d.value; });

                  var svg = element
                      .append("svg")
                      .attr("class","wordpie-chart")
                      .attr("width", 200)
                      .attr("height", 200)
                      .append("g")
                      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

                  var g = svg.selectAll(".arc")
                      .data(pie(data))
                    .enter().append("g")
                      .attr("class", "arc");

                  g.append("path")
                      .attr("d", arc)
                      .attr("data-legend", function(d){ return d.data.label })
                      .style("fill", function(d) { return d.data.color; });

                  g.append("text")
                      .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
                      .attr("dy", ".25em")
                      .style("fill","#000")
                      .style("fill-opacity","0.8")
                      .style("text-anchor", "middle")
                      .text(function(d) { return d.data.label; });

                  svg.append("g")
                      .attr("class", "legend")
                      .attr("transform", "translate(50,30)")
                      .style("font-size", "12px")
                      // .call(d3.legend)
                }

                function drawWordPath() {

                    var wordPathExt=wordsData.edges.map(function(d){ return d.weight }),
                        wordPathWeight=d3.scale.linear().domain(d3.extent(wordPathExt)).range([1, 4]),
                        wordPathOpacity=d3.scale.linear().domain(d3.extent(wordPathExt)).range([.1, 1]);
                    
                    wordPath.each(function (d, i) {
                        var self = d3.select(this);
                        
                        self.style("stroke", function(d) { return "#de2d26" })
                            .style("stroke-width", function(d) {  return wordPathWeight(d.weight) })
                            .style("stroke-opacity", function(d) {  return wordPathOpacity(d.weight) });
                    })
                }

                var ext=wordsData.nodes.map(function(d){ return d.children.length }), 
                    wordScaleOpacity=d3.scale.linear().domain(d3.extent(ext)).range([.5,1]);

                function tickWord() {

                    // remove transition for force
                    var ww = ($scope.wordForceStarted)? wordNodes : wordNodes.transition();

                    ww.attr("transform", function(d) { 
                    
                        var r=wordScaleFont(d.children.length),
                            x=(d.x==undefined || !$scope.wordForceStarted)? wordsX[d.name] : Math.max(r, Math.min(w - r, d.x)),
                            y=(d.y==undefined || !$scope.wordForceStarted)? wordsY[d.name] : Math.max(r, Math.min(h - r, d.y));

                        wordsX[d.name]=x;
                        wordsY[d.name]=y;

                        return "translate(" + x + "," + y + ")"; 

                    }).attr("fill-opacity",function(d){
                        if($scope.selection) {
                            if(!d.selected) return 0;
                            else return wordScaleOpacity(d.children.length);
                        } else return wordScaleOpacity(d.children.length);
                    });

                    tickWordPath();
                }

                function tickWordPath() {
                    var wordPathExt=wordsData.edges.map(function(d){ return d.weight }),
                        wordPathWeight=d3.scale.linear().domain(d3.extent(wordPathExt)).range([1, 4]),
                        wordPathOpacity=d3.scale.linear().domain(d3.extent(wordPathExt)).range([.1, 1]);

                    wordPath.each(function (d, i) {
                        var self=d3.select(this);

                        self.style("stroke-opacity", function(d) { 
                             if($scope.selection) {
                                if( d.target.selected && d.source.selected) return wordPathOpacity(d.weight)
                                else return 0;
                            } else return wordPathOpacity(d.weight);

                        })
                        
                        var w=wordForce.size()[0],
                            h=wordForce.size()[1],
                            r1=wordScaleFont(d.source.count),
                            x1=Math.max(r1, Math.min(w, d.source.x));
                            y1=Math.max(r1, Math.min(h, d.source.y)),
                            r2=wordScaleFont(d.target.count),
                            x2=Math.max(r2, Math.min(w, d.target.x)),
                            y2=Math.max(r2, Math.min(h, d.target.y));

                        if(!isNaN(x1) && !isNaN(y1) && !isNaN(x2) && !isNaN(y2)) {
                            self.attr("x1", x1)
                                .attr("y1", y1)
                                .attr("x2", x2)
                                .attr("y2", y2)
                        }
                    })       
                }

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
            
            var svg_w=d3.select(element[0]).style('width'),
                h=500,
                w=600;
            
            var sw=1,
                sh=1,
                sx=0,
                sy=0;

            var viz=d3.select(element[0]).append("svg")
                .attr("class","svg-viz")
                .attr("width", svg_w)
                .attr("height", h)
                .attr("preserveAspectRatio", "xMidYMid")
                .attr("viewBox", "0 0 "+ w + " " + h)
                

            var divUsers=viz.append("g").attr("class","userzone")
                    .attr("transform","scale("+sh+","+sw+") translate("+sx+","+sy+")")


            var userEdges = divUsers.append("g")
                        .attr("class", "usergraph")

            var users = divUsers.append("g")
                        .attr("class", "users")

            var usersLegend=divUsers.append("g")
                        .attr("class", "users-legend")
                        .attr("transform", "translate("+(100)+","+(h-50)+")");
                    
            $scope.$watch('memeName', function(newVal, oldVal) {
                console.log(newVal);
                if(newVal!=undefined) {                           
                    usersLegend.append("text")
                        .attr("dx",1)
                        .attr("dy",12)
                        .text("Conversational graph for '"+newVal+"'")
                        .style("fill","#404040")
                        .style("margin-left",5)
                        .style("font-size",10)
                        .call(wrap, 135);

                    usersLegend.append("text")
                        .attr("transform","translate(0,30)")
                        .attr("dx",1)
                        .attr("dy",10)
                        .text("Users interactions (@,RT)")
                        .style("fill","#aaa")
                        .style("margin-left",5)
                        .style("font-size",10)
                        .call(wrap, 150);
                }
            });



            function wrap(text, width) {
                text.each(function() {
                    var text = d3.select(this),
                        words = text.text().split(/\s+/).reverse(),
                        word,
                        line = [],
                        lineNumber = 0,
                        lineHeight = 0.7, // ems
                        y = text.attr("y"),
                        dy = parseFloat(text.attr("dy")),
                        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy );
                    while (word = words.pop()) {
                      line.push(word);
                      tspan.text(line.join(" "));
                      if (tspan.node().getComputedTextLength() > width) {
                        line.pop();
                        tspan.text(line.join(" "));
                        line = [word];
                        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy ).text(word);
                      }
                    }
                });
            }


            var userColor=d3.scale.category20b();
            $scope.$watch("usersLength", function(newVal,oldVal){
                if(newVal==undefined) return
                // console.log(newVal);
                var userData=$scope.users;

                // parse data properly                     
                var myUsersNodes={}
                var color = d3.scale.category20c();

                for (var i = 0; i < userData.nodes.length; i++) {
                    myUsersNodes[userData.nodes[i]["name"]]=userData.nodes[i];
                    userData.nodes[i].children=[];
                    userData.nodes[i].selected=false;
                };

                userData.edges.forEach(function(link) {

                     myUsersNodes[link.source].children.push(myUsersNodes[link.target]);
                     myUsersNodes[link.target].children.push(myUsersNodes[link.source]);

                    link.source = myUsersNodes[link.source] || 
                        (myUsersNodes[link.source] = {name: link.source});
                    link.target = myUsersNodes[link.target] || 
                        (myUsersNodes[link.target] = {name: link.target});
                    link.value = link.weight;
                });


                // TODO : move data logic to controllers
                var myCommunities={},
                    myProvinces={},
                    leaders={};

                var communities=userData.nodes.map(function(d){
                    if(myCommunities[d.community]== undefined) myCommunities[d.community]=[]
                        myCommunities[d.community].push(d);
                        return d.community
                })

                
                for (com in myCommunities) {
                    myCommunities[com].sort(function(a,b){ return b.count-a.count});
                    leaders[com]=myCommunities[com][0]; // keep only the biggest node
                    
                    // count by provinces
                    var pc=count(myCommunities[com].map(function(d){ return d.province }))
                    myProvinces[com]=[]
                    for (p in pc) { 
                        myProvinces[com].push({"label":p, "value":pc[p], "color": color(p)})
                    }
                }

                function count(arr){
                    var obj={}
                    for (var i = 0, j = arr.length; i < j; i++) {
                       if (obj[arr[i]]) {
                          obj[arr[i]]++;
                       }
                       else {
                          obj[arr[i]] = 1;
                       } 
                    }
                    return obj;
                }

                d3.selectAll(".user-link").remove();
                d3.selectAll(".user").remove();

                var userForce=d3.layout.force()
                        .nodes(userData.nodes)
                        .links(userData.edges)
                        .size([w,h])
                        // .linkDistance(50)
                        .charge(-100)
                        .gravity(.4)
                        .on("tick", tickUsers);

                var userPath=userEdges.selectAll(".user-link")
                        .data(userForce.links())
                
                userPath.enter()
                    .append("line")
                    .attr("class", "user-link")

                var userNodes=users.selectAll(".user")
                        .data(userForce.nodes())

                userNodes.enter()
                    .append("g")
                    .attr("class", "user")

                if($scope.userForceStarted) {
                    userForce.start();
                    // console.log(userNodes.call(""));
                    userNodes.call(userForce.drag);
                } 


                drawUsers();
                
                var padding = 5, // separation between same-color circles
                    clusterPadding = 36, // separation between different-color circles
                    maxRadius = 20;

                function drawUsers(){

                    var userExt=userData.nodes.map(function(d){ return d.children.length }),
                        legendExt=d3.scale.linear().domain([0,3]).range(d3.extent(userExt)),
                        userSize=d3.scale.linear().domain(d3.extent(userExt)).range([3,20]);

                    userNodes.each(function (d, i) {
                            
                            var self = d3.select(this);
                            
                            self.append("circle")
                            .attr("r",function(d){ 
                                d.radius=userSize(d.children.length);
                                return d.radius;
                            })
                            .style("fill", function(d){return userColor(d.community)})
                    }).on("mouseover",function(d,i){
                        // var self = d3.select(this);

                        $scope.selection=true;
                        d.selected=true;
                        d.children.forEach(function(e){
                            e.selected=true;
                        })
                        
                        drawUserPie(d3.select(".pie-container"),myProvinces[d.community])
                    }).on("mouseout",function(d,i){
                        $scope.selection=false;
                        d.selected=false;
                        d.children.forEach(function(e){
                            e.selected=false;
                        })
                        d3.select(".pie-chart").remove()
                    });
                    

                    // legend
                    d3.select(".legend-communities").remove()

                    var legendCommunities=usersLegend.append("g")
                        .attr("class","legend-communities")
                        .attr("transform","translate("+(w-100)+",0)")
                        .append("g")
                        .attr("class","legend-size")

                    
                    for (var i = 0; i < 3; i++) {
                        
                        var d=legendExt(i);

                        legendCommunities
                        .append("circle")
                        .attr("r",userSize(d) )
                        .attr("cy",userSize(d))
                        .attr("cx", 50)
                        .style("fill","transparent")
                        .style("stroke","#ccc")

                    legendCommunities
                        
                        .append("line")
                        .attr("x1", 50)
                        .attr("y1", userSize(d)*2)
                        .attr("x2", 100)
                        .attr("y2", userSize(d)*2)
                        .style("stroke","#ccc")
                        .style("stroke-width",.5);
                    
                    legendCommunities
                        
                        .append("text")
                        .attr("dx", 100)
                        .attr("dy", userSize(d)*2)
                        .style("font-size",9)
                        .style("fill","#aaa")

                        .text((Math.round(d)+1)+" interactions")
                    
                    }
                    drawUserPath()
                }

                function drawUserPath() {
                    
                    userPath.each(function (d, i) {
                        var self = d3.select(this);
                        self.style("stroke", function(d){return "#ccc"})
                            .style("stroke-width",2)
                    })
                }

                function tickUsers(e) {

                    var r=5,
                        w=userForce.size()[0],
                        h=userForce.size()[1];

                    userPath.each(function (d,i) {
                        var self=d3.select(this);

                        var x1=Math.max(r, Math.min(w - r, d.source.x)),
                            y1=Math.max(r, Math.min(h - r, d.source.y)),
                            x2=Math.max(r, Math.min(w - r, d.target.x)),
                            y2=Math.max(r, Math.min(h - r, d.target.y));

                        self.attr("stroke-opacity",function(e){
                            if($scope.selection) {
                                if(!d.selected) return 0;
                                else return 1;
                            } else return 1;
                        })

                        if(!isNaN(x1) && !isNaN(y1) && !isNaN(x2) && !isNaN(y2)) {
                            self.attr("x1", x1)
                                .attr("y1", y1)
                                .attr("x2", x2)
                                .attr("y2", y2)
                        }
                        
                    })
                        

                    userNodes
                        // .each(cluster(12 * e.alpha * e.alpha))
                        .each(collide(.5))
                        .attr("transform", function(d) { 
                            
                            var r=5,
                                w=userForce.size()[0],
                                h=userForce.size()[1],
                                x=Math.max(r, Math.min(w - r, d.x)),
                                y=Math.max(r, Math.min(h - r, d.y));
                                // x=d.x,
                                // y=d.y;

                            return "translate(" + x + "," + y + ")"; 
                        }).attr("fill-opacity",function(d){
                            if($scope.selection) {
                                if(!d.selected) return 0;
                                else return 1;
                            } else return 1;
                        });
                }

                // Move d to be adjacent to the cluster node.
                function cluster(alpha) {
                  return function(d) {
                    var cluster = leaders[d.community];
                    // console.log(cluster);
                    if (cluster === d) return;
                    var x = d.x - cluster.x,
                        y = d.y - cluster.y,
                        l = Math.sqrt(x * x + y * y),
                        r = d.radius + cluster.radius;
                    if (l != r) {
                      l = (l - r) / l * alpha;
                      d.x -= x *= l;
                      d.y -= y *= l;
                      cluster.x += x;
                      cluster.y += y;
                    }
                  };
                }

                // Resolves collisions between d and all other circles. 
                function collide(alpha) {
                  var quadtree = d3.geom.quadtree(userData.nodes);
                  return function(d) {
                    var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
                        nx1 = d.x - r,
                        nx2 = d.x + r,
                        ny1 = d.y - r,
                        ny2 = d.y + r;
                    quadtree.visit(function(quad, x1, y1, x2, y2) {
                      if (quad.point && (quad.point !== d)) {
                        var x = d.x - quad.point.x,
                            y = d.y - quad.point.y,
                            l = Math.sqrt(x * x + y * y),
                            r = d.radius + quad.point.radius + (d.cluster === quad.point.cluster ? padding : clusterPadding);
                        if (l < r) {
                          l = (l - r) / l * alpha;
                          d.x -= x *= l;
                          d.y -= y *= l;
                          quad.point.x += x;
                          quad.point.y += y;
                        }
                      }
                      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                    });
                  };
                }

                function drawUserPie(element, data) {

                  d3.select(".pie-chart").remove()

                  data.map(function(d){
                    if(d.label != 0) return d
                  })

                  var width = 200,
                    height = 200,
                    radius = Math.min(width, height) / 2;

                  var arc = d3.svg.arc()
                      .outerRadius(radius - 10)
                      .innerRadius(0);

                  var pie = d3.layout.pie()
                      .sort(null)
                      .value(function(d) { return d.value; });

                  var svg = element
                      .append("svg")
                      .attr("class","pie-chart")
                      .attr("width", 200)
                      .attr("height", 200)
                      .append("g")
                      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

                  var g = svg.selectAll(".arc")
                      .data(pie(data))
                    .enter().append("g")
                      .attr("class", "arc");

                  g.append("path")
                      .attr("d", arc)
                      .attr("data-legend", function(d){ return d.data.label })
                      .style("fill", function(d) { return d.data.color; });

                  g.append("text")
                      .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
                      .attr("dy", ".25em")
                      .style("fill","#000")
                      .style("fill-opacity","0.8")
                      .style("text-anchor", "middle")
                      .text(function(d) { return d.data.label; });

                  svg.append("g")
                      .attr("class", "legend")
                      .attr("transform", "translate(50,30)")
                      .style("font-size", "12px")
                      // .call(d3.legend)
                }

            })
        }
    }
})