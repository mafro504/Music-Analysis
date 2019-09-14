#import relevant packages
import json
import numpy as np 
import pandas as pd 

#read JSON file in
#update with json file directory location
jsonfile = "/DIRECTORY/sc_data_science_challenge.json"
myfile = open(jsonfile,'r')
mydata = myfile.read()

#parse file by converting to dictionary
skipdata = json.loads(mydata)
#print(skipdata)

#confirm type is dict
typeout=type(skipdata) is dict
print(typeout)

###LOOKING AT DATA###
#access sub-list records by printing associated values with 'data' key
#look at first list and print first item in it
print(skipdata['data'][0][0])

#printed first list in subset
print(skipdata['data'][0])

#create loop to loop through all lists and pull out info
sublists=skipdata['data']
print (sublists)
for list in sublists:
    print (list[4]) #should print rec algorithm name. mostly content-based

#convert dict to pandas dataframe for analysis
#add in column headers as labels
labels = ['ts', 'country_code', 'client_version', 'listening_context', 'recommender_algorithm_name', 'track_id', 'track_genre_category', 'track_upload_date', 'track_duration', 'listen_duration', 'listener_id', 'listener_signup_date', 'listener_top_genre_category', 'listener_prev_month_listening_time', 'listener_pre_month_avg_daily_tracks_listening']
df = pd.DataFrame.from_records(sublists, columns=labels)
#print(df) #828169 rows x 15 cols
#print first 3 records
print(df.iloc[:3])

##EXPLORE COLUMNS##
#count of user listening sessions by client version
print(df["client_version"].value_counts()) 
#204.0.0 most popular version

#count of user listening sessions by listening contet
print(df["listening_context"].value_counts())
#tracks                   478340
#users                    101695
#playlists                91953
#collection               59582
#you                      41961
#stream                   31668
#search                   11232
#charts                    6326
#personal-recommended      5412

#count of user listening sessions by rec algorithm
print(df["recommender_algorithm_name"].value_counts())
#content-based 737843
#collaborative 47225
#hybrid 40754
#fallback 2347

print(df["track_genre_category"].value_counts())
# HipHop & R&B          439394
# Dance & Electronic    244999
# Pop                    59622
# Rock                   37748
# World                  25095
# Reggae                  5687
# Speech                  4488
# Latin                   2931
# Classical               2807
# Jazz                    1846
# Metal                   1518
# Country                 1123
# Unknown                  911

print(df["listen_duration"].value_counts())
# 0          3640
#-17          883 #how can listen duration be negative? maybe skip before it starts playing?

#view what data type each column is
print(df.dtypes)
# ts                                                 int64
# country_code                                      object #2 letter code
# client_version                                    object 
# listening_context                                 object #categorical names
# recommender_algorithm_name                        object #categorical names
# track_id                                          object
# track_genre_category                              object #categorical names
# track_upload_date                                  int64
# track_duration                                     int64
# listen_duration                                    int64
# listener_id                                       object
# listener_signup_date                               int64
# listener_top_genre_category                       object #categorical names
# listener_prev_month_listening_time               float64
# listener_pre_month_avg_daily_tracks_listening    float64


# creating dictionaries to map categorical values to numerical values
listeningcontext = {'tracks': 1,'users': 2, 'playlists': 3, 'collection': 4, 'you': 5, 'stream': 6, 'search': 7, 'charts': 8, 'personal-recommended': 9}  
algorithm = {'content-based': 1,'collaborative': 2, 'hybrid': 3, 'fallback': 4}
trackgenre = {'HipHop & R&B': 1, 'Dance & Electronic': 2, 'Pop': 3, 'Rock': 4, 'World': 5, 'Reggae': 6, 'Speech': 7, 'Latin': 8, 'Classical': 9, 'Jazz': 10, 'Metal': 11, 'Country': 12, 'Unknown': 13}

# traversing through dataframe to replace each categorical item with its numerical value where key matches
df.listening_context = [listeningcontext[item] for item in df.listening_context] 
df.recommender_algorithm_name = [algorithm[item] for item in df.recommender_algorithm_name] 
df.track_genre_category = [trackgenre[item] for item in df.track_genre_category] 

#check if conversions worked
print(df['listening_context'][:15])
print(df['recommender_algorithm_name'][:15])
print(df['track_genre_category'][:15])

#see correlation matrix between all columns
corrmat=df.corr()
print(corrmat)
#too large to view in output, so export
#update with relevant directory
corrmat.to_csv("DIRECTORY/correlationmatrix.csv")


#see correlation between all columns and how quick listener moves on to next song (listen_duration)
corr=df[df.columns[1:]].corr()['listen_duration'][:]
print(corr)

# listening_context                                0.057455 **
# recommender_algorithm_name                      -0.013432
# track_genre_category                             0.048295 **
# track_upload_date                               -0.050453 **
# track_duration                                   0.497346 **
# listen_duration                                  1.000000
# listener_signup_date                            -0.028216
# listener_prev_month_listening_time               0.056944 **
# listener_pre_month_avg_daily_tracks_listening   -0.045343

##Highest correlations are:
# track_duration                                   0.497346
# listening_context                                0.057455
# listener_prev_month_listening_time               0.056944
# track_upload_date                               -0.050453

#create subset df where listen duration <=0 and see if correlation results differ
subsetdf = df[df['listen_duration'] <= 0]
print(subsetdf['listen_duration'][:15])

#correlation between listen duration <=0 and all columns
corrsub=subsetdf[subsetdf.columns[1:]].corr()['listen_duration'][:]
print(corrsub)

# listening_context                                0.022406
# recommender_algorithm_name                      -0.012165
# track_genre_category                             0.017693
# track_upload_date                                0.032453 
# track_duration                                  -0.000534
# listen_duration                                  1.000000
# listener_signup_date                             0.099070 **
# listener_prev_month_listening_time              -0.154236 **
# listener_pre_month_avg_daily_tracks_listening   -0.020518

##Highest correlations are:
# listener_prev_month_listening_time              -0.154236 **
# listener_signup_date                             0.099070 **


##look at the values of each column with new subset df
#count of user listening sessions by listening contet
print(subsetdf["listening_context"].value_counts())
# 4    4404   collection
# 1    2653   tracks 

#count of user listening sessions by rec algorithm
print(subsetdf["recommender_algorithm_name"].value_counts())
# 1    7424   content-based
# 2     622   collaborative

print(subsetdf["track_genre_category"].value_counts())
# 1     4859  HipHop & R&B
# 2     2823  Dance & Electronic

#people skipping tracks when they are:
##listening in the 'collection' and 'tracks' sections of the soundcloud app
##recommended a song from the content-based algorithm
##when they are listening to hip hop & r&b and dance & electronic 