from server import server_intialize

if __name__== "__main__":
    server_intialize().run(debug=True,use_reloader=True, host='0.0.0.0')