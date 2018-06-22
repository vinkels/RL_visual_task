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
if(!require(influence.ME)){install.packages("influence.ME")}
if(!require(piecewiseSEM)){install.packages("piecewiseSEM")}

library(readr)
df <- read_csv("/Users/yannick/Desktop/df.csv")
df.lr <- df[which(df$phase == 'lr' & df$response != 0),]

# Order levels of factors
df.lr$response = factor(df.lr$response,
                        levels=c(1,3,5))

df.lr$ppn = factor(df.lr$ppn,
                   levels=unique(df.lr$ppn))

df.lr$condition = factor(df.lr$condition,
                         levels=c('l','m','h'))

# assumption of normality
shapiro.test(df.lr$percent[(df.lr$condition=='l') & (df.lr$response==1)])
shapiro.test(df.lr$percent[(df.lr$condition=='l') & (df.lr$response==3)])
shapiro.test(df.lr$percent[(df.lr$condition=='l') & (df.lr$response==5)])
shapiro.test(df.lr$percent[(df.lr$condition=='m') & (df.lr$response==1)])
shapiro.test(df.lr$percent[(df.lr$condition=='m') & (df.lr$response==3)])
shapiro.test(df.lr$percent[(df.lr$condition=='m') & (df.lr$response==5)])
shapiro.test(df.lr$percent[(df.lr$condition=='h') & (df.lr$response==1)])
shapiro.test(df.lr$percent[(df.lr$condition=='h') & (df.lr$response==5)])

# niet normaal verdeeld
shapiro.test(df.lr$percent[(df.lr$condition=='h') & (df.lr$response==3)]) 




