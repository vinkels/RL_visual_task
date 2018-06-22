if(!require(lawstat)){install.packages("lawstat")}
if(!require(ez)){install.packages("ez")}
if(!require(pwr)){install.packages("pwr")}
if(!require(car)){install.packages("car")}
if(!require(psych)){install.packages("psych")}
if(!require(multcompView)){install.packages("multcompView")}
if(!require(lsmeans)){install.packages("lsmeans")}
if(!require(lme4)){install.packages("lme4")}
if(!require(ggplot2)){install.packages("ggplot2")}
if(!require(agricolae)){install.packages("agricolae")}

lme4
library(nlme) 


#get data
df.lr <- df[which(df$phase == 'lr' & df$response != 0),]
df.lr

# Order levels of factors
df.lr$response = factor(df.lr$response,
                         levels=c(1,3,5))

df.lr$ppn = factor(df.lr$ppn,
                    levels=unique(df.lr$ppn))

df.lr$condition = factor(df.lr$condition,
                     levels=c('l','m','h'))

lr.l <- df.lr[which(df.lr$condition == 'l'),]
lr.m <- df.lr[which(df.lr$condition == 'm'),]
lr.h <- df.lr[which(df.lr$condition == 'h'),]

l.1 <- df.lr$percent[(df.lr$condition=='l') & (df.lr$response==1)]
l.3 <- df.lr$percent[(df.lr$condition=='l') & (df.lr$response==3)]
l.5 <- df.lr$percent[(df.lr$condition=='l') & (df.lr$response==5)]
m.1 <- df.lr$percent[(df.lr$condition=='m') & (df.lr$response==1)]
m.3 <- df.lr$percent[(df.lr$condition=='m') & (df.lr$response==3)]
m.5 <- df.lr$percent[(df.lr$condition=='m') & (df.lr$response==5)]
h.1 <- df.lr$percent[(df.lr$condition=='h') & (df.lr$response==1)]
h.3 <- df.lr$percent[(df.lr$condition=='h') & (df.lr$response==3)]
h.5 <- df.lr$percent[(df.lr$condition=='h') & (df.lr$response==5)]

shapiro.test(df.lr$percent[(df.lr$condition=='l') & (df.lr$response==1)])
shapiro.test(df.lr$percent[(df.lr$condition=='l') & (df.lr$response==3)])
shapiro.test(df.lr$percent[(df.lr$condition=='l') & (df.lr$response==5)])
shapiro.test(df.lr$percent[(df.lr$condition=='m') & (df.lr$response==1)])
shapiro.test(df.lr$percent[(df.lr$condition=='m') & (df.lr$response==3)])
shapiro.test(df.lr$percent[(df.lr$condition=='m') & (df.lr$response==5)])
shapiro.test(df.lr$percent[(df.lr$condition=='h') & (df.lr$response==1)])
shapiro.test(df.lr$percent[(df.lr$condition=='h') & (df.lr$response==3)])
shapiro.test(df.lr$percent[(df.lr$condition=='h') & (df.lr$response==5)])


mean(lr.l$percent[lr.l$response==1])
mean(lr.l$percent[lr.l$response==3])
mean(lr.l$percent[lr.l$response==5])
mean(lr.m$percent[lr.m$response==1])
mean(lr.m$percent[lr.m$response==3])
mean(lr.m$percent[lr.m$response==5])
mean(lr.h$percent[lr.h$response==1])
mean(lr.h$percent[lr.h$response==3])
mean(lr.h$percent[lr.h$response==5])

sd(lr.l$percent[lr.l$response==1])
sd(lr.l$percent[lr.l$response==3])
sd(lr.l$percent[lr.l$response==5])
sd(lr.m$percent[lr.m$response==1])
sd(lr.m$percent[lr.m$response==3])
sd(lr.m$percent[lr.m$response==5])
sd(lr.h$percent[lr.h$response==1])
sd(lr.h$percent[lr.h$response==3])
sd(lr.h$percent[lr.h$response==5])

l.aov <- aov(percent ~ response, data=lr.l)
m.aov <- aov(percent ~ response, data=lr.m)
h.aov <- aov(percent ~ response, data=lr.h)
summary(l.aov)
summary(m.aov)
summary(h.aov)
t.test(m.3, h.3)

summary(df.lr)
df.lr

