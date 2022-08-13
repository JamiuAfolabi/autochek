import datetime

def handle_exception(err,log_filename='logs.txt'):
    """
    This function logs exception to file

    PARAMETER:
    
    err: 
        Description: Error to be logged
    filename:
        Type: str
        Description: filename where error is logged
    """
    with open(log_filename,'a') as f:
        f.write(f'{datetime.datetime.now()}' + ': ' + str(err) + '\n')
    f.close()
