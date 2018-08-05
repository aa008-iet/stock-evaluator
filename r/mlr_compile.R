# Title     : mlr_compile
# Objective : Implementation of neural network in R
# Created by: Justin Huang
# Created on: 8/4/2018

library("mlr")

# df <- read.csv("test.csv", header=TRUE, row.names=1, sep=',')
# View(df)

t <- makeClassifTask(id = 'SAP', data = alpha_SAP, target = 'Score')

tune = function(params, learner) {

  ctrl <- makeTuneControlRandom(maxit = 100L)
  rdesc <- makeResampleDesc("CV", iters = 5L)
  res = tuneParams(learner, task = t, resampling = rdesc, par.set = params, control = ctrl, show.info = TRUE)
  
  return(setHyperPars(makeLearner(learner), par.vals = res$x))
}

m <- train(l, t, subset=seq(1, getTaskSize(t), 2))

p <- predict(m, t, subset=seq(2, getTaskSize(t), 2))
print(performance(p, measures = acc))
print(calculateConfusionMatrix(p))