// config object

var Config = function() {

    var self = this;

     /*
      MODEL

      self.tstart      : Date
      self.tend        : Date
      self.provinces   : Array
      self.users       : Array
      self.words       : Array
      self.layout      : String

    */

    self.validLayout =  [
      "user", 
      "map",
      "geo"
    ];

    self.setName= function(name) {
      self.name=name;
    }

    self.setStart = function(start) {
      // if(!isValidDate(start)) throw new Error("Invalid datetime: " + start);
      self.start = start;
    }

    self.setEnd = function(end) {
      // if(!isValidDate(end)) throw new Error("Invalid datetime: " + end);
      self.end = end;
    }

    self.getFilename = function() {
      var s=String(new Date(self.start)).split(" ").slice(1,4).join("_")
      var e=String(new Date(self.end)).split(" ").slice(1,4).join("_")
      return self.name+"_"+s+"_"+e;
    }


    self.toJSON = function() {
      return JSON.stringify({
        start: self.start,
        end: self.end,
        name: self.name
      })
    }

}

function isValidDate(d) {
  if ( Object.prototype.toString.call(d) !== "[object Date]" )
    return false;
  return !isNaN(d.getTime());
}

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}