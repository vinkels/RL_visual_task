# RFL task for image complexity preference
Visual decision task with reinforcement learning using images categorized by SC/CE scores.
task consists of three experimental phases:
- control phase
- learning phase
- testing phase
Control and testing phase are the same but with different image sets.

### To Do
- clean up code
- data analysis

### Getting Started

All code is designed to run and tested in python 2.7 and 3.6. To be able to run the code you need all libraries mentioned in prerequisites.To run the code navigate to the directory in your terminal and run main.py (python main.py).

### Prerequisites

All code is tested in python3.6, but experiment scripts are also python 2.7 compatible.
All external libraries needed can be found in requirements.txt. To install required libraries run the following line in terminal/command line. Read more about pip [here](https://pip.readthedocs.io/en/1.1/requirements.html).

```
pip install requirements-txt
```
### project structure
main.py is the execution script for the experiment. Here you can adjust parameters like participant number, reward scheme and keybinding for the learning phase.
All scripts used for preprocessing of images are located in the img_prep folder.
These scripts are not always python2.7 compatible and are not needed to run the experiment.
In the experiment folder you can find scripts session.py that contains the actual experiment
and img_sets.py that creates randomized images lists for every session.



### Running
Download complete repository and navigate to repository in terminal.
Run main.py in python 2 or 3 to run the experiment.
**Make sure capslock is off, otherwise globalKeys will not work**
```
python main.py
```


## Authors

* **Yannick Vinkesteijn** - *Initial work* - [Github](https://github.com/yvinkesteijn)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Sara Jahfari
* Noor Seijdel
