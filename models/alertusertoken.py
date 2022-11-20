from dbconnection import connectdb as db

alert_user_token_collection=db()['alert-user-token']

#ALERTUSERTOKE MODEL
class Add_TOKEN:

    def add_token_for_user(self,user_id,token):
        token_list=self.take_token_list(user_id)
        if token_list is None:
            alert_user_token_collection.insert_one({'user_id':user_id,'token_list':[token]})
        elif token not in token_list:
            token_list.append(token)
            self.update_token_list(user_id,token_list)
        return self.take_token_list(user_id)

    def take_token_list(self,user_id):
        try:
            user=alert_user_token_collection.find_one({"user_id":user_id})
        except Exception as e:
            print(e)
        if user:
            return user['token_list']
        return 

    def update_token_list(self,user_id,token_list):
        alert_user_token_collection.update_one(
            {'user_id':user_id},
                    {
                        "$set":{"token_list":token_list}
                    }
        )

    def remove_token_for_user(self,user_id,token):
        token_list=self.take_token_list(user_id)
        if token_list:
            token_list.remove(token)
            self.update_token_list(user_id,token_list)

        return self.take_token_list(user_id)
    