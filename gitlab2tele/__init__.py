# -*- coding: utf-8 -*-
import telebot
import json
import dateutil.parser

class TeleSender():
    def __init__(self, token, chat_id):
        self.bot = telebot.TeleBot(token)
        self.chat_id = chat_id

    def post_project_event(self, json_obj):
        obj = json_obj
        event_type = obj['object_kind']
        if event_type == 'push':
            self.__revice_push(obj)
        if event_type == 'merge_request':
            self.__revice_merge_request(obj)

    def __revice_push(self, json_obj):
        msg = self.__parse_push_event(json_obj)
        self.bot.send_message(self.chat_id, msg, parse_mode='Markdown')

    def __parse_push_event(self, json_obj):
        push_user = json_obj['user_name']
        commit_count = json_obj['total_commits_count']
        repo_url = json_obj['repository']['homepage']
        repo_name = json_obj['repository']['name']
        commits = json_obj['commits']

        if commit_count == 1:
            msg = '*%s pushed 1 commit ' % push_user
        else:
            msg = '*%s pushed %d commits ' % (push_user, commit_count)

        if commit_count > 3:
            msg += 'to %s (showing last 3):*\n' % repo_name
        else:
            msg += 'to %s:*\n' % repo_name

        for commit in commits[-3:]:
            dt = dateutil.parser.parse(commit['timestamp']).replace(tzinfo=None)
            pd = pretty_date(dt)

            commit_message = commit['message'].rstrip()
            msg += '_%s (%s)_\n``` %s ```\n' % (commit['author']['name'], pd, commit_message)

        return msg

    def __revice_merge_request(self, json_obj):
        msg = self.__parse_merge_request(json_obj)
        self.bot.send_message(self.chat_id, msg)

    def __parse_merge_request(self, json_obj):
        request_user = json_obj['user']['name']
        mr_title = json_obj['object_attributes']['title']
        url = json_obj['object_attributes']['url']
        state = json_obj['object_attributes']['state']
        ret = u'%s %s a merge request : %s. %s' % (request_user, state, mr_title, url)
        return ret

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc.

    Nicked from https://stackoverflow.com/a/1551394.
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"
