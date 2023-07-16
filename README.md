
<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>IPL_Simulation
</h1>
<h3>◦ </h3>
<h3>◦ Developed with the software and tools listed below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Markdown-000000.svg?style&logo=Markdown&logoColor=white" alt="Markdown" />
<img src="https://img.shields.io/badge/JSON-000000.svg?style&logo=JSON&logoColor=white" alt="JSON" />
</p>
<img src="https://img.shields.io/github/languages/top/Jainbaba/IPL_Simulation?style&color=5D6D7E" alt="GitHub top language" />
<img src="https://img.shields.io/github/languages/code-size/Jainbaba/IPL_Simulation?style&color=5D6D7E" alt="GitHub code size in bytes" />
<img src="https://img.shields.io/github/commit-activity/m/Jainbaba/IPL_Simulation?style&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/license/Jainbaba/IPL_Simulation?style&color=5D6D7E" alt="GitHub license" />
</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [⚙️ Features](#-features)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)
- [🤝 Contributing](#-contributing)

---


## 📍 Overview
The Cricket Match Simulation project is a comprehensive and flexible script that simulates a cricket match. It allows developers and cricket enthusiasts to simulate and analyze cricket matches using realistic game mechanics. The project combines multiple classes, modules, and utility functions to create an immersive cricket match simulation experience. With customizable match parameters and extensibility, users can tailor the simulation to their specific requirements and explore various aspects of the game.

---

## ⚙️ Features
> Team Management: The project includes classes to represent cricket teams, allowing users to create and manage teams participating in the match. It provides methods to add players, set lineups, and track team statistics.

> Player Performance Tracking: Each player participating in the match is tracked using the Tracker class. It keeps a record of runs scored, balls faced, wickets taken, and other performance metrics, enabling detailed analysis of player performance.

> Realistic Match Simulation: The simulation takes into account various match factors, such as balls bowled, wickets fallen, and target scores, to adjust player stats dynamically. This creates a realistic gameplay experience where player performance evolves based on the match situation.

> Umpire Decision Making: The Umpire class acts as the umpire in the simulation, making decisions on players' dismissals. It considers rules and probabilities to determine whether a player is out or not.

> Match Outcome Analysis: The MatchSummary class provides a summary of the match statistics, including batting and bowling performance for all players. It generates tables to display runs scored, balls faced, wickets taken, economy rates, and other relevant match data.

> Customizability and Extensibility: The project offers flexibility for customization and extension. Users can modify match parameters, add new features, or integrate the simulation into larger projects, tailoring it to their specific needs.

> User-Friendly Interface: The project includes well-organized classes, utility functions, and modules, making it easy to understand, modify, and build upon. It provides clear and concise code, allowing developers to explore and enhance the simulation effortlessly.

The Cricket Match Simulation project provides a valuable resource for developers, cricket enthusiasts, and anyone interested in understanding the dynamics of cricket matches. It serves as a foundation for creating cricket match simulations and offers a platform for analyzing player and team performance.


---


## 📂 Project Structure


```bash
repo
├── Commentator.py
├── Feild.py
├── Match.py
├── Players.py
├── README.md
├── Settings.py
├── Summary.py
├── Teams.py
├── Tracking.py
├── Umpire.py
├── Utils.py
├── main.py
├── player.json
├── requirement.txt
└── teams.json

1 directory, 15 files
```

---

## 🧩 Modules
The Cricket Match Simulation project consists of several modules that provide specific functionalities and enhance the simulation experience. These modules encapsulate related classes, functions, and utility code, enabling modularity and easy integration into other projects. Here are the key modules included in the project:

> Players: This module defines the Player class, which represents a cricket player participating in the match. It includes attributes and methods to track player statistics, such as runs scored, balls faced, wickets taken, and bowling economy rates. The module also provides functions to manage player data and perform calculations related to player performance.

> Tracking: The Tracking module contains the Tracker class, responsible for tracking player performance during the match. It records player-specific data, including runs scored, balls faced, wickets taken, and other relevant metrics. The module offers functions to update and retrieve player performance data, enabling real-time tracking and analysis.

> Setting: The Setting module comprises the Setting class, which handles adjustments to player statistics based on the match situation. It includes methods to adjust the stats of batsmen and bowlers, considering factors like balls bowled, wickets fallen, target scores, and pitch conditions. The module allows the simulation to simulate realistic gameplay and dynamic player performance.

> Umpire: The Umpire module introduces the Umpire class, which acts as the umpire in the simulation. It implements the decision-making process for player dismissals, taking into account rules and probabilities. The module enables the simulation to replicate umpire decisions accurately, enhancing the authenticity of the match experience.

> MatchSummary: This module provides the MatchSummary class, which generates match summaries and statistics. It includes methods to create tables displaying batting and bowling performance for all players, such as runs scored, balls faced, wickets taken, and economy rates. The module offers valuable insights into player and team performance, facilitating match outcome analysis.

> Teams: The Teams module consists of the Team class, representing a cricket team participating in the match. It includes attributes and methods to manage team-specific information, such as team name, players, and team statistics. The module allows for easy team creation, management, and interaction within the simulation.

> Match: The Match module introduces the Match class, which orchestrates the cricket match simulation. It brings together the players, teams, umpire, and other components to simulate a complete cricket match. The module provides methods to initialize the match, simulate innings, track scores, and determine match outcomes.

> Field: The Field module defines the Field class, representing the cricket field where the match takes place. It includes attributes and methods to manage field-related information, such as pitch conditions, weather, and fielding positions. The module enhances the realism of the simulation by incorporating field dynamics into player and match performance.

These modules work together to create a comprehensive cricket match simulation environment. They provide the necessary components to simulate matches, track player performance, analyze match outcomes, and customize the simulation experience. By leveraging these modules, users can gain a deeper understanding of cricket dynamics and explore various aspects of the game.

---

## 🚀 Getting Started

### ✔️ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:
> - `ℹ️ Python 3.8.0 >=`
> - `ℹ️ Tabulate`

Refer the Requriment.txt for more details

### 📦 Installation

1. Clone the IPL_Simulation repository:
```sh
git clone https://github.com/Jainbaba/IPL_Simulation
```

2. Change to the project directory:
```sh
cd IPL_Simulation
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using IPL_Simulation

```sh
python main.py
```
---

## 🤝 Contributing

Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.
