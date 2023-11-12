# Автоучастие lolzteam
Простенькая реализация на undetected_chromedriver (для обхода cloudflare капчи)
```sh
pip install -r requirements.tx
```

### Что нужно знать?
Если вы хостите на VDS/VPS и выбираете Windows Server старой версии, то скорее всего версия хрома будет ограничена определенным значением, в таком случае открываете
```sh
lolz_contests.py
```
и меняете
https://github.com/m0ne0n/lolz_auto_contest/blob/64799ccad799af8272aaf906cab28ab53489dbca/lolz_contests.py#L23
на это:
```python
driver = Chrome(options=options, version_main=109)
```
Версию ставите свою, для примера указана 109.

