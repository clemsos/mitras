var wordForce,
    arcs,
    wordForce,
    wordsToUsers,
    wordPath,
    words,
    communities,
    map,
    nodeCentroids,
    mapToUsers;

function drawD3Layers(graphFile,mapFile) {

    var vizWidth=1000;
    var vizHeight=1000;

    var viz = d3.select("#viz").append("svg")
            .attr("width", vizWidth)
            .attr("height", vizHeight)
            .attr("preserveAspectRatio", "xMidYMid")
            .attr("viewBox", "0 0 " + vizWidth + " " + vizHeight);
    
// LOAD DATA /////////////////////////////////////////////////////////////
    queue()
        .defer(d3.json, "maps/zh-mainland-provinces.topo.json") // mainland
        .defer(d3.json, "maps/zh-chn-twn.topo.json") // taiwan 
        .defer(d3.json, "maps/zh-hkg-mac.topo.json") // hk and macau
        .defer(d3.json, mapFile)
        .defer(d3.json, graphFile)
        .await(draw); // function that uses files

// PARSE DATA /////////////////////////////////////////////////////////////
    function draw(error,mainland,taiwan,hkmacau,mapData,graphData) {

        // USER  communities
        var userNodes=graphData.users.nodes;
        var userEdges=graphData.users.edges;
        var userCommunities = [];

        var usersX={}
        var communitiesX={}
        var communitiesY=518;

        // parse nodes
        var myUserNodes = {};
        var myUserCommunities = {};
        for (var i = 0; i < userNodes.length; i++) {
             
            myUserNodes[userNodes[i]["name"]] =userNodes[i]
            
            if(myUserCommunities[userNodes[i]["community"]] == undefined) myUserCommunities[userNodes[i]["community"]]=[]
            myUserCommunities[userNodes[i]["community"]].push(userNodes[i])        

        };

        for (var c in myUserCommunities){
            userCommunities.push( { "id": c, "users": myUserCommunities[c], "children" :null } );
        }

        // Compute the distinct nodes from the links.
        userEdges.forEach(function(link) {            
            link.source = myUserNodes[link.source] || 
                (nodes[link.source] = {name: link.source});
            link.target = myUserNodes[link.target] || 
                (myUserNodes[link.target] = {name: link.target});
            link.value = +link.weight;
        });

        // WORD nodes
        var wordNodes=graphData.words.nodes;
        var myWordNodes={},
            wordsX={},
            wordsY={};

        for (var i = 0; i < wordNodes.length; i++) {
            myWordNodes[wordNodes[i]["name"]] =wordNodes[i]
        };

        // Compute edges for words force
        var wordEdges=graphData.words.edges;
        wordEdges.forEach(function(link) {            
            link.source = myWordNodes[link.source] || 
                (myWordNodes[link.source] = {name: link.source});
            link.target = myWordNodes[link.target] || 
                (myWordNodes[link.target] = {name: link.target});
            link.value = +link.weight;
        });

        // calculate communities coordinates
        var xprev=0,rprev=0;
        for (var i = 0; i < userCommunities.length; i++) {
            var r=userCommunities[i].users.length,
                x=xprev+r*2+rprev-2,
                y=399;

            communitiesX[userCommunities[i].id]=x;
            xprev=x;
            rprev=r;
        };

        // WORD2USERS
        var wordsUsersPath=graphData.words_user;    
        var wordsToCommunities=[]
        var tmp={};

        // clean data to match communities instead of users
        wordsUsersPath.forEach(function(word){
            var p=word.source+"_"+word.community; 
            if (!tmp[p]) tmp[p]=0;
            tmp[p]+=word.weight;
        })
        

        for(var word in  tmp) {
            var data= word.split("_")
            if( !isNaN(communitiesX[data[1]]) ) wordsToCommunities.push({"source": data[0], "target" : data[1], "weight": tmp[word]})
        }

        wordsToCommunities.forEach(function(link) {            
            link.source = myWordNodes[link.source] || 
                (myWordNodes[link.source] = {name: link.source});
            link.target = myWordNodes[link.target] || 
                (myWordNodes[link.target] = {name: link.target});
            link.value = +link.weight;
        });

        // MAP : parse data properly
        var colorScale, color;
        var umap=[];

        // sort provinces 
        mapData.provinces.map(function(d) { umap[d.name]=d.count });
        delete(umap[null]); // remove useless elements
        delete(umap[0]);

        var v = Object.keys(umap).map(function(k){return umap[k]})

        var mapY=communitiesY+30;

        var projection = d3.geo.mercator()
            .center([116,39])
            .scale(600);

        var mapPath = d3.geo.path()
            .projection(projection);

        // CENTROIDS
        // Get provinces centroids
        var mapCentroids=[];
        var mapFeatures= [topojson.feature(mainland, mainland.objects.provinces).features,topojson.feature(taiwan, taiwan.objects.layer1).features.filter(function(d) { return d.properties.GU_A3 === 'TWN'; }),topojson.feature(hkmacau, hkmacau.objects.layer1).features]
        
        for (var i = 0; i < mapFeatures.length; i++) {
            mapFeatures[i].forEach(function(d, i) {

                // if (d.id === 2 || d.id === 15 || d.id === 72) return; // lower 48
                var centroid = mapPath.centroid(d);
                if (centroid.some(isNaN)) return;
                centroid.x = centroid[0];
                centroid.y = centroid[1];
                centroid.cx = centroid[0];
                centroid.cy = centroid[1];
                centroid.feature = d;
                if (d.properties.name != undefined) centroid.name=d.properties.name
                else if (d.properties.name==undefined && d.properties.NAME=="Taiwan") centroid.name='Taiwan';
                else if (d.properties.name==undefined && d.properties.NAME=="Macao") centroid.name='Aomen';
                else centroid.name='Xianggang';

                centroid.type="province";
                // centroid.color="#ccc";    
                mapCentroids.push(centroid);
            });
        };

        var centroids={}
        for (var i = 0; i < mapCentroids.length; i++) {
            var c=mapCentroids[i];
            centroids[c.name]=c;
        };

        // GEO COMMUNITIES        
        var mapUsersEdges=[];
        var tmpUE={}

        for (var i = 0; i < userNodes.length; i++) {
            var o=userNodes[i];
            if( o.province!="0" && o.province != "Qita" && o.province != "Haiwai") {
                if(tmpUE[o.community+"_"+o.province] == undefined ) tmpUE[o.community+"_"+o.province]=0;
                tmpUE[o.community+"_"+o.province]+=1;
            }
        };

        for (a in tmpUE) {
            var data=a.split("_");
            mapUsersEdges.push({
                    "source" : data[0],
                    "target" : data[1],
                    "weight" : tmpUE[a] })
        }


// SVG SETUP //////////////////////////////////////////////////////////

    arcs=viz.append("g").attr("class","arcs")
        .selectAll('.arc')
        .data(userEdges.filter(function (d) { return true })) // if conditionfilter
        .enter()
        .append('g')
        .attr('class', 'arc')

    var maxRadius=100,
        charge=-500,
        gravity=.5,
        linkDistance=102;

    wordForce= d3.layout.force()
        .nodes(wordNodes)
        .links(wordEdges)
        .size([vizHeight,vizWidth/3])
        .linkDistance(linkDistance)
        .charge(charge)
        .gravity(gravity)
        .on("tick", wordTick);
        // .start();

    wordsToUsers = viz.append("g")
        .attr("class", "wordusers")
        .selectAll("path")
        .data(wordsToCommunities)
        .enter()
        .append("line")
        .attr("class", "word-link")

    // Word Graph links 
    wordPath = viz.append("g")
       .attr("class", "wordgraph")
       .selectAll("path")
        .data(wordForce.links())
      .enter() //.append("svg:path")
        .append("line")
        .attr("class", "word-link")
        .style("stroke", function(d) { return "red" })
        .style("stroke-opacity", function(d) { return 0.3 })
        .style("stroke-width", function(d) {  return 1 });

    words = viz.append("g")
        .attr("class", "words")
        .selectAll("path")
        .data(wordNodes)
        .enter()
        .append("g")
        .attr("class", "word")
        .call(wordForce.drag);

    map = viz.append("g")
        .attr("class", "map")
        .attr("transform", function(d) { return "translate(0,"+ mapY +")";})

    // Draw centroids
    nodeCentroids = viz.append("g")
        .attr("class", "mapCentroids")
        .selectAll(".centroids")
            .data(mapCentroids)
      .enter().append("g")
        .attr("class", "centroid")

    mapToUsers = viz.append("g")
        .attr("class", "mapusers")
        .selectAll("path")
        .data(mapUsersEdges)
        .enter()
        .append("line")
        .attr("class", "map-user")

    communities = viz.append("g").attr("class","communities")
        .selectAll('.community')
        .data(userCommunities.filter(function (d) { return true })) // if conditionfilter


// DRAW FUNCTIONS ///////////////////////////////////////////////////////

    function drawCentroids() {
        // console.log(centroids, mapCentroids);
        nodeCentroids.each(function (d, i) {
            var self=d3.select(this);

            var y=mapY+d.cy,
                x=d.cx; 


            self.append("circle")
                .attr("r", 2)
                .style("fill", function(d) {return "green"})

            self.append("text")
                .attr("dx", 2)
                .attr("dy", "0.35em")
                .style("fill", "#aaa" )
                .style("fill-opacity", "0.8" )
                .text(d.name)

            self.attr("transform", function(d) { return "translate(" + x + "," + y + ")"; })
        })
    }

    function drawMapToUsers() {

        mapToUsers.each(function (d, i) {
            
            var self=d3.select(this);
            
            var x1=communitiesX[d.source],
                y1=communitiesY,
                x2=centroids[d.target].x,
                y2=mapY+centroids[d.target].y;

            // console.log(!isNaN(x1),!isNaN(y1),!isNaN(x2),!isNaN(y2));

            if(!isNaN(x1) && !isNaN(y1) && !isNaN(x2) && !isNaN(y2)) {
                self.attr("x1", x1)
                    .attr("y1", y1)
                    .attr("x2", x2)
                    .attr("y2", y2)
                    .style("stroke", function(d) { return "green" })
                    .style("stroke-opacity", function(d) { return 0.1 })
                    .style("stroke-width", function(d) {  return d.weight });
            }
            /*
            */

        })
    }

    function wordTick(e) {

        wordPath.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });        

        words.attr("transform", function(d) { 
            wordsX[d.name]=d.x;
            wordsY[d.name]=d.y;
            return "translate(" + d.x + "," + d.y + ")"; 
        });

        // drawWords()
        drawWordsToUsers()
    } 

    function drawWords() {
        
        var wordColor = d3.scale.category20b();
        var wordScaleSize=d3.scale.linear().domain([100, 3000]).range([65, maxRadius]);
        var wordScaleFont=d3.scale.linear().domain([100, 3000]).range([15, 80]);

        words.each(function (d, i) {

            var self = d3.select(this);

            self.append("rect")
                .attr("width", function(d) { return wordScaleSize(d.count) })
                .attr("height", function(d) { return 20 })
                .style("fill", function(d) {  return "transparent"; })
                .style("stroke", function(d) { return "transparent" })
                ;

            self.append("text")
                .attr("dx", 12)
                .attr("dy", 15)
                .style("font-size", function(d) { return wordScaleFont(d.count) })//scale_size(d.btw_cent) })
                .style("fill", function(d) {  return wordColor(d.count) })
                .attr("text-anchor", "middle") // text-align: right
                .text(function(d) { return d.name });

            var x=i*20;
            var y=80;
            self.attr("transform", function(d) { return "translate(" + x + "," + y + ")"; });

            wordsX[d.name]=x;
            wordsY[d.name]=y;

        })
    }

    function drawWordsToUsers() {

        wordsToUsers.each(function (d, i) {
            
            var self=d3.select(this);
            // console.log(d,self);

            var x1=wordsX[d.source.name],
                y1=wordsY[d.source.name],
                x2=communitiesX[d.target.name],
                y2=communitiesY;
            // console.log(x1,y1,x2,y2);

            if(!isNaN(x1) && !isNaN(y1) && !isNaN(x2) && !isNaN(y2)) {
                self.attr("x1", x1)
                    .attr("y1", y1)
                    .attr("x2", x2)
                    .attr("y2", y2)
                    .style("stroke", function(d) { return "#CCC" })
                    .style("stroke-opacity", function(d) { return 0.3 })
                    .style("stroke-width", function(d) {  return d.weight*0.1 });
            }
            /*
            */

        })
    }

    function drawUserArcs() {

        var userPathColor = d3.scale.category20b();
            
        arcs.each(function (d, i) {
            
                var self = d3.select(this);

                var startx=communitiesX[d.source.community],
                    starty=communitiesY,
                    endx=communitiesX[d.target.community],
                    endy=communitiesY;

                // console.log(d.source.community,d.target.community,startx,endx)
                var r = (endx - startx) * 0.51;
                var ry = Math.min(r, 490);

                if (!isNaN(startx) && !isNaN(endx) && !isNaN(r) && !isNaN(ry)) {
                    var path = 'M ' + startx + ','+starty+' A ' + r + ',' + ry + ' 0 0,1 ' + endx + ','+endy ;
                    self.append('path')
                        .attr('d', path)
                        .style("fill","transparent")
                        .style('opacity', .5)
                        .style('stroke', function (start, end) { return  userPathColor(d.weight);}(startx, endx));
                }
            })
            .on('mouseover', function (d) {
                var self = d3.select(this);
                self.select("path")
                    .style("stroke","#000")
                    .style("opacity","1");
            })
            .on('mouseout', function (d) {
                var self = d3.select(this);
                self.select("path")
                    .style("stroke",function(d) { return  userPathColor(d.weight);})
                    .style("opacity",".5");
            })
    }

    function drawCommunity() {

        var userColor = d3.scale.category20b();

        communities.enter()
            .append("g")
            .attr("class","community")
            .each(function (d, i) {
                var self = d3.select(this);
                var r=d.users.length,
                    x=communitiesX[d.id],
                    y=communitiesY;

                self.append("circle")
                    .attr("class",function(d) { return "community_"+d.id; })
                    .attr("r",r)
                    // .attr("x",x)
                    // .attr("y",y)
                    .style("fill", function(d) { return (!d.children)? userColor(d.id) : "#000"; })
                    .attr("transform", function(d) { 
                        return "translate(" + x + "," + y + ")"; });

                // Draw users
                if(d.children) {
                    var childrenNodes=[]
                    d.children.forEach( function(node) {

                        // draw users

                        //     x=self.attr("x")+10;
                        //     y=self.attr("y")+10;

                        //     console.log(self,d,x,y);

                        //     self.append("circle")
                        //         .attr("class",function(d) { return "community_"+d.id; })
                        //         .attr("r",3)
                        //         .style("fill", function(d) { return userColor(d.id);})
                        //         .attr("transform", function(d) { 
                        //             return "translate(" + x + "," + y + ")"; });
                    })
                }

            }).on('click', function (d) {
                toggleChildren(d)
                drawCommunity()
            })
    }

    // Mainland provinces
    function drawMainland(error, cn) {
        
        // var codes=[];
        // for (var i = 0; i < topojson.feature(cn, cn.objects.provinces).features.length; i++) {
        //     codes.push(topojson.feature(cn, cn.objects.provinces).features[i].properties.name)
        //     console.log(topojson.feature(cn, cn.objects.provinces).features[i])
            
        // };
        // console.log(codes);

        map.append("g")
            .attr("class", "mainland")
            .selectAll("path")
            .data(topojson.feature(cn, cn.objects.provinces).features)
            .enter()
            .append("g")
            .attr("class", "province")
            .append("path")
            .attr("d", mapPath)
            .attr("id", function(d) { return d.id; })
            .attr("class", "province")
            .attr("fill", "#cccccc")
            .attr("fill", function(d) { return color(umap[d.properties.name]); })
            .attr("stroke", "black")
            .attr("stroke-width", "0.35");

            // .text(function(d) {return "hha"});
    }

    // Taiwan
    function drawTaiwan(error, cn) {
        // console.log(error)
        // console.log(topojson.feature(cn, cn.objects.layer1))

        // Taiwan
        map.append('g')
            .attr("class", "taiwan")
            .selectAll("path")
            .data(topojson.feature(cn, cn.objects.layer1).features.filter(function(d) { return d.properties.GU_A3 === 'TWN'; }))
            .enter()
            .append("path")
            .attr("d", mapPath)
            .attr("id", function(d) { return d.id; })
            .attr("class", "province")
            .attr("fill", "#cccccc")
            .attr("fill", function(d) { return color(umap["Taiwan"]); })
            .attr("stroke", "black")
            .attr("stroke-width", "0.35");
    }

    // HK and Macau
    function drawHkMacau(error, cn) {
        // console.log(error)
        
        // console.log(topojson.feature(cn, cn.objects.layer1).features.filter(function(d) { return d.properties.GU_A3 === "HKG" }))

        var projection2 = d3.geo.mercator()
        .center([126,17])
        .scale(2000);

        var path2 = d3.geo.path()
            .projection(projection2);
      
        map.select('.map')
            .append("g")
            .attr("class", "hk")
            .attr("transform", "translate(50,"+(map_height-120)+")")
            .selectAll("path")
            .data(topojson.feature(cn, cn.objects.layer1).features)
            .enter()
            .append("path")
            .attr("d", path2)
            .attr("id", function(d) { return d.id; })
            .attr("class", "province")
            .attr("fill", function(d) { return color(umap["Xianggang"]); })
            .attr("stroke", "black")
            .attr("stroke-width", "0.35");

        map_svg.select(".hk")
            .append("text") //add some text
            .attr("dx", function(d){return 20})
            .attr("dy", function(d){return 35})
            .attr("font-family", "sans-serif")
            .attr("fill", "#aaaaaa")
            .attr("font-size", 10)
            .text("Hong Kong & Macau")

        // add demarcation
        map_svg.select(".hk")
           .append("svg:line")
             .attr("x1", 30)
             .attr("y1", -10)
             .attr("x2", 150)
             .attr("y2", 20)
             .style("stroke", "#cccccc")
             .style("stroke-width", 3);
        
        map_svg.select(".hk")
            .append("svg:line")
             .attr("x1", 150)
             .attr("y1", 20)
             .attr("x2", 150)
             .attr("y2", 60)
             .style("stroke", "#cccccc")
             .style("stroke-width", 3);
    }

    function drawMap() {
        colorScale= d3.scale.linear()
                   .domain(d3.extent(v))
                   .interpolate(d3.interpolateHcl)
                   .range(["white","red"]);

        // add grey color if no values
        color = function(i){ 
            if (i==undefined) {return "#cccccc"}
            else return colorScale(i)
        }

        drawMainland(error,mainland);
        drawTaiwan(error,taiwan);
        // drawHkMacau(error,hkmacau);
    }

