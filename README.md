# Logistic Simulator Blog Post series


## Summary

This repository accompanies blog post series about building logistic simulator.


# Quickstart 

To set up this project, make sure you have a python and virtualenv installed. Then:
```bash

# create a new virtual environment
# this environment will keep this project and its depedencies safely isolated
virtualenv -p `which python3` venv

# activate this virtual environment in the terminal
source venv/bin/activate

# install python package into this environment in editable mode
# this leverages remove_brackets_and_call_setup.py package format and installs
# we include code for both prediction and training
pip install --editable '.'
```

From here you could open the folder in PyChart, VS Code or run individual steps.


```bash

logisim2 --origin Steamdrift --dest Leverstorm
# prints:
# 0.00h DEPART Steamdrift
#14.26h ARRIVE Cogburg
#24.81h ARRIVE Irondale
#31.88h ARRIVE Leverstorm

logisim3 --origin Steamdrift --dest Leverstorm --test_ratio 0.1
# prints:
# Mean squared error is 46.7742
# 0.00h DEPART Steamdrift
#17.62h ARRIVE Cogburg
#31.28h ARRIVE Copperhold
#38.83h ARRIVE Leverstorm
```


