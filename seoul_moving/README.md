### HJD and SEC geolocation data

```python
hjd = load_hjd("seoul_moving/assets/land")
sec = load_sec("seoul_moving/assets/land")

db = SDA()

db.insert_geodataframe(hjd, "hjd", "nimbus")
db.insert_geodataframe(sec, "sec", "nimbus")
```