from car import Player
from position import pos
from geneticAlgorithms import ga
import pygame
from colors import WHITE

class Generation():
    def __init__(self, screen, race_track, offsprings):
        self.screen, self.track = screen, race_track
        self.scoresDict = {}
        if not offsprings:
            popNumber = 25
            self.randomInitialise(popNumber)
        self.popNumber = 0

    def randomInitialise(self, popNumber):
        population = []
        for i in range(popNumber):
            population.append(Player(self.screen, self.track, position=pos(64 + 5 * i, 54)))
        self.population = population
        self.alive_agents = population.copy()

    def update(self):
        indices_to_pop = []
        for i, player in enumerate(self.alive_agents):
            player.updateDynamics()
            player.collision_check()
            player.getDistances()
            player.draw()
            player.updateScore()
            player.handleAIOutput()

            if player.collision_check():
                indices_to_pop.append(i)

        counter = 0
        for index in indices_to_pop:
            dead = self.alive_agents.pop(index - counter)
            counter += 1
            self.scoresDict[dead.score] = dead.AI.getWeightsVector()
        self.drawGenerationInfo()

    def isPopulationDead(self):
        return len(self.alive_agents) == 0

    def selectKBestParents(self, K=10):
        sorted_keys = sorted(self.scoresDict.keys(), reverse=True)
        parentsDict = {}
        for key in sorted_keys[:K]:
            parentsDict[key] = self.scoresDict[key]
        self.parents = parentsDict

    def getMates(self, n_offsprings=20):
        parentsDict = self.parents
        mates = []

        while len(mates) < n_offsprings:
            index1 = ga.rouletteWheelParentSelection(parentsDict)
            index2 = index1
            while index1 == index2:
                index2 = ga.rouletteWheelParentSelection(parentsDict)
            mate = (index1, index2)
            if mate not in mates:
                mates.append(mate)

        self.mates = mates

    def combineMates(self):
        mates = self.mates
        offsprings = []
        offsprings.append(self.parents[max(self.parents.keys())])
        for par1, par2 in mates:
            par1, par2 = self.parents[par1], self.parents[par2]
            x = ga.uniform_crossover(par1, par2)
            y = ga.addMutationstoArray(x, n_mutations=10)
            offsprings.append(y)

        self.offsprings = offsprings

    def updatePopulation(self, offsprings):
        player = Player(self.screen, self.track, position=pos(64, 54))
        player.AI.getWeightsVector()
        weightsShapes = player.AI.weightsShapes

        for i, offspring in enumerate(offsprings):
            self.population[i].AI.weightsShapes = weightsShapes
            self.population[i].AI.setWeightsFromVector(offspring)
            self.population[i].score = 0
            self.population[i].rect.x = 64
            self.population[i].rect.y = 54
            self.population[i].old_center = self.population[i].rect.center
            self.population[i].orientation = 0
            self.population[i].canMove = True

        self.alive_agents = self.population.copy()
        self.popNumber += 1

    def drawGenerationInfo(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        string = "Generation #" + str(int(self.popNumber))
        text = font.render(string, True, WHITE, None)
        textRect = text.get_rect()
        textRect.center = (1000, 10)
        self.screen.blit(text, textRect)
        
        if self.alive_agents:
            distance_string = "Distance: " + str(int(self.alive_agents[0].score))
            distance_text = font.render(distance_string, True, WHITE, None)
            distance_textRect = distance_text.get_rect()
            distance_textRect.center = (1000, 40)
            self.screen.blit(distance_text, distance_textRect)
