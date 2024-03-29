import requests;
import json;
import csv;
import os;

## Projared's ID. Can be substituted for testing purposes.
user_id = '13153992';

## API to get the current stream information
URL = "https://api.twitch.tv/helix/streams?user_id=" + user_id;

## To get client-id
f = open('../system.config', 'r');
contents = f.readlines();
f.close();

reader = csv.reader(contents);
a = [];

id = 'null';

for row in reader:
    a.append(row);
    
for item in row:
    temp = item.split(':');
    if temp[0] == 'Client-ID':
        id = str(temp[1]);

## User-agent information
headers = {'Client-ID':id};

## Foreign API used to obtain hosting information
host_URL = "https://tmi.twitch.tv/hosts?include_logins=1&host=" + user_id;

## API to obtain game information based on title provided
game_URL = "https://api.twitch.tv/helix/games?id=";

response = requests.get(URL, headers=headers);

json_data = json.loads(response.text);

path = 'status/status.txt';

if os.path.exists(path):
    os.remove(path);

## First will attempt to get his live data
try:
    ## Finishes URL to obtain game currently being played. Will fail if not streaming
    game_URL = game_URL + str(json_data['data'][0]['game_id']);
    response_game = requests.get(game_URL, headers=headers);
    game_json_data = json.loads(response_game.text);
    game = game_json_data['data'][0]['name'];
    viewer_count = json_data['data'][0]['viewer_count'];
    ## We now have the game he is playing and the viewer count of it.
    f = open(path, 'w');
    f.write("Status:Live\n");
    f.write("Game:" + game + "\n");
    f.write("Viewer_Count:" + str(viewer_count) + "\n");
    f.close();
    
# Exception will occur if he is offline
# Will now check if he is hosting
except:
    try:
        response_host = requests.get(host_URL);
        host_json_data = json.loads(response_host.text);
        target = host_json_data['hosts'][0]['target_login'];
        ## We now have the name of the streamer he is hosting.
        f = open(path, 'w');
        f.write("Status:Hosting\n");
        f.write("Hosting:" + target);
        f.close();
    ## An error here means Projared is asleep :)
    except:        
        f = open(path, 'w');
        f.write("Status:asleep");
        f.close();
