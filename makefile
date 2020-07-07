# Run autopep8 style filter
style:
	autopep8 --in-place $(FILE)

# Runs Program
miner:
	python3 twitter_miner_1.py

# Interactive Mode
iminer:
	python3 -i twitter_miner_1.py

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