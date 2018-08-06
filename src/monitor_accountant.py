import logging, time, verify_attachments, verify_move_periods, verify_payments
FORMAT = '%(asctime)s UTC - %(levelname)s:\n%(message)s'
logging.basicConfig(filename="/dev/tty1", filemode="w", level='INFO', format=FORMAT, datefmt='%m-%d %H:%M')

while 1:
    verify_attachments.run()
    verify_move_periods.run()
    verify_payments.run()
    logging.info('Monitoring cycle completed')
    time.sleep(3600)
