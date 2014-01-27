function(key, values) {
    var count = 0;
    var ids=[]
    
    values.forEach(function(value) {
        count += value.count;
        ids.push(value.ids)
    });
    return key, { ids:ids, count: count};
}