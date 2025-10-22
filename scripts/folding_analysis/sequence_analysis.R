library("ggplot2")
library("dplyr")
library("tidyr")
library("ggseqlogo")
library("DiffLogo")

# read fasta files for two selected samples
path_to_seqs_sample_1 <- "sample1_inserts_i50_51.fasta"
path_to_seqs_sample_2 <- "sample2_inserts_i50_51.fasta"

# collect sequences and plot logo per sample (full sequence)
sample_1_name = "R2-2"
seqs_sample_1 <- readDNAStringSet(path_to_seqs_sample_1)
seqs_char_sample_1 <- as.character(seqs_sample_1)
ggseqlogo(seqs_char_sample_1, method = "prob")

sample_2_name = "R3"
seqs_sample_2 <- readDNAStringSet(path_to_seqs_sample_2)
seqs_char_sample_2 <- as.character(seqs_sample_2)
ggseqlogo(seqs_char_sample_2, method = "prob")

# difference logo
seqs_pwm_sample_1 <- getPwmFromFastaFile(path_to_seqs_sample_1)
seqs_pwm_sample_2 <- getPwmFromFastaFile(path_to_seqs_sample_2)

diffLogoFromPwm(seqs_pwm_sample_2, seqs_pwm_sample_1)


# cluster sequences based on k-mer frequency
# prepare targets for clustering
path_to_targets <- "R2-2_R3_only_targets.csv"
targets_sequences <- read.csv(path_to_targets, header = FALSE)

targets_sequences <- targets_sequences %>% dplyr::rename(sample = V1, target_seq = V2)

sample_1_targets <-  targets_sequences %>% filter(sample == "R2-2") %>% pull(target_seq)
sample_1_targets <- DNAStringSet(sample_1_targets)

sample_2_targets <- targets_sequences %>% filter(sample == "R3") %>% pull(target_seq)
sample_2_targets <- DNAStringSet(sample_2_targets)

# clustering
k <- 2
kmer_table_sample_1 <- oligonucleotideFrequency(sample_1_targets, width = k)
kmer_table_sample_2 <- oligonucleotideFrequency(sample_2_targets, width = k)

sample_1_df <- as.data.frame(kmer_table_sample_1)
sample_1_df$group <- "R0"

sample_2_df <- as.data.frame(kmer_table_sample_2)
sample_2_df$group <- "R1"

combined_df <- rbind(sample_1_df, sample_2_df)

# PCA and visualization of top 10 000 sequences
pca <- prcomp(combined_df[, -ncol(combined_df)], scale. = TRUE)

fviz_pca_ind(pca,
             geom.ind = "point",
             col.ind = combined_df$group,
             #palette = c("blue", "green", "red"),
             addEllipses = TRUE, ellipse.level=0.8,
             legend.title = "Sample",
             select.ind = list(contrib = 10000),
             title = "PCA of DNA Sequences (2-mer)")+
  scale_color_brewer(palette="Set2") 
