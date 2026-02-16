import customtkinter
import ast
import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode("System")
customtkinter.set_appearance_mode("dark-blue")

AU = 1.495978707e11
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#app
class app(customtkinter.CTk):
    def __init__(self):
        customtkinter.CTk.__init__(self)

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
            xy = pos[:,:,:2]
            #plotting the data
            fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))

            #sets axis limits for each view point
            if view == "Earth":
                axis_dim = 0.01
            else:
                axis_dim = 1.2
            ax.set_xlim(-axis_dim, axis_dim)
            ax.set_ylim(-axis_dim, axis_dim)

            ax.set_xlabel("Distance (AU)")
            ax.set_ylabel("Distance (AU)")

            trails = []
            points = []
            #creats the points(bodies) and related trails
            for i in range(3):
                (tr,)= ax.plot([],[],lw=1)
                (pt,)= ax.plot([],[],"o")
                trails.append(tr)
                points.append(pt)

            trail_len = 800
            artists = [*trails, *points]

            def init():
                for tr in trails:
                    tr.set_data([], [])
                for pt in points:
                    pt.set_data([], [])
                return artists
            #function to create each frame of the animation
            def update_frames(i):
                #i is the frame index
                xyi = xy[:,i,:].copy()
                # changes the view if view point is set to earth to center the canvas on body 1 (earth)
                if view == "Earth":
                    xyi -= xyi[1]

                start = max(0, i-trail_len)

                for b in range(3):
                    #points data
                    points[b].set_data([xyi[b, 0]], [xyi[b, 1]])
                    #trails
                    trail_xy = xy[b, start:i+1, :].copy()

                    if view == "Earth":
                        trail_xy -= xy[1, start:i+1, :]

                    trails[b].set_data(trail_xy[:,0], trail_xy[:,1])

                return artists

            # destroys old animation if ran more than once
            for widget in self.anim_frame.winfo_children():
                widget.destroy()


            #actually creates and draws the animation, to change the animation speed simply adjust the interval value
            self.canvas = FigureCanvasTkAgg(fig, self.anim_frame)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.anim = FuncAnimation(fig, update_frames, frames=range(T), blit=True, interval=5, init_func=init)
            self.canvas.draw()
            self.anim.event_source.start()

        #window configurations
        self.title("Phases of the Moon")
        self.geometry("1400x1000")

        #configure grid layout (currently an even 2x2 grid
        self.grid_rowconfigure((0,1) , weight=1)
        self.grid_columnconfigure((0,1) , weight=1)
        
        #frame for the animation
        self.anim_frame = customtkinter.CTkFrame(self)
        self.anim_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        #frame for the viewpoint buttons (can later be switched to a tab view with each viewpoint)
        self.viewpoint_frame = customtkinter.CTkFrame(self)
        self.viewpoint_frame.grid(row=0, column=1, pady=20, padx=20, sticky="nsew")
        self.solarview=customtkinter.CTkButton(self.viewpoint_frame, text="Solar View", height=20, width=50, command=lambda: show_anim("Solar"))
        self.viewbutton = customtkinter.CTkButton(self.viewpoint_frame, text="Earth View", height=20, width=50, command=lambda: show_anim("Earth"))
        self.solarview.pack(side="top", padx=20, pady=20)
        self.viewbutton.pack(side="top", padx=20, pady=20)






app().mainloop()