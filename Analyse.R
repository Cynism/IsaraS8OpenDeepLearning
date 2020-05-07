setwd("C:/Users/axelf/Desktop/Codage/OPEN/Python/IsaraS8OpenDeepLearning")

library(ggplot2)

raw <- read.csv("models.csv",sep=",",colClasses=c(rep("numeric",2),"character",rep("numeric",2),"character",rep("numeric",2)),na.strings="NA")

str(raw)
names(raw)<-c("NbClasses","NbNeurones","DataCat","NbImageTrain","Nbpassages","Dataset","NbTestPic","Accuracy")

raw$Factor <- paste(raw$NbNeurones, raw$DataCat)
#raw$Factor <- paste(raw$NbImageTrain, raw$DataCat)

#raw$NbNeurones <- as.factor(raw$NbNeurones)
#raw$DataCat <- as.factor(raw$DataCat)

png("plot1.png",width=800,height=600)
qplot(Nbpassages,Accuracy,data=raw,color=Factor,geom ="smooth",main = "Analyse de la précision de la reconnaissance d'image d'un programme DeepLearning" ,xlab = "Nombre de passages",ylab = "Précision de l'IA")
dev.off()



