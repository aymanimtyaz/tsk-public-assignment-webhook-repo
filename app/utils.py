import datetime

def format_date(date_string):

    ''' Converts the datetime string received from mongodb to the required format. Example: "10th April 2021 - 5:45 PM UTC"
    '''
    
    date_format = "%Y-%m-%d %H:%M:%S"
    req_format = "%-d %B %Y - %I:%M %p UTC"
    date_comp = datetime.datetime.utcfromtimestamp(datetime.datetime.timestamp(datetime.datetime.strptime(date_string, date_format))).strftime(req_format).split(' ')
    #       Getting the suffix of the date component
    if 4 <= int(date_comp[0]) <= 20 or 24 <= int(date_comp[0]) <= 30:
        suffix = 'th'
    else:
        suffix = ["st", "nd", "rd"][int(date_comp[0]) % 10 - 1]
    date_comp[0] += suffix
    final =  ' '.join(date_comp)
    return final