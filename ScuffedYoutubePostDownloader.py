import requests
from bs4 import BeautifulSoup
import json
import filetype

# define the URLs to scrape
#https://chromewebstore.google.com/detail/link-grabber/caodelkhipncidmoebgbbeemedohcdma
urls = r"D:\\SYPD\\Input URLS.txt"
# MUST BE IN A TEXT DOCCUMENT. VERY IMPORTANT
# CAN NOT BE JUST A URL. DOES NOT WORK LIKE THAT.

Debug = False
raw = r"D:\\SYPD\\Raw.txt"#Part of Debugging
important = r"D:\\SYPD\\important.json"#Part of Debugging


# leave blank to output in the same directory as the .py file
output_directory = r"D:\\SYPD\\"#Where the text files and images get written

                    
def write_json(data, file_name):#random function I stole from ChatGPT
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


with open(urls, "r", encoding="UTF-8") as temp:#get all the URLS
    urls = temp.readlines() 

for Post_Number, URL in enumerate(urls):
    URL = URL.strip()
    if Debug:
        with open(raw, "w") as file:#reset the file
            pass

        


    # make a GET request to the URL
    response = requests.get(URL)

    # check if the request was successful
    if response.status_code == 200:
        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # find all the text elements in the HTML tree
        texts = soup.find_all(text=True)

        # loop through the text elements and print them
        for text in texts:
            # strip any leading or trailing whitespace
            text = text.strip()

            # skip any empty strings
            if text == "":
                continue

            # print the text
            if Debug:
                with open(raw, "a", encoding="UTF-8") as file:
                    file.write(text + "\n\n")
            
            if "var ytInitialData = " in text:#if the thing is the thing we want, write it to the json for fun
                text = text.replace("var ytInitialData = ", "").strip(";")
                YTjson = json.loads(text)
                if Debug:
                    write_json(YTjson, important)
    else:
        # print an error message if the request failed
        print(f"Request failed with status code {response.status_code}")

    #ok I now have a lovely Dictionary full of torment and useless stuff

    #Going through to get the text of the post
    DiggingThroughRecurse = [#Why_Must_They_Have_So_Many_Recursed_Lists_And_Dictionaries
        "contents",
        "twoColumnBrowseResultsRenderer",
        "tabs",
        0,
        "tabRenderer",
        "content",
        "sectionListRenderer",
        "contents",
        0,
        "itemSectionRenderer",
        "contents",
        0,
        "backstagePostThreadRenderer",
        "post",
        "backstagePostRenderer",
        "contentText",
        "runs"
    ]

    digging = dict(YTjson)
    for index in DiggingThroughRecurse:
        digging = digging[index]
    Post_Text = digging#Finally
    #Now to do it again for the Post ID because im too lazy to extract it from the URL and I love tormenting myself

    DiggingThroughRecurse = [#Why_Must_They_Have_So_Many_Recursed_Lists_And_Dictionaries
        "contents",
        "twoColumnBrowseResultsRenderer",
        "tabs",
        0,
        "tabRenderer",
        "content",
        "sectionListRenderer",
        "contents",
        0,
        "itemSectionRenderer",
        "contents",
        0,
        "backstagePostThreadRenderer",
        "post",
        "backstagePostRenderer"
    ]

    digging = dict(YTjson)#make a copy? idk if this actually does anything
    for index in DiggingThroughRecurse:#Using a list because I think this is easier
        digging = digging[index]#That way I can check every level of recursion
    Post_ID = digging["postId"]#Nab the Post ID (Thank god its close by)
    Post_Text = digging["contentText"]["runs"]#Nab the text
    Publish_Time_Text = digging["publishedTimeText"]["runs"][0]["text"]
    try:
        Images = digging["backstageAttachment"]
        try:
            Images = Images["postMultiImageRenderer"]["images"]#If there are multiple get them
        except:
            Images = [Images]#Otherwise put it by itself in a list so I don't need to change my further code
    except:
        Images = None

    #round 2, FIGHT
    DiggingThroughRecurse = [
        "actionButtons",
        "commentActionButtonsRenderer",
        "likeButton",
        "toggleButtonRenderer",
        "accessibility",
        "label"
    ]
    for index in DiggingThroughRecurse:
        digging = digging[index]
    
    likes = digging
    likes = likes.replace("Like this post along with", "").replace("other people", "").replace(",", "").strip()

    with open(f"{output_directory}{str(Post_Number).zfill(4)} [{Post_ID}].txt", "w", encoding="UTF-8") as Details:
        for index in Post_Text:
            index = index['text']
            Details.write(index)
        Details.write("\n\n\n\nLikes: ")
        Details.write(likes)
        Details.write("\nPosted: ")
        Details.write(Publish_Time_Text)
        Details.write("   -> best I can get\n\n\n\n\nThere's no API for community posts,\nthere's no timestamp in the request, nor in the F12 menu.\nThere's no visible function/method being used when the page loads.\nI genuinely don't know where this info is being stored, but I don't have it.")


    #ok now we download the images
    if Images != None:
        for index, url2 in enumerate(Images):
            if "pollRenderer" in url2:
                continue
            
            url2 = url2["backstageImageRenderer"]["image"]["thumbnails"][-1]['url']
            response = requests.get(url2)
            kind = filetype.guess(response.content)
            with open(f"{output_directory}{str(Post_Number).zfill(4)} [{str(index).zfill(2)}].{kind.extension}", "wb") as Output:
                Output.write(response.content)




exit()
# Import the library
import requests

# Specify the image URL
image_url = "https://yt3.ggpht.com/pBWGXYN6ODBD8iO99coAYbR3UFOSR9B6JKFm6W47nKGrBcCuojj4VD3-hcGtCi--4G2wVRP3aUBA=s800-nd-v1"

# Get the image content
response = requests.get(image_url)
kind = filetype.guess(response.content)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in binary mode
    with open("imagedd.png", "wb") as file:
        # Write the image content to the file
        file.write(response.content)
