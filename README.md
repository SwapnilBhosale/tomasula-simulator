# tomasula-simulator
A python based Tomasula simulator for configurable cpu architecture


### How to Run the project:

###### There is no need to build and clean the project, Since python has a interpreter and do not create any bianry files.

```bash
python src/main.py config_files/inst.txt config_files/data.txt config_files/config.txt config_files/result.txt
```


#### Submission Pcakages:

1) 	cpu.py 
	It represents the actual CPU including generalm purpose registers, floating point registers, cache, memory etc
	
2) 	fp_unit.py
	This is the base class for the all functional unit  of the CPU
3) 	scoreboard.py:
	This class represents each instruction being executed in the Tomasula Scoreboard
4) 	icache.py
	This class represents the Instruction cache which is direct mapped
5) 	dcache.py
	This class represnts the Data cache which is 2-way set associative and have 4 blocks
6) 	instruction.py
	This class is the base class for the all instructions and represnts src, dest and third operands in the instructions.
	Also this class decodes each instruction and execute them.
	
	

##### Refrences:

http://math-atlas.sourceforge.net/devel/assembly/mips-iv.pdf
https://stackoverflow.com/questions/27260792/python-combinations-of-parent-child-hierarchy
https://stackoverflow.com/questions/42858964/python-code-to-extract-last-16-characters-from-32-characters
https://github.com/mlahir1/Simulator-for-CDC-6600-Scoreboard
