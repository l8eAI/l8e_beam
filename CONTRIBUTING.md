# Contributing to l8e-beam

First off, thank you for considering contributing to l8e-beam! It's people like you that make open source such a great community.

## Where do I go from here?

If you've noticed a bug or have a feature request, [make one](https://github.com/l8eAI/l8e_beam/issues/new)! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

### Fork & create a branch

If this is something you think you can fix, then [fork l8e-beam](https://github.com/l8eAI/l8e_beam/fork) and create a branch with a descriptive name.

A good branch name would be (where issue #38 is the ticket you're working on):

```bash
git checkout -b 38-add-a-new-feature
```

### Get the project running

1.  Clone your fork of the repository.
2.  We recommend using a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  Install the dependencies for development:
    ```bash
    pip install -r requirements.txt
    ```

### Build the Project

To build the project, you can use the `build.sh` script. This script will download the required spaCy models, run the tests, and build the wheel file.

```bash
chmod +x build.sh
./build.sh
```

### Run the tests

To make sure everything is working as expected, run the tests:

```bash
pytest
```

### Test with Examples

The `examples` directory contains scripts that demonstrate how to use the library. You can run these scripts to test the functionality of the library.

For example, to run the `decorator_usage.py` script:

```bash
python examples/decorator_usage.py
```

For more details on how to run the examples, please see the `examples/README.md` file.

### Make your changes

Make your changes to the codebase.

We use [pdoc](https://pdoc.dev/) for documentation, so please make sure that your code is well-commented and that you've updated any relevant docstrings.

### Push to your fork and submit a pull request

Push your changes to your fork and then [submit a pull request](https://github.com/l8eAI/l8e_beam/compare). Please provide a good description of the changes you've made.

At this point you're waiting on us. We like to at least comment on pull requests within three business days (and, typically, one business day). We may suggest some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is accepted:

* Write tests.
* Follow the existing code style.
* Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
