library(readr)
df <- read_csv("/Users/yannick/Code/RL_visual_task/analysis/output/data_percent_clean.csv")
ct <- read_csv("/Users/yannick/Code/RL_visual_task/analysis/output/dif_ct.csv")
ct.t <- ct[ct$phase == 't',]
ct.c <- ct[ct$phase == 'c',]

# normality
shapiro.test(ct.t$percent[(ct.t$condition == 'lm') & (ct.t$response == 'l')])
shapiro.test(ct.t$percent[(ct.t$condition == 'lm') & (ct.t$response == 'm')])
shapiro.test(ct.t$percent[(ct.t$condition == 'lh') & (ct.t$response == 'l')])
shapiro.test(ct.t$percent[(ct.t$condition == 'lh') & (ct.t$response == 'h')])
shapiro.test(ct.t$percent[(ct.t$condition == 'mh') & (ct.t$response == 'm')])
shapiro.test(ct.t$percent[(ct.t$condition == 'mh') & (ct.t$response == 'h')])

shapiro.test(ct.c$percent[(ct.c$condition == 'lm') & (ct.c$response == 'l')])
shapiro.test(ct.c$percent[(ct.c$condition == 'lm') & (ct.c$response == 'm')])
shapiro.test(ct.c$percent[(ct.c$condition == 'lh') & (ct.c$response == 'l')])
shapiro.test(ct.c$percent[(ct.c$condition == 'lh') & (ct.c$response == 'h')])
shapiro.test(ct.c$percent[(ct.c$condition == 'mh') & (ct.c$response == 'm')])
shapiro.test(ct.c$percent[(ct.c$condition == 'mh') & (ct.c$response == 'h')])

leveneTest(percent ~ condition*response, data=ct.c)
leveneTest(percent ~ condition*response, data=ct.t)

c.lm <- lm(formula=percent ~ condition*response,data=ct.c,na.action=na.omit)
Anova(c.lm,type='II',white.adjust=F)

t.lm <- lm(formula=percent ~ condition*response,data=ct.t,na.action=na.omit)
Anova(t.lm,type='II',white.adjust='hc3')

t.llm <- ct.t$percent[(ct.t$condition == 'lm') & (ct.t$response == 'l') & (ct.t$reward == 5)]
t.mlm <- ct.t$percent[(ct.t$condition == 'lm') & (ct.t$response == 'm') & (ct.t$reward == 5)]
t.llh <- ct.t$percent[(ct.t$condition == 'lh') & (ct.t$response == 'l') & (ct.t$reward == 5)]
t.hlh <- ct.t$percent[(ct.t$condition == 'lh') & (ct.t$response == 'h') & (ct.t$reward == 5)]
t.mmh <- ct.t$percent[(ct.t$condition == 'mh') & (ct.t$response == 'm') & (ct.t$reward == 5)]
t.hmh <- ct.t$percent[(ct.t$condition == 'mh') & (ct.t$response == 'h') & (ct.t$reward == 5)]
c.llm <- ct.c$percent[(ct.c$condition == 'lm') & (ct.c$response == 'l') & (ct.c$reward == 5)]
c.mlm <- ct.c$percent[(ct.c$condition == 'lm') & (ct.c$response == 'm') & (ct.c$reward == 5)]
c.llh <- ct.c$percent[(ct.c$condition == 'lh') & (ct.c$response == 'l') & (ct.c$reward == 5)]
c.hlh <- ct.c$percent[(ct.c$condition == 'lh') & (ct.c$response == 'h') & (ct.c$reward == 5)]
c.mmh <- ct.c$percent[(ct.c$condition == 'mh') & (ct.c$response == 'm') & (ct.c$reward == 5)]
c.hmh <- ct.c$percent[(ct.c$condition == 'mh') & (ct.c$response == 'h') & (ct.c$reward == 5)]

t.test(t.llm, mu=50)
t.test(t.mlm, mu=50)
t.test(t.llh, mu=50)
t.test(t.hlh, mu=50)
t.test(t.mmh, mu=50)
t.test(t.hmh, mu=50)


t.aov <- anova(lm(percent ~ condition * response, data=ct.t))
t.aov




df.t <- df[df$phase == 't',] 
df.c <- df[(df$phase == 'c') & df$reward,] 
df.c$response = factor(df.c$response,
                       levels=unique(df.c$response))
df.c$ppn = factor(df.c$ppn,
                  levels=unique(df.c$ppn))
df.c$condition = factor(df.c$condition,
                        levels=unique(df.c$condition))

c.1 <- df.c$percent[df.c$reward == 1]
c.3 <- df.c$percent[df.c$reward == 3]
c.5 <- df.c$percent[df.c$reward == 5]
shapiro.test(c.1)
shapiro.test(c.3)
shapiro.test(c.5)
df.t
t.1 <- df.t$percent[df.t$reward == 1]
t.3 <- df.t$percent[df.t$reward == 3]
t.5 <- df.t$percent[df.t$reward == 5]
shapiro.test(t.1)
shapiro.test(t.3)
shapiro.test(t.5)

t.test(t.1, t.5, paired=T)

t.c <- df[(df$phase != 'lr') & (df$reward == 5),]
t.c
t.test(c.1, t.1, paired=T)
t.test(c.3, t.3, paired=T)
t.test(c.5, t.5, paired=T)
plot(c.1)
plot(t.1)


