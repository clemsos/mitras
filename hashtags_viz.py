# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Analyse des hashtags les plus populaires sur Weibo dans l'année 2012

# <markdowncell>

# Nous cherchons ici à définir quels sont les hashtags qui peuvent nous intéresser, répondant à deux critères précis :
# 
# * Le volume de tweets échangés doit être suffisement conséquent (pour nous permettre de décrire la structure de diffusion)
# * Les échanges doivent être suffisement riches (pour éviter les hashtags publicitaires)
# * Le nombre d'utilisateurs impliqués doit être suffisant (pour éviter les bots)

# <codecell>

# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd
import mpld3
from mpld3 import plugins

# some iPython notebook setup
# mpld3.enable_notebook() # here : http://jakevdp.github.io/blog/2014/01/10/d3-plugins-truly-interactive/
# pd.set_option('display.notebook_repr_html', False)

# <markdowncell>

# Nous chargeons tout d'abord les données que nous avons au préalable préparées.

# <codecell>

root_path="/home/clemsos/Dev/mitras/out/hashtags/"
data_path=root_path+"data/"

# lire les données avec pandas
df=pd.read_csv(root_path+"hashtags_stats.csv")

# supprimer les 3 plus grosses valeurs qui introduisent trop de bruits dans les données
df=df.drop(df.index[:3])


# ne conserver que les hastags contenant plus de 1600 tweets
df=df[df['tweets'] > 1600]

# ne conserver que les hastags contenant plus de 100000 échanges 
df=df[df['conversation'] > 100000]

df # show content

# <markdowncell>

# Ensuite nous réalisons un graphe pour mieux observer les mèmes les plus indiqués pour notre étude.

# <codecell>

# support for Chinese Font
#zh_font = matplotlib.font_manager.FontProperties(fname='wqy-microhei')
#s=u'\u54c8\u54c8' #Need the unicode for your Chinese Char.
fontP = font_manager.FontProperties()
fontP.set_family('WenQuanYi Zen Hei')
fontP.set_size(14)
# plt.text(0.5,0.5,s,fontproperties=fontP, size=50) #example: plt.text()

# start graph
fig,ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'),figsize=(20, 10))

scatter = ax.scatter(df.tweets,
                     df.conversation,
                     s=df["tweets"]/50,
                     c=df.conversation,
                     alpha=0.5,
                     cmap=plt.cm.jet)

ax.set_title("Hashtags distribution per tweet and conversation", size=20)

labels = ['point {0}'.format(i + 1) for i in range(len(df))]
# labels=df.label.values.tolist()

fig.plugins = [plugins.PointLabelTooltip(scatter, labels)]

# <codecell>


# <codecell>


