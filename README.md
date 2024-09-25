# Style guide

Follow this [style Guide](docs/style_guide.md) here and add to as needed.

# Setup for a new domain

- Copy and edit:
  - docker-compose-software.yml
  - config_data_stats_skills.py

# SSL problems install in authlib

Network Issues / Firewall
If the SSL certificate issue persists, and you need a quick fix (not recommended for long-term use due to security concerns), you can bypass SSL verification by using the --trusted-host option with pip:

```
pip install authlib --trusted-host pypi.org --trusted-host files.pythonhosted.org
```
