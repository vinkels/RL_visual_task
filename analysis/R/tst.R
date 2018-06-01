df.t <- df[which(df$phase == 't'),]
t.1 <- df.t[which(df.t$reward == '1'),] 
t.3 <- df.t[which(df.t$reward == '3'),] 
t.5 <- df.t[which(df.t$reward == '5'),] 


lml.1 = t.1$percent[t.1$condition =='lm' & t.1$response == 'l']
lmm.1 = t.1$percent[t.1$condition =='lm' & t.1$response == 'm']
lhl.1 = t.1$percent[t.1$condition =='lh' & t.1$response == 'l']
lhh.1 = t.1$percent[t.1$condition =='lh' & t.1$response == 'h']
mhm.1 = t.1$percent[t.1$condition =='mh' & t.1$response == 'm']
mhh.1 = t.1$percent[t.1$condition =='mh' & t.1$response == 'h']
shapiro.test(lml.1)
shapiro.test(lmm.1)
shapiro.test(lhl.1)
shapiro.test(lhh.1)
shapiro.test(mhm.1)
shapiro.test(mhh.1)

lml.3 = t.3$percent[t.3$condition =='lm' & t.3$response == 'l']
lmm.3 = t.3$percent[t.3$condition =='lm' & t.3$response == 'm']
lhl.3 = t.3$percent[t.3$condition =='lh' & t.3$response == 'l']
lhh.3 = t.3$percent[t.3$condition =='lh' & t.3$response == 'h']
mhm.3 = t.3$percent[t.3$condition =='mh' & t.3$response == 'm']
mhh.3 = t.3$percent[t.3$condition =='mh' & t.3$response == 'h']
shapiro.test(lml.3)
shapiro.test(lmm.3)
shapiro.test(lhl.3)
shapiro.test(lhh.3)
shapiro.test(mhm.3)
shapiro.test(mhh.3)

lml.5 = t.5$percent[t.5$condition =='lm' & t.5$response == 'l']
lmm.5 = t.5$percent[t.5$condition =='lm' & t.5$response == 'm']
lhl.5 = t.5$percent[t.5$condition =='lh' & t.5$response == 'l']
lhh.5 = t.5$percent[t.5$condition =='lh' & t.5$response == 'h']
mhm.5 = t.5$percent[t.5$condition =='mh' & t.5$response == 'm']
mhh.5 = t.5$percent[t.5$condition =='mh' & t.5$response == 'h']
shapiro.test(lml.5)
shapiro.test(lmm.5)
shapiro.test(lhl.5)
shapiro.test(lhh.5)
shapiro.test(mhm.5)
shapiro.test(mhh.5)

leveneTest(percent ~ (condition*response), data = t.1)
leveneTest(percent ~ (condition*response), data = t.3)
leveneTest(percent ~ (condition*response), data = t.5)

t.1.aov <- aov(percent ~ condition + response, data=t.1)
summary(t.1.aov)
t.3.aov <- aov(percent ~ condition + response, data=t.3)
summary(t.3.aov)
t.5.aov <- aov(percent ~ condition + response, data=t.5)
summary(t.5.aov)

t.lml = df.t$percent[df.t$condition =='lm' & df.t$response == 'l']
t.lmm = df.t$percent[df.t$condition =='lm' & df.t$response == 'm']
t.lhl = df.t$percent[df.t$condition =='lh' & df.t$response == 'l']
t.lhh = df.t$percent[df.t$condition =='lh' & df.t$response == 'h']
t.mhm = df.t$percent[df.t$condition =='mh' & df.t$response == 'm']
t.mhh = df.t$percent[df.t$condition =='mh' & df.t$response == 'h']
t.lmn = df.t$percent[df.t$condition =='lm' & df.t$response == 'n']
t.lhn = df.t$percent[df.t$condition =='lm' & df.t$response == 'n']
t.mhn = df.t$percent[df.t$condition =='lm' & df.t$response == 'n']

shapiro.test(t.lml)
shapiro.test(t.lmm)
shapiro.test(t.lhl)
shapiro.test(t.lhh)
shapiro.test(t.mhm)
shapiro.test(t.mhh)

df.t$response = factor(df.t$response,
                       levels=unique(df.t$response))
df.t$ppn = factor(df.t$ppn,
                  levels=unique(df.t$ppn))
df.t$condition = factor(df.t$condition,
                        levels=unique(df.t$condition))

# repeated measures anova
t.test(t.lml,t.lmm, paired=TRUE)
t.test(t.lhl,t.lhh, paired=TRUE)
t.test(t.mhm,t.mhh, paired=TRUE)

leveneTest(percent ~ group, data = df.t)

lr.aov <- aov(percent ~ response*condition*reward + Error(ppn/reward), data=df.lr)
summary(lr.aov)
lr.aov <- aov(percent ~ response*condition + Error(ppn/condition), data=df.lr)

