# Title     : mlr_compile
# Objective : Implementation of neural network in R
# Created by: Justin Huang
# Created on: 8/4/2018

library("mlr")

preprocess = function(df) {
  df$Score <- 0
  for(i in c(1:(nrow(df) - 1))) {
    if(df$adj_close[i] < df$adj_close[i + 1]) {
      df$Score[i] <- 1
    }
  }
  df$Score <- as.factor(df$Score)
  return(normalizeFeatures(df, target = 'Score', method = 'standardize'))
}

tune = function(learner) {

  if(learner == "classif.nnet") {
    params <- makeParamSet(
      makeIntegerParam('size', lower = 2, upper = 6),
      makeNumericParam('rang', lower = -4, upper = 3, trafo = function(x) 2^x),
      makeNumericParam('decay', lower = -2, upper = 2, trafo = function(x) 2^x),
      makeNumericParam('abstol', lower = -7, upper = -3, trafo = function(x) 10^x),
      makeNumericParam('reltol', lower = -10, upper = -6, trafo = function(x) 10^x)
    )
  } else if(learner == "classif.randomForest") {
    params <- makeParamSet(
      makeIntegerParam('ntree', lower = 2, upper = 3, trafo = function(x) 10^x),
      makeIntegerParam('nodesize', lower = 0, upper = 4, trafo = function(x) 2^x)
    )
  } else if(learner == "classif.ksvm"){
    params <- makeParamSet(
      makeNumericParam('C', lower = 0, upper = 4, trafo = function(x) 2^x),
      makeNumericParam('sigma', lower = -5, upper = -3, trafo = function(x) 10^x),
      makeNumericParam('tol', lower = -5, upper = -1, trafo = function(x) 10^x)
    )
  }
  ctrl <- makeTuneControlRandom(maxit = 100L)
  rdesc <- makeResampleDesc("CV", iters = 5L)
  res = tuneParams(learner, task = t, resampling = rdesc, measures = acc, par.set = params, control = ctrl, show.info = TRUE)
  
  return(setHyperPars(makeLearner(learner), par.vals = res$x))
}

df <- preprocess(read.csv("test.csv", header=TRUE, row.names=1, sep=','))
# View(df)

t <- makeClassifTask(id = 'AAPL', data = df, target = 'Score')

l <- tune("classif.ksvm")

m <- train(l, t, subset=seq(1, getTaskSize(t), 2))

p <- predict(m, t, subset=seq(2, getTaskSize(t), 2))
print(performance(p, measures = acc))
print(calculateConfusionMatrix(p))

# all the plots 

# plotFilterValues(generateFilterValuesData(t))
