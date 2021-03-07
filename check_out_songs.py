import cPickle
import os

def camel(text):
    words = text.split(" ")
    output = ""
    for i in range(len(words)):
        output += "%s%s " % (words[i][0], words[i][1:].lower())

    return output.strip()

def fix(text):
    text = text.replace("|", " ")
    while "  " in text:
        text = text.replace("  ", " ")

    return text.upper()

def regen():
    global blacklist
    
    # Regenerate the song listing
    try:
        with open("info.dat") as f:
            info = cPickle.load(f)

        output = ""
        artists = sorted(info.keys())
        for i in range(len(artists)):
            artist = artists[i]
            tracks = sorted(info[artist])
            for j in range(len(tracks)):
                combo = camel("%s - %s" % (artist, tracks[j]))
                if combo in blacklist:
                    continue
                output += "%s\n" % combo

        with open("list.txt", "w") as f:
            f.write(output)
    except:
        pass

try:
    with open("list.txt") as f:
        tracks = f.readlines()
except:
    tracks = []

try:
    with open("blacklist.dat") as f:
        blacklist = cPickle.load(f)
except:
    blacklist = []

# Reverse it so pop() pulls from the front
tracks.reverse()

        
while len(tracks) > 0:
    os.system("cls")
    track = tracks.pop().strip()

    if track in blacklist:
        continue
    
    print """We have %s tracks to listen to! What do you think about this track?

%s

Type "no" to kill it, or anyhing else to keep it.
""" % (len(tracks) + 1, track)
    
    choice = raw_input("> ")

    if (choice.lower().strip() == "no"):
        blacklist.append(track)
        with open("blacklist.dat", "w") as f:
            cPickle.dump(blacklist, f)
        regen()
