import logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s:%(name)s:%(levelname)s:%(filename)s:%(message)s")
import verify_attachments
import verify_move_periods
import verify_payments

verify_attachments.run()
verify_move_periods.run()
verify_payments.run()
