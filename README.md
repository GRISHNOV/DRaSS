# DRaSS

Document Recognition and Storage System for tablets on the Linux x86 platform

## Description

Recognition and storage of passports in the database using AES encryption. 
Use a photo or scan of your passport for recognition. 
A personally generated password is used to access your personal storage.

![alt text][AES]
![alt text][DOC]

## Creators

This project was created by [Denis Stasyev](https://github.com/denisstasyev), [Ilya Grishnov](https://github.com/GRISHNOV), [Mikhail Pakhomov](https://github.com/mikhan333)

## Quick start

Setup:

```
make install
source ./env/bin/activate
pip3 install -r requirements.txt
deactivate
```

Run:

```
source ./env/bin/activate
make start
```

> To exit from virtualenv use `deactivate`

## Available commands

### `make`

Installs all necessary dependencies.

### `make install`

Installs all necessary dependencies.

### `make start`

Runs the application in the background mode.

### `make end`

In progress...

### `make clean`

Deletes all installed packages.

### `make uninstall`

Deletes all installed dependencies.

### `make info`

Shows current packages.

## Testing

Load custom images of passports:

```src/recognition/tests/passport_test0.jpg```

Data for test.drass:

```UK:  mgjo2```

[AES]:https://img.icons8.com/wired/2x/security-aes.png
[DOC]:https://unitel.com.tr/wp-content/uploads/2018/03/010108-e1521992990865.png
