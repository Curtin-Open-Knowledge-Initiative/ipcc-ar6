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
df_dois <- df %>%
  # select all lines with field DO or string 'doi'
  filter(str_detect(RIS, regex('DO  - |doi', ignore_case = TRUE))) %>%
  #detect presence of actual doi string, to exclude e.g author names containing 'doi'
  filter(str_detect(RIS, '10\\.')) %>%
  # split strings on whitespace
  mutate(RIS = str_split(RIS, '\\s')) %>%
  # get each substring into a row 
  unnest_longer(RIS) %>%
  # replace url-encoding for '/'
  mutate(RIS = str_replace(RIS, '%2F', '\\/')) %>%
  # filter on DOI string'10.' at beginning of string or after '/'
  filter(str_detect(RIS, '^10\\.|\\/10\\.')) %>%
  rename(dois = RIS)

# Clean DOIs
df_dois <- df_dois %>%
  #remove everything before first '10.' to get rid of url prefixes
  mutate(dois = str_replace(dois, '^.*?10\\.', '10\\.')) %>%
  # remove trailing punctuation marks
  mutate(dois = str_remove(dois, '[[:punct:]]*$')) %>%
  # remove string with only DOI prefix, i.e. not containing '/'
  filter(str_detect(dois, '\\/')) %>%
  # remove string with only one character after DOI suffix, e.g. '10.1016/J'
  filter(str_detect(dois, '^[^\\/]*\\/.$')) %>%
  # remove duplicate '10.' at beginning of DOI string
  mutate(dois = str_replace(dois, '^.*?(10\\.)+', '10\\.'))

#write to file
write_csv(df_dois, "data/IPCC_AR6_WGII_dois.csv")