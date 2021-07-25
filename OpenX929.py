from selenium import webdriver


#######################################################################################################################
#This is to get the song list from the website, and save it to a list
#######################################################################################################################


my_url = "https://www.x929.ca/recently-played/"
driver = webdriver.PhantomJS(executable_path = 'C:\\Users\\hitma\\PycharmProjects\\SpotifyX929_2\\phantomjs-2.1.1-windows\\bin\\phantomjs')
driver2 = webdriver.Chrome

driver.get(my_url)

#Turns out all of the day's songs are hidden behind the "more" button. Guess we will click it. Takes 17 clicks to expand
#An entire day's worth of songs.
#So, click that button 17 damn times!

for i in range(17):

    elem = driver.find_elements_by_link_text(text="More")
    if len(elem) > 0:
        elem[0].click()

#so all the songs are now loaded, time to grab them

p_element = driver.find_element_by_xpath("//div[contains(@class,'songs')]")
#p_element = driver.find_element_by_id(id_="theContent") ##the old find by for the song list
# p_element = driver.find_element_by_partial_link_text(link_text="Recently Played")

raw_song_list = str(p_element.text)

edited_song_list = [""] * len(raw_song_list)
letter_Counter = 0

#######################################################################################################################
#time to modify some strings, get this on a list!
#######################################################################################################################

for i in range(len(raw_song_list)):



    if raw_song_list[i] != "\n":
        edited_song_list[letter_Counter] = edited_song_list[letter_Counter] + raw_song_list[i]

    else:
        letter_Counter = letter_Counter + 1

#######################################################################################################################
#alright, so that is in a list and the strings make sense. Now we wanna get rid of the junk strings we dont need
#first 10 lines are all garbage
#######################################################################################################################

edited_song_list = edited_song_list[10::]

#######################################################################################################################
#awesome, you're doing great. Now lets take that song list, and separate it into a list of lists for song, artist, and time it was last played
#######################################################################################################################

songs_for_Excel = [edited_song_list[i:i + 3] for i in range(0, len(edited_song_list), 3)]

#######################################################################################################################
#time to put that shit in an excel spreadsheet. Last step, lets try this
#######################################################################################################################

import pandas as pd

excel_Songs_name_path = "C:\\Users\\hitma\\PycharmProjects\\x929_Song_List.xlsx"

writer = pd.ExcelWriter(excel_Songs_name_path, engine='xlsxwriter')

##Update Data frames with song lists
recent_pull_List = pd.DataFrame(songs_for_Excel)
#recent_pull_List.columns = ["Time" , "Artist" , "Song Title"] ##old way of writing data, time stamp seems to have swapped locations and is now last in the list
recent_pull_List.columns = ["Artist" , "Song Title", "Time"] ##added to swap time and artist as website seems to have re-arranged how their data is laid out

old_SongList = pd.read_excel(excel_Songs_name_path, sheet_name="All Songs")

newSongList = old_SongList
newSongList= newSongList.append(recent_pull_List, sort=False)


songPlayCounts = newSongList.pivot_table(index=['Artist' , 'Song Title'] , aggfunc='size')
songPlayCounts.columns = ["Artist","Song Title", "Play Count"]

duplicates_Removed = newSongList
duplicates_Removed.drop_duplicates(subset="Song Title")
del duplicates_Removed["Time"]

#section for writing to sheets
sheets_to_Write = {'All Songs': newSongList, 'Song Play Counts': songPlayCounts, "Unique Songs": duplicates_Removed}

for sheet_name in sheets_to_Write.keys():
    if sheet_name == "Song Play Counts":
        sheets_to_Write[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    else:
        sheets_to_Write[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

writer.save()

# old_SongList.to_excel(excel_Songs_name_path , index=False)
# duplicateSongs.to_excel(excel_Songs_name_path , index=False , sheet_name="duplicates")
