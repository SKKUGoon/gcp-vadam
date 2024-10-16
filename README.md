# VaDaM, Various Data Modules 

For each data science projects, we need data. This module creates data modules for each dataset, and containerize it.

For data orchestration tool, we use [prefect](https://docs.prefect.io/3.0/get-started/install). The github package only installs the client part for minimal installation size

```
pip install -U prefect-client
```

---

[comment]: <> (| URL | <Some URL> |)
[comment]: <> (|-----|------------|)

## Data

#### 1. Weather

| KEY | VALUE                               |
|-----|-------------------------------------|
| URL | [기상예보](https://apihub.kma.go.kr/) |
| USE | Baseball TOTO, HECON |
| KEY | `APIKEY_KOREA_WEATHER` |
