import tweepy
import urllib3
from bs4 import BeautifulSoup
import time

from dataclasses import dataclass

 

@dataclass

class CountryRecord:
    Country : str
    RecordedTotalCases: int = 0    
    TotalCases: int = 0

    NewCases: int = 0

    TotalDeath: int = 0

    NewDeath: int = 0

    def __str__(self):
        #Worldometer #USA data was updated to 7,590,218 cases (+40183 from yesterday), and 214065 death (+543 from yesterday)
        return "#Worldometer #{} data was updated to {} cases ({} from yesterday), and {} death ({} from yesterday)".format(self.Country, self.TotalCases, self.NewCases, self.TotalDeath, self.NewDeath)



def GetCountryData(content, countryRecord : CountryRecord):
    countryIndex = content.find(countryRecord.Country)
    tr1index = content.rfind("<tr", 0, countryIndex)
    tr2index = content.find("</tr>", countryIndex)

    countryStr = content[tr1index: tr2index+5]

 

    tempLine = countryStr.splitlines()[3]
   
    countryRecord.TotalCases = tempLine[tempLine.find(">") + 1: tempLine.find("</td>")]
 
    tempLine = countryStr.splitlines()[4]

    countryRecord.NewCases = tempLine[tempLine.find(">") + 1: tempLine.find("</td>")].replace (',', '')

    tempLine = countryStr.splitlines()[5]

    countryRecord.TotalDeath = tempLine[tempLine.find(">") + 1: tempLine.find("</td>")].replace (',', '')

    tempLine = countryStr.splitlines()[7]

    countryRecord.NewDeath = tempLine[tempLine.find(">") + 1: tempLine.find("</td>")].replace (',', '')

def PrintTweet(tweetStatus):
    # Authenticate to Twitter

    auth = tweepy.OAuthHandler("***", "************")

    auth.set_access_token("*****", "*************")
 

    # Create API object

    api = tweepy.API(auth)

    # for friend in user.friends():

    #   print(friend.screen_name)

    # Create a tweet
    tweetStatus += " #covid19 #Bot"

    api.update_status(tweetStatus)


countryRecords = [CountryRecord("Israel"), CountryRecord("Brazil"), CountryRecord("India"),
CountryRecord("Russia"), CountryRecord("Colombia"), CountryRecord("Peru"), CountryRecord("Spain"),
CountryRecord("France"), CountryRecord("Italy"), CountryRecord("Germany"), CountryRecord("UK")]
 

while True:

 

    http = urllib3.PoolManager()

    r = http.request('GET', 'https://www.worldometers.info/coronavirus/')

    content2 = r.data.decode("utf-8")

    for record in countryRecords:
        GetCountryData(content2, record)

    tweetStatus = ''
    numUpdated = 0

    for record in countryRecords:
        if (record.RecordedTotalCases == record.TotalCases):
            continue
        else:
            numUpdated +=1
            record.RecordedTotalCases = record.TotalCases
            tweetStatus += str(record)
            tweetStatus += "\n\n"
            if (numUpdated == 2):
                PrintTweet(tweetStatus)
                numUpdated = 0
                tweetStatus = ''  

    if (numUpdated == 0):
        time.sleep (1200)
        continue
    
    PrintTweet(tweetStatus)





