setwd("C:/Users/axelf/Desktop/Codage/OPEN/Python/IsaraS8OpenDeepLearning")

library(ggplot2)

raw <- read.csv("models.csv",sep=",",colClasses=c(rep("numeric",2),"character",rep("numeric",2),"character",rep("numeric",2)),na.strings="NA")
raw2 <- read.csv("ClasseurSynth.csv",sep=";")


str(raw)
str(raw2)
names(raw)<-c("NbClasses","NbNeurones","DataCat","NbImageTrain","Nbpassages","Dataset","NbTestPic","Accuracy")

raw$Factor <- paste(raw$NbNeurones, raw$DataCat)
raw2$Factor2 <- paste(raw2$Categorie)
#raw$Factor <- paste(raw$NbImageTrain, raw$DataCat)

#raw$NbNeurones <- as.factor(raw$NbNeurones)
#raw$DataCat <- as.factor(raw$DataCat)

png("plot1.png",width=800,height=600)
qplot(Nbpassages,Accuracy,data=raw,color=Factor,geom ="smooth",main = "Analyse de la précision de la reconnaissance d'image d'un programme DeepLearning" ,xlab = "Nombre de passages",ylab = "Précision de l'IA")
dev.off()

png("plot2.png",width=800,height=600)
qplot(Nombre.de.passage,Precision,data=raw2,color=Factor2,geom ="line",main = "Analyse de la précision de la reconnaissance d'image d'un programme DeepLearning" ,xlab = "Nombre de passages",ylab = "Précision de l'IA")
dev.off()



