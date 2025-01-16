Steps to start from scratch:
1. Execute in the terminal: `pip install poetry`
2. If needed execute `poetry init`
3. From the project root: `poetry install --no-root` or `poetry install`
4. Run `poetry lock`
5. Use '`poetry env info -p`' to get path to virtual environment
6. Add new interpreter > existing poetry env > paste path from step 3
7. `poetry update` to install the most recent version of the libs