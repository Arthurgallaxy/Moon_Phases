# 🌘 Moon Phases Simulation

**Course:** Practical Python Programming Language – Introduction to OOP  
**Institution:** Maastricht Science Programme  
**Date:** February/March 2026  
**Team members and student IDs:** Arthur Foulon (i6374980), Aleksandra Chmielewska (i6382400), Luna Hoenders (i6352961), Laura-Jo Lykles (i6375390), Margot Portier (i6344762) 

*This project aims to create a simple but accurate stimulation that would enable one to visualize the phases of the Moon from an Earth-bound observer.*

## README instructions
(Only for us, to be deleted before final submission, check boxe only if part is fully finished):  
- Essential:
    - [x] Clear project title  
    - [x] One-line description  
    - [ ] What it does (2-3 sentences)
    - [ ] Installation instructions that work
    - [ ] At least one usage example
    - [ ] No typos or broken links
- Recommended:
    - [ ] Features list
    - [ ] Prerequisites clearly stated
    - [ ] Project structure diagram
    - [ ] Contributing guidelines (for group projects)
    - [x] License information
    - [x] Contact information
    - [ ] Screenshots or GIFs (if applicable)
- Optional but nice:
    - [ ] Table of contents (for long READMEs)
    - [ ] Changelog (are we really doing that?)

