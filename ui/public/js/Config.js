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

    self.setStart = function(start) {
      if(!isValidDate(start))
        throw new Error("Invalid datetime: " + start);
      self.start = start;
    }

    self.setEnd = function(end) {
      if(!isValidDate(end))
        throw new Error("Invalid datetime: " + end);
      self.end = end;
    }

    self.toJSON = function() {
      return JSON.stringify({
        start: self.start,
        end: self.end,
        cosming: self.cosming

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