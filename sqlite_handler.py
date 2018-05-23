#!/usr/bin/python3
#  -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import sqlite3 as sqlite
import operator


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
        participants.prel_place
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
            if reg_dict['status_1'] in (4, 5, 6):
                self.cur.execute('''UPDATE participants
                            SET semi_result = ?, final_result = ?
                            WHERE participants.id = ?
                            ''', (reg_dict['status_1'], reg_dict['status_1'], reg_dict['num_1']))

            if reg_dict['num_2'] != 0:
                self.cur.execute('''UPDATE participants
            SET prel_time = ?, prel_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_2'], reg_dict['status_2'], reg_dict['num_2']))
                if reg_dict['status_2'] in (4, 5, 6):
                    self.cur.execute('''UPDATE participants
                                SET semi_result = ?, final_result = ?
                                WHERE participants.id = ?
                                ''', (reg_dict['status_2'], reg_dict['status_2'], reg_dict['num_2']))

            if reg_dict['num_3'] != 0:
                self.cur.execute('''UPDATE participants
            SET prel_time = ?, prel_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_3'], reg_dict['status_3'], reg_dict['num_3']))
                if reg_dict['status_3'] in (4, 5, 6):
                    self.cur.execute('''UPDATE participants
                                SET semi_result = ?, final_result = ?
                                WHERE participants.id = ?
                                ''', (reg_dict['status_3'], reg_dict['status_3'], reg_dict['num_3']))

            if reg_dict['num_4'] != 0:
                self.cur.execute('''UPDATE participants
            SET prel_time = ?, prel_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_4'], reg_dict['status_4'], reg_dict['num_4']))
                if reg_dict['status_4'] in (4, 5, 6):
                    self.cur.execute('''UPDATE participants
                                SET semi_result = ?, final_result = ?
                                WHERE participants.id = ?
                                ''', (reg_dict['status_4'], reg_dict['status_4'], reg_dict['num_4']))

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

    def get_next_second_run_number(self):
        qry = self.cur.execute('SELECT MAX(DISTINCT prel_run) FROM participants')

        prel_max = qry.fetchone()[0]

        qry = self.cur.execute('SELECT MAX(DISTINCT semi_run) FROM participants')

        semi_max = qry.fetchone()[0]

        if semi_max:
            return semi_max + 1
        else:
            return prel_max + 1

    def register_second_run(self, run_dict):
        run_number = run_dict['num']

        try:
            if run_dict['first_id'] != 0:
                self.cur.execute('''UPDATE participants
                SET semi_run = ?, semi_jacket = 1, semi_result = 1
                WHERE participants.id = ?
                ''', (run_number, run_dict['first_id']))

            if run_dict['second_id'] != 0:
                self.cur.execute('''UPDATE participants
                SET semi_run = ?, semi_jacket = 2, semi_result = 1
                WHERE participants.id = ?
                ''', (run_number, run_dict['second_id']))

            if run_dict['third_id'] != 0:
                self.cur.execute('''UPDATE participants
                SET semi_run = ?, semi_jacket = 3, semi_result = 1
                WHERE participants.id = ?
                ''', (run_number, run_dict['third_id']))

            if run_dict['fourth_id'] != 0:
                self.cur.execute('''UPDATE participants
                SET semi_run = ?, semi_jacket = 4, semi_result = 1
                WHERE participants.id = ?
                ''', (run_number, run_dict['fourth_id']))

            self.conn.commit()
            return True
        except:
            return False

    def register_time_second_run(self, reg_dict):
        try:
            self.cur.execute('''UPDATE participants
            SET semi_time = ?, semi_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_1'], reg_dict['status_1'], reg_dict['num_1']))
            if reg_dict['status_1'] in (4, 5, 6):
                self.cur.execute('''UPDATE participants
                            SET final_result = ?
                            WHERE participants.id = ?
                            ''', (reg_dict['status_1'], reg_dict['num_1']))

            if reg_dict['num_2'] != 0:
                self.cur.execute('''UPDATE participants
            SET semi_time = ?, semi_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_2'], reg_dict['status_2'], reg_dict['num_2']))
                if reg_dict['status_2'] in (4, 5, 6):
                    self.cur.execute('''UPDATE participants
                                SET final_result = ?
                                WHERE participants.id = ?
                                ''', (reg_dict['status_2'], reg_dict['num_2']))

            if reg_dict['num_3'] != 0:
                self.cur.execute('''UPDATE participants
            SET semi_time = ?, semi_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_3'], reg_dict['status_3'], reg_dict['num_3']))
                if reg_dict['status_3'] in (4, 5, 6):
                    self.cur.execute('''UPDATE participants
                                SET final_result = ?
                                WHERE participants.id = ?
                                ''', (reg_dict['status_3'], reg_dict['num_3']))

            if reg_dict['num_4'] != 0:
                self.cur.execute('''UPDATE participants
            SET semi_time = ?, semi_result = ?
            WHERE participants.id = ?
            ''', (reg_dict['time_4'], reg_dict['status_4'], reg_dict['num_4']))
                if reg_dict['status_4'] in (4, 5, 6):
                    self.cur.execute('''UPDATE participants
                                SET final_result = ?
                                WHERE participants.id = ?
                                ''', (reg_dict['status_4'], reg_dict['num_4']))

            self.conn.commit()
            return True
        except:
            return False

    def delete_semi_run(self, run_num):
        try:
            qry = self.cur.execute('''
            UPDATE participants SET semi_run = NULL, semi_jacket = NULL, semi_time = NULL,
            semi_result = 7 WHERE semi_run = ?
            ''', (run_num, ))
            self.conn.commit()
            return True
        except:
            return False

    def get_semi_runs_info(self):
        qry = self.cur.execute('''SELECT participants.id, 
        dogs.name, 
        categories.name, 
        participants.semi_run, 
        participants.semi_jacket, 
        participants.semi_time,
        participants.semi_result,
        participants.semi_place
        FROM participants INNER JOIN dogs ON participants.dog_id = dogs.id
        INNER JOIN categories ON participants.category_id = categories.id
        WHERE participants.semi_result != 7 
        ORDER BY participants.semi_jacket
        ''')

        runs_info_list = qry.fetchall()

        return runs_info_list

    def get_dog_for_second_run(self, cat_id):
        qry = self.cur.execute('''SELECT participants.id, dogs.name 
        FROM participants INNER JOIN dogs 
        ON participants.dog_id = dogs.id 
        WHERE participants.category_id = ? AND participants.semi_result = 7''', (cat_id, ))

        names_ids = []

        for line in qry.fetchall():
            names_ids.append((line[0], line[1]))

        return names_ids

    def get_second_participants_summary(self):
        participants = []

        qry = self.cur.execute('''SELECT participants.id, dogs.name, categories.name, 
        participants.prel_time, participants.prel_result, participants.prel_place,
        participants.semi_time, participants.semi_result, participants.semi_place,
        participants.final_time, participants.final_result, participants.final_place
        FROM participants INNER JOIN dogs ON participants.dog_id = dogs.id 
        INNER JOIN categories ON participants.category_id = categories.id''')

        for line in qry.fetchall():
            num = line[0]
            name = line[1]
            category = line[2]
            fin_place = ' '
            prel_place = ' '
            time_1 = ' '
            if line[4] == 2:
                time_1 = self.pretty_time(str(line[3]))
            elif line[4] == 4:
                time_1 = 'ДИСКВ'
            elif line[4] == 5:
                time_1 = 'СВ'
            elif line[4] == 6:
                time_1 = 'СНЯТ'

            time_2 = ' '
            if line[7] == 2:
                time_2 = self.pretty_time(str(line[6]))
            elif line[7] == 4:
                time_2 = 'ДИСКВ'
            elif line[7] == 5:
                time_2 = 'СВ'
            elif line[7] == 6:
                time_2 = 'СНЯТ'

            time_fin = ' '
            if line[10] == 2:
                time_fin = self.pretty_time(str(line[9]))
                fin_place = line[11]
            elif line[10] == 4:
                time_fin = 'ДИСКВ'
            elif line[10] == 5:
                time_fin = 'СВ'
            elif line[10] == 6:
                time_fin = 'СНЯТ'

            best_prel_time = ' '

            if line[4] == 2 and line[7] == 2:
                best_prel_time = self.pretty_time(min(line[3], line[6]))
                prel_place = line[8] if line[8] else '---'

            participants.append((num, name, category, time_1, time_2, best_prel_time, prel_place, time_fin, fin_place))

        return participants

    def update_places(self):
        categories_qry = self.cur.execute('SELECT * FROM categories')
        cat_list = categories_qry.fetchall()

        for category, _ in cat_list:
            qry = self.cur.execute('''SELECT participants.id, participants.prel_time, participants.semi_time
            FROM participants
            WHERE participants.category_id = ? AND
            participants.prel_result = 2 AND
            participants.semi_result = 2 
            ''', (category, ))

            part_list = qry.fetchall()
            part_min_list = [(p[0], min(p[1], p[2])) for p in part_list]
            part_min_list.sort(key=operator.itemgetter(1))

            for place, participant in enumerate(part_min_list, start=1):
                self.cur.execute('''UPDATE participants
                SET semi_place = ?
                WHERE id = ?
                ''', (place, participant[0]))

        self.conn.commit()

    def pretty_time(self, time_int):
        s = str(time_int)
        return s[:-2] + '.' + s[-2:]

    def add_final_run(self, cat_num):
        pass

    def get_final_runs_info(self):
        pass
