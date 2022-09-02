
# cmsengine

Software for local detection CMS on the site.
## Installation

Install with git.

```bash
  git clone https://github.com/securityhigh/cmsengine
  cd cmsengine
  pip3 install -r requirements.txt
```
    
## Usage

```bash
  python3 cmsengine.py perfeo.ru
```

Wait a few seconds and get the next answer if successful detected:
```
  [ok] OpenCart
```

If CMS is not detected:
```
  [error] CMS not found
```
## CMS Database
- OpenCart
- Bitrix
- CS-Cart
- PrestaShop
- Simpla
- Webasyst
- Drupal
- WordPress
