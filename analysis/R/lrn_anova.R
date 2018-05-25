if(!require(lawstat)){install.packages("lawstat")}
if(!require(ez)){install.packages("ez")}
if(!require(pwr)){install.packages("pwr")}
if(!require(car)){install.packages("car")}
if(!require(psych)){install.packages("psych")}
if(!require(multcompView)){install.packages("multcompView")}
if(!require(lsmeans)){install.packages("lsmeans")}
if(!require(FSA)){install.packages("FSA")}


# Order levels of factors

lr_set$response = factor(lr_set$response,
                      levels=unique(lr_set$response))

lr_set$ppn = factor(lr_set$ppn,
                         levels=unique(lr_set$ppn))

lr_set$type = factor(lr_set$type,
                    levels=unique(lr_set$type))

# Check the data frame
headTail(lr_set)
str(lr_set)
summary(lr_set)

# normality check
shapiro.test(lr_set$response_size[lr_set$type=="l" & lr_set$response==1])
shapiro.test(lr_set$response_size[lr_set$type=="l" & lr_set$response==3])
shapiro.test(lr_set$response_size[lr_set$type=="l" & lr_set$response==5])
shapiro.test(lr_set$response_size[lr_set$type=="m" & lr_set$response==1])
shapiro.test(lr_set$response_size[lr_set$type=="m" & lr_set$response==3])
shapiro.test(lr_set$response_size[lr_set$type=="m" & lr_set$response==5])
shapiro.test(lr_set$response_size[lr_set$type=="h" & lr_set$response==1])
shapiro.test(lr_set$response_size[lr_set$type=="h" & lr_set$response==3])
shapiro.test(lr_set$response_size[lr_set$type=="h" & lr_set$response==5])


# mixed anova
aov_response_type <- aov(response_size ~ response*type + Error(ppn/type), data=lr_set)
summary(aov_response_type)



histogram(~ type | ppn,
          data=lr_set,
          layout=c(1,5)      #  columns and rows of individual plots
)

#non-parametric friedman for type + kendall for effect size
friedman.test(response_size ~ ppn | type,
              data = lr_set)
XT = xtabs(response_size ~ ppn + type,
           data = lr_set)

XT
KendallW(XT, 
         correct=TRUE, 
         test=TRUE)

library(rcompanion)

# post-hoc test for friedman results
PT = pairwiseSignTest(response_size ~ ppn, 
                      data   = lr_set,
                      method = "fdr")

PT

cldList(p.adjust ~ Comparison,
        data = PT,
        threshold  = 0.05)


#model = lm(response_size ~ type + response + type:response,
#           data = lr_set)


# library(car)

#Anova(model,
 #     type = "II")
#
#modellmer = lmer(response_size ~ response + type + response:type + (1+type|ppn), lr_set)

