import customtkinter
import ast
import os
from tkinter import END
from simulation import simulate

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("dark-blue")




AU = 1.495978707e11
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#app
class app(customtkinter.CTk):
    def __init__(self):
        customtkinter.CTk.__init__(self)

        self.result_label_frame = customtkinter.CTkLabel(self, text="", font = ("Arial", 16))
        self.result_label_frame.grid(row=1,column=0, columnspan=2, pady = (10,5))

        def submit():
            try: 
                str_time=self.time_entry.get()
                time=float(str_time)
        
            #this time i would like to have as an imput to the simulation, here we connect it to the moon phases
        
                simulate()
            #function starting the simulation imported from simulation.py
            except ValueError:
                self.result_label_frame.configure(text="Can't see the moon now!")
        #the method for clearing the button so we can put next thing 

        def clear(self):
            self.time_entry.delete(0,END)






        #function to make the matplot animation
        def show_anim(view):
            bodies=[]
            for body in range(0, 3):
                path = os.path.join(BASE_DIR, "Sim_data", f"body{body}.csv")
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Missing: {path} (cwd={os.getcwd()})")
                arr =np.genfromtxt(path,delimiter=",")
                bodies.append(arr[:, :3].astype(float))

            T = min(a.shape[0] for a in bodies)
            pos_m = np.stack([a[:T] for a in bodies], axis=0)

            #adjust the scale of the data from meters to AUs
            pos = pos_m/AU
            xyz = pos
            #plotting the data
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection="3d")

            #sets axis limits for each view point
            if view == "Earth":
                axis_dim = 0.01
            else:
                axis_dim = 1.2

            ax.set_xlabel("Distance (AU)")
            ax.set_ylabel("Distance (AU)")
            ax.set_zlabel("Distance (AU)")

            trails = []
            points = []

            #creats the points(bodies) and related trails
            for i in range(3):
                (tr,)= ax.plot([],[], [], lw=1)
                (pt,)= ax.plot([],[], [],"o")
                trails.append(tr)
                points.append(pt)


            trail_len = 800
            artists = [*trails, *points]

            def _set_limits(cx=0.0, cy=0.0, cz=0.0):
                ax.set_xlim(cx - axis_dim, cx + axis_dim)
                ax.set_ylim(cy - axis_dim, cy + axis_dim)
                ax.set_zlim(cz - axis_dim, cz + axis_dim)

                # initial limits

            _set_limits(0.0, 0.0, 0.0)

            def init():
                for tr in trails:
                    tr.set_data([], [])
                    tr.set_3d_properties([])
                for pt in points:
                    pt.set_data([], [])
                    pt.set_3d_properties([])
                return artists
            #function to create each frame of the animation
            def update_frames(i):
                #i is the frame index
                p = xyz[:,i,:].copy()
                # changes the view if view point is set to earth to center the canvas on body 1 (earth)
                if view == "Earth":
                    p -= p[1]


                start = max(0, i-trail_len)

                for b in range(3):
                    #points data
                    points[b].set_data([p[b, 0]], [p[b, 1]])
                    points[b].set_3d_properties([p[b, 2]])
                    #trails
                    trail_xy = xyz[b, start:i+1, :].copy()

                    if view == "Earth":
                        trail_xy -= xyz[1, start:i+1, :]

                    trails[b].set_data(trail_xy[:,0], trail_xy[:,1])
                    trails[b].set_3d_properties(trail_xy[:,2])

                return artists

            # destroys old animation if ran more than once
            for widget in self.anim_frame.winfo_children():
                widget.destroy()


            #actually creates and draws the animation, to change the animation speed simply adjust the interval value
            self.canvas = FigureCanvasTkAgg(fig, self.anim_frame)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.anim = FuncAnimation(fig, update_frames, frames=range(T), blit=False, interval=2, init_func=init)
            self.canvas.draw()
            self.anim.event_source.start()
            #self.phase = 

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

        #frame for the viewpoint buttons, we have is spaced in 4 rows nicely, and sun and earth views are next to each other
        self.right_panel = customtkinter.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, pady=20, padx=20, sticky="nsew")
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_rowconfigure(2, weight=1)
        self.right_panel.grid_rowconfigure(3, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(1, weight=1)

     

        self.solarview=customtkinter.CTkButton(self.right_panel, text="Solar View", height=30, width=70, command=lambda: show_anim("Solar"))
        self.viewbutton = customtkinter.CTkButton(self.right_panel, text="Earth View", height=30, width=70, command=lambda: show_anim("Earth"))
        
        self.solarview.grid(row=0, column = 0, pady = (12,6), padx = (12,6))
        self.viewbutton.grid(row=0, column = 1, pady = (12,6) , padx = (6,12))
    



        self.time_entry_frame= customtkinter.CTkEntry(self.right_panel, placeholder_text="Enter the date",  height=100, width=250 )
        self.time_entry_frame.grid(row=2,column=0, columnspan=2, pady= 10, padx=12)

        #the submition button which needs to be connected to the pre-definied function submit
        self.my_button_frame= customtkinter.CTkButton(self.right_panel,text="Start simulation",command=submit, height=30, width=70)
        self.my_button_frame.grid(row=3, column=0, columnspan=2, pady = (0,12), padx = 12)

        #the result text popping up when we have an error input - i have to work on it
        #self.result_label_frame = customtkinter.CTkLabel(self, text="", font = ("Arial", 16))
        #self.result_label_frame.grid(row=0,column=0, columnspan=2, pady = (10,5))
        


        """"
        #configure grid layout (currently an even 2x2 grid
        self.grid_rowconfigure((0,1) , weight=1)
        self.grid_columnconfigure((0,1) , weight=1)



        #frame for the animation
        self.anim_frame = customtkinter.CTkFrame(self)
        self.anim_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        #frame for the viewpoint buttons (can later be switched to a tab view with each viewpoint)
        self.viewpoint_frame = customtkinter.CTkFrame(self)
        self.viewpoint_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        self.solarview=customtkinter.CTkButton(self.viewpoint_frame, text="Solar View", height=20, width=50, command=lambda: show_anim("Solar"))
        self.viewbutton = customtkinter.CTkButton(self.viewpoint_frame, text="Earth View", height=20, width=50, command=lambda: show_anim("Earth"))
        
        self.solarview.grid(row=0, column = 0, pady = (0,8))
        self.viewbutton.grid(row=0, column = 1)
    

        #self.solarview.pack(side="top", padx= 20, pady=20)
        #self.viewbutton.pack(side="top", padx=20, pady=20)

        self.time_entry_frame= customtkinter.CTkEntry(self, placeholder_text="Enter the date",  height=100, width=250 )
        self.time_entry_frame.grid(row=0,rowspan=2, column=0,columnspan=2, pady=(10,5))

        #the submition button which needs to be connected to the pre-definied function submit
        self.my_button_frame= customtkinter.CTkButton(self,text="Start simulation",command=submit)
        self.my_button_frame.grid(row=0, column=0, columnspan=2, pady = (10,5))

        #the result text popping up when we have an error input
        self.result_label_frame = customtkinter.CTkLabel(self, text="", font = ("Arial", 16))
        self.result_label_frame.grid(row=0,column=0, columnspan=2, pady = (10,5))
        """






app().mainloop()