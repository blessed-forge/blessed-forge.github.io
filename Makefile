
# putting a GITHUB_BASIC_AUTH def into Makefile.local makes life more pleasant
-include Makefile.local

.PHONY: default
default:
	@echo Choose what to make:
	@echo   repo_update - update the latest info of the repos from github

.PHONY: repo_update
repo_update:
	python3 ./update_addon_info.py
