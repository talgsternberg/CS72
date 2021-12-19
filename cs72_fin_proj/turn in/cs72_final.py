# Final Project By Tal Sternberg (tal.g.sternberg.23@dartmouth.edu)
# Description: Using a Kaggle dataset for covid-19 vaccine related tweets, I will calculate the sentiment
# of verified users over time and by locations of interest (India, USA, UK, Canada, China)


import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date
from geopy.geocoders import Nominatim
nm = Nominatim(user_agent = "geopy.geocoders.options.default_user_agent")


# function for calulating the net senitment of a given input text
def calculate_sentiment(text):
    # init values
    anger = 0
    anticipation = 0
    disgust = 0
    fear = 0
    joy = 0
    negative = 0
    positive = 0
    sadness = 0
    surprise = 0
    trust = 0

    #open and read NRC
    NRC = open("NRC-Emotion-Lexicon-Wordlevel-v0.92.txt").readlines()
    count = len(open("NRC-Emotion-Lexicon-Wordlevel-v0.92.txt").readlines(  ))

    # generate a list of words at lowercase from text input
    words = text.strip().split()
    for word in words:
        word = word.lower()

        # now compare each word to the NRC
        for lineNRC in range(0, count-10):
          if word in (NRC[lineNRC].strip('\n').split('\t')):

            # each line for a word
            NRC_line_split_1 = NRC[lineNRC].strip('\n').split('\t')
            NRC_line_split_2 = NRC[lineNRC+1].strip('\n').split('\t')
            NRC_line_split_3 = NRC[lineNRC+2].strip('\n').split('\t')
            NRC_line_split_4 = NRC[lineNRC+3].strip('\n').split('\t')
            NRC_line_split_5 = NRC[lineNRC+4].strip('\n').split('\t')
            NRC_line_split_6 = NRC[lineNRC+5].strip('\n').split('\t')
            NRC_line_split_7 = NRC[lineNRC+6].strip('\n').split('\t')
            NRC_line_split_8 = NRC[lineNRC+7].strip('\n').split('\t')
            NRC_line_split_9 = NRC[lineNRC+8].strip('\n').split('\t')
            NRC_line_split_10 = NRC[lineNRC+9].strip('\n').split('\t')

            # update emotions
            anger += int(NRC_line_split_1[2])
            anticipation += int(NRC_line_split_2[2])
            disgust += int(NRC_line_split_3[2])
            fear += int(NRC_line_split_4[2])
            joy += int(NRC_line_split_5[2])
            negative += int(NRC_line_split_6[2])
            positive += int(NRC_line_split_7[2])
            sadness += int(NRC_line_split_8[2])
            surprise += int(NRC_line_split_9[2])
            trust += int(NRC_line_split_10[2])

            sentiment = [anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust]

            # subtract the negative values, add the positive
            net_sentiment_value = trust + anticipation - disgust - fear + joy - negative + positive - sadness + surprise - anger

            return net_sentiment_value


#############################################################################################
# function to calc number of days between 2 given dates (for plotting purposes)
def numOfDays(date1, date2):
    return (date2-date1).days

def calc_sent_verified(times, sentiments, dict, dict_location_count):
    ind = 0
    with open('vaxx_tweets.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # loop througn csv
        for row in reader:
            ind += 1
            if (ind % 30 == 0):
                if (row['user_verified'] == 'True'):
                    # append to sentiment list
                    sent = calculate_sentiment(row['text'])
                    # if there is no sentiment assign it zero
                    if (sent == 'None'):
                        sent = 0
                    sentiments.append(sent)
                    # get the date breakdown
                    date_val = str(row['date'])
                    date_alone = date_val.split(' ')
                    date_day = date_alone[0].split('-')
                    year = int(date_day[0])
                    month = int(date_day[1])
                    day = int(date_day[2])


                    # take day zero to be 2020-12-13
                    # append to dates list
                    date1 = date(2020,12,13)
                    date2 = date(year,month,day)
                    days_since = numOfDays(date1, date2)
                    times.append(days_since)

                    if(nm.geocode(row['user_location']) and sent):
                        place, (lat, lng) = nm.geocode(row['user_location'])
                        country = ""
                        if (place.split()[-1] == "Kingdom" or place.split()[-1] == "States" or place.split()[-1] == "Rica" or place.split()[-1] == "Verde"):
                            country = place.split()[-2] + " " + place.split()[-1]
                        elif(place.split()[-1] == "Emirates" ):
                            country = place.split()[-3] + " " + place.split()[-2] + " " + place.split()[-1]
                        else:
                            country = place.split()[-1]
                        # add to dict if not contient only
                        if (country != "America" or country != "Asia" or country != "Asia"):
                            if(country in dict.keys()):
                                dict[country] += sent
                                dict_location_count[country] += 1

                            else:
                                dict[country] = sent
                                dict_location_count[country] = 1







# run the function and fill the lists to plot
times = []
sentiments = []
location_scores = {}
location_counts = {}

calc_sent_verified(times, sentiments, location_scores, location_counts)


# plot for sentiment versus time
plt.scatter(times, sentiments)
plt.title("Sentiment Value of Verified Twitter Users Over Time")
plt.xlabel("Days Since 2020-12-14")
plt.ylabel("Sentiment Val")
plt.show()

countries_of_interest = {}

count_china = 0
count_india = 0
count_us = 0
count_uk = 0
count_canada = 0

# generate a dict of scores for the following countries of interest:
for key in location_scores:
    if (key == "United Kingdom"):
        countries_of_interest[key] = location_scores[key]
        count_uk = location_counts[key]
    elif(key == "United States"):
        countries_of_interest[key] = location_scores[key]
        count_us = location_counts[key]
    elif(key == "India"):
        countries_of_interest[key] = location_scores[key]
        count_india = location_counts[key]
    elif(key == "Canada"):
        countries_of_interest[key] = location_scores[key]
        count_canada = location_counts[key]
    elif (key == "中国"):
        countries_of_interest["China"] = location_scores[key]
        count_china = location_counts[key]



# bar for TOTAL sentiment of countries of interest
keys = countries_of_interest.keys()
values = countries_of_interest.values()
plt.bar(keys, values)
plt.title("Total Sentiment of Tweets From Countries of Interest")
plt.show()

print("China :  " + str(count_china))
print("UK :  " + str(count_uk))
print("USA :  " + str(count_us))
print("India :  " + str(count_india))
print("Canada :  " + str(count_canada))



# divide the values by the number of tweets per country
avg_countries_of_interest = {}
for key in countries_of_interest:
    if (key == "United Kingdom"):
        avg_countries_of_interest[key] = (countries_of_interest[key])/(count_uk)
    elif (key == "United States"):
        avg_countries_of_interest[key] = (countries_of_interest[key])/(count_us)
    elif (key == "India"):
        avg_countries_of_interest[key] = (countries_of_interest[key])/(count_india)
    elif (key == "Canada"):
        avg_countries_of_interest[key] = (countries_of_interest[key])/(count_canada)
    elif (key == "China"):
        avg_countries_of_interest[key] = (countries_of_interest[key])/(count_china)

print("averages: ")
print(avg_countries_of_interest)


# bar for AVERAGE sentiments of countries of interest
keys = avg_countries_of_interest.keys()
values = avg_countries_of_interest.values()
plt.bar(keys, values)
plt.title("Average Sentiment of Tweets From Countries of Interest")
plt.show()
