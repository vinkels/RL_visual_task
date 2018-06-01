if(!require(lawstat)){install.packages("lawstat")}
if(!require(ez)){install.packages("ez")}
if(!require(pwr)){install.packages("pwr")}
if(!require(car)){install.packages("car")}


lml = df.c$percent[df.c$condition =='lm' & df.c$response == 'l']
lmm = df.c$percent[df.c$condition =='lm' & df.c$response == 'm']
lhl = df.c$percent[df.c$condition =='lh' & df.c$response == 'l']
lhh = df.c$percent[df.c$condition =='lh' & df.c$response == 'h']
mhm = df.c$percent[df.c$condition =='mh' & df.c$response == 'm']
mhh = df.c$percent[df.c$condition =='mh' & df.c$response == 'h']
lmn = df.c$percent[df.c$condition =='lm' & df.c$response == 'n']
lhn = df.c$percent[df.c$condition =='lm' & df.c$response == 'n']
mhn = df.c$percent[df.c$condition =='lm' & df.c$response == 'n']

shapiro.test(lml)
shapiro.test(lmm)
shapiro.test(lhl)
shapiro.test(lhh)
shapiro.test(mhm)
shapiro.test(mhh)

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


