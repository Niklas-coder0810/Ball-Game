import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Forest Runner", layout="wide")

st.title("🌙 Forest Runner – Night Edition")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
    body { margin: 0; overflow: hidden; background: #0b1020; }

    canvas {
        display: block;
        margin: auto;
        background: linear-gradient(#050814, #0b1020);
        border-radius: 12px;
    }

    #ui {
        position: absolute;
        width: 100%;
        bottom: 20px;
        text-align: center;
        font-family: Arial;
    }

    button {
        font-size: 18px;
        padding: 12px 20px;
        margin: 8px;
        border-radius: 14px;
        border: none;
        cursor: pointer;
        background: #1f2a44;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        transition: 0.2s;
    }

    button:active {
        transform: scale(0.95);
        background: #2d3c63;
    }

    #score {
        position: absolute;
        top: 10px;
        left: 20px;
        color: white;
        font-size: 20px;
        font-family: Arial;
    }

    #gameover {
        position: absolute;
        top: 40%;
        width: 100%;
        text-align: center;
        color: white;
        font-size: 60px;
        display: none;
        font-weight: bold;
        animation: drop 0.8s ease-out;
    }

    #restart {
        display: none;
        position: absolute;
        top: 55%;
        left: 50%;
        transform: translateX(-50%);
        padding: 15px 30px;
        font-size: 20px;
        background: #ffcc00;
        color: black;
        border-radius: 12px;
    }

    @keyframes drop {
        from { transform: translateY(-200px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
</style>
</head>
<body>

<canvas id="game" width="900" height="420"></canvas>

<div id="score">Score: 0</div>

<div id="gameover">GAME OVER</div>
<button id="restart" onclick="resetGame()">Neustart</button>

<div id="ui">
    <button onmousedown="jump()">⬆ Springen</button>
    <button onmousedown="duck(true)" onmouseup="duck(false)">⬇ Ducken</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let score = 0;
let gameOver = false;

let player = {
    x: 120,
    y: 300,
    w: 30,
    h: 30,
    vy: 0,
    ducking: false
};

let gravity = 1.1;
let ground = 300;

let obstacles = [];

function jump() {
    if (player.y >= ground && !gameOver) {
        player.vy = -15;
    }
}

function duck(state) {
    player.ducking = state;
}

function spawnObstacle() {
    if (gameOver) return;

    let type = Math.random() > 0.5 ? "log" : "highlog";

    obstacles.push({
        x: 900,
        y: type === "log" ? 320 : 260,
        w: 40,
        h: 40,
        type: type
    });
}

setInterval(spawnObstacle, 1800);

function drawBackground() {
    // night sky stars
    ctx.fillStyle = "#ffffff";
    for (let i = 0; i < 40; i++) {
        ctx.fillRect(Math.random()*900, Math.random()*200, 2, 2);
    }

    // forest silhouettes
    ctx.fillStyle = "#0a1a10";
    for (let i = 0; i < 20; i++) {
        ctx.fillRect(i * 50, 320, 30, 100);
    }
}

function update() {
    if (gameOver) return;

    player.y += player.vy;

    if (player.y < ground) {
        player.vy += gravity;
    } else {
        player.y = ground;
        player.vy = 0;
    }

    for (let o of obstacles) {
        o.x -= 6;
    }

    // score
    score++;
    document.getElementById("score").innerText = "Score: " + Math.floor(score/10);

    // collision
    for (let o of obstacles) {
        let ph = player.ducking ? 15 : player.h;

        if (
            player.x < o.x + o.w &&
            player.x + player.w > o.x &&
            player.y < o.y + o.h &&
            player.y + ph > o.y
        ) {
            endGame();
        }
    }

    obstacles = obstacles.filter(o => o.x > -100);
}

function drawPlayer() {
    ctx.fillStyle = "#f1c40f";
    let ph = player.ducking ? 15 : player.h;
    ctx.fillRect(player.x, player.y, player.w, ph);

    // eyes 👀
    ctx.fillStyle = "black";
    ctx.fillRect(player.x + 6, player.y + 8, 4, 4);
    ctx.fillRect(player.x + 18, player.y + 8, 4, 4);
}

function drawObstacles() {
    for (let o of obstacles) {
        ctx.fillStyle = "#8b5a2b";
        ctx.fillRect(o.x, o.y, o.w, o.h);

        // wood texture lines
        ctx.strokeStyle = "#5c3b1a";
        ctx.beginPath();
        ctx.moveTo(o.x, o.y+10);
        ctx.lineTo(o.x+40, o.y+10);
        ctx.stroke();
    }
}

function draw() {
    ctx.clearRect(0, 0, 900, 420);

    drawBackground();
    drawPlayer();
    drawObstacles();
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

function endGame() {
    gameOver = true;
    document.getElementById("gameover").style.display = "block";
    document.getElementById("restart").style.display = "block";
}

function resetGame() {
    score = 0;
    gameOver = false;
    obstacles = [];
    player.y = ground;
    player.vy = 0;

    document.getElementById("gameover").style.display = "none";
    document.getElementById("restart").style.display = "none";
}

loop();
</script>

</body>
</html>
"""

components.html(game_html, height=600)
