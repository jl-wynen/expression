# expression
Card game where the two players build a mathematical expression together, trying to reach 100 or -100 respectively.


## install
To install such that you can edit the template and test it, use the terminal command below. It should be executed from the folder with the source code.

pip install -e .

## Run
python test_expression.py

## Keybindings:
- enter: toggle auto mode
- space: if not in aout mode, proceed to next step
- up arrow: increase time waiting in each step
- down arrow: decrease time waiting in each step
- right arrow: increase card speed
- left arrow: decrease card speed
- b: show bracket when running tournament

## Playing as a human
Use the mouse, and click the little area in the right top and bottom corner to play the selected cards. Play as human by setting positive or negative player to None in test_expression.py 
