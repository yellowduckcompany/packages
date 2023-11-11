# Python

Add ``seatbelt`` to your requirements file or install using pip:
```bash
pip install seatbelt
```

And add this snippet anywhere in your code base:

```python
from yellowduck.service import Service

Service(package_id='goose').start()
```

### Administrators

Build distribution and publish:
```bash
python -m build
python -m twine upload dist/*
```
