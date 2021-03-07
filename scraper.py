import cPickle
import datetime
import json
import urllib2

def camel(text):
    words = text.split(" ")
    output = ""
    for i in range(len(words)):
        word = words[i].strip()
        if word == "":
            continue
        elif len(word) == 1:
            output += "%s " % word
        else:
            output += "%s%s " % (word[0], word[1:].lower())

    return output.strip()

def fix(text):
    text = text.upper().strip().encode('ascii', 'ignore').decode('ascii')
    text = text.replace("&", "AND").strip()
    
    orig_text = text
    
    ignores = "@#$%^*()_-+=[]{}\\|;:\",<>/?"
    for ignore in ignores:
        text = text.replace(ignore, " ")
        
    while "  " in text:
        text = text.replace("  ", " ")

    if text == "":
        return orig_text

    return text

def regenerateFiles(new_tracks):
    try:
        with open("info.dat") as f:
            info = cPickle.load(f)
    except:
        info = {}

    try:
        with open("blacklist.dat") as f:
            blacklist = cPickle.load(f)
    except:
        blacklist = {}

    for track in new_tracks:
        # If the artist and title are in our blacklist skip it
        if track in blacklist:
            # Delete the combination from the info if necessary
            if track in info:
                del info[track]
                
            continue

        # Otherwise add it to our new list
        info[track] = ""
                
    # Save the updated file
    with open("info.dat", "w") as f:
        cPickle.dump(info, f)
        
    # Regenerate the song listing
    with open("list.txt", "w") as f:
        f.write("\n".join(sorted(info.keys())))

def scrape(stationId):
    # Get the latest playlist items
    req = urllib2.Request("https://%s.radio.com/get.php?callback=_freq_tagstation_data&type=recent&count=30" % stationId)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
    response = urllib2.urlopen(req)
    data = json.loads(response.read())
    tracks = data["recentEvents"]

    new_tracks = []

    # Pull out the Artist + Song info
    for i in range(len(tracks)):
        track = tracks[i]
        if "artist" not in track or "title" not in track:
            continue

        artist = fix(track["artist"])    
        title = fix(track["title"])
        combo = camel("%s - %s" % (artist, title))
        new_tracks.append(combo)

    return new_tracks

def start():
    # These are all the radio stations we want to scrape
    stationIds = [
        "947", # KNRK - Portland, Oregon
        "1077theend", # KNDD - Seattle, Washington
        "alternativebuffalo", # WLKK - Buffalo, New York
        "alt949", # KBZT - San Diego, California
        "xl102richmond", # WRXL - Richmond, Virginia
        "alt947", # KKDO - Sacramento, California
        "alt923", # WNYL - New York, New York
        "kroq", # KROQ - Los Angeles, California
        "fm1019", # WQMP - Orlando, Florida
        "hfs", # WWMX-HD2 - Baltimore, Maryland
        "1043theshark", # WSFS - Miami, Florida
        "alt1053", # KITS - San Francisco, California
        "965thebuzz", # KRBZ - Kansas City, Kansas
        "alt1037dfw", # KVIL - Dallas-Fort Worth, Texas
        #"bayou957", # WKBU - New Orleans, Louisiana (killed as it's primarily classic rock)
        "933theplanetrocks", # WTPT - Greenville, North Carolina
        "wxrt", # WXRT - Chicago, Illinois
        "x1075lasvegas", # KXTE - Las Vegas, Nevada
        "jackontheweb", # KJKK - Dallas-Fort Worth, Texas
    ]

    unique_new_tracks = {}

    for stationId in stationIds:
        try:
            new_tracks = scrape(stationId)
        except:
            continue

        for track in new_tracks:
            unique_new_tracks[track] = ""

    unique_new_tracks = unique_new_tracks.keys()
    regenerateFiles(unique_new_tracks)

try:
    start()
except Exception, e:
    with open("error.log", "a") as f:
        f.write(repr(e))
    raise
