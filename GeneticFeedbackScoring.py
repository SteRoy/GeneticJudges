import numpy
import math
import random
import copy


class Judge:

    def setRanking(self, rank):
        self.ranking = rank
    
    def __init__(self):
        randomValue = numpy.random.normal(50, 100,1)
        randomValue %= 100
        randomValue = math.floor(math.fabs(randomValue))
        self.objRanking = randomValue

        caRanking = numpy.random.normal(self.getObjRanking(), 10, 1)
        caRanking = math.floor(math.fabs(caRanking % 100))
        self.ranking = caRanking

        self.rankHistory = [randomValue, caRanking]
        self.feedback = []

    def getObjRanking(self):
        return self.objRanking

    def getCurRanking(self):
        return self.ranking

    def getDiffRanking(self):
        return self.getObjRanking() - self.getCurRanking()

    def getRankHistory(self):
        return self.rankHistory

    def addRankToHistory(self, rank):
        self.rankHistory.append(rank)

    def addFeedback(self, feedback):
        self.feedback.append(feedback)

    def getFeedback(self):
        return self.feedback

    def getFeedbackCount(self):
        return len(self.feedback)


class Feedback:

    def __init__(self, ranking, objRanking):
        if random.randint(0,2) == 1:
            self.judgeFeedback = True
            self.ranking = ranking
        else:
            self.judgeFeedback = False

        if self.judgeFeedback:
            self.rankValue = math.fabs(math.floor(numpy.random.normal(objRanking, ranking, 1)%100))
        else:
            # team feedback
            if random.randint(0,2) == 1:
                # team won
                self.rankValue = math.fabs(math.floor(numpy.random.normal(objRanking, 10, 1)%100))
                self.ranking = 5
            else:
                # team didnt win
                # more likely to be wrong
                self.rankValue = math.fabs(math.floor(numpy.random.normal(objRanking, 20, 1)%100))
                self.ranking = 5

    def getEvalValue(self):
        return self.rankValue

    def getSubmitRanking(self):
        return self.ranking

class Node:

    def setValue(self, val):
        self.value = val

    def getValue(self):
        return self.value
    
    def __init__(self, typeNode):
        # + - / *. type0
        self.nType = typeNode
        # sin(), cos(), tan(). type1
        # =. type2
        # startScore, caScore, sizeOfFeedback, feedbackRank, feedbackfValue. type3

        if typeNode == 0:
            self.type = 0
            rx = random.randint(0,3)
            if rx == 0:
                # +
                self.value = "+"
            elif rx == 1:
                # -
                self.value = "-"
            elif rx == 2:
                # *
                self.value = "*"
            elif rx == 3:
                # /
                self.value = "/"
        elif typeNode == 1:
            self.type = 1
            rx = random.randint(0,2)
            if rx == 0:
                # sin
                self.value = "sin"
            elif rx == 1:
                # cos
                self.value = "cos"
            elif rx == 2:
                # tan
                self.value = "tan"
        elif typeNode == 2:
            self.type = 2
            self.value = "="
        elif typeNode == 3:
            self.type = 3
            rx = random.randint(0,4)
            if rx == 0:
                self.value = "startScore"
            elif rx == 1:
                self.value = "caScore"
            elif rx == 2:
                self.value = "sizeOfFeedback"
            elif rx == 3:
                self.value = "feedbackRank"
            elif rx == 4:
                self.value = "feedbackValue"
            else:
                self.value = "fack"
        elif typeNode == 4:
            self.type = 4
            self.value = str(random.random())
        else:
            self.value = "fuck"

    def getType(self):
        return self.type

class Algorithm:
    def getNodes(self):
        return self.nodeList

    def prnt(self):
        stri = "currentScore "
        for i in self.nodeList:
            stri += i.getValue()
            stri += " "
        print(stri)
    
    def doesThisCountAsCompiling(self, judge):
        rnk = random.randint(1,99)
        feedback = Feedback(rnk, judge.objRanking)
        startScore = judge.getCurRanking()
        caScore = judge.getRankHistory()[1]
        sizeOfFeedback = judge.getFeedbackCount()
        feedbackRank = rnk
        feedbackValue = feedback.getEvalValue()

        
        currentTotal = judge.ranking
        workingList = copy.deepcopy(self.nodeList)

        self.prnt()
        while workingList != []:
            node = workingList.pop()
            if node.getType() == 0:
            # if it's an operator, perform it on the currentTotal
                nextNode = workingList.pop()
                expr = "currentTotal "
                expr += node.getValue()
                expr += " "
                if nextNode.getType() == 1:
                    exp = "math."
                    exp += nextNode.getValue()
                    exp += "("
                    nextNode = workingList.pop()
                    exp +=  nextNode.getValue()
                    exp += ")"
                    val = eval(exp)
                    expr += str(int(val))
                else:
                    expr += nextNode.getValue()
                value = eval(expr)
                value = int(value)
                currentTotal = value
            elif node.getType() == 1:
                expr = "currentTotal "
                expr +
            elif node.getType() == 2:
                judge.setRanking(currentTotal)
            else:
                #malformed
                print("MALFORMED2")
                currentTotal = 0
                self.nodeList = []


        
    def __init__(self):
        nodeGenerated = -1
        self.nodeList = []
        while nodeGenerated != 2:
            nType = random.randint(0,4)
            if nType == 2 and len(self.nodeList) < 40:
                nodeGenerated = -1
            else:
                nodeGenerated = nType
                if nType == 0:
                    self.nodeList.append(Node(nType))
                    self.nodeList.append(Node(3))
                elif nType == 2:
                    self.nodeList.append(Node(nType))
                elif nType == 1:
                    # func
                    self.nodeList.append(Node(0))
                    self.nodeList.append(Node(nType))
                    self.nodeList.append(Node(3))
                elif nType == 3:
                    self.nodeList.append(Node(0))
                    self.nodeList.append(Node(4))
                    nodded = Node(0)
                    nodded.setValue("*")
                    self.nodeList.append(nodded)
                    self.nodeList.append(Node(nType))
                elif nType == 4:
                    self.nodeList.append(Node(0))
                    self.nodeList.append(Node(nType))


class Tournament:
    def __init__(self, noJudges, noAlgorithms):
        self.judgesList = []
        self.algorithmsList = []
        self.tournamentDictionary = {}
        self.goodnessranking = {}
        for i in range(noJudges):
            self.judgesList.append(Judge())

        for i in range(noAlgorithms):
            self.algorithmsList.append(Algorithm())

        for algorithm in self.algorithmsList:
            self.tournamentDictionary[algorithm] = copy.deepcopy(self.judgesList)

    def runNextRound(self):
        for algo, judgz in self.tournamentDictionary.iteritems():
            # run algorithm on judgz
            for j in judgz:
                algo.doesThisCountAsCompiling(j)

            self.tournamentDictionary[algo] = judgz

    def evaluateGoodness(self):
        for algo, judgz in self.tournamentDictionary.iteritems():
            bestcase = sorted(judgz, key=lambda x: x.objRanking, reverse=True)
            curcase = sorted(judgz, key=lambda x: x.ranking, reverse=True)

            goodsofar = 0
            algo.prnt()
            for i in range(len(bestcase)):
                if bestcase[i].objRanking == curcase[i].objRanking:
                    goodsofar += 1

            self.goodnessranking[algo] = goodsofar
            



toor = Tournament(10, 10)
toor.runNextRound()

        














        
