# Runs Program
miner:
	python3 main.py

# Interactive Mode
iminer:
	python3 -i main.py

# Run in Debug Mode; pauses execution at point where an error is thrown.
debug:
	python3 -m pdb -c continue $(FILE)

# Run autopep8 style filter
style:
	autopep8 --in-place $(FILE)

# Removes __pycache__ Folder [pycache optimizes code, use post-development]
clean:
	rm -rf __pycache__

# Removes Python Artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {} 

# Removes Build Artifacts
clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

