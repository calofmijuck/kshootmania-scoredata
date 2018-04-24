# -*- coding: utf-8 -*-
import os
import sys
import traceback

class song:
    def __init__(self):
        self.name = ''
        self.difficulty = ''
        self.level = ''
        self.clear_n = False
        self.clear_h = False
        self.uc = False
        self.puc = False
        self.score = 0
        self.play_count = 0
        self.normal_count = 0
        self.hard_count = 0
        self.uc_count = 0
        self.puc_count = 0
        self.volforce = 0

    def setName(self, name):
        self.name = name

    def setDifficulty(self, diff):
        self.difficulty = diff

    def setLevel(self, level):
        self.level = level

    def setClear_n(self):
        self.clear_n = True

    def setClear_h(self):
        self.clear_h = True

    def setUC(self):
        self.uc = True

    def setPUC(self):
        self.puc = True

    def setScore(self, score):
        self.score = max(self.score, score)

    def setPlayCount(self, pc):
        self.play_count += pc

    def setNormalCount(self, nc):
        self.normal_count += nc

    def setHardCount(self, hc):
        self.hard_count += hc

    def setUCCount(self, ucc):
        self.uc_count += ucc

    def setPUCCount(self, pucc):
        self.puc_count += pucc

    def setVF(self, vf):
        self.volforce = vf

    ##SongName/Difficulty/Level/CLEARSTATE/SCORE/PLAYCOUNT/ClearCount/HardCount/UC/PUC
    def song_print(self, file, vf):
        file.write(self.name)
        file.write("{0:^5s}".format(self.difficulty))
        file.write("{0:<3d}".format(self.level))
        if self.puc:
            file.write("{0:^7s}".format("PUC"))
        elif self.uc:
            file.write("{0:^7s}".format("UC"))
        elif self.clear_h:
            file.write("{0:^7s}".format("HC"))
        elif self.clear_n:
            file.write("{0:^7s}".format("C"))
        else:
            file.write("{0:^7s}".format("PLAYED"))
        file.write("{0:>7s}".format(self.print_rank()[0]))
        if vf:
            file.write("{0:10d}{1:>5d}{2:>5d}{3:>5d}{4:>5d}{5:>5d}\n".format(self.score, self.play_count, self.normal_count, self.hard_count, self.uc_count, self.puc_count))
        else:
            file.write("{0:10d}{1:>5d}{2:>5d}{3:>5d}{4:>5d}{5:>5d}{6:>10d}\n".format(self.score, self.play_count, self.normal_count, self.hard_count, self.uc_count, self.puc_count, self.volforce))


    def check_vf(self):
        force = int(25 * (self.level + 1) * self.score / 10000000 * self.print_rank()[1])
        self.volforce = force
        return force


    def print_rank(self):
        score = self.score
        if score >= 9900000:
            return ["S", 1]
        elif score >= 9800000:
            return ["AAA+", 0.99]
        elif score >= 9700000:
            return ["AAA", 0.98]
        elif score >= 9500000:
            return ["AA+", 0.97]
        elif score >= 9300000:
            return ["AA", 0.96]
        elif score >= 9000000:
            return ["A+", 0.95]
        elif score >= 8700000:
            return ["A", 0.94]
        elif score >= 7500000:
            return ["B", 0.93]
        elif score >= 6500000:
            return ["C", 0.92]
        else:
            return ["D", 0.91]



def process(lines, song):
    for line in lines:
        try:
            data = line.split(',')
            if data[0] == 'normal':
                if int(data[8]) >= 70:
                    song.setClear_n()
                song.setNormalCount(int(data[11]))
            elif data[0] == 'hard':
                if int(data[8]) > 0:
                    song.setClear_h()
                song.setHardCount(int(data[11]))
            score = int(data[5].split('=')[-1])
            song.setScore(score)
            song.setPlayCount(int(data[10]))
            if int(data[12]) > 0:
                song.setUC()
                song.setUCCount(int(data[12]))
            if int(data[13]) > 0:
                song.setPUC()
                song.setPUCCount(int(data[13]))
        except:
            pass


def getDataFromKSH(chart_file):
    name = ''
    difficulty = ''
    level = 0
    for line in chart_file:
        if "title=" in line:
            ind1 = line.find("=")
            name = line[ind1 + 1:]
        if line.startswith("difficulty="):
            ind2 = line.find("=")
            diff = line[ind2 + 1:]
            difficulty = difficulty_id(diff)
        if line.startswith("level="):
            ind3 = line.find("=")
            level = int(line[ind3 + 1:])
            break
    return (name, difficulty, level)


def difficulty_id(str):
    if str.find("light") >= 0:
        return "NOV"
    if str.find("challenge") >= 0:
        return "ADV"
    if str.find("extended") >= 0:
        return "EXH"
    if str.find("infinite") >= 0:
        return "MXM"

def search(player_name, song_list_vf):
    global pc
    pc = 0
    output = open("score_data.txt", 'w', encoding="utf8")
    output.write("{0:^5s}".format(" "))
    output.write("{0:<3s}".format("Lv"))
    output.write("{0:^7s}".format("CLEAR"))
    output.write("{0:>7s}".format("RANK"))
    output.write("{0:>10s}{1:>5s}{2:>5s}{3:>5s}{4:>5s}{5:>5s}{6:>10s}\n".format("SCORE", "PC", "NC", "HC", "UC", "PUC", "VOLFORCE"))

    for (path, dir, files) in os.walk(os.getcwd()):
        song_location = str(path).replace("score\\" + player_name, "songs")
        for filename in files:
            s = song()
            ext = os.path.splitext(filename)[-1]
            if ext == '.ksc':
                chart_name = filename.replace("ksc", "ksh")
                try:
                    song_chartdata = open(song_location + "\\" + chart_name, 'r', encoding='utf8')
                    (song_name, difficulty, level) = getDataFromKSH(song_chartdata)
                    s.setName(song_name)
                    s.setDifficulty(difficulty)
                    s.setLevel(level)
                    f = open(path + "\\" + filename, 'r')
                    lines = f.readlines()
                    process(lines, s)
                    vf = s.check_vf()
                    song_list_vf.append(s)
                    pc += s.play_count
                    s.song_print(output, False)
                except Exception as e:
                    traceback.print_exc()


def volforce(song):
    return song.volforce


def print_vf(songlist):
    output = open("volforce.txt", 'w', encoding="utf8")
    totalvf = 0
    for i in range(0, 20):
        totalvf += songlist[i].volforce
    output.write("VOLFORCE: {0:>10d}\nTotal Play Count: {1:>10d}\n\n".format(totalvf, pc))

    output.write("{0:^5s}".format(" "))
    output.write("{0:<3s}".format("Lv"))
    output.write("{0:^7s}".format("CLEAR"))
    output.write("{0:>7s}".format("RANK"))
    output.write("{0:>10s}{1:>5s}{2:>5s}{3:>5s}{4:>5s}{5:>5s}{6:>10s}\n".format("SCORE", "PC", "NC", "HC", "UC", "PUC", "VOLFORCE"))

    for i in range(0, 20):
        songlist[i].song_print(output, False)

    output.write("------------------------------------------------------------------------\n")
    for i in range(20, len(songlist)):
        songlist[i].song_print(output, False)

song_list_vf = []

player_name = sys.argv[1]
search(player_name, song_list_vf)

song_list_vf.sort(key=volforce, reverse=True)


print_vf(song_list_vf)

print(pc)
