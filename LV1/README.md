# AMR LV1: ROS2, Docker i Rosbridge

Autonomni mobilni roboti, 2026/2027.

## Sadržaj

- `zadatak1/` ROS2 Jazzy kontejner: turtlesim, čvor `path_follower` (kretanje po putanji `x = 5.544 + 4 sin(ω)`, `y = 5.544 + 4 sin(ω) cos(ω)`) i rosbridge server.
- `zadatak2/` Python aplikacija (roslibpy + matplotlib) u zasebnom kontejneru, bez ROS-a. Spaja se na rosbridge i prikazuje pozu i putanju robota.
- `compose.yaml` pokreće oba kontejnera odjednom.

## Pokretanje (Ubuntu)

    cd LV1
    xhost +local:docker
    docker compose up --build

Otvaraju se dva prozora: TurtleSim i graf s putanjom. Zaustavljanje: Ctrl+C, zatim `docker compose down`.

## Zahtjevi

- Docker Engine s Docker Compose pluginom
- X11 prikaz (za GUI prozore iz kontejnera)
