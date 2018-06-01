if(!require(lawstat)){install.packages("lawstat")}
if(!require(ez)){install.packages("ez")}
if(!require(pwr)){install.packages("pwr")}
if(!require(car)){install.packages("car")}
if(!require(psych)){install.packages("psych")}
if(!require(multcompView)){install.packages("multcompView")}
if(!require(lsmeans)){install.packages("lsmeans")}
if(!require(FSA)){install.packages("FSA")}

#get data
df.lr <- df[which(df$phase == 'lr' & df$response != 0),]

# Order levels of factors
df.lr$response = factor(df.lr$response,
                         levels=unique(df.lr$response))

df.lr$ppn = factor(df.lr$ppn,
                    levels=unique(df.lr$ppn))

df.lr$condition = factor(df.lr$condition,
                     levels=unique(df.lr$condition))

lr.l <- df.lr[which(df.lr$condition == 'l'),]
lr.m <- df.lr[which(df.lr$condition == 'm'),]
lr.h <- df.lr[which(df.lr$condition == 'h'),]


shapiro.test(lr.l$percent[lr.l$response==1])
shapiro.test(lr.l$percent[lr.l$response==3])
shapiro.test(lr.l$percent[lr.l$response==5])
shapiro.test(lr.m$percent[lr.m$response==1])
shapiro.test(lr.m$percent[lr.m$response==3])
shapiro.test(lr.m$percent[lr.m$response==5])
shapiro.test(lr.h$percent[lr.h$response==1])
shapiro.test(lr.h$percent[lr.h$response==3])
shapiro.test(lr.h$percent[lr.h$response==5])

l.aov <- aov(percent ~ response, data=lr.l)
m.aov <- aov(percent ~ response, data=lr.m)
h.aov <- aov(percent ~ response, data=lr.h)
summary(l.aov)
summary(m.aov)
summary(h.aov)

shapiro.test(df.lr$percent[df.lr$condition=="l" & df.lr$response==3])
shapiro.test(df.lr$percent[df.lr$condition=="l" & df.lr$response==5])
shapiro.test(df.lr$percent[df.lr$condition=="m" & df.lr$response==1])
shapiro.test(df.lr$percent[df.lr$condition=="m" & df.lr$response==3])
shapiro.test(df.lr$percent[df.lr$condition=="m" & df.lr$response==5])
shapiro.test(df.lr$percent[df.lr$condition=="h" & df.lr$response==1])
shapiro.test(df.lr$percent[df.lr$condition=="h" & df.lr$response==3])
shapiro.test(df.lr$percent[df.lr$condition=="h" & df.lr$response==5])

lr.aov <- aov(percent ~ response*condition + Error(ppn/condition), data=df.lr)
summary(lr.aov)

# rewards
lr.1 <- df.lr[which(df.lr$response == 1),]
lr.3 <- df.lr[which(df.lr$response == 3),]
lr.5 <- df.lr[which(df.lr$response == 5),]


one.aov <- aov(percent ~ condition, data=lr.1)
thr.aov <- aov(percent ~ condition, data=lr.3)
fiv.aov <- aov(percent ~ condition, data=lr.5)

summary(one.aov)
summary(thr.aov)
summary(fiv.aov)

