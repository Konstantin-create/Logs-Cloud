from flask import Flask, redirect, request, render_template, flash, send_file
from werkzeug.utils import secure_filename
from modules import find, sort_new_files, get_loc

app = Flask(__name__)
from modules.routes import *


if __name__ == '__main__':
    app.run()
