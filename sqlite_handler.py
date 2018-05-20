#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sqlite3 as sqlite


class DBHandler(object):
    def __init__(self, db_path):
        self.conn = sqlite.connect(db_path)  # 'db/rcng_2017-07-23.db'
        self.cur = self.conn.cursor()

    def get_breeds(self):
        qry = self.cur.execute('SELECT * FROM breeds')

        breeds_fetch = []

        for line in qry.fetchall():
            breeds_fetch.append((line[0], line[1]))

        return breeds_fetch

    def add_dog_to_db(self, dog_dict):

        try:
            self.cur.execute(
                "INSERT INTO dogs (name, breed_id, gender_id, owner, birth, doc, racebook, tattoo, comments) " \
                "VALUES ('{0}',{1},{2},'{3}','{4}','{5}','{6}','{7}','{8}')".format(dog_dict['name'],
                                                                                    dog_dict['breed_id'],
                                                                                    dog_dict['gender_id'],
                                                                                    dog_dict['owner'],
                                                                                    dog_dict['birthday'],
                                                                                    dog_dict['doc'],
                                                                                    dog_dict['racebook'],
                                                                                    dog_dict['tattoo'],
                                                                                    dog_dict['comments']))
            self.conn.commit()
            return True
        except:
            return False

    def commit_close(self):
        self.conn.commit()
        self.conn.close()

    def get_categories(self):
        qry = self.cur.execute('SELECT * FROM categories')

        cat_fetch = []

        for line in qry.fetchall():
            cat_fetch.append((line[0], line[1]))

        return cat_fetch

    def get_ids_names(self):
        qry = self.cur.execute('SELECT id, name FROM dogs')

        dogs_fetch = []

        for line in qry.fetchall():
            dogs_fetch.append((line[0], line[1]))

        return dogs_fetch

    def add_participant(self, part_dict):
        try:
            self.cur.execute(
                "INSERT INTO participants (id, dog_id, category_id) VALUES ({0},{1},{2})".format(part_dict['id'],
                                                                                                 part_dict['dog_id'],
                                                                                                 part_dict['category_id']))
            self.conn.commit()
            return True
        except:
            return False

    def get_participants_summary(self):
        participants = []

        qry = self.cur.execute('SELECT participants.id, dogs.name, categories.name FROM participants INNER JOIN dogs '
                               'ON participants.dog_id = dogs.id INNER JOIN categories ON participants.category_id = '
                               'categories.id')

        for line in qry.fetchall():
            participants.append((line[0], line[1], line[2], '-', '-', '-', '-', '-', '-', '-', '-', '-'))

        return participants

    def get_next_prel_run_number(self):
        qry = self.cur.execute('SELECT MAX(DISTINCT prel_run) FROM participants')

        if qry.fetchone()[0]:
            return qry.fetchone()[0] + 1
        else:
            return 1

    def get_dog_for_prel_run(self, cat_id):
        qry = self.cur.execute('''SELECT participants.id, dogs.name 
        FROM participants INNER JOIN dogs 
        ON participants.dog_id = dogs.id 
        WHERE participants.category_id = ? AND participants.prel_result = 7''', (cat_id, ))

        names_ids = []

        for line in qry.fetchall():
            names_ids.append((line[0], line[1]))

        return names_ids
