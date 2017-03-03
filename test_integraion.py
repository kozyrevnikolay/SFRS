import numpy as np
import time
import SFRS_module
import glb
from tkinter import *
from math import pi
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
matplotlib.use('TkAgg')


experiment_unnormalized = (2069.12, 3022.23, 1573.9, 1588.56, 845.46, 694.96, 383.82, 265.25)
experiment = tuple(i/sum(experiment_unnormalized) for i in experiment_unnormalized)
print(experiment)

phi0 = list(np.linspace(5*pi/180, 30*pi/180, 10))
sigma = list(np.linspace(1*pi/180, 30*pi/180, 10))
tau = list(np.linspace(1e-12, 30e-12, 10))
N_Mn = list(np.linspace(1, 40, 20))
B_exch = list(np.linspace(1, 3, 3))
number_of_iterations = len(phi0)*len(sigma)*len(tau)*len(N_Mn)*len(B_exch)
integral_value = np.zeros((len(phi0), len(sigma), len(tau), len(N_Mn), len(B_exch)))
error_value = integral_value


main_window = Tk()
label_one_iteration_time = None
label_total_time_elapsed = None
label_iteration_number = None
current_iteration = 0
time_elapsed = 0
r = []

len_x = int(1e2)
len_phi = int(1e2)

figure_handle = Figure(figsize=(5, 5), dpi=100)
axes_handle = [figure_handle.add_subplot(8, 1, i) for i in range(1, 9)]
canvas = FigureCanvasTkAgg(figure_handle, master=main_window)
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
for phi0C in phi0:
    glb.phi0 = phi0C
    for sigmaC in sigma:
        glb.sigma = sigmaC
        for tauC in tau:
            glb.tau = tauC
            for N_MnC in N_Mn:
                glb.N_Mn = N_MnC
                for B_exchC in B_exch:
                    glb.B_exch = B_exchC


                    time_of_one_iteration_start = time.time()
                    x = np.linspace(0, glb.tau*7, int(len_x))
                    y = np.linspace(glb.phi0-glb.sigma*5, glb.phi0+glb.sigma*5, int(len_phi))
                    t, phi = np.meshgrid(x, y)
                    f = list(map(lambda n: SFRS_module.with_selection_rules(t, phi, n), list(range(8))))
                    integral_t = list(map(lambda n: np.trapz(f[n-1], x=x), list(range(8))))
                    integral = list(map(lambda n: np.trapz(integral_t[n-1], x=y), list(range(8))))
                    time_of_one_iteration_finish = time.time()
                    time_of_one_iteration = time_of_one_iteration_finish - time_of_one_iteration_start
                    time_elapsed += time_of_one_iteration
                    current_iteration += 1
                    map(lambda x: axes_handle[x].plot(current_iteration, experiment[x], 'r.', current_iteration, integral[x], 'b.'), range(8))
                    canvas.draw()
                    if label_one_iteration_time is not None:
                        label_one_iteration_time.destroy()
                    if label_total_time_elapsed is not None:
                        label_total_time_elapsed.destroy()
                    if label_iteration_number is not None:
                        label_iteration_number.destroy()
                    label_one_iteration_time = Label(main_window,
                                                     text=('Time elapsed on one iteration ' + str(time_of_one_iteration)
                                                           + ' seconds'),
                                                     width=60)
                    label_total_time_elapsed = Label(main_window,
                                                     text=('Total time elapsed ' + str(time_elapsed) + ' seconds'),
                                                     width=60)
                    label_iteration_number = Label(main_window,
                                                   text=('Iteration: ' + str(current_iteration) + '/'
                                                         + str(number_of_iterations)))
                    label_iteration_number.pack()
                    label_one_iteration_time.pack()
                    label_total_time_elapsed.pack()
                    main_window.update()

main_window.mainloop()
