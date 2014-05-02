# list of hashtags 
db.tweets.aggregate( 
    {$project: {a: '$hashtags'}}, 
    {$unwind: '$a'}, 
    {$group: {_id: 'a', items: {$addToSet: '$a'}}}
    );

# count for each  hashtags

    # { $limit : 500000 },
    # { $skip : 100000 },

db.tweets.aggregate([
    { $group: {
            _id: "$_id",
            hasht: { $addToSet : "$hashtags" } 
            }
    },
    { $unwind : "$hasht" }, 
    { $unwind : "$hasht" },
    { $group : { _id : "$hasht", count: { $sum : 1 } } },
    { $sort : { "count" : -1}  },
    { $limit : 100 }
])

db.tweets.find({hashtags : "三国来了"}, { mid :1}).count()
db.tweets.find({hashtags : "罗志祥730生日快乐"}, { mid :1}).count()

db.tweets.find({hashtags : ""})

# get hashtags with more than 100 answers
db.hashtags.find( { 'value.tweets.100' :{ $exists : true } }, {key:1})