// INIT /////////////////////////////////////////////////////////
    
    drawUserArcs()
    drawWords()
    drawWordsToUsers()
    drawCommunity()
    wordForce.start()
    drawMap()

    drawMapToUsers()
    drawCentroids()

// UTILS //////////////////////////////////////////////////////////

        // Toggle children.
    function toggleChildren(d) {
      if (d.children) {
        d.children = null;
      } else {
        d.children = d.users;
      }
    }

    /*
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
    */
    }

// UTILS //////////////////////////////////////////////////////////

}

// BUTTONS //////////////////////////////////////////////////////////

// arcs
// wordForce
// wordsToUsers
// wordPath
// words
// communities
// map
// nodeCentroids
// mapToUsers

$(".btn-arcs").click(function(e){
    console.log(arcs);
    $(".arcs").toggle()
})
$(".btn-communities").click(function(e){
    console.log(communities);
    $(".communities").toggle()
})
$(".btn-map").click(function(e){
    $(".map").toggle()
})
$(".btn-centroids").click(function(e){
    $(".mapCentroids").toggle()
})
$(".btn-words").click(function(e){
    console.log(words);
    $(".words").toggle()
})

var wfStarted=true;
$(".btn-wordforce").click(function(e){
    if(wfStarted) {
        wordForce.stop();
        wfStarted=false;
    } else {
        wordForce.start();
        wfStarted=true;
    }
    
    $(".btn-wordforce").html( (wfStarted) ?  "Stop Words" : "Start Words");
})

$(".btn-mapusers").click(function(e){
    // console.log(mapToUsers);
    $(".mapusers").toggle()

})
$(".btn-wordusers").click(function(e){
    console.log(wordsToUsers);
    $(".wordusers").toggle()
})

$(".btn-wordgraph").click(function(e){
    $(".wordgraph").toggle()

})

/*
function toggleGraph() {
    $(".graph").toggle()
    console.log(wordForce);
    wordForce.stop()
}

    function toggleUsers() {
        $(".users").toggle()
    }

    function toggleMap() {
        $(".map").toggle()
    }

    function toggleMapCentroids() {
        $(".mapCentroids").toggle()
    }

    function toggleUserMaps() {
        $(".users-map").toggle()
    }

    function toggleWordsPath() {
        $(".word-paths").toggle()
    }

    function toggleWords() {
        $(".words").toggle()
    }
*/