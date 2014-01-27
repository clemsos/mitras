function() {
    // if (!this.hashtags) {
    //     return;
    // }

    // print("yo");
    var id = this._id.str;
    this.hashtags.forEach(function(h) {
        emit(h, {ids : id, count: 1});
    })
}