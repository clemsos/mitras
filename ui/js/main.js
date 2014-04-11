var memes_list="data/2012_sina-weibo-memes_list.csv",
      memes={},
      loadmeme,
      showInfo,
      safename="biaoge";

$(document).ready(function() {

  // DATA : load the list of memes from csv
  $.get(memes_list, function(memes_list_data) {                  
      var memesdata=$.csv.toObjects(memes_list_data);
      console.log(memes)
      
      // memes=memes_list_data.data;
      memesdata.forEach(function(meme) {
        add_meme(meme);
        memes[meme.safename]=meme;
      })
      // console.log(current_meme)
      loadmeme("biaoge")
  });

  // parse data and add menu item
  function add_meme(meme) {

    // skip memes 
    if(meme.safename == "diaosi" || meme.safename == "diaosi" || meme.safename == "tuhao")return

    // console.log(meme.safename);
    var li='<li><a class="meme" onClick="loadmeme('+"'"+meme.safename+"'"+')" href="#'+meme.safename+'">'+meme.safename+'</a></li>';
    // console.log(li)
    
    $(".memelist").append(li);

    meme.graphFile="data/"+meme.safename+"/"+meme.safename+"_d3graph.json";
    meme.mapFile="data/"+meme.safename+"/"+meme.safename+"_usermap.json";
    meme.timeFile="data/"+meme.safename+"/"+meme.safename+"_time_series.json";
    meme.wordsFile="data/"+meme.safename+"/"+meme.safename+"_words.json";  
  }

  loadmeme=function load_meme(meme_name) {

    reset_display()

    console.log("meme_name:"+meme_name);
    var meme = memes[meme_name];
    console.log(meme);

    // console.log(meme);
    var title= meme.safename+' <small>'+meme.name+'<small>'
    $("h1.page-header").html(title);

    // var baidu
    var text={};
    // text.name="<p>Name : "+meme.name+"</p>";
    // text.safename="<p>"++"</p>"
    text.keywords="<p>Keywords : "+meme.keywords+"</p>";
    text.start="<p> Date start :"+meme.start+"</p>";
    // text.type="<p>Type :"+meme.type+"</p>";
    // text.link2="<p><a href='"+meme.link2+" '>Read More</a></p>";
    text.links="<p>Links : <a href='"+meme.wikipedia+" '>Wikipedia</a>, <a href='"+meme.baidu+" '>Baidu</a>, <a href='"+meme.link1+" '>Read More</a></p>";
    text.dataset="<p>Dataset : xxx tweets"

    for (var i = 0; i < Object.keys(text).length; i++) {
      $("#info").append(text[Object.keys(text)[i]]);
      console.log();
    };

    // console.log((meme.graphFile,meme.mapFile))
    drawD3Layers(meme.graphFile,meme.mapFile);
    drawD3Time(meme.timeFile);
    drawD3Map(meme.mapFile)

    // drawD3Words(meme.wordsFile);
  }

  function reset_display() {
      $("#info").html("");
      $("#words").html("");
      $("#urls").html("");
      $("#hashtags").html("");
      $("#timeserie").html("");
      $("#map").html("");
      $("#viz").html("");
    }
  
  showInfo = function showInfo(info) {
    
    if(! typeof(a)=="object") throw "Info should be an object"
    $(".infobox").html("")
    if(info==null) return

    console.log(info);
    var d=info.data;
    var infodiv="<div>";
    if(info.type == "community") {
      
      var ul="<ul>";
      ul+="<li><strong>Number of users :</strong>"+d.users.length+"</li>";

      // var provinces_count={};
      // for (var i = 0; i < d.users.length; i++) {
      //   var num=d.users[i].province;
      //   provinces_count[num] = provinces_count[num] ? provinces_count[num]+1 : 1;
      // };
      
      // console.log(provinces_count);
      // var myData=[];
      // for( key in provinces_count )  myData.push({"label":key,"value":provinces_count[key]});
      // drawPie(".chart", myData);

      ul+="<ul>";
      infodiv+=ul;
    }

    infodiv+="</div>";
    console.log(infodiv)
    $(".infobox").html(infodiv)

  }
  // parse URL
  // var url=getLocation(document.URL)
  // var current_meme=url.hash
  // console.log(current_meme)
  // console.log(url.pathname.split('#')+url.hash)
});

// function getLocation(href) {
//   var match = href.match(/^(https?\:)\/\/(([^:\/?#]*)(?:\:([0-9]+))?)(\/[^?#]*)(\?[^#]*|)(#.*|)$/);
//   return match && {
//       protocol: match[1],
//       host: match[2],
//       hostname: match[3],
//       port: match[4],
//       pathname: match[5],
//       search: match[6],
//       hash: match[7]
//   }
// }
/*
function drawPie(self, data) {

  data.forEach(function(d) {
    d.value = +d.value;
  });
  console.log(data)

  var width = 200,
    height = 200,
    radius = Math.min(width, height) / 2;

  var color = d3.scale.category20c();

  var arc = d3.svg.arc()
      .outerRadius(radius - 10)
      .innerRadius(0);

  var pie = d3.layout.pie()
      .sort(null)
      .value(function(d) { console.log(d);return d.value; });

  var svg = d3.select(self)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var g = svg.selectAll(".pie")
      .data(pie(data))
    .enter().append("g")
      .attr("class", "pie");

  g.append("path")
      .attr("d", arc)
      .attr("data-legend", function(d){return d.data.label})
      .style("fill", function(d) { return color(d.data.label); });

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
      .call(d3.legend)
}*/