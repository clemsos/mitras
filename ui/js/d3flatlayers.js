var wordForce,
    arcs,
    wordForce,
    wordsToUsers,
    wordPath,
    words,
    communities,
    map,
    nodeCentroids,
    mapToUsers,
    colorScale,
    markers;

// Layout
var wfStarted=false,
    centroidsOnMap=false,
    initViz;

// hide/show things
var displayWordForce=false,
    displayWordToUsers=true,
    displayMapToUsers=true;

var updateCommunityXY,
    communityLayout="XAxis", //default layout : "YAxis", "XAxis"
    tickCommunity,
    drawMapToUsers,
    updateWordXY,
    tickWords,
    drawCentroids;

var selectedCommunity=11 //null;

function drawD3Layers(graphFile,mapFile) {

    var vizWidth=860,
        vizHeight=700,
        vizMiddleY=500,
        mapY=200;

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

        // USER COMMUNITIES
        var userNodes=graphData.users.nodes;
        var userEdges=graphData.users.edges;
        var userCommunities = [];
        
        var usersX={}
        var communitiesX={}
        var communitiesY={}

        // Parse user nodes into Community
        var myUserNodes = {};
        var myUserCommunities = {};
        for (var i = 0; i < userNodes.length; i++) {
             
            myUserNodes[userNodes[i]["name"]] =userNodes[i]
            
            if(myUserCommunities[userNodes[i]["community"]] == undefined) myUserCommunities[userNodes[i]["community"]]=[]
            userNodes[i].btw_cent=Math.random()
            myUserCommunities[userNodes[i]["community"]].push(userNodes[i])        

        };

        // INIT COMMUNITIES NODES {Id, Users, Province}
        for (var c in myUserCommunities){
            var myUsers=myUserCommunities[c];
            var provinces_count={}
            for (var i = 0; i < myUsers.length; i++) {
                var num=myUsers[i].province;
                provinces_count[num] = provinces_count[num] ? provinces_count[num]+1 : 1;
            };
              
            // Create Provinces Data
            var userProvinces=[];
            for( key in provinces_count ) userProvinces.push({"label":key,"value":provinces_count[key]});
            
            userCommunities.push( 
                {   "id": c, 
                    "users": myUsers, 
                    "words":null, 
                    "children" : null, 
                    "provinces": userProvinces,
                    "btw_cent" : Math.random()
                }
                );
        }

        // ARCS (Links between communities)
        userEdges.forEach(function(link) {
            link.source = myUserNodes[link.source] || 
                (nodes[link.source] = {name: link.source});
            link.target = myUserNodes[link.target] || 
                (myUserNodes[link.target] = {name: link.target});
            link.value = +link.weight;            
        });

        // Create edges between communities
        var communitiesEdges = [],
            myCommunitiesEdges={};

        for (var i = 0; i < userEdges.length; i++) {
            var u1=userEdges[i].source, u2=userEdges[i].target;
            
            // skip users in the same community
            if(u1.community!=u2.community) {
                communitiesEdges.push(userEdges[i]);
                if(myCommunitiesEdges[u1.community]==undefined) myCommunitiesEdges[u1.community]=[]
                myCommunitiesEdges[u1.community].push({"name": u2.community, "direction" :"to", "weight": userEdges[i].weight})
                if(myCommunitiesEdges[u2.community]==undefined) myCommunitiesEdges[u2.community]=[]
                myCommunitiesEdges[u2.community].push({"name": u1.community, "direction" :"from", "weight": userEdges[i].weight})
            }
        }

        // WORD nodes
        var wordNodes=graphData.words.nodes;
        var myWordNodes={},
            wordsX={},
            wordsY={};

        for (var i = 0; i < wordNodes.length; i++) {
            myWordNodes[wordNodes[i]["name"]] =wordNodes[i];
            wordNodes[i].words=null;
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
        updateCommunityXY=function communityPos() {

            var xprev=0,yprev=0,rprev=0;
        
            for (var i = 0; i < userCommunities.length; i++) {
                var r,x,y;
                if(communityLayout=="YAxis") {

                    r=userCommunities[i].users.length,
                    x=vizWidth-50,
                    y=yprev+r*2+rprev-2;

                } else if (communityLayout=="XAxis") {

                    r=userCommunities[i].users.length,
                    x=xprev+r*2+rprev-2,
                    y=vizMiddleY;
                    // x=i*5*2,
                    // x=vizWidth-50,
                    // y=yprev+r*2+rprev-2;
                }

                communitiesX[userCommunities[i].id]=x;
                communitiesY[userCommunities[i].id]=y;
                xprev=x;
                yprev=y;
                rprev=r;
            }
        }

        updateCommunityXY()

        // WORD TO COMMUNITIES EDGES
        var wordsUsersPath=graphData.words_user;    
        var tmp={};
        wordsToCommunities=[];
        var communitiesToWords={};

        // clean data to match communities instead of users
        wordsUsersPath.forEach(function(word){
            var p=word.source+"_"+word.community; 
            if (!tmp[p]) tmp[p]=0;
            tmp[p]+=word.weight;
        })
        
        for(var word in  tmp) {
            var data= word.split("_")
            if( !isNaN(communitiesX[data[1]]) ) { 
                wordsToCommunities.push({"source": data[0], "target" : data[1], "weight": tmp[word]})
                
                // init word
                if(communitiesToWords[data[1]]== undefined) communitiesToWords[data[1]]=[]
                communitiesToWords[data[1]].push({"word": data[0], "weight": tmp[word]})
            }
        }
        
        wordsToCommunities.forEach(function(link) {            
            link.source = myWordNodes[link.source] || 
                (myWordNodes[link.source] = {name: link.source});
            link.target = myWordNodes[link.target] || 
                (myWordNodes[link.target] = {name: link.target});
            link.value = +link.weight;
        });

        updateWordXY= function updateWordXY() {
            // console.log("updateWordXY")
            var margin=50,
                rgx=d3.scale.linear().domain([0,wordNodes.length]).range([margin,vizWidth-margin]),
                s=d3.shuffle(wordNodes);
            // var rgy=d3.scale.linear().domain([0,wordNodes.length]).range([0,vizHeight])

            for (var i = 0; i < wordNodes.length; i++) {
                var d=s[i];

                // console.log(wordScaleFont(d.count))
                wordsX[d.name]=rgx(i);
                wordsY[d.name]=wordScaleFont(d.count)*8;

            };
            // console.log("wordsXY",wordsX,wordsY);
        }

        // COMMUNITIES NODES - PUSH DATA
        communitiesIndex={}

        userCommunities.forEach(function(community){
            
            community.words=communitiesToWords[community.id];

            if(myCommunitiesEdges[community.id]!=undefined)community.children=myCommunitiesEdges[community.id];

            communitiesIndex[community.id]=community;
        })
        // console.log(communitiesToWords);


        // MAP : parse data properly
        var umap=[];
        // sort provinces 
        mapData.provinces.map(function(d) { umap[d.name]=d.count });
        delete(umap[null]); // remove useless elements
        delete(umap[0]);

        var v = Object.keys(umap).map(function(k){return umap[k]})

        var projection = d3.geo.mercator()
            .center([116,39]) // china long lat 
            .scale(vizWidth/2);

        var mapPath = d3.geo.path()
            .projection(projection);

        // CENTROIDS
        // Get provinces centroids
        var mapCentroids=[];
        var mapFeatures= [topojson.feature(mainland, mainland.objects.provinces).features,topojson.feature(taiwan, taiwan.objects.layer1).features.filter(function(d) { return d.properties.GU_A3 === 'TWN'; }),topojson.feature(hkmacau, hkmacau.objects.layer1).features]
        
        var centroids={}

        function updateCentroidsXY() {
            
            // console.log("updateCentroidsXY")

            mapCentroids=[];
            centroids={};
            var cnt=0,
                margin=20,
                rgx=d3.scale.linear().domain([0,30]).range([margin,vizWidth-margin]);

            for (var i = 0; i < mapFeatures.length; i++) {
                mapFeatures[i].forEach(function(d, i) {
                    cnt++;

                    // if (d.id === 2 || d.id === 15 || d.id === 72) return; // lower 48
                    var centroid = mapPath.centroid(d);
                    if (centroid.some(isNaN)) return;

                    centroid.x = centroid[0];
                    centroid.y = centroid[1];
                    centroid.cx = centroid[0];
                    centroid.cy = centroid[1];
                    centroid.fixx = rgx(cnt); // fix display
                    centroid.fixy = vizHeight-50; // fix display

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
            
            for (var i = 0; i < mapCentroids.length; i++) {
                var c=mapCentroids[i];
                centroids[c.name]=c;
            };
            // console.log(centroids);
        }

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

    var maxRadius=100,
        charge=-1000,
        gravity=.4,
        linkDistance=150;

    function setupSVG() {

        arcs=viz.append("g").attr("class","arcs")
            .selectAll('.arc')
            .data(userEdges.filter(function (d) { 
                // console.log(d)
                if(selectedCommunity!=null) {
                    if(d.source.community == selectedCommunity) return true 
                    else if(d.target.community == selectedCommunity) return true 
                } else return true
            })) // if conditionfilter
            .enter()
            .append('g')
            .attr('class', 'arc')
            .attr("marker-end", "url(#end)")

        markers=viz.append("defs")
          .selectAll("marker")
            .data(["end"])
          .enter()
            .append("svg:marker")

        wordForce= d3.layout.force()
            .nodes(wordNodes.filter(function (d) {
                if(selectedCommunity!=null) {
                    var com=communitiesIndex[selectedCommunity];
                    for (var i = 0; i < com.words.length; i++) if(com.words[i].word == d.name) d.visible=true;
                } else return true

            }))
            .links(wordEdges.filter(function (d) { 
                if(selectedCommunity!=null) {
                    var com=communitiesIndex[selectedCommunity];
                    var sourceIn=false, targetIn=false;
                    for (var i = 0; i < com.words.length; i++) {
                        if(com.words[i].word==d.source.name) sourceIn=true;
                        if(com.words[i].word==d.target.name) targetIn=true;
                    }
                    if(sourceIn && targetIn)  return true// d.visible=false;                
                } else return true

            }))
            .size([vizWidth, vizMiddleY-30])
            .linkDistance(linkDistance)
            .charge(charge)
            .gravity(gravity)
            .on("tick", tickWord);
            // .start();

        wordsToUsers = viz.append("g")
            .attr("class", "wordusers")
            .selectAll("path")
            .data(wordsToCommunities.filter(function (d) { 
                if(selectedCommunity!=null) {
                    var com=communitiesIndex[selectedCommunity];
                    // console.log(d);
                    for (var i = 0; i < com.words.length; i++) {
                        if(com.id == d.target.name && com.words[i].word == d.source.name) return true 
                    };
                } else return true
            }))
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

        // console.log(wordNodes)
        words = viz.append("g")
            .attr("class", "words")
            .selectAll("path")
            .data(wordNodes.filter(function (d) { 
                if(selectedCommunity!=null) {
                    var com=communitiesIndex[selectedCommunity];
                    for (var i = 0; i < com.words.length; i++) {
                        if(com.words[i].word == d.name) return true 
                    };
            } else return true
            }))
            .enter()
            .append("g")
            .attr("class", "word")
            .call(wordForce.drag);

        map = viz.append("g")
            .attr("class", "map")
            .attr("transform", function(d) { return "translate(0,"+ mapY +")";})

        var usermap = d3.select().append("g")
            .attr("class", "usermap")
            .attr("transform", function(d) { return "translate(0,"+ mapY +")";})

        // Draw centroids
        nodeCentroids = viz.append("g")
            .attr("class", "centroids")
            .selectAll(".centroid")
                .data(mapCentroids.filter(function (d) { 
                    if(selectedCommunity!=null) {
                        // console.log(d)
                        var com=communitiesIndex[selectedCommunity];
                        for (var i = 0; i < com.provinces.length; i++) {
                            // if(com.provinces[i].label==d.name) console.log(d.name)
                            if(com.provinces[i].label==d.name) return true 
                        };
                } else return true
            }));

        mapToUsers = viz.append("g")
            .attr("class", "mapusers")
            .selectAll("path")
            .data(mapUsersEdges.filter(function (d) { 
                if(selectedCommunity!=null) {
                    var com=communitiesIndex[selectedCommunity];
                    for (var i = 0; i < com.provinces.length; i++) {
                        if(com.id==d.source && com.provinces[i].label==d.target) return true 
                    };
            } else return true
            }))
            .enter()
            .append("line")
            .attr("class", "map-user")

        communities = viz.append("g").attr("class","communities")
            .selectAll('.community')
            .data(userCommunities.filter(function (d) { 
                // console.log(d);
                    if(selectedCommunity!=null) {
                        
                        if(d.children) {
                            for (var i = 0; i < d.children.length; i++) {
                                if(d.children[i].name==selectedCommunity) return true 
                            };
                        }
                        if(d.id==selectedCommunity) return true 
                    } else return true
            }))
        
    }

    function drawLegend() {

        var legendWidth=250,
            legendHeight=50,
            legendMargin=3;

        var legend= d3.select(".legend").append("svg")
            .attr("width", legendWidth)
            .attr("height", legendHeight)
            // .attr("preserveAspectRatio", "xMidYMid")
            // .attr("viewBox", "0 0 " + vizWidth + " " + vizHeight);

        var communitiesLength=d3.extent(communities.data().map(function(d){ return d.users.length }))
        communitiesLength.push(Math.round((communitiesLength[0]+communitiesLength[1])/2))
        
        legendCommunities = legend.append("g")
            .attr("class","legend-communities")
            .selectAll("circle")
                .data(communitiesLength);

        // legendCommunities
        //     .append("text")
        //     .text("Communities")

        legendCommunities
            .enter()
            .append("circle")
            .attr("r", function(d,i){  return d })
            .attr("cy", function(d,i){ return legendMargin+d})
            .attr("cx", 50)
            .style("fill","transparent")
            .style("stroke","#ccc")

        legendCommunities
            .enter()
            .append("line")
            .attr("x1", 50)
            .attr("y1", function(d,i){ return legendMargin+d*2})
            .attr("x2", 100)
            .attr("y2", function(d,i){ return legendMargin+d*2})
            .style("stroke","#ccc")
            .style("stroke-width",.5);
        
        legendCommunities
            .enter()
            .append("text")
            .attr("dx", 100)
            .attr("dy", function(d,i){ return legendMargin+d*2})
            .style("font-size",9)
            .style("fill","#aaa")
            // .attr("transform",function(d){ "translate("+ d*2+",150)" })
            .text(function(d){ return d+" users" })

        legendBtwCent = legend
            .append("g")
            .attr("class","btw_centr")
            .attr("transform","translate(130,0)")
            .selectAll("rect")
                .data([1,2,3,4,5])
            .enter()

        legendBtwCent.append("rect")
            .attr("width",15)
            .attr("height",10)
            .attr("x",function(d){ return legendMargin+d*10})
            .attr("y",legendMargin+30)
            .style("fill", function(d){ return greens(d)})

        legendBtwCent.append("text")
            .text(function(d){return d/10})
            .attr("dx", function(d){ return legendMargin+7+d*10})
            .attr("dy", legendMargin+30)
            .style("fill","#aaa")
            .style("font-size",6)
            // .attr("transform","rotate(-30)")

        d3.select(".btw_centr")
            .append("text")
            .attr("dx",".35em")
            .attr("dy",10)
            .text("Betweeness Centrality")
            .style("fill","#aaa")
            .style("margin-left",5)
            .style("font-size",10)
            .call(wrap, 10);

    }



// DRAW FUNCTIONS ///////////////////////////////////////////////////////

    
    // colors
        var wordScaleFont=d3.scale.linear().domain([100, 3000]).range([15, 80]);
        var userPathColor = d3.scale.category20b();
        var provinceColor= d3.scale.category20b();
        var greens=d3.scale.quantize().domain([1,5]).range(colorbrewer.Greens[9]);
        
        // province color scale
        var pro={}, i=0, val=[];
        for(key in umap) { pro[key]=i; i++; val.push(umap[key])}
        
        // range of green with grey color if no values
        // var greens=d3.scale.quantize().domain(d3.extent(val)).range(colorbrewer.Greens[9]);
        // colorProvinces = function(key){ return (key==undefined)? "#cccccc" : greens(key) };
       
        var c=d3.scale.category20c();
        colorProvinces= function(key){ return c(pro[key])}

    // WORDS
    function drawWords() {
        
        var wordColor = d3.scale.category20b();
        var wordScaleSize=d3.scale.linear().domain([100, 3000]).range([65, maxRadius]);
        words.each(function (d, i) {

            var self = d3.select(this);
            
            var fontSize=0;
            if(selectedCommunity) {
                var com=communitiesIndex[selectedCommunity];
                for (var i = 0; i < com.words.length; i++) {
                    if(com.words[i].word == d.name) fontSize=com.words[i].weight*5;
                };
            } else fontSize=d.count;

            self.append("rect")
                .attr("width", function(d) { return wordScaleSize(d.count) })
                .attr("height", function(d) { return 20 })
                .style("fill", function(d) {  return "transparent"; })
                .style("stroke", function(d) { return "transparent" })
                ;

            self.append("text")
                .attr("dx", 12)
                .attr("dy", 8)
                .style("font-size", function(d) { return wordScaleFont(fontSize) })//scale_size(d.btw_cent) })
                .style("fill", function(d) {  return wordColor(d.count) })
                .attr("text-anchor", "middle") // text-align: right
                .text(function(d) { return d.name });

            var x=i*20;
            var y=80;

            wordsX[d.name]=x;
            wordsY[d.name]=y;
            // self.attr("transform", function(d) { return "translate(" + x + "," + y + ")"; });

        })
    }

    function tickWord() {
        
        // remove transition for force
        var ww = (wfStarted)? words : words.transition();

        ww.attr("transform", function(d) { 
            
            // console.log(d.count)
            var r=wordScaleFont(d.count),
                w=vizWidth,
                h=vizMiddleY-30,
                x=(d.x==undefined || !wfStarted)? wordsX[d.name] : Math.max(r, Math.min(w - r, d.x)),
                y=(d.y==undefined || !wfStarted)? wordsY[d.name] : Math.max(r, Math.min(h - r, d.y));

            // console.log(d.x,x,d.y,y,r,w,h);
            wordsX[d.name]=x;
            wordsY[d.name]=y;

            return "translate(" + x + "," + y + ")"; 

        });

        if(displayWordForce) tickWordPath();
        if(displayWordToUsers) drawWordsToUsers();
    }

    // CENTROIDS
    function drawCentroids() {

        nodeCentroids.enter()
          .append("g")
          .attr("class", "centroid")
          .each(function (d, i) {
            var self=d3.select(this);

            self.append("circle")
                .attr("r", 2)
                .style("fill", function(d) {return "green"});

            self.append("text")
                .attr("dx", 2)
                .attr("dy", "0.35em")
                .style("fill", "#aaa" )
                .style("fill-opacity", "0.8" )
                .text(d.name);

            if (!centroidsOnMap) 
                self.select("text")
                    .attr("transform", "rotate(60)")
                    .attr("dy","0.45em")

        })

        tickCentroids();
    }

    tickCentroids = function() {

        nodeCentroids.each(function (d, i) {

            var x=(centroidsOnMap)? d.x :d.fixx;
            var y=(centroidsOnMap)? mapY+d.y : d.fixy;

            var self=d3.select(this);
            self.transition().attr("transform", "translate(" + x + "," + y + ")")
        })
    }

    // COMMUNITY 
    function drawCommunity() {
        
        var scaleBtwCent=d3.scale.linear().domain([0,1]).range([1,5])

        communities.enter()
            .append("g")
            .attr("class","community")
            .each(function (d, i) {
                var self = d3.select(this);
                var r=d.users.length,
                    x=communitiesX[d.id],
                    y=communitiesY[d.id];

                var pie = d3.layout.pie()
                      .sort(null)
                      .value(function(d) { return d.value });

                // round to int and scale
                var mapBtw=d.users.map(function(d){ 
                    return Math.round(scaleBtwCent(d.btw_cent));
                });
                
                // count occurences
                var userBtw={}
                mapBtw.map(function(d){ 
                    if(userBtw[d]==undefined) userBtw[d]=0
                    userBtw[d]+=1
                })

                mapBtw=[] // init with rioght values
                for(u in userBtw) mapBtw.push({"label":u, "value":userBtw[u]})

                var g = self.append("g").attr("class","pie")
                    .selectAll(".piece")
                      // .data(pie(d.provinces))
                      .data(pie(mapBtw))
                    .enter().append("g")
                      .attr("class", "piece")
                      .attr("transform", function(d) { 
                        return "translate(" + x + "," + y + ")"; });

                var arc = d3.svg.arc()
                  .outerRadius(r*2 - 10)
                  .innerRadius(0);

                g.append("path")
                  .attr("d", arc)
                  .style("fill", function(d) { return greens(Number(d.data.label)); });


            }).on('click', function (d) {

                // toggleChildren(d);
                showInfo((d.children ==null)?{"type":"community","data":d}:null);
                // selectedCommunity=(selectedCommunity)? null:d.id
                selectedCommunity=d.id;
                initViz();
            })

            tickCommunity();
    }    

    // MAP TO USERS
    function tickMapToUsers() {
        mapToUsers.each(function (d, i) {
            
            var self=d3.select(this);

            var x1=communitiesX[d.source],
                y1=communitiesY[d.source],
                x2=(!centroidsOnMap)? centroids[d.target].fixx : centroids[d.target].x,
                y2=(!centroidsOnMap)? centroids[d.target].fixy : mapY+centroids[d.target].y;

            if(!isNaN(x1) && !isNaN(y1) && !isNaN(x2) && !isNaN(y2)) {
                self.transition()
                    .attr("x1", x1)
                    .attr("y1", y1)
                    .attr("x2", x2)
                    .attr("y2", y2)
                    .style("stroke", function(d) { return colorProvinces(d.weight) })
                    .style("stroke-opacity", function(d) { return 1 })
                    .style("stroke-width", function(d) {  return 1 });
            }
            
        })
    }

    // build the arrows
    function tickArrows() {
        markers
            .attr("id", String)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", -1.5)
            // .attr("markerWidth",50)
            // .attr("markerHeight",50)
            .attr("markergraph_Width", 10)
            .attr("markergraph_Height", 10)
            .attr("orient", "auto")
          .append("svg:path")
            .attr("d", "M0,-5L10,0L0,5");  
    }

    // WORDS FORCE
    function tickWordPath() {

        wordPath.each(function (d, i) {
            
            var self=d3.select(this);

            self.attr("x1", function(d){
                var r=wordScaleFont(d.source.count),
                    w=wordForce.size()[0],
                    x=Math.max(r, Math.min(w, d.source.x));
                    // console.log(x>w)
                    return d.source.x=x;
                })
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
                });
            });
    }

    // WORDS TO USERS
    function drawWordsToUsers() {

        if(displayWordToUsers){
            wordsToUsers.each(function (d, i) {                
                
                var self=d3.select(this);
                var x1=wordsX[d.source.name],
                    y1=wordsY[d.source.name],
                    x2=communitiesX[d.target.name],
                    y2=communitiesY[d.target.name];

                if(!isNaN(x1) && !isNaN(y1) && !isNaN(x2) && !isNaN(y2)) {
                    self.style("stroke", function(d) { return "#aaa" })
                        .style("stroke-opacity", function(d) { return (d.weight > 50)? d.weight*0.002:0 })
                        .style("stroke-width", function(d) {  return 2 })
                        .transition()
                        .attr("x1", x1)
                        .attr("y1", y1)
                        .attr("x2", x2)
                        .attr("y2", y2)
                }
            })
        }
    }

    // ARCS 
    function drawUserArcs() {
            
        arcs.each(function (d, i) {
            var self = d3.select(this);
            self.append("path")
        }).on('mouseover', function (d) {
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
        tickArcs()
    }

    function tickArcs() {
        arcs.each(function (d, i) {
            
                var self = d3.select(this);

                var startx=communitiesX[d.source.community],
                    starty=communitiesY[d.source.community],
                    endx=communitiesX[d.target.community],
                    endy=communitiesY[d.target.community];


                var path;
                var toItself=false;
                if(communityLayout=="XAxis") {
                    if(endx==startx) toItself=true;
                    var r = (endx - startx) * 0.51,
                        ry = Math.min(r, 490);
                    path = 'M ' + startx + ','+starty+' A ' + r + ',' + ry + ' 0 0,1 ' + endx + ','+endy ;

                } else if(communityLayout=="YAxis") {
                    // if(endy!=starty) console.log(Math.min(endy-starty*0.51, 490))
                    if(endx==startx) toItself=true;
                    var r = (endy - starty) * 0.51,
                        rx = Math.min(r,490);
                    path = 'M ' + startx + ','+starty+' A ' + r + ',' + rx + ' 0 0,1 ' + endx + ','+endy ;
                }

                if (path != undefined) {
                    self.select('path')
                        .transition()
                        .attr('d', path)
                        .style("fill","transparent")
                        .style('opacity', .5)
                        .style('stroke', function (start, end) { return  userPathColor(d.weight);}(startx, endx));
                }
            })
    }

    // API
    tickCommunity=function () {
        // var userColor = d3.scale.category20b();
        // console.log("tickCommunity");

        communities.each(function (d, i) {
                var self = d3.select(this);
                var r=d.users.length,
                    x=communitiesX[d.id],
                    y=communitiesY[d.id];

                self.select(".pie")
                    // .enter()
                    .selectAll(".piece")
                    .transition()
                    .attr("transform", function(d) {return "translate(" + x + "," + y + ")"; });
                    // .attr("r",r)
                    // .style("fill", function(d) { return (!d.children)? userColor(d.id) : "#000"; })
                    // .attr("r", 5)
                    // .style("fill", "#000")

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
            })
        tickArcs();
    }

    tickWords=function(){ 
        
        (wfStarted)? wordForce.start():wordForce.stop();
        if(!wfStarted) updateWordXY();
        // showWordPath=!wfStarted;
        tickWord();
    };

    // MAP
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
            // .attr("fill", function(d) { return colorProvinces(umap[d.properties.name]); })
            .attr("fill", function(d) { return colorProvinces(d.properties.name); })
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
            // .attr("fill", function(d) { return colorProvinces(umap["Taiwan"]); })
            .attr("fill", function(d) { return colorScale(umap["Taiwan"]); })
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

        drawMainland(error,mainland);
        drawTaiwan(error,taiwan);
        // drawHkMacau(error,hkmacau);
    }

// INIT /////////////////////////////////////////////////////////
      
    initViz=function initViz() {

        viz.selectAll("*").remove()

        updateCentroidsXY();
        updateWordXY(); // sort data

        setupSVG();
        
        drawWords();
        tickWords();
        
        drawCommunity();
        drawUserArcs();
        tickArrows();
        
        drawCentroids();
        tickMapToUsers();

        drawWordsToUsers()


        // drawMap()
        // drawMapToUsers()
    }

    initViz();
    drawLegend();

// UTILS //////////////////////////////////////////////////////////

    // Toggle children.
    function toggleChildren(d) {
      if (d.children) {
        d.children = null;
      } else {
        d.children = d.users;
      }
    }

    function toggleWords(d, words) {
      d.words=words;
    }


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

    }

}

// BUTTONS //////////////////////////////////////////////////////////


$(".btn-wordforce").click(function(e){
    
    wfStarted=(wfStarted)?false:true;
    tickWords();  
    $(".btn-wordforce").html( (wfStarted) ?  "Stop Words" : "Start Words");
})

$(".btn-centroids").click(function(e){
    
    centroidsOnMap=(centroidsOnMap)?false:true;
    tickCentroids(); 
    console.log(centroidsOnMap)
    // $(".btn-wordforce").html( (wfStarted) ?  "Show map" : "Show list");
})


$(".btn-userlayout").click(function(e){
    communityLayout=(communityLayout == "YAxis")? "XAxis":"YAxis";
    updateCommunityXY();
    tickCommunity();
    $(".btn-userlayout").html(communityLayout)
})

$(".btn-showall").click(function(e){
    selectedCommunity=null;
    initViz();
})

$(".switchs button").each(function(e){
    var n=$(this).attr("class").split(" ")[$(this).attr("class").split(" ").length-1].slice(4);
    // console.log($("."+n)).attr("class")
    $(this).addClass( ($("."+n).css('display') != 'none')? "active":"" );

    $(this).click(function(e){
        $("."+n).toggle()
        $(this).removeClass( ($("."+n).css('display') != 'none')? "":"active" );
        $(this).addClass( ($("."+n).css('display') != 'none')? "active":"" );
    })
})