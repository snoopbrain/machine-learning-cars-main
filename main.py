import pygame
import sys
from colors import *
from car import *
from track import *
from pygame.locals import *
from generations import Generation
import tensorflow as tf

# Verificar dispositivos GPU disponibles
print(tf.config.list_physical_devices('GPU'))

# Configurar para usar la GPU si está disponible
if tf.config.list_physical_devices('GPU'):
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)  # Configurar crecimiento de memoria



def main():
    global play_again
    running = True

    windowLenWidth = (1200, 700)
    screen = pygame.display.set_mode(windowLenWidth)
    pygame.display.set_caption("Machine Learning Cars")
    clock = pygame.time.Clock()
    race_track = track(screen, windowLenWidth)
    pygame.init()

    clock = pygame.time.Clock()

    offsprings = []
    n_generations = 20
    current_generation = 0
    generation = Generation(screen, race_track, offsprings)
    
    while current_generation < n_generations and running:


        print('Generation #', current_generation)
        if not offsprings:
            generation.randomInitialise(25)
        else:
            generation.updatePopulation(offsprings)
        
        while not generation.isPopulationDead() and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    play_again = False
            
            race_track.draw()
            generation.update()
            generation.drawGenerationInfo()  # Draw generation info on screen
            pygame.display.update()
            clock.tick(30)
        
        if running:  # Proceed to the next generation if the game is still running
            generation.selectKBestParents(K=8)
            generation.getMates(n_offsprings=24)
            generation.combineMates()
            offsprings = generation.offsprings
            current_generation += 1
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False

    #     screen.fill((0, 0, 0))
    #     race_track.draw()  # Dibujar la pista
    #     race_track.draw_mask()  # Dibujar la máscara de la carretera
    #     generation.update()

    #     if generation.isPopulationDead():
    #         generation.selectKBestParents()
    #         generation.getMates()
    #         generation.combineMates()
    #         generation.updatePopulation(generation.offsprings)

    #     pygame.display.flip()
    #     clock.tick(30)

    # pygame.quit()
    # sys.exit()

if __name__ == "__main__":
    main()
