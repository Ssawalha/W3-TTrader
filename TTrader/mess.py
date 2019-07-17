# import bcrypt

# def hash_password(password): #add saltedpw to db (same column), lookup salt in db to crack pword
#     password = password.encode()
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password, salt)

# # def check_password(username, password):
# #     user = a.Account()
# #     user_info = user.one_from_where_clause('WHERE username = ?', username)
# #     hashed_pw = (user_info.values['password_hash'])
# #     hashed_pw = hashed_pw.encode()
# #     password = password.encode()
# #     return bcrypt.checkpw(password, hashed_pw) #returns True or False

# print(type(hash_password('1234')))

from time import time

current_time = time()
print(current_time)