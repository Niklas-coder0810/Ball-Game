import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Forest Runner", layout="wide")

st.title("🌲 Forest Runner – Jump & Duck Game")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
    body { margin: 0; overflow: hidden; background: #1b2b1b; }
    canvas { display: block; margin: 0 auto; background: linear-gradient(#2e4d2e, #1b2b1b); }
    #controls {
        position: absolute;
        bottom: 20px;
        width: 100%;
        text-align: center;
    }
    button {
        font-size: 20px;
        padding: 15px 25px;
        margin: 10px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
    }
</style>
</head>
<body>

<canvas id="game" width="900" height="400"></canvas>

<div id="controls">
    <button onmousedown="jump(true)" onmouseup="jump(false)">⬆ Springen</button>
    <button onmousedown="duck(true)" onmouseup="duck(false)">⬇ Ducken</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let player = {
    x: 100,
    y: 300,
    w: 40,
    h: 40,
    vy: 0,
    jumping: false,
    ducking: false
};

let gravity = 1.2;
let ground = 300;

let obstacles = [];

function spawnObstacle() {
    let type = Math.random() > 0.5 ? "high" : "low";
    obstacles.push({
        x: 900,
        y: type === "high" ? 260 : 320,
        w: 30,
        h: 40,
        type: type
    });
}

setInterval(spawnObstacle, 2000);

function jump(active) {
    if (active && player.y >= ground) {
        player.vy = -15;
    }
}

function duck(active) {
    player.ducking = active;
}

function update() {
    // gravity
    player.y += player.vy;
    if (player.y < ground) {
        player.vy += gravity;
    } else {
        player.y = ground;
        player.vy = 0;
    }

    // obstacles move
    for (let o of obstacles) {
        o.x -= 5;
    }

    // collision
    for (let o of obstacles) {
        let py = player.y;
        let ph = player.ducking ? 20 : player.h;

        if (
            player.x < o.x + o.w &&
            player.x + player.w > o.x &&
            py < o.y + o.h &&
            py + ph > o.y
        ) {
            alert("💥 Game Over!");
            document.location.reload();
        }
    }

    obstacles = obstacles.filter(o => o.x > -50);
}

function drawForest() {
    ctx.fillStyle = "#2e5d2e";
    for (let i = 0; i < 20; i++) {
        ctx.fillRect(i * 50, 350, 20, 50);
    }
}

function draw() {
    ctx.clearRect(0, 0, 900, 400);

    drawForest();

    // player
    ctx.fillStyle = "yellow";
    let ph = player.ducking ? 20 : player.h;
    ctx.fillRect(player.x, player.y, player.w, ph);

    // obstacles
    ctx.fillStyle = "red";
    for (let o of obstacles) {
        ctx.fillRect(o.x, o.y, o.w, o.h);
    }
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
"""

components.html(game_html, height=500)
