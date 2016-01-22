#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Telegram bot using Flask that acts like a GitLab webhook to
# share the commits of a GitLab project to a Telegram chat.
#
# Copyright (c) 2015 eternnoir
# Modified by Sijmen Schoon
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import os
from flask import Flask, request
import gitlab2tele
import logging

app = Flask(__name__)
app.logger.setLevel(level=0)
app.logger.addHandler(logging.StreamHandler())
TOKEN = os.environ['TOKEN']
CHAT_ID = int(os.environ['CHAT_ID'])
app.logger.info('TOKEN:' + TOKEN)
app.logger.info('CHAT_ID: ' + str(CHAT_ID))


@app.route("/gitlab/project", methods=["PUT", "POST"])
def gitlab_project():
    json_obj = request.get_json()
    app.logger.info(json_obj)
    ts = gitlab2tele.TeleSender(TOKEN, CHAT_ID)
    ts.post_project_event(json_obj)
    return 'OK'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run('0.0.0.0', port=port, debug=True)