lr.aov <- aov(percent ~ condition*response +Error(ppn/condition), data=df.lr)  
l.aov <- aov(percent ~ response*condition +Error(ppn/condition), data=df.lr)
lr.aov

lr.lm <- lm(percent ~ condition + response + condition*response, data=df.lr)
summary(lr.lm)

results.lme <- lme(percent ~ response*condition, random=~1|ppn, data=df.lr)
anova(results.lme)
lr.5
lm.5 <- lme(percent ~ as.factor(condition), random = ~1|ppn, data=lr.5)
anova(lm.5)
summary(lm.5)
summary(l.aov)

jup <- lmer(percent ~ response*condition+(1|ppn),data=df.lr)
summary(jup)
# rewards
lr.1 <- df.lr[which(df.lr$response == 1),]
lr.3 <- df.lr[which(df.lr$response == 3),]
lr.5 <- df.lr[which(df.lr$response == 5),]

lr.5$ppn <- factor(lr.3$ppn,
                   levels=unique(lr.3$ppn))

lr.5$condition <- factor(lr.3$condition,
                         levels=unique(lr.3$condition))

one.aov <- aov(percent ~ as.factor(condition), data=lr.1)
thr.aov <- aov(percent ~ as.factor(condition), data=lr.3)
fiv.aov <- aov(percent ~ as.factor(condition), data=lr.5)
summary(thr.aov)
summary(one.aov)
summary(fiv.aov)

summary(aov(percent~as.factor(condition), lr.3)) 
TukeyHSD(aov(percent~as.factor(condition), lr.3)) 

summary(one.aov)
summary(thr.aov)
summary(fiv.aov)
thr.aov
library(agricolae)
posthoc <- TukeyHSD(x=thr.aov, 'lr.3$condition', conf.level=0.95)
pst <- HSD.test(thr.aov, 'lr.3$condition')
summary(posthoc)

a2 <- aov(percent ~ as.factor(condition)+as.factor(response) +Error(ppn/as.factor(condition)), data=df.lr) 
summary(a2) 
posthoc <- TukeyHSD(x=a2, 'lr.df$condition', conf.level=0.95)
pst <- HSD.test(a2, 'df.lr$condition')
summary(pst)

library(ggplot2)
ggplot(df.lr, aes(factor(reward, levels=c(1, 3, 5)), percent, fill = factor(condition, levels=c("l", "m", "h")),group=factor(condition, levels=c("l", "m", "h")))) +
  geom_bar(stat = "summary", fun.y = "mean", position = position_dodge(),colour="black",size=.3) + 
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se),
                size=.4,    # Thinner lines
                width=.2,
                position=position_dodge(.9)) +
  expand_limits(y=c(NA, 120)) +
  coord_cartesian(ylim=c(80.0,100.0)) +
  scale_fill_brewer(palette = "Set2") + 
  labs(x = "reward value", y='% correct',fill='CE/CS')

df.lr
spineplot(percent ~ (condition*reward), data=df.lr)


outliers = boxplot(percent ~ (condition*reward), data=df.lr, main="Ozone reading across months")$out
outliers

lr.c <- df.lr[!(df.lr$percent %in% outliers),]

shapiro.test(lr.c$percent[(lr.c$condition=='l') & (lr.c$response==1)])
shapiro.test(lr.c$percent[(lr.c$condition=='l') & (lr.c$response==3)])
shapiro.test(lr.c$percent[(lr.c$condition=='l') & (lr.c$response==5)])
shapiro.test(lr.c$percent[(lr.c$condition=='m') & (lr.c$response==1)])
shapiro.test(lr.c$percent[(lr.c$condition=='m') & (lr.c$response==3)])
shapiro.test(lr.c$percent[(lr.c$condition=='m') & (lr.c$response==5)])
shapiro.test(lr.c$percent[(lr.c$condition=='h') & (lr.c$response==1)])
shapiro.test(lr.c$percent[(lr.c$condition=='h') & (lr.c$response==3)])
shapiro.test(lr.c$percent[(lr.c$condition=='h') & (lr.c$response==5)])

m <- m(igf1~as.factor(tanner))
res <- residuals(m)
hist(res)
qqnorm(res); qqline(res)

ggplot(df.lr, aes(x=factor(reward, levels=c(1, 3, 5)), y=percent, group=factor(condition, levels=c("l", "m", "h")))) +
      geom_point(stat = "summary", fun.y = "mean") +
      stat_summary(fun.y=mean, geom="line")
