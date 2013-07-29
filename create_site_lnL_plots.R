fn = commandArgs(TRUE)
d = read.table(fn, header=TRUE, sep="\t");
parsimony.discriminates = d$PTree1 != d$PTree2;
pdf(paste(fn, '-diff-by-site.pdf', sep=""));
diff = d$LTree1 - d$LTree2
plot(d$Site, diff, 
     xlab="Site", ylab="lnL(T1) - lnL(T2)",
     type="p",
     main=sprintf("Difference in lnL across sites.\nTotal lnL(T1) - lnL(T2) = %g ", sum(diff))
     );
points(d$Site[parsimony.discriminates],
    diff[parsimony.discriminates],
    pch=20,
    col="red");
abline(h=0);
dev.off();

pdf(paste(fn, '-scatterplot.pdf', sep=""));
plot(d$LTree1, d$LTree2, 
     xlab="lnL(T1)", ylab="lnL(T2)",
     type="p",
     main=sprintf("Scatterplot of site lnL on 2 trees.\nTotal lnL(T1) - lnL(T2) = %g ", sum(diff))
     );
points(d$LTree1[parsimony.discriminates],
    d$LTree2[parsimony.discriminates],
    pch=20,
    col="red");
abline(a=0, b=1); # equality line
dev.off();

mabs = max(abs(max(diff)), abs(min(diff)))
pdf(paste(fn, '-diff-histogram.pdf', sep=""));
hist(diff,
    seq(-mabs, mabs, mabs/75),
    xlab=c("lnL(T1) - lnL(T2)"),
    main="Distribution of the differences in lnL scores");
dev.off();

mabs = max(abs(max(diff)), abs(min(diff)))
pdf(paste(fn, '-diff-histogram-cropped.pdf', sep=""));
hist(diff,
    seq(-mabs, mabs, mabs/75),
    xlab=c("lnL(T1) - lnL(T2)"),
    ylim=c(0,300),
    main="Distribution of the differences in lnL scores cropped at 300");
dev.off();
