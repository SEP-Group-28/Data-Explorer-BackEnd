from dbconnection import connectdb as db

watchlist_collection=db().watchlist

#WATCHLIST MODEL
class Watchlist:
    def __init__(self):
        return

    def getwatchlist(self,id):
        watchlist=watchlist_collection.find_one({'userid':id})
        if not watchlist:
            return False
        if 'list' in watchlist:
            return watchlist['list']
        return False

        
    def createwatchlist(self,id):
        watchlist=watchlist_collection.insert_one(
            {
                'userid':id,
                'list':[]
            }
        )
        return watchlist

        
    def updatewatchlist(self,id,watchlist):
        watchlist_collection.update_one({'userid':id},{"$set":{'list':watchlist}})

        if not watchlist:
            return False
        return watchlist



