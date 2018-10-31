library(deldir)
library(kknn)


df1 = read.csv('./Python/hk_housing_web/df1.csv',header = T) ## BLDG_GOV
df2 = read.csv('./Python/hk_housing_web/df2.csv',header = T) ## Temp
df1 = distinct(df1)
df2 = distinct(df2)
summary(df2)
plot(df2$cor_x,df2$cor_y)

info_bldg = deldir(df2$cor_x,df2$cor_y)
df2[1] = NA

nrow(df2)
nrow(distinct(df2,df2$cor_x,df2$cor_y))

##Combine 2 data sets into a data frame to be impluted
df3 = rbind(df1,df2)
impluted_bldg = kNN(df3, k = 1)
df3 = distinct(df3)

# write.csv(impluted_bldg,'./Python/hk_housing_web/impluted_bldg.csv',row.names = F)

df4 = impluted_bldg[impluted_bldg$GEO_REFNO_imp ==T,1:3]
df4 = distinct(df4) 
# write.csv(df4,'./Python/hk_housing_web/impluted_temp.csv',row.names = F)

## 
df5 = left_join(df4,df1, by = 'GEO_REFNO')
df2_1 = read.csv('./Python/hk_housing_web/df2.csv',header = T) ## Temp
df2_1 = distinct(df2_1)
df5 = cbind(df5,df2_1$GEO_REFNO)

colnames(df5) = c("GEO_REFNO", "cor_x.centa" ,  "cor_y.centa"  , "cor_x.gov","cor_y.gov","GEO_REFNO_CENTA")
# write.csv(df5,'./Python/hk_housing_web/impluted_compare.csv',row.names = F)
plot(df5$cor_x.centa[100:200],df5$cor_y.centa[100:200],col = 'red',
     title("Imputed Centa Coor. to Goverments Coor."),pch = 16)
points(df5$cor_x.gov[100:200],df5$cor_y.gov[100:200],col = 'blue')
legend("topleft", c("Centa Coor.", "Gov Coor."),
       pch = 16, col = c("red", "blue"), cex = .75)


library('rgdal')
library('spdplyr')
library('geojsonio')
library('rmapshaper')
library('leaflet')

#######################
df_shp = readOGR(dsn = './GIS/BG1000_wgs/Bldg_2014_filtered',verbose = FALSE)

## Filter all useless data from shape file and remove NA from Address
# df_shp = shp %>%
#   select(.,-c('BLDG_CHNNA','ADDR_TYPE','SITE_CODE','ST_CHNNAM','ST_CODE')) %>% 
#   filter(.,!is.na(BLDG_ENGNA))

## Covert all Address toupper
# df_shp@data$BLDG_ENGNA =toupper(df_shp@data$BLDG_ENGNA)
# temp = df_shp@data


## Load web scrapped data

library(dplyr)
library(tidyr)
centa_info = read.csv('Python/hk_housing_web/centa_info_CLEANED.csv',header = T)
centa_last = read.csv('Python/hk_housing_web/centa_last_CLEANED.CSV',header = T)

temp = centa_last %>% 
          group_by(.,bldg_code) %>% 
          summarise(.,'Avg_Saleable_Area' = round(mean(Saleable_Area)),
                    'Median_Price_Per_Sqft' = round(median(Price_Per_Sqft)))

df_info = df_info %>% 
            select(.,bldg_code,GEO_REFNO) %>% 
            distinct()

centa_shp = left_join(centa_info,df_info,by = "bldg_code")
colnames(centa_shp)[12] = 'GEO_REFNO_CENTA'

centa_shp = left_join(centa_shp, temp,by = "bldg_code")

centa_shp = centa_shp %>% 
              select(.,c(1,2,4:9,11:14)) %>% 
              filter(.,Age >0)
write.csv(centa_shp,file = 'Python/hk_housing_web/centa_shp.csv',row.names = F)

## Try joining address from BLDG_ENGNA from GOV to CENTA Phase, Name
df_info=read.csv('./GIS/BG1000_wgs/centa_info.csv',header = T)

df_info = distinct(df_info)
a = inner_join(df_shp@data,df_info[c(3,6:10)],by = "BLDG_ENGNA") 

## Join with address phase name
temp = df_shp@data
df_years = read.csv('./GIS/BG1000_wgs/df_years.csv',header = T)
b = dplyr::inner_join(df_shp@data,df_years, by = "BLDG_ENGNA")

write.csv(file = 'bldg_filtered_data.csv',x = temp,row.names = FALSE)


## Join with impluted_bldg 


centa_shp_data = left_join(df5,centa_shp,by = "GEO_REFNO_CENTA" )
# centa_shp_data$GEO_REFNO = factor(centa_shp_data$GEO_REFNO)
centa_shp_data$GEO_REFNO = as.character(centa_shp_data$GEO_REFNO)
# df_shp@data$GEO_REFNO = as.character(df_shp@data$GEO_REFNO)
class(centa_shp_data$GEO_REFNO)
class(df_shp@data$GEO_REFNO)
newobj <- sp::merge(df_shp, centa_shp_data)

temp = df_shp@data
temp$GEO_REFNO = as.character(temp$GEO_REFNO)

df_shp@data = left_join(temp,centa_shp_data ,by = 'GEO_REFNO')









