library(tidyverse)
library(gridExtra)


data <- data.frame(
  x = c(0, 1, 2, 3, 4),
  y = c(1, 0, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 1, 0),
  Class = c("No", "No", "No", "No","No",
            "Mild", "Mild", "Mild","Mild", "Mild",
            "Moderate", "Moderate", "Moderate", "Moderate", "Moderate",
            "Severe", "Severe", "Severe", "Severe", "Severe")
)

data$Class <- factor(data$Class, levels = c("No", "Mild", "Moderate", "Severe"))


p1<-ggplot(data, aes(x, y, color=Class)) +
  geom_step(direction = "hv") +
  scale_y_continuous(breaks = seq(0, 1, 0.5)) +
  theme_minimal() +
  labs(x="Input", y="Degree of Membership") + 
  facet_wrap(~ Class, ncol=1) + 
  theme(legend.position = "none")


# data0 <- data.frame(
#   x = c(0, 2, 3, 4, 5),
#   y = c(1, 0, 0, 0, 0),
#   Class = "No"
# )

# data <- data.frame(
#   x = c(0, 1, 2, 3, 4, 5),
#   y = c(0, 1, 1, 0, 0, 0),
#   Class = "Mild"
# )
# data2 <- data.frame(
#   x = c(0, 1, 2, 3, 4, 5),
#   y = c(0, 0, 0, 1, 1, 0),
#   Class = "Moderate"
# )
# data3 <- data.frame(
#   x = c(0, 1, 2, 3, 4, 5),
#   y = c(0, 0, 0, 0, 1, 1),
#   Class = "Severe"
# )
data0 <- data.frame(
  x = c(0, 1, 5),
  y = c(1, 0, 0),
  Class = "No"
)

data <- data.frame(
  x = c(0, 1, 3, 5),
  y = c(0, 1, 0, 0),
  Class = "Mild"
)

data2 <- data.frame(
  x = c(0, 1, 3, 5),
  y = c(0, 0, 1, 0),
  Class = "Moderate"
)

data3 <- data.frame(
  x = c(0, 3, 5),
  y = c(0, 0, 1),
  Class = "Severe"
)

combined_data <- rbind(data0, data, data2, data3)
combined_data$Class <- factor(combined_data$Class, levels = c("No", "Mild", "Moderate", "Severe"))

ggplot(combined_data, aes(x, y, color = Class)) +
  geom_line() +
  scale_y_continuous(breaks = seq(0, 1, 0.5)) +
  theme_minimal() +
  labs(x="Input", y=NULL) + 
  facet_wrap(~ Class, ncol=1) + 
  theme(legend.position = "none") + theme(axis.text.y=element_blank(), 
                                          axis.ticks.y=element_blank())

p2<- ggplot(combined_data, aes(x, y, color = Class)) +
  geom_line() +
  scale_y_continuous(breaks = seq(0, 1, 0.5)) +
  theme_minimal() +
  labs(x="Input", y=NULL) + 
  facet_wrap(~ Class, ncol=1) + 
  theme(legend.position = "none") + theme(axis.text.y=element_blank(), 
                                          axis.ticks.y=element_blank())

data0 <- data.frame(
  x = c(0, 1, 5),
  y = c(1, 0, 0),
  Class = "No"
)

data <- data.frame(
  x = c(0, 1, 4, 5),
  y = c(0, 1, 0, 0),
  Class = "Mild"
)

data2 <- data.frame(
  x = c(0, 3, 5),
  y = c(0, 1, 0),
  Class = "Moderate"
)

data3 <- data.frame(
  x = c(0, 2, 5),
  y = c(0, 0, 1),
  Class = "Severe"
)

combined_data <- rbind(data0, data, data2, data3)
combined_data$Class <- factor(combined_data$Class, levels = c("No", "Mild", "Moderate", "Severe"))

ggplot(combined_data, aes(x, y, color = Class)) +
  geom_line() +
  scale_y_continuous(breaks = seq(0, 1, 0.5)) +
  theme_minimal() +
  labs(x="Input", y=NULL) + 
  facet_wrap(~ Class, ncol=1) + 
  theme(legend.position = "none") + theme(axis.text.y=element_blank(), 
                                          axis.ticks.y=element_blank())

p3<- ggplot(combined_data, aes(x, y, color = Class)) +
  geom_line() +
  scale_y_continuous(breaks = seq(0, 1, 0.5)) +
  theme_minimal() +
  labs(x="Input", y=NULL) + 
  facet_wrap(~ Class, ncol=1) + 
  theme(legend.position = "none") + theme(axis.text.y=element_blank(), 
                                          axis.ticks.y=element_blank())

grid.arrange(p1, p2, p3, ncol = 3)
