# # 필요한 라이브러리 설치
# install.packages("reshape2")
# install.packages("dplyr")
# install.packages("ggplot2")
# install.packages("openxlsx")

# 필요한 라이브러리 로드
library(reshape2)
library(dplyr)
library(ggplot2)
library(openxlsx)

# 데이터 불러오기 및 컬럼명 정리
file_path <- "C:/Users/user/Desktop/0719 dominance_modify.csv"  # 여기에 파일 경로를 수정하세요
df <- read.csv(file_path)

# 컬럼명 정리
colnames(df) <- c('order', 'RoomTemp', 'Humidity', 'Age', 'Enclosure', 'Time', 
                  'location_pink', 'location_orange', 'location_green', 'location_black', 
                  'location_purple', 'location_navy', 'sum', 'Carton_pink', 
                  'Carton_orange', 'Carton_green', 'Carton_black', 'Carton_purple', 
                  'Carton_navy', 'Unnamed_19', 'Unnamed_20')

# Age 컬럼의 결측값을 제거한 후 int 형식으로 변환
df <- df %>% filter(!is.na(Age))
df$Age <- as.integer(df$Age)

compute_agg_df <- function(enclosure_df) {
  # 데이터를 long-form으로 변환
  long_df <- melt(enclosure_df, id.vars = c('Age', 'Time'), 
                  measure.vars = c('location_pink', 'location_orange', 'location_green', 
                                   'location_black', 'location_purple', 'location_navy'),
                  variable.name = 'Location', value.name = 'Rank')
  
  # Age별, Location별 Rank의 중앙값, 표준편차 계산
  agg_df <- long_df %>% 
    group_by(Age, Location) %>% 
    summarize(median = median(Rank), 
              std = sd(Rank), 
              n = n()) %>% 
    ungroup()
  
  # 신뢰 구간 계산 (95% 신뢰 구간)
  agg_df <- agg_df %>% 
    mutate(ci95_hi = median + 1.96 * (std / sqrt(n)),
           ci95_lo = median - 1.96 * (std / sqrt(n)))
  
  return(agg_df)
}

plot_median_rank_with_confidence_intervals <- function(enclosure_df, title) {
  agg_df <- compute_agg_df(enclosure_df)
  
  p <- ggplot(agg_df, aes(x = Age, y = median, color = Location, group = Location)) +
    geom_line() +
    geom_point() +
    geom_ribbon(aes(ymin = ci95_lo, ymax = ci95_hi), alpha = 0.2) +
    geom_text(aes(label = paste(Location, round(median, 1), sep = ":")), 
              hjust = 1.5, vjust = 0.5, position = position_dodge(width = 0.9)) +
    scale_y_reverse() +
    labs(title = title, x = "Age", y = "Median Rank") +
    theme_minimal() +
    theme(legend.position = "bottom")
  
  return(p)
}

# Enclosure 1부터 5까지의 데이터 필터링 및 결과 저장
enclosures <- unique(df$Enclosure)
all_agg_df <- data.frame()

# PDF 파일로 그래프 저장
pdf("dominance_ranking.pdf", width = 14, height = 8)

for (enclosure in enclosures) {
  enclosure_df <- df %>% filter(Enclosure == enclosure)
  p <- plot_median_rank_with_confidence_intervals(enclosure_df, paste("Enclosure", enclosure, "Median Rank Over Age"))
  print(p)
  enclosure_agg_df <- compute_agg_df(enclosure_df)
  enclosure_agg_df$Enclosure <- enclosure  # Enclosure 컬럼 추가
  all_agg_df <- bind_rows(all_agg_df, enclosure_agg_df)
}

dev.off()

# agg_df 엑셀 파일로 저장
write.xlsx(all_agg_df, 'agg_df.xlsx', row.names = FALSE)
