# DLA_Generator
This program will create and analyze DLA clusters \n
\n
Assumptions for this simulation:  \n
Particles are introduced from an infinite distance (simulatated infinity)\n
Particles undergo random-walks as transport mechanism\n
Particles aggregate irreversibly upon contact, contact defined by a particle occupying an adjacent site\n
Adjacent sites are defined either by Von Neumann(DLA_Main) or Moore Neighborhoods(animation)
If a particle moves past the allowable distance from the origin, it is removed and another is introduced
A seed-particle is located at the origin
The concentraion of particles is limited to one free(non-aggregated) particle at any given moment
 

PREFACE:  I am still learning how to use python, I have about 40 minutes of "formal training" with the language.  I know there are probably more efficient ways to do just about everything in here, so don't be scared to leave some costructive feedback :)


DLA_Main:
DLA_Main will provide an image of the finished aggregate upon completion.  DLA_Main uses a Von-Neumann neighborhood to determine adjacent sites. Towards the bottom of the code there are options to perform analysis and return the results to an output .csv file. Default is to calculate the Correlation Density of the generated aggregate. A Box-Counting dimension calculation is also available, you will need to uncomment lines at the bottom.  The overall matrix dimensions are set in the main function, ~line 100.  Increasing these numbers will allow you to create a larger, highly intricate DLA cluster but be warned: Increasing the resolution greatly increases program run-time. The growth is set to stop when the number of particles reaches the default of 5% of total matrix sites. 

animation:

!!!!!WARNING!!!!!! Animation is still under development and doesn't function properly yet.  It was intended to provide a gif of the growing cluster, creating a frame for every additional particle once it has aggregated. Unfortuantely, it does not work correctly... yet!  You will probably have to restart your terminal to exit the program early(each new frame pops up in the figure-space, otherwise), and the .gif the program creates will most likely be blank.  Any help with acheiving a proper animation would be greatly appreciated. 

animation uses Moore Neighborhoods to determine adjacent sites, leading to some problems with overlapping of the spawning-ring.  You may have to tweak some of the resolution, cut-off population, and spawning-ring radius values to ensure the cluster does not experience distortion-effects 

Future plans include: Expanding to 3D and ability to save completed aggreagate as an .stl file for processing and printing.

Happy Growing!
