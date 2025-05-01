# Artur - ur robot interactive demo
Interaktívna demonštračná aplikácia s robotickým ramenom UR5e.

## Potrebné knižnice

Pre spustenie je potrebné mať nainštalované nasledujúce knižnice:

cv2:
```bash
pip install opencv-python
```

mediapipe:
```bash
pip install mediapipe
```

pygame:
```bash
pip install pygame
```

requests:
```bash
pip install requests
```

## Použitie
Pred spustením hry je potrebné rozmiestniť kocky na podstavu, s týmto vám pomôže program `cubes_setup.py`. Potom je možné sputiť hru.

## Spustenie
Spustenie programu na prípravu kociek `cubes_setup.py`:
```
Usage: ./cubes_setup.py -a <IP:PORT> -t <table_height_cm> [-s] [-h]
 -a <IP:PORT>         Specify the server IP address and port (required)
 -t <table_height_cm> Specify the table height in centimeters (required)
 -s                   Start the robot (optional)
 -h                   Show this help message and exit
```

Spustenie hry `Artur.py`:
```
Usage: ./Artur.py -a <IP:PORT> -t <table_height_cm> [-s] [-h]
 -a <IP:PORT>         Specify the server IP address and port (required)
 -t <table_height_cm> Specify the table height in centimeters (required)
 -s                   Start the robot (optional)
 -h                   Show this help message and exit
```