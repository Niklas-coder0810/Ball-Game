import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Forest Runner", layout="wide")

st.title("🌙 Forest Runner – Night Evolution")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
    body {
        margin: 0;
        overflow: hidden;
        background: #070b18;
    }

    canvas {
        display: block;
        margin: auto;
        background: linear-gradient(#04060f, #0b1020);
        border-radius: 12px;
    }

    #ui {
        position: absolute;
        bottom: 20px;
        width: 100%;
        text-align: center;
    }

    button {
        font-size: 18px;
        padding: 14px 28px;
        margin: 10px;
        border-radius: 14px;
        border: none;
        cursor: pointer;
        background: #1b2440;
        color: white;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }

    button:active {
        transform: scale(0.95);
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
        top: 35%;
        width: 100%;
        text-align: center;
        color: white;
        font-size: 64px;
        display: none;
        font-weight: bold;
        animation: drop 0.8s ease-out;
    }

    #restart {
        display: none;
        position: absolute;
        top: 52%;
        left: 50%;
        transform: translateX(-50%);
        padding: 16px 32px;
        font-size: 20px;
        background: #ffd54a;
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
    <button onmousedown="jump()">⬆ SPRINGEN</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let score = 0;
let gameOver = false;
let speed = 6;

let player = {
    x: 120,
    y: 300,
    w: 28,
    h: 28,
    vy: 0
};

let gravity = 1.1;
let ground = 300;

let obstacles = [];

function jump() {
    if (player.y >= ground && !gameOver) {
        player.vy = -15;
    }
}

function spawnObstacle() {
    if (gameOver) return;

    let type = Math.random() > 0.5 ? "log" : "logHigh";

    obstacles.push({
        x: 900,
        y: type === "log" ? 320 : 260,
        w: 40,
        h: 40
    });
}

setInterval(spawnObstacle, 1700);

function drawMoon() {
    ctx.fillStyle = "#f5f3ce";
    ctx.beginPath();
    ctx.arc(750, 80, 40, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#070b18";
    ctx.beginPath();
    ctx.arc(770, 70, 35, 0, Math.PI * 2);
    ctx.fill();
}

function drawTrees() {
    ctx.fillStyle = "#050a12";
    for (let i = 0; i < 20; i++) {
        ctx.fillRect(i * 60, 250, 20, 170);
        ctx.beginPath();
        ctx.arc(i * 60 + 10, 250, 30, 0, Math.PI * 2);
        ctx.fill();
    }
}

function drawGround() {
    ctx.fillStyle = "#1a1f2e";
    ctx.fillRect(0, 340, 900, 80);

    ctx.fillStyle = "#0e1422";
    for (let i = 0; i < 30; i++) {
        ctx.fillRect(i * 30, 340, 15, 80);
    }
}

function updateDifficulty() {
    if (score % 200 === 0 && score > 0) {
        speed += 0.5;
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
        o.x -= speed;
    }

    score++;
    document.getElementById("score").innerText = "Score: " + Math.floor(score / 10);

    updateDifficulty();

    for (let o of obstacles) {
        if (
            player.x < o.x + o.w &&
            player.x + player.w > o.x &&
            player.y < o.y + o.h &&
            player.y + player.h > o.y
        ) {
            endGame();
        }
    }

    obstacles = obstacles.filter(o => o.x > -100);
}

function drawPlayer() {
    ctx.fillStyle = "#ffd54a";
    ctx.fillRect(player.x, player.y, player.w, player.h);

    // eyes
    ctx.fillStyle = "black";
    ctx.fillRect(player.x + 6, player.y + 8, 3, 3);
    ctx.fillRect(player.x + 16, player.y + 8, 3, 3);
}

function drawObstacles() {
    for (let o of obstacles) {
        ctx.fillStyle = "#7a4a1f";
        ctx.fillRect(o.x, o.y, o.w, o.h);

        ctx.strokeStyle = "#4b2e12";
        ctx.beginPath();
        ctx.moveTo(o.x, o.y + 10);
        ctx.lineTo(o.x + 40, o.y + 10);
        ctx.stroke();
    }
}

function draw() {
    ctx.clearRect(0, 0, 900, 420);

    drawMoon();
    drawTrees();
    drawGround();
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
    speed = 6;
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
