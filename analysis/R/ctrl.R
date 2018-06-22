if(!require(lawstat)){install.packages("lawstat")}
if(!require(ez)){install.packages("ez")}
if(!require(pwr)){install.packages("pwr")}
if(!require(car)){install.packages("car")}

df.c <- df[df$phase =='c',]
lml = df.c$percent[df.c$condition =='lm' & df.c$response == 'l']
lmm = df.c$percent[df.c$condition =='lm' & df.c$response == 'm']
lhl = df.c$percent[df.c$condition =='lh' & df.c$response == 'l']
lhh = df.c$percent[df.c$condition =='lh' & df.c$response == 'h']
mhm = df.c$percent[df.c$condition =='mh' & df.c$response == 'm']
mhh = df.c$percent[df.c$condition =='mh' & df.c$response == 'h']

lml
lmm

mean(lml)
sd(lml)
mean(lmm)
sd(lmm)
mean(lhl)
sd(lhl)
mean(lhh)
sd(lhh)
mean(mhm)
sd(mhm)
mean(mhh)
sd(mhh)


shapiro.test(lml)
shapiro.test(lmm)
shapiro.test(lhl)
shapiro.test(lhh)
shapiro.test(mhm)
shapiro.test(mhh)
t.test(lml, mu=50.0)
t.test(lmm, mu=50.0)
t.test(lhl, mu=50.0)
t.test(lhh, mu=50.0)
t.test(mhm, mu=50.0)
t.test(mhh, mu=50.0)

df.c$response = factor(df.c$response,
                            levels=unique(df.c$response))
df.c$ppn = factor(df.c$ppn,
                       levels=unique(df.c$ppn))
df.c$condition = factor(df.c$condition,
                        levels=unique(df.c$condition))

# repeated measures anova
t.test(lml,lmm, paired=TRUE)
t.test(lhl,lhh, paired=TRUE)
t.test(mhm,mhh, paired=TRUE)

df.c$group = factor(df.c$group,
                       levels=unique(df.c$group))
df.c$ppn = factor(df.c$ppn,
                  levels=unique(df.c$ppn))

leveneTest(percent ~ group, data = df.c)


friedman.test(percent ~ ppn | group,
              data = df.c)

library(ggplot2)
ggplot(df.c, aes(factor(condition, levels=c("lm", "lh", "mh")), percent, fill = factor(response, levels=c("l", "m", "h")))) +
  geom_bar(stat = "summary", fun.y = "mean", position = "dodge") + 
  scale_fill_brewer(palette = "Set2") + 
  coord_cartesian(ylim=c(40,60)) + labs(x = "CE/SC set", y='% chosen',fill='CE/CS class')

ggplot(df.c, aes(condition, percent, fill = response)) +
  geom_bar(stat="identity", position = "dodge") + 
  scale_fill_brewer(palette = "Set2")  + labs(x = "CE/SC set", y='% chosen',fill='CE/CS class')


df.c <- df[df$phase == 'c',] 


 

