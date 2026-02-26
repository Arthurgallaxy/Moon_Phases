# 🌘 Moon Phases Simulation

**Course:** Practical Python Programming Language – Introduction to OOP  
**Institution:** Maastricht Science Programme  
**Date:** February/March 2026  
**Team members and student IDs:** Arthur Foulon (ID), Aleksandra Chmielewska (ID), Luna Hoenders (ID), Laura-Jo Lykles (i6375390), Margot Portier (i6344762) 

*This project aims to create a simple but accurate stimulation that would enable one to vizualize the phases of the moon from an Earth-bound observer.*

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
    - [ ] Contact/support information
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
- [Contact Informations](#-contact-informations)

## 📌 Description
Our main motivation, for this python pratical, was to challenge ourselves and learn to code by collaborating on Github to create an interesting stimulation with its visualization and with a scientific relevance that may be used as a lame educational tool in secondary schools.

In our stimulation, we want to visualize the dynamic between three very familiar bodies: the Earth, the Sun and the Moon. In order to do so, we created four classes: celestial bodies, orbits, observer and user interface (abbreviated as UI). The goal is to provide a user-friendly interface that could be used to visualize the phases and tilt of the moon depending on the date and latitude on Earth. The Earth-bound observer is represented by a cat that can either be dead or alive with a 50% chance (little nerdy quantum add to this astronomy project.)

Inputs needed from the user:
- date (and time of the day?)
- latitude on Earth

Outputs given by the code:
- visualization of the phase of the moon (example image?) and tilt amongst these 8 possible phases: 
    - 🌑 (New Moon)
    - 🌒 (Waxing Crescent Moon)
    - 🌓 (First Quarter Moon)
    - 🌔 (Waxing Gibbous Moon)
    - 🌕 (Full Moon)
    - 🌖 (Waning Gibbous Moon)
    - 🌗 (Last Quarter Moon)
    - 🌘 (Waning Crescent Moon)
- if the cat is dead or alive? 🐈‍⬛

## ✨ Features
(what our code does)
- Moon orbit simulation around the Earth?
- Gravitational force modeling?
- Date-dependant Moon phase visualization
- Latitude-dependent Moon tilt visualization?

## 🧠 Physics Background
### 🌍 Gravitational Force
The first physical principle used in this project is a simplified version of the **gravitational force**. In astronomy, planets orbit stars and moons orbit planets due to **gravitational force**. Newton's law of universal gravitation describes the force between two objects as being:  

**F = G × (m₁ × m₂) / r²**  

Where:  
- **F** = gravitational force (in Newtons)
- **G** = gravitational constant = 6.674 × 10⁻¹¹ m³/ (in kg·s²)
- **m₁, m₂** = masses of the two objects (in kg)
- **r** = distance between centers of the two objects (in meters)

This formula, in its simplest form, is used to compute an approximation of the orbits of the Earth around the Sun and the Moon around the Earth (as a basis for our simulation). Any relativisty effect was ignored.

### 🌘 Phases of the Moon
<p align="center">
  <img src="https://github.com/user-attachments/assets/b9852746-aa5a-438e-8754-ac3d4552f078" alt="Gift Moon phases" width="300">
</p>

GIFT from https://science.nasa.gov/moon/moon-phases/

Moving on to the physics behind the phases of the Moon, a very widly spread misconception is that they are created by the Earth's shadow. This exactly is what happends during a lunar eclipse but this process is NOT what creates the different phases of the Moon.  

Half of the Moon is actually constantly lit by light coming straight from the Sun. As the Moon revolves around the Earth (with a period of around 28 days), the relative Sun-Earth-Moon positions change. It means that, for an observer on Earth, the lit part of the Moon would look different at different times of the month as shown on the folowing figure. 
(need citation? sources https://theplanets.org/the-moon/waning-crescent-moon/ OR https://science.nasa.gov/moon/moon-phases/)
<p align="center">
  <img src="https://github.com/user-attachments/assets/4b052cb7-88dd-414c-a4e5-3c77bd9c7a74" alt="Understand Moon phases as seen from Earth" width="700">
</p>

### 🌙 Tilt of the Moon
Then, buildong on to that, we had to consider that the apparent tilt of the moon changes for different latitudes on Earth as represented in this image below (needs citation? source: https://www.reddit.com/r/coolguides/comments/11hns5c/moon_phases_based_on_latitude/).  

<p align="center">
  <img src="https://github.com/user-attachments/assets/28748a2d-e61d-42c5-a798-b574e8098a1f" alt="Moon phases tilt based on latitude" width="700">
</p>

The Moon seems "upright" and at the poles, and seems to be "laying down" at the equator. The precise degree of the tilt of the Moon can be simplified by:

**L ≈ T**

Where:  
- **L** = observer's latitude (in degrees) between 0° (at the equator) and +/-90° (at the poles)
- **T** = apparent tilt angle (in degrees) between 0° ("laying down") and +/- 90° ("uprigth")

This linear approximation doesn't take into account the Sun's and Moon's azimuth and altitude.

## 🛠 Libraries Used

- Python version 3.11+ ??
- rebound – N-body gravitational simulation package
- tkinter – GUI framework for user interaction (ctkinter??)
- matplotlib – Orbit visualization and plotting
- skyfield/ephem?? – Astronomical calculations for phases of the Moon

## 📚 Data Used
Luna's images of the Moon? source and citation? from https://science.nasa.gov/moon/moon-phases/ ?
other type of data?

## ⚙ Installation

### Prerequisites

- Python 3.8+
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
(not complete)
```
Moon_Phases/
│
├── main/
│   ├── file1.py
│   ├── file2.py
│   └── main.py
│
├── tests/
└── README.md #This file :)
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
This project is licensed under the MIT License. (Open acess.)

## 💬 Contact Informations

If you have any suggestion or ideas to improve this project, feel free to contact any of us!  
Arthur Foulon – a.foulon@student.maastrichtuniversity.nl    
Aleksandra Chmielewska – a.chmielewska@student.maastrichtuniversity.nl  
Laura-Jo Lykles – l.lykles@student.maastrichtuniversity.nl   
Margot Portier – m.portier@student.maastrichtuniversity.nl  
Luna Hoenders – l.hoenders@student.maastrichtuniversity.nl  