levels=c("4", "r", "f")

library(ggplot2)
ggplot(t.c, aes(factor(condition, levels=c("lm", "lh", "mh")), percent, fill = factor(response, levels=c("l", "m", "h")))) +
  geom_bar(stat = "summary", fun.y = "mean", position = "dodge") + 
  scale_fill_brewer(palette = "Set2") + expand_limits(y=c(NA, 70)) + 
  geom_errorbar(aes(ymin=mean_af-se_af, ymax=mean_af+se_af),
                size=.4,    # Thinner lines
                width=.2,
                position=position_dodge(.9)) +
  coord_cartesian(ylim=c(30,80)) + labs(x = "reward value", y='% chosen',fill='CE/CS')

ggplot(dif_ct, aes(factor(response, levels=c("l", "m", "h")), dif, fill = factor(condition, levels=c("lm", "lh", "mh")))) +
  geom_bar(stat = "summary", fun.y = "mean", position = "dodge") + 
  scale_fill_brewer(palette = "Set2") + expand_limits(y=c(NA, 80)) + 
 # geom_errorbar(aes(ymin=mean_af-se_af, ymax=mean_af+se_af),
  #              size=.4,    # Thinner lines
   #             width=.2,
    #            position=position_dodge(.9)) +
  coord_cartesian(ylim=c(-10,10)) + labs(x = "reward value", y='% chosen',fill='CE/CS')

library(ggplot2)
ggplot(dif_ct, aes(factor(condition, levels=c("lm", "lh", "mh")), dif, fill = factor(response, levels=c("l", "m", "h")))) +
  geom_boxplot() + 
  scale_fill_brewer(palette = "Set2") + 
  labs(x = "reward value", y='% chosen',fill='CE/CS')

tc_dif
t.tc <- t.c[t.c$phase == 't',]
c.tc <- t.c[t.c$phase == 'c',]
t.llm <- t.tc$percent[(t.tc$condition == 'lm') & (t.tc$response == 'l') & (t.tc$reward == 5)]
t.mlm <- t.tc$percent[(t.tc$condition == 'lm') & (t.tc$response == 'm') & (t.tc$reward == 5)]
t.llh <- t.tc$percent[(t.tc$condition == 'lh') & (t.tc$response == 'l') & (t.tc$reward == 5)]
t.hlh <- t.tc$percent[(t.tc$condition == 'lh') & (t.tc$response == 'h') & (t.tc$reward == 5)]
t.mmh <- t.tc$percent[(t.tc$condition == 'mh') & (t.tc$response == 'm') & (t.tc$reward == 5)]
t.hmh <- t.tc$percent[(t.tc$condition == 'mh') & (t.tc$response == 'h') & (t.tc$reward == 5)]
c.llm <- c.tc$percent[(c.tc$condition == 'lm') & (c.tc$response == 'l') & (c.tc$reward == 5)]
c.mlm <- c.tc$percent[(c.tc$condition == 'lm') & (c.tc$response == 'm') & (c.tc$reward == 5)]
c.llh <- c.tc$percent[(c.tc$condition == 'lh') & (c.tc$response == 'l') & (c.tc$reward == 5)]
c.hlh <- c.tc$percent[(c.tc$condition == 'lh') & (c.tc$response == 'h') & (c.tc$reward == 5)]
c.mmh <- c.tc$percent[(c.tc$condition == 'mh') & (c.tc$response == 'm') & (c.tc$reward == 5)]
c.hmh <- c.tc$percent[(c.tc$condition == 'mh') & (c.tc$response == 'h') & (c.tc$reward == 5)]
shapiro.test(t.llm) 
shapiro.test(t.mlm)
shapiro.test(t.llh)
shapiro.test(t.hlh)
shapiro.test(t.mmh)
shapiro.test(t.hmh)
t.llm
t.mlm
shapiro.test(c.mlm)
shapiro.test(c.llh)
shapiro.test(c.hlh)
shapiro.test(c.mmh)
shapiro.test(c.hmh)
#aov(percent ~ condition + response, data=t.3)

shapiro.test(tc$percent)
t.test(t.tc$percent,mu=50.0)
t.test(t.tc$percent,mu=50.0)

t.test(t.llm,mu=50.0)
t.test(t.mlm, mu=50.0)
t.test(t.llh,mu=50.0)
t.test(t.hlh, mu=50.0)
t.test(t.mmh,mu=50.0)
t.test(t.hmh, mu=50.0)

hist(tc$percent)

shapiro.test(tc$percent[tc$phase=="c" & tc$response==3])
shapiro.test(tc$percent[tc$condition=="l" & tc$response=='l'])
shapiro.test(tc$percent[tc$condition=="m" & tc$response=='m'])
shapiro.test(tc$percent[tc$condition=="m" & tc$response=='l'])
shapiro.test(tc$percent[tc$condition=="m" & tc$response=='h'])
shapiro.test(tc$percent[tc$condition=="h" & tc$response==''])

mean(t.llm)
sd(t.llm)
mean(t.mlm)
sd(t.mlm)
mean(t.llh)
sd(t.llh)
mean(t.hlh)
sd(t.hlh)
mean(t.mmh)
sd(t.mmh)
mean(t.hmh)
sd(t.hmh)
