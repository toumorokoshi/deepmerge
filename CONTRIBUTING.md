# Contributing

## 1.Setup a virtualenv

The directives in the Makefile are designed to be
run in CI as well as locally. It assumes that you have
virtualenv installed as a dependency:

```
python -m pip install virtualenv
```

## Use make for common actions

See the `Makefile` file for a list of
common tasks that help with development.

Generally, to verify your code is ready for a PR, the following commands must pass:

```
make ready-pr
```
