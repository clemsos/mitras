#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os

root_path="/home/clemsos/Dev/mitras/out/hashtags/"
data_path=root_path+"data/"

def list_to_csv(_keys,_rows,_csv_filepath):
    
    with open(_csv_filepath,'w') as f: # writes the final output to CSV
        csv_out=csv.writer(f)
        csv_out.writerow(_keys) # add header
        for row in _rows:
            csv_out.writerow(row)

    print " csv has been stored as %s"%_csv_filepath

# get hashtags list
hashtags_path=data_path+"top_hashtags.csv"
with open(hashtags_path, 'rb') as cs_file:
    cs_file.next() # skip header
    csv_hash=csv.reader(cs_file)
    hashtags=[word for word in csv_hash]

hashtags_path_2=data_path+"top_hashtags_2.csv"
with open(hashtags_path_2, 'rb') as cs_file:
    cs_file.next() # skip header
    csv_hash=csv.reader(cs_file)
    hashtags+=[word for word in csv_hash]

print "%d hashtags in files"%len(hashtags)

# get censored
censored_list_path=os.path.dirname(os.path.dirname(root_path))+"/SensitiveSinaWeiboSearchTerms.csv"

censored_words=[]
with open(censored_list_path, 'rb') as cs_file:
    csv_censor=csv.reader(cs_file)
    censored_words=[word[0] for word in csv_censor]

censored_words+=["18禁","3月13日","March","3月20日","4月3日","6月4日","71遊行","89运动","一中一台","一党专制","一党专政","一边一国movement","x","七五八大洪水","七宗罪","三人性交","三八大盖","x","上海帮","下台","东京热","东方闪电","东突independence activists","东长安街1989 Tiananmen","严家其sub institute","中俄密约","中国军事","中央军委","中宣部","中联办","中革军委","丹增嘉措","主神教","乌尔","乔石to have","九评affiliated Epoch","乱伦","乳交","亂倫","二月逆流","x","五四事件","五四运动","五毛","交趾支那","人大常委","人民报","人造阴道","令计划","伊斯兰","何厚铧","余杰","做爱","储波","八一广场Uprising","八四事件","六月初","六月四日","共军","共狗","兽交","兽奸","内射","军阀","冯正虎for XX","刘宾雁","刘晓原","刘贤斌","副主席","办假证","办证","加兹温","包叙定International Engineering","敏感","北京政权","北高联studentreps","卖淫","博讯","x","卫星电视","厉以宁","反共","反革命罪","叠氮化钠Harvard scientists","台湾独立","台风露丝","向巴平措","吞精","吴仪","吴扬明","吴阶平","N","呼喊派","咪咪","四五运动","四六事件","四君子","N","N","四清运动","团中央","国台办","N","x","夏耕","外挂","外蒙","x","x","x","x","大紀元","x","大陸當局","大麻","xen.wikipedia","天安门","天葬","太安","奥克托今","女優","女同","女阴","奶子","妓女","妓男","姬胜德Chinese Communist","媚药","宋祖英","宗凤鸣","实际神","密勒日巴","封从德","射颜","x","x","x","x","尤物","屄","巨乳","巨奶","x","布局","希望之声","干你娘","干你老母","平可夫","幸運☆星","幸運星","x","库车","x","开放杂志","张筱雨","彭丽媛","彭博社","彭珮云","快闪党","性派对","性虐","x","情色","成克杰","成思危","我的奋斗","戴相龙","打炮","打飞机","抵制日货","操我","操逼","作秀","文鲜明","新闻管制","方励之","无毛","春药","暴露狂","暴露癖","曾培炎","曾蔭培","李洪志","李瑞环","李肇星","李鹏","杜冷丁","杜宪","杜导正","林嘉祥","x","x","梁保华","梯恩梯","毒龙","毛匪","x","毛片","江建曾","江浙民系","澤民","江澤民","江绵恒","江青","x","法輪","法轮","洪学智","淫水","淫液","温云松","滴蜡","激流中国","火凤凰","焦国标","独裁","猥亵","獸交","x","?","王宝森","王小丫","王文怡","由喜贵","白恩培","x","盘古乐队","砍刀","硝酸钍","硝酸铵","磷化锌","穆斯林","气枪","立法会","第38军","維基揭密","維多利亞candlelight vigil","经叔平","统一教","xhttp://en","维基揭密","x","美分党","翻墙","x","x","肛交","胡星斗","胡海峰","胡石根","脚交","膏药旗","自由亚洲","色情电影","色欲","色诱中毒posioned?","艾晓明","苦味酸","苹果日报tabloid","范徐丽泰national security","茉莉革命","草你妈","董建华","N","蔡赴朝","薄熙来","藏独","虐肛","Nms?ie","被立王","裙底春","裙底風光","裙底风光","裸露","观音法门","讣告","费孝通","赤化","赤匪","赵紫阳leniency in","足交","轮奸","连裤袜","迷奸","退党","遊行","x","邓力群","邓朴方","邓颖超","郭金龙","金人庆","钴","铁血旗army_Wuhan_flag_(1911","阴囊","阴毛","阴蒂","阴部","陈子明","陈希同","陈炳德","陳水扁","隗福临","零八宪章","雷洁琼globaltimes.cn","xof skin","露点","颜射","x","驗證碼","魏京生","鲍彤","鸡奸","鸡巴","黄色","黄雀行动","N","黎智英empire,","黑索今","x","龍應台","龟头","64","六四","八八","八九","九八","1989","adult","A片","BLOOD","CCP","dalai","Evolution","GFW","gov","IP封锁","K粉","lama","porn","XMLHTTP","YHWH","冲突"]

print len(censored_words)

# image size 
total=0
hashtags_stats=[]
for i,h in enumerate(hashtags):
    censored=0
    if h in censored_words: print h # censored=1

    hashtag=h[0]
    count=int(float(h[1]))
    '''
        try :
            # TODO : improve granularity by scanning csv rows count, not size
            gv_path=root_path+"/0-1000/gv/"+hashtag+".gv"
            gv_row=[1 for row in open(gv_path, 'r')]
            size=len(gv_row)
            print size
            # size=os.path.getsize(root_path+"/0-1000/gv/"+hashtag+".gv")
            hashtags_stats.append((hashtag, count, size, censored))
            total+=1
        except :
            try :
                # TODO : idem
                # size=os.path.getsize(root_path+"/1000-2000/gv/"+hashtag+".gv")
                gv_path=root_path+"/1000-2000/gv/"+hashtag+".gv"
                size=len([row for row in open(gv_path, 'r')])
                hashtags_stats.append((hashtag, count, size, censored))
                total+=1
            except :
                pass
        '''

print 
print "TOTAL :%d results"%len(hashtags_stats)

#  list_to_csv(["label","tweets","conversation","censored"],hashtags_stats,root_path+"hashtags_stats.csv")
