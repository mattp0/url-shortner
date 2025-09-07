# urlshortner

[![Release](https://img.shields.io/github/v/release/mattp0/urlshortner)](https://img.shields.io/github/v/release/mattp0/urlshortner)
[![Build status](https://img.shields.io/github/actions/workflow/status/mattp0/urlshortner/main.yml?branch=main)](https://github.com/mattp0/urlshortner/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mattp0/urlshortner/branch/main/graph/badge.svg)](https://codecov.io/gh/mattp0/urlshortner)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mattp0/urlshortner)](https://img.shields.io/github/commit-activity/m/mattp0/urlshortner)
[![License](https://img.shields.io/github/license/mattp0/urlshortner)](https://img.shields.io/github/license/mattp0/urlshortner)

a url shortner project

- **Github repository**: <https://github.com/mattp0/urlshortner/>
- **Documentation** <https://mattp0.github.io/urlshortner/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:mattp0/urlshortner.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version



---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
