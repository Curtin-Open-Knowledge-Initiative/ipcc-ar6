library(tidyverse)
library(tidytext)


#Import RIS files into named list, convert to dataframe
path = "data/scholarcy/RIS"

rd.files = list.files(path = path,
                     pattern ='*.ris',
                     full.names = TRUE)

rd.names <- list.files(path = path,
                       pattern ='*.ris')
rd.names <- str_remove(rd.names, pattern = ".ris")

rd.files <- set_names(rd.files, rd.names)

df <- rd.files %>%
  map(readLines) %>%
  map_dfr(as_tibble, .id = "Report_part") %>%
  rename("RIS" = "value")

rm(path, rd.files, rd.names)

# Extract DOIs
df_processed <- df %>%
  # select all lines with field DO or string 'doi'
  filter(str_detect(RIS, 'DO  - |doi')) %>%
  filter(str_detect(RIS, '10\\.')) %>%
  # split strings on whitespace
  mutate(RIS = str_split(RIS, '\\s')) %>%
  # get each substring into a row 
  unnest_longer(RIS) %>%
  # replace url-encoding for '/'
  mutate(RIS = str_replace(RIS, '%2F', '\\/')) %>%
  # filter on DOI string'10.' at beginning of string or after '/'
  filter(str_detect(RIS, '^10\\.|\\/10\\.'))


# Clean DOIs
df_processed2 <- df_processed %>%
  #remove everything before first '10.' to get rid of url prefixes
  mutate(RIS = str_replace(RIS, '^.*?10\\.', '10\\.')) %>%
  # remove single trailing punctuation marks
  mutate(RIS = str_remove(RIS, '[[:punct:]]?$')) %>%
  # remove string with only DOI prefix, i.e. not containing '/'
  filter(str_detect(RIS, '\\/')) %>%
  # remove string with only one character after DOI suffix, e.g. '10.1016/J'
  filter(!str_detect(RIS, '^[^\\/]*\\/.$'))

  
  