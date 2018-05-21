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

        qry = self.cur.execute('''SELECT participants.id, dogs.name, categories.name, 
        participants.prel_run, participants.prel_time 
        FROM participants INNER JOIN dogs ON participants.dog_id = dogs.id 
        INNER JOIN categories ON participants.category_id = categories.id''')

        for line in qry.fetchall():
            participants.append((line[0], line[1], line[2], line[3], line[4], '-', '-', '-', '-', '-', '-', '-'))

        return participants

    def get_next_prel_run_number(self):
        qry = self.cur.execute('SELECT MAX(DISTINCT prel_run) FROM participants')

        cur_max = qry.fetchone()[0]

        if cur_max:
            return cur_max + 1
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

    def register_prel_run(self, run_dict):
        run_number = run_dict['num']

        try:
            if run_dict['first_id'] != 0:
                self.cur.execute('''UPDATE participants
                SET prel_run = ?, prel_jacket = 1, prel_result = 1
                WHERE participants.id = ?
                ''', (run_number, run_dict['first_id']))

            if run_dict['second_id'] != 0:
                self.cur.execute('''UPDATE participants
                SET prel_run = ?, prel_jacket = 2, prel_result = 1
                WHERE participants.id = ?
                ''', (run_number, run_dict['second_id']))

            if run_dict['third_id'] != 0:
                self.cur.execute('''UPDATE participants
                SET prel_run = ?, prel_jacket = 3, prel_result = 1
                WHERE participants.id = ?
                ''', (run_number, run_dict['third_id']))

            if run_dict['fourth_id'] != 0:
                self.cur.execute('''UPDATE participants
                SET prel_run = ?, prel_jacket = 4, prel_result = 1
                WHERE participants.id = ?
                ''', (run_number, run_dict['fourth_id']))

            self.conn.commit()
            return True
        except:
            return False

    def get_prel_runs_info(self):
        qry = self.cur.execute('''SELECT participants.id, 
        dogs.name, 
        categories.name, 
        participants.prel_run, 
        participants.prel_jacket, 
        participants.prel_time,
        participants.prel_result,
        participants.prel_comments
        FROM participants INNER JOIN dogs ON participants.dog_id = dogs.id
        INNER JOIN categories ON participants.category_id = categories.id
        WHERE participants.prel_result != 7 
        ORDER BY participants.prel_jacket
        ''')

        runs_info_list = qry.fetchall()

        return runs_info_list

    def get_participants_by_run_number(self, num):
        qry = self.cur.execute('''SELECT participants.id, dogs.name 
        FROM participants INNER JOIN dogs 
        ON participants.dog_id = dogs.id 
        WHERE participants.prel_run = ? ORDER BY participants.prel_jacket''', (num, ))

        names_ids = []

        for line in qry.fetchall():
            names_ids.append((line[0], line[1]))

        return names_ids

    def get_statuses(self):
        qry = self.cur.execute('SELECT * FROM results')

        results = []

        for line in qry.fetchall():
            results.append((line[0], line[1]))

        return results

    def register_time_prel_run(self, reg_dict):
        try:
            self.cur.execute('''UPDATE participants
            SET prel_time = ?, prel_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_1'], reg_dict['status_1'], reg_dict['num_1']))

            if reg_dict['num_2'] != 0:
                self.cur.execute('''UPDATE participants
            SET prel_time = ?, prel_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_2'], reg_dict['status_2'], reg_dict['num_2']))

            if reg_dict['num_3'] != 0:
                self.cur.execute('''UPDATE participants
            SET prel_time = ?, prel_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_3'], reg_dict['status_3'], reg_dict['num_3']))

            if reg_dict['num_4'] != 0:
                self.cur.execute('''UPDATE participants
            SET prel_time = ?, prel_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_4'], reg_dict['status_4'], reg_dict['num_4']))

            self.conn.commit()
            return True
        except:
            return False

    def delete_run(self, run_num):
        try:
            qry = self.cur.execute('''
            UPDATE participants SET prel_run = NULL, prel_jacket = NULL, prel_time = NULL,
            prel_result = 7 WHERE prel_run = ?
            ''', (run_num, ))
            self.conn.commit()
            return True
        except:
            return False
