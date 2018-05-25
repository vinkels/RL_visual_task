if(!require(lawstat)){install.packages("lawstat")}
if(!require(ez)){install.packages("ez")}
if(!require(pwr)){install.packages("pwr")}
if(!require(car)){install.packages("car")}

ctrl_data <- pivot_set[pivot_set$condition == 'c',] 
lml = ctrl_data$response_size[ctrl_data$type =='lm' & ctrl_data$response == 'l']
lmm = ctrl_data$response_size[ctrl_data$type =='lm' & ctrl_data$response == 'm']
lhl = ctrl_data$response_size[ctrl_data$type =='lh' & ctrl_data$response == 'l']
lhh = ctrl_data$response_size[ctrl_data$type =='lh' & ctrl_data$response == 'h']
mhm = ctrl_data$response_size[ctrl_data$type =='mh' & ctrl_data$response == 'm']
mhh = ctrl_data$response_size[ctrl_data$type =='mh' & ctrl_data$response == 'h']
lmn = ctrl_data$response_size[ctrl_data$type =='lm' & ctrl_data$response == 'n']
lhn = ctrl_data$response_size[ctrl_data$type =='lm' & ctrl_data$response == 'n']
mhn = ctrl_data$response_size[ctrl_data$type =='lm' & ctrl_data$response == 'n']
shapiro.test(lml)
shapiro.test(lmm)
shapiro.test(lhl)
shapiro.test(lhh)
shapiro.test(mhm)
shapiro.test(mhh)

# means % chosen of all groups
ctrl.mean <- aggregate(ctrl_data$response_size,
                         by = list(ctrl_data$response,
                                   ctrl_data$type),
                         FUN = 'mean')
ctrl_data$response = factor(ctrl_data$response,
                            levels=unique(ctrl_data$response))
ctrl_data$ppn = factor(ctrl_data$ppn,
                            levels=unique(ctrl_data$ppn))
ctrl_data$type = factor(ctrl_data$type,
                            levels=unique(ctrl_data$type))

# repeated measures anova
ctrl.AOV <- aov(response_size~(response*type)+Error(ppn/(type*response)), data = ctrl_data)
summary(ctrl.AOV)


 
