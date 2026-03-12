import customtkinter
from PIL import Image
import ast
import os
from tkinter import END
import simulation
import moon_phases_pictures
import Bodies
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("dark-blue")

AU = 1.495978707e11 # Astronomical Unit (= distance from the Earth to the Sun) expressed here in meters
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #sets the directory of the program so it is less likely to break when downloaded in different directories

#app
class app(customtkinter.CTk):
    def __init__(self):
        customtkinter.CTk.__init__(self)

        def submit():
            
            try: 

            #this time i would like to have as an imput to the simulation, here we connect it to the moon phases
                date_str=self.time_entry_frame.get().strip()
                moon_phases_calc = moon_phases_pictures.MoonPhaseCalculator("moon_images")
                phase_name, img_path = moon_phases_calc.moon_phase_for_date(date_str)

            #configuring the text of the result
            #    self.result_label_frame.configure(text=f"{phase_name}")

            #displaying the image in the ui
                pil_img=Image.open(img_path)

            #for an image to stay where it is 
                self._phase_img = customtkinter.CTkImage(light_image = pil_img , dark_image = pil_img, size = (248, 348))
                self.image_label_frame.configure(image=self._phase_img, text ="")
            
            #this one ought to be displayed when it is daytime/ wrong side of Earth
            except ValueError:
               self.result_label_frame.configure(text="Can't see the moon now!")
            #this one is for us to check whether the directory works
            except FileNotFoundError:
                self.result_label_frame.configure("Image not found")

            #Check if the simulation data exists or not
            missing = False
            for name in body_names:
                pos_path = os.path.join(BASE_DIR, "Sim_data", f"{name}_pos.csv")
                vel_path = os.path.join(BASE_DIR, "Sim_data", f"{name}_vel.csv")

                if not os.path.exists(pos_path) or not os.path.exists(vel_path):
                    missing = True
                    break

            if missing:
                sim = simulation.Simulator()
                sim.simulate(bodies)

            show_anim("Solar", body_names)

        #the method for clearing the button so we can put next thing 

        #def clear(self):
           # self.time_entry.delete(0,END)

        #function to make the matplot animation
        def show_anim(view, sim_body_names, focus_body_name="Earth"):

            body_positions=[]

            for name in sim_body_names:
                path = os.path.join(BASE_DIR, "Sim_data", f"{name}_pos.csv")
                if not os.path.exists(path):

                    if len(sim_body_names)>3:
                        sim = simulation.Simulator(10000, 36000)
                        sim.simulate(solar)
                    else:
                        sim = simulation.Simulator()
                        sim.simulate(bodies)

                arr = np.genfromtxt(path, delimiter=",")
                arr = np.atleast_2d(arr)  #REQUIRED after testing: protects against weird 1-row shape issues
                body_positions.append(arr[:, :3].astype(float))

            n_bodies = len(body_positions)
            T = min(arr.shape[0] for arr in body_positions)

            #shape of array: (number of bodies, T, 3)
            pos_m = np.stack([arr[:T] for arr in body_positions], axis=0)

            # meters -> AU
            xyz = pos_m / AU

            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection="3d")


            axis_dim = 0.01 if view == "Earth" else 1.2 #the else value needs to be changed in the future to check how far the furthest body will go while in orbit (also must not count bodies that have been slung/thrown out of the simulation)

            ax.set_xlabel("Distance (AU)")
            ax.set_ylabel("Distance (AU)")
            ax.set_zlabel("Distance (AU)")

            # Find which body to center on
            focus_index = None
            if view == "Earth":
                if focus_body_name not in sim_body_names:
                    raise ValueError(f"{focus_body_name} is not in body_names")
                focus_index = sim_body_names.index(focus_body_name)

            trails = []
            points = []

            for i in range(n_bodies):
                (tr,) = ax.plot([], [], [], lw=1, label=sim_body_names[i])
                (pt,) = ax.plot([], [], [], "o")
                trails.append(tr)
                points.append(pt)

            trail_len = 800
            artists = [*trails, *points]

            def _set_limits(cx=0.0, cy=0.0, cz=0.0):
                ax.set_xlim(cx - axis_dim, cx + axis_dim)
                ax.set_ylim(cy - axis_dim, cy + axis_dim)
                ax.set_zlim(cz - axis_dim, cz + axis_dim)

            _set_limits(0.0, 0.0, 0.0)
            ax.legend()

            def init():
                for tr in trails:
                    tr.set_data([], [])
                    tr.set_3d_properties([])
                for pt in points:
                    pt.set_data([], [])
                    pt.set_3d_properties([])
                return artists

            def update_frames(i):
                current = xyz[:, i, :].copy()

                # Recenter current frame if needed
                if focus_index is not None:
                    current -= current[focus_index]

                start = max(0, i - trail_len)

                for b in range(n_bodies):
                    #current point
                    points[b].set_data([current[b, 0]], [current[b, 1]])
                    points[b].set_3d_properties([current[b, 2]])

                    #trail
                    trail_xyz = xyz[b, start:i+1, :].copy()

                    if focus_index is not None:
                        trail_xyz -= xyz[focus_index, start:i+1, :]

                    trails[b].set_data(trail_xyz[:,0], trail_xyz[:,1])
                    trails[b].set_3d_properties(trail_xyz[:,2])

                return artists

            # Destroy old animation widgets
            for widget in self.anim_frame.winfo_children():
                widget.destroy()

            # actually creates and draws the animation, to change the animation speed simply adjust the interval value
            self.canvas = FigureCanvasTkAgg(fig, self.anim_frame)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.anim = FuncAnimation(fig, update_frames, frames=range(T), blit=False, interval=0, init_func=init)
            self.canvas.draw()
            self.anim.event_source.start()

        #window configurations
        self.title("Phases of the Moon")
        self.geometry("1400x1000")

        #configure grid layout for the whole screen (1x2)
        self.grid_rowconfigure(0 , weight=1)
        self.grid_columnconfigure(0 , weight=4)
        self.grid_columnconfigure(1 , weight=1)

        #frame for the animation
        self.anim_frame = customtkinter.CTkFrame(self)
        self.anim_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        #frame for the viewpoint buttons, we have is spaced in 5 rows nicely, and sun and earth views are next to each other
        self.right_panel = customtkinter.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, pady=20, padx=20, sticky="nsew")
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_rowconfigure(2, weight=1)
        self.right_panel.grid_rowconfigure(3, weight=3)
        self.right_panel.grid_rowconfigure(4, weight=1)        
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(1, weight=1)

        self.solarview=customtkinter.CTkButton(self.right_panel, text="Full Solar System", height=30, width=70, command=lambda: show_anim("Solar", solar_names))
        self.simplifiedsolar = customtkinter.CTkButton(self.right_panel, text="simplified Solar View", height=30, width=70, command=lambda: show_anim("Solar", body_names))
        self.viewbutton = customtkinter.CTkButton(self.right_panel, text="Earth View", height=30, width=70, command=lambda: show_anim("Earth", body_names, focus_body_name="Earth"))
        
        self.solarview.grid(row=1, column = 0, columnspan=2, pady = (12,6), padx = (12,12))
        self.simplifiedsolar.grid(row=0, column = 0, pady = (12,6), padx = (12,6))
        self.viewbutton.grid(row=0, column = 1, pady = (12,6) , padx = (6,12))

        self.time_entry_frame= customtkinter.CTkEntry(self.right_panel, placeholder_text="Enter the date : YYYY-MM-DD",  height=100, width=250 )
        self.time_entry_frame.grid(row=3,column=0, columnspan=2, pady= 10, padx=12)

        #the submition button which needs to be connected to the pre-definied function submit
        self.my_button_frame= customtkinter.CTkButton(self.right_panel,text="Show phase",command=submit, height=30, width=70)
        self.my_button_frame.grid(row=4, column=0, columnspan=2, pady = (0,12), padx = 12)

        #the result text popping up when we have an error input - i have to work on it
        self.result_label_frame = customtkinter.CTkLabel(self, text="", font = ("Arial", 16))
        self.result_label_frame.grid(row=5,column=0, columnspan=2, pady = (10,5))

        # the image object in the ui 
        self.image_label_frame = customtkinter.CTkLabel(self.right_panel, text = "")
        self.image_label_frame.grid(row=2, column=0, columnspan=2, pady = (12,6), padx = (6,12))
        self.phase_img = None

        # This would be set to user input in the future for each body and then they would each be placed in an array, however for the time being it is hard coded to the solar system with sun earth and moon
        bodies = [
            Bodies.Body(
                name="Sun",
                mass=1.9891e30,
                body_radius=6.957e8,
                position=(0.0, 0.0, 0.0),
                velocity=(0.0, 0.0, 0.0)
            ),
            Bodies.Body(
                name="Earth",
                mass=5.9722e24,
                body_radius=6.378e6,
                semi_major_axis=1.495978707e11,
                eccentricity=0.0167086,
                orbital_tilt=0.0,
                longitude_ascending_node=0.0,
                perihelion=102.9372,
                true_anomaly=0.0,
                primary="Sun"
            ),
            Bodies.Body(
                name="Moon",
                mass=7.34767309e22,
                body_radius=1.737e6,
                semi_major_axis=3.844e8,
                eccentricity=0.0549,
                orbital_tilt=5.145,
                longitude_ascending_node=125.08,
                perihelion=318.15,
                true_anomaly=0.0,
                primary="Earth"
            )
        ]
        body_names = [body.name for body in bodies]

        # Solar system with major moons
        solar = [
            Bodies.Body(
                name="Sun",
                mass=1.9891e30,
                body_radius=6.957e8,
                position=(0.0, 0.0, 0.0),
                velocity=(0.0, 0.0, 0.0)
            ),

            Bodies.Body(
                name="Mercury",
                mass=3.3011e23,
                body_radius=2.4397e6,
                semi_major_axis=5.7909e10,
                eccentricity=0.2056,
                orbital_tilt=7.005,
                longitude_ascending_node=48.331,
                perihelion=29.124,
                true_anomaly=0.0,
                primary="Sun"
            ),
            Bodies.Body(
                name="Venus",
                mass=4.8675e24,
                body_radius=6.0518e6,
                semi_major_axis=1.0821e11,
                eccentricity=0.0068,
                orbital_tilt=3.3946,
                longitude_ascending_node=76.680,
                perihelion=54.884,
                true_anomaly=0.0,
                primary="Sun"
            ),
            Bodies.Body(
                name="Earth",
                mass=5.9722e24,
                body_radius=6.378e6,
                semi_major_axis=1.495978707e11,
                eccentricity=0.0167086,
                orbital_tilt=0.0,
                longitude_ascending_node=0.0,
                perihelion=102.9372,
                true_anomaly=0.0,
                primary="Sun"
            ),
            Bodies.Body(
                name="Moon",
                mass=7.34767309e22,
                body_radius=1.737e6,
                semi_major_axis=3.844e8,
                eccentricity=0.0549,
                orbital_tilt=5.145,
                longitude_ascending_node=125.08,
                perihelion=318.15,
                true_anomaly=0.0,
                primary="Earth"
            ),

            Bodies.Body(
                name="Mars",
                mass=6.4171e23,
                body_radius=3.3895e6,
                semi_major_axis=2.2794e11,
                eccentricity=0.0934,
                orbital_tilt=1.850,
                longitude_ascending_node=49.558,
                perihelion=286.502,
                true_anomaly=0.0,
                primary="Sun"
            ),
            Bodies.Body(
                name="Phobos",
                mass=1.0659e16,
                body_radius=1.1267e4,
                semi_major_axis=9.376e6,
                eccentricity=0.0151,
                orbital_tilt=1.093,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Mars"
            ),
            Bodies.Body(
                name="Deimos",
                mass=1.4762e15,
                body_radius=6.2e3,
                semi_major_axis=2.3463e7,
                eccentricity=0.0002,
                orbital_tilt=0.93,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Mars"
            ),

            Bodies.Body(
                name="Jupiter",
                mass=1.8982e27,
                body_radius=6.9911e7,
                semi_major_axis=7.7857e11,
                eccentricity=0.0489,
                orbital_tilt=1.304,
                longitude_ascending_node=100.464,
                perihelion=273.867,
                true_anomaly=0.0,
                primary="Sun"
            ),
            Bodies.Body(
                name="Io",
                mass=8.9319e22,
                body_radius=1.8216e6,
                semi_major_axis=4.217e8,
                eccentricity=0.0041,
                orbital_tilt=0.036,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Jupiter"
            ),
            Bodies.Body(
                name="Europa",
                mass=4.7998e22,
                body_radius=1.5608e6,
                semi_major_axis=6.711e8,
                eccentricity=0.0094,
                orbital_tilt=0.466,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Jupiter"
            ),
            Bodies.Body(
                name="Ganymede",
                mass=1.4819e23,
                body_radius=2.6341e6,
                semi_major_axis=1.0704e9,
                eccentricity=0.0013,
                orbital_tilt=0.177,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Jupiter"
            ),
            Bodies.Body(
                name="Callisto",
                mass=1.0759e23,
                body_radius=2.4103e6,
                semi_major_axis=1.8827e9,
                eccentricity=0.0074,
                orbital_tilt=0.192,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Jupiter"
            ),

            Bodies.Body(
                name="Saturn",
                mass=5.6834e26,
                body_radius=5.8232e7,
                semi_major_axis=1.4335e12,
                eccentricity=0.0565,
                orbital_tilt=2.485,
                longitude_ascending_node=113.665,
                perihelion=339.392,
                true_anomaly=0.0,
                primary="Sun"
            ),
            Bodies.Body(
                name="Titan",
                mass=1.3452e23,
                body_radius=2.57473e6,
                semi_major_axis=1.22187e9,
                eccentricity=0.0288,
                orbital_tilt=0.34854,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Saturn"
            ),
            Bodies.Body(
                name="Uranus",
                mass=8.6810e25,
                body_radius=2.5362e7,
                semi_major_axis=2.8725e12,
                eccentricity=0.0457,
                orbital_tilt=0.772,
                longitude_ascending_node=74.006,
                perihelion=96.998857,
                true_anomaly=0.0,
                primary="Sun"
            ),
            Bodies.Body(
                name="Miranda",
                mass=6.59e19,
                body_radius=2.358e5,
                semi_major_axis=1.299e8,
                eccentricity=0.0013,
                orbital_tilt=4.338,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Uranus"
            ),
            Bodies.Body(
                name="Ariel",
                mass=1.353e21,
                body_radius=5.788e5,
                semi_major_axis=1.909e8,
                eccentricity=0.0012,
                orbital_tilt=0.041,
                longitude_ascending_node=0.0,
                perihelion=0.0,
                true_anomaly=0.0,
                primary="Uranus"
            ),
            Bodies.Body(
                name="Neptune",
                mass=1.02413e26,
                body_radius=2.4622e7,
                semi_major_axis=4.4951e12,
                eccentricity=0.0113,
                orbital_tilt=1.769,
                longitude_ascending_node=131.784,
                perihelion=273.187,
                true_anomaly=0.0,
                primary="Sun"
            )
        ]
        solar_names = [body.name for body in solar]



app().mainloop()
