 start_pub_sub_model()
    scheduler.add_job(start_streaming)
    scheduler.start()