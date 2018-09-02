
#To Search
REHAVIA = "https://www.facebook.com/groups/1374475339518708"
NACHLAOT = "https://www.facebook.com/groups/312431032180135"
RASKO = "https://www.facebook.com/groups/762393650515665"
JERUS = "https://www.facebook.com/groups/1592170434330768"

CHAT_ID = "@hshshshsjs" #GENERAL CHAT
#Will search all the keyword in each group (kinda grid search :D)
KEYS = ["למסירה"]
# LINKS =[REHAVIA, NACHLAOT, JERUS]
LINKS =[REHAVIA]
GROUPS = []
for key in KEYS:
    for link in LINKS:
        GROUPS.append({"link": link, "search": key, "chat": CHAT_ID})


# this file should contain GROUPS, array of objects
# each object should look like {"link": link to group, "search": keyword to search}