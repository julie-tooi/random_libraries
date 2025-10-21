library("ggplot2")
library("dplyr")

path_to_len_stats <- "len_collection_T7_HH_HDV"
len_distribution <- read.csv(path_to_len_stats, header = FALSE)

len_distribution <- len_distribution %>% dplyr::rename(sample = V1, 
                                                length = V2, 
                                                read_number = V3)

ggplot(len_distribution, aes(x = length, y = read_number)) +
  geom_col()+
  facet_wrap(~sample)+
  scale_x_continuous(name="Read length", limits = c(-1,75))+
  scale_y_continuous(name="Number of reads")+
  theme_bw()
