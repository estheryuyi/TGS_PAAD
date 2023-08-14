Args <- commandArgs(T)
if (length(Args) != 3){
                print("density.r <p1> <s1> <pdf>")
                q()
}

p1 <- Args[1]
s1 <- Args[2]
out <-  Args[3]
library(ggplot2)
plt_s1=read.csv(s1,sep="\t",header=T)
plt_s1$person="s1"
plt_p1=read.csv(p1,sep="\t",header=T)
plt_p1$person="p1"
plt_ps=cbind(plt_p1,plt_s1)

#???p1???s1????????????????????????????????????????????????fisher??????
for (n in 1:nrow(plt_ps)){
  data1=plt_ps[n,]
  dat <- matrix(c(data1[1,2],data1[1,3],data1[1,6],data1[1,7]),nrow=2,ncol=2)
  result = fisher.test(dat)
  #result2 = chisq.test(dat,correct=T)
  up=result$conf.int[1]
  down=result$conf.int[2]
  pvalue=result$p.value
  or=result$estimate
  plt_ps[n,9]=up
  plt_ps[n,10]=down
  plt_ps[n,11]=pvalue
  plt_ps[n,12]=or
  plt_ps[n,13]=log10(up)
  plt_ps[n,14]=log10(down)
  plt_ps[n,15]=log10(or)
}
colnames(plt_ps)[9]="ps_up"
colnames(plt_ps)[10]="ps_down"
colnames(plt_ps)[11]="pvalue"
colnames(plt_ps)[12]="OR"
colnames(plt_ps)[13]="log_ps_up"
colnames(plt_ps)[14]="log_ps_down"
colnames(plt_ps)[15]="logOR"

plt_ps$significant=""
if (sum(plt_ps$pvalue>=0.05)>0){plt_ps[plt_ps$pvalue>=0.05,]$significant="no"}
if (sum(plt_ps$pvalue<0.05)>0){plt_ps[plt_ps$pvalue<0.05,]$significant="yes"}
plt_ps$significance=as.factor(plt_ps$significant)

#???????????????p??????????????????????????????
pdf(out)
ggplot(data=plt_ps,aes(y=OR,x=reorder(Function,pvalue)))+
  geom_pointrange(mapping=aes(y=OR,ymin=ps_up,ymax=ps_down,color=significance))+
  scale_color_manual(values=c("#8ECFC9","#FA7F6F"))+theme_bw()+
  geom_hline(yintercept = 1,linetype="dotted")+ylim(0,3)+xlab("Function")+
  ylab("Odds ratio")+theme(axis.text.x=element_text(angle=60,hjust=1,vjust=1))
  
#ggplot(data=plt_ps,mapping=aes(y=ratio,x=Function,color=person))+geom_pointrange(mapping=aes(y=ratio,ymin=up,ymax=down))+theme(axis.text.x=element_text(angle=60,hjust=1,vjust=1))+geom_hline(yintercept = 1,linetype="dotted")
dev.off()

out1=paste(out,"_log.pdf",sep="")
pdf(out1)
ggplot(data=plt_ps,aes(y=logOR,x=reorder(Function,pvalue)))+
  geom_pointrange(mapping=aes(y=logOR,ymin=log_ps_up,ymax=log_ps_down,color=significance))+
  scale_color_manual(values=c("#8ECFC9","#FA7F6F"))+theme_bw()+
  geom_hline(yintercept = 0,linetype="dotted")+xlab("Function")+
  ylab(bquote(log[10](OR)))+theme(axis.text.x=element_text(size=14,angle=60,hjust=1,vjust=1),axis.text.y=element_text(size=14))
#ggplot(data=plt_ps,mapping=aes(y=logratio,x=Function,color=person))+geom_pointrange(mapping=aes(y=logratio,ymin=logup,ymax=logdown))+theme(axis.text.x=element_text(angle=60,hjust=1,vjust=1))+geom_hline(yintercept = 0,linetype="dotted")
dev.off()

out2=paste(out,".csv",sep="")
write.table (plt_ps,file =out2, sep ="\t",row.names = FALSE, col.names =T, quote =FALSE)   #??????????????????????????????????????????????????????????????????????????????
