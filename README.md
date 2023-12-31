# xG and xP Analysis ⚽️

Returning to the project? Jump straight to the [xG ](assets/xG_by_player_per_90.md) and [xP](assets/full_table.md) tables

## Introduction

### PSxG (Post Shot Expected Goals) Model
The PSxG model in this project aims to quantify the quality of a goal-scoring opportunity in a football match, providing a probability that a given shot will result in a goal. The model considers various factors such as:

- **Shot Distance**: The distance between the player and the goal at the time of the shot.
- **Shot Angle**: The angle between the ball and the goal posts.
- **Play Context**: Whether the shot was taken from open play, a set-piece, etc.
- **Shot Location**: Where the player takes the shot on the pitch
- **Goal Mouth Location**: Where the ball crosses the goalline

Explore the methodology and calculations in detail in the [PSxG Model Notebook](models/xG_model.ipynb).

### xP (Expected Points) Model
The xP model takes the data from the PSxG model and simulates 100,000 possible matches to generate the probability that each team would win. These win probabilities are then used to calculate the number of expected points each team would receive. 

- Step one: Simulate each shot in the match 100,000 times, where the probability the shot results in a goal is the xG of that shot, predicted by the xG model

- Step two: Calculate the scorelines from each simulated match by summing the goals scored by the home and away team in each of the simulated matches

![width=1in](assets/sim_score_diff.png)

- Step three: Calculate the percentage of games each side wins, draws, or loses in these simulated outcomes 

![width=1in](assets/sim_outcome_prob.png)


- Step four: Translate the win probabilities to expected points

![width=1in](assets/sim_xp.png)

For more on the methodology, see the [xP Model Notebook](models/xP_model.ipynb).

## Tables
Based on the PSxG and xP data I have compiled tables to track PSxG leaders across the premier league and the premier league table ranked by xP.

- [PSxG Leaders](assets/xG_by_player_per_90.md)
- [xP Team Table](assets/full_table.md)

## Structure
This project is organized as follows:

- **models/**: Contains notebooks such as [xG Model](models/xG_model.ipynb) and [xP Model](models/xP_model.ipynb) which detail the methodologies and calculations.
- **scripts/**: Includes scripts like [convert\_and\_run\_models.sh](scripts/convert_and_run_models.sh) which automate model execution and updater.py which handles data scraping and dataset maintenance.
- **datasets/**: Houses datasets utilized in the models.
- **logs/**: Contains log files for debugging and tracking script executions.

## Contributing
I welcome contributions and feedback to enhance the models and methodologies! Please feel free to raise issues or submit pull requests.

## Contact Information
For inquiries, support, or collaboration, please contact:

- **Name**: Harrison Ward
- **Email**: [hward4116@gmail.com](mailto:hward4116@gmail.com)

**COYS**