## 📑 Table of Contents
In this README file, you can find:
- [Description](#-description)
- [Features](#-features)
- [Physics Background](#-physics-background)
- [Libraries used](#-libraries-used)
- [Data used](#-data-used)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Usage Example](#-usage-example)
- [Project Structure](#-project-structure)
- [Challenges & Solutions](#-challenges--solutions)
- [What We Learned](#-what-we-learned)
- [Future Improvements](#-future-improvements)
- [Team Contributions](#-team-contributions)
- [License](#-license)
- [Contact Information](#-contact-information)
- [References](#-references)

## 📌 Description
Our main motivation, for this python practical, was to challenge ourselves and learn to code by collaborating on GitHub to create an interesting stimulation with its visualization and with a scientific relevance that may be used as a lame educational tool in secondary schools.

In our stimulation, we want to visualize the dynamic between three very familiar bodies: the Earth, the Sun and the Moon. In order to do so, we created four classes: celestial bodies, orbits, observer and user interface (abbreviated as UI). The goal is to provide a user-friendly interface that could be used to visualize the phases and tilt of the Moon depending on the date and latitude on Earth. The Earth-bound observer is represented by a cat that can either be dead or alive with a 50% chance (little nerdy quantum add to this astronomy project.)

Inputs needed from the user:
- date (and time of the day?)
- latitude on Earth

Outputs given by the code:
- visualization of the phase of the Moon amongst these 8 possible phases: 
    - 🌑 (New Moon)
    - 🌒 (Waxing Crescent Moon)
    - 🌓 (First Quarter Moon)
    - 🌔 (Waxing Gibbous Moon)
    - 🌕 (Full Moon)
    - 🌖 (Waning Gibbous Moon)
    - 🌗 (Last Quarter Moon)
    - 🌘 (Waning Crescent Moon)
- visualization of the apparent tilt of the Moon
- if the cat is dead or alive... 🐈‍⬛

## ✨ Features
- Moon orbit simulation around the Earth from an Earth or Sun perspective?
- Gravitational force modeling?
- Date-dependant Moon phase visualization
- Latitude-dependent Moon tilt visualization?

## 🧠 Physics Background
### 🌍 Gravitational Force
The first physical principle used in this project is a simplified version of the **gravitational force**. In astronomy, planets orbit stars and moons orbit planets due to a **gravitational pull** between them. Newton's law of universal gravitation describes this force between two objects as being:  

**F = G × (m₁ × m₂) / r²**  

Where:  
- **F** = gravitational force (in Newtons)
- **G** = gravitational constant = 6.674 × 10⁻¹¹ m³/ (in kg·s²)
- **m₁, m₂** = masses of the two objects (in kg)
- **r** = distance between the centers of mass of the two objects (in meters)

This formula, in its simplest form, is used to compute an approximation of the orbits of the Earth around the Sun (?) and the Moon around the Earth as a basis for our simulation. Any relativistic effect was ignored.

### 🌘 Phases of the Moon
<p align="center">
  <img src="https://github.com/user-attachments/assets/b9852746-aa5a-438e-8754-ac3d4552f078" alt="Gift Moon phases" width="300">
</p>

<p align="center">
  <em>
  Figure 1: Moon phases visualization over a month.  
  Source: NASA (2026).
  </em>
</p>

Moving on to the physics behind the phases of the Moon, a very widely spread misconception is that they are created by the Earth's moving shadow on our satellite. This exactly is what happens during lunar eclipses but this process is NOT what creates the different phases of the Moon over a month.  

Half of the Moon is actually constantly lit by light coming straight from the Sun. As the Moon revolves around the Earth (with a period between 29 and 30 days), the relative Sun-Earth-Moon positions change. It means that, for an observer on Earth, the lit part of the Moon would look different at different times of the month as shown on the following figure. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/4b052cb7-88dd-414c-a4e5-3c77bd9c7a74" alt="Understand Moon phases as seen from Earth" width="700">
</p>

<p align="center">
  <em>
  Figure 2: Understand the phases of the Moon as seen from Earth.  
  Source: NASA (2026).
  </em>
</p>

### 🌙 Tilt of the Moon
Then, building on this idea, we must also consider that the Moon's apparent tilt depending of the observer's latitude on Earth as represented in the image below.  

<p align="center">
  <img src="https://github.com/user-attachments/assets/28748a2d-e61d-42c5-a798-b574e8098a1f" alt="Moon phases tilt based on latitude" width="700">
</p>

<p align="center">
  <em>
  Figure 3: Moon phases tilt based on latitude.  
  Source: Reddit (2023).
  </em>
</p>

To an observer at the poles, the Moon appears “upright,” whereas to an observer at the equator, it appears to be “lying on its side.” The exact degree of the Moon’s tilt can be simplified by:

**L ≈ T**

Where:  
- **L** = observer's latitude (in degrees) between 0° (at the equator) and +/-90° (at the poles)
- **T** = apparent tilt angle (in degrees) between 0° ("laying down") and +/- 90° ("upright")

This linear approximation doesn't take into account the Sun's and Moon's respective azimuth and altitude.

## 🛠 Libraries Used

- Python (version 3.14)
- rebound – N-body gravitational simulation package
- customtkinter – GUI framework for user interaction
- matplotlib – Orbit visualization and plotting
- skyfield/ephem (?) – Astronomical calculations for phases of the Moon
- Pillow – Image processing library  
- numpy – Numerical computing library for array operations and mathematical calculations  

## 📚 Data Used
The Moon phases images used as output were obtained from NASA (2026).

## ⚙ Installation

### Prerequisites

- Python 3.8+ ??
- pip
- [Other requirements?]

### Setup
```
git clone https://github.com/[username]/[repository-name].git
cd [repository-name?]
pip install -r requirements.txt
```

## 🚀 Running the Project
```
python main.py
```

## 💻 Usage Example
```
XXX
```

## 📁 Project Structure
(Main branch only)
```
Moon_Phases/
├── Bodies.py
├── moon_phases_pictures.py
├── simulation.py
├── UI.py
├── README.md  # This file :)
| 
├──.idea
|   ├── .gitignore
|   ├── misc.xml
|   ├── modules.xml
|   ├── Moon_Phases.iml
|   ├── vcs.xml
|   ├── workspace.xml 
|   └── inspectionProfiles
|           profiles_settings.xml    
|      
└── moon_images/
    ├── first_quarter.jpg
    ├── full_moon.jpg
    ├── last_quarter.jpg
    ├── new_moon.jpg
    ├── waning_crescent.jpg
    ├── waning_gibbous.jpg
    ├── waxing_crescent.jpg
    └── waxing_gibbous.jpg
```
## 🚧 Challenges & Solutions

## 📚 What we learned

## 📈 Future Improvements
redundant with the challenges and solutions part??

## 👥 Team Contributions

Arthur Foulon – animation? helping everyone :)

Aleksandra Chmielewska – UI?

Laura-Jo Lykles – 

Margot Portier – README.md writer?

Luna Hoenders – moon phases simulation?

## 📜 License
This project is licensed under the MIT License. (Open access.)

## 💬 Contact Information

If you have any suggestion or ideas to improve this project, feel free to contact any of us!  
Arthur Foulon – a.foulon@student.maastrichtuniversity.nl    
Aleksandra Chmielewska – a.chmielewska@student.maastrichtuniversity.nl  
Laura-Jo Lykles – l.lykles@student.maastrichtuniversity.nl   
Margot Portier – m.portier@student.maastrichtuniversity.nl  
Luna Hoenders – l.hoenders@student.maastrichtuniversity.nl  

## 📚 References

1. Vogel, T., Vogel, T., Team, N. M., Barry, C., & Nguyen, V. (2026, February 12). Moon Phases - NASA Science. NASA Science. https://science.nasa.gov/moon/moon-phases/
2. Reddit user aim179. (2023, March 4). Moon phases based on latitude [Reddit post]. Reddit. https://www.reddit.com/r/coolguides/comments/11hns5c/moon_phases_based_on_latitude
