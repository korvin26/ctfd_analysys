import logging

def setup_logging(log_to="stdout", debug=False):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if log_to == "file":
        logging.basicConfig(filename="ctfd_analysis.log", level=logging.DEBUG if debug else logging.INFO, format=log_format)
    else:
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, format=log_format)
