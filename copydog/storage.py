# -*- coding: utf-8 -*-
import redis
from copydog.redmine import Issue
from copydog.trello import Card


class Storage(object):

    def __init__(self):
        self.redis = redis.StrictRedis()

    def get_item_id(self, service_name, id):
        return self.redis.hget('{service_name}:items:{id}'.format(service_name=service_name, id=id), 'foreign_id')

    def get_item_list_id(self, service_name, id):
        return self.redis.hget('{service_name}:list_status_mapping'.format(service_name=service_name), id)

    def get_last_time_read(self, service_name):
        return self.redis.get('{service_name}:last_read_time'.format(service_name))

    def mark_read(self, service_name, items):
        pipe = self.redis.pipeline()
        for item in items:
            pipe.hset('{service_name}:items:{id}'.format(service_name=service_name, id=id),
                'updated', item.last_updated())
        pipe.execute()



class Mapper(object):

    def __init__(self, storage, clients, config=None):
        self.config = config
        self.storage = storage
        self.clients = clients

    def issue_to_trello(self, issue):
        assert isinstance(issue, Issue)
        service_from = 'redmine'
        service_to = 'trello'
        card = Card(
            id = self.storage.get_item_id(service_from, issue.id),
            idMembers = [None],
            name = issue.subject,
            desc = issue.description,
            idList = self.storage.get_item_list_id(service_from, issue.status['id']),
            idBoard = self.config.default_board_id,
            due = issue.due_date,
            client = self.clients[service_to]
        )
        return card

    def card_to_redmine(self, card):
        assert isinstance(card, Card)
        service_from = 'trello'
        service_to = 'redmine'
        issue = Issue(
            id = self.storage.get_item_id(service_from, card.id),
            assigned_to = None,
            subject = card.name,
            description = card.desc,
            status_id = self.storage.get_item_list_id(service_from, card.idList),
            project_id = self.config.default_project_id,
            due_date = card.due,
            client = self.clients[service_to]
        )
        return issue